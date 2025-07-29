import random
import math
from pathlib import Path
from functools import lru_cache
from typing import Union, Tuple
import numpy as np
import cv2
from PIL import Image
import torch
from torch import nn
from torchvision import transforms
from torchvision.models import WeightsEnum
from model_wrapper.utils import get_device


def read_img(img_path, imgsz: Tuple[int, int], mode: str = 'RGB') -> np.ndarray:
    """返回的是归一化后的numpy数组"""
    img = Image.open(img_path).convert(mode).resize(imgsz)  # (h, w, c)
    return np.array(img).astype(np.uint8) / 255.


def get_img_mean_std(data_path: Union[str, Path], imgsz: Union[int, Tuple[int, int]] = (224, 224), 
                     img_prefix: str = 'jpg', sample: Union[int, float] = 2048) -> Tuple[np.ndarray, np.ndarray]:
    """
    计算图片数据集的均值和标准差

    Args:
        data_path: 数据集路径
        img_size: 图片尺寸
        img_prefix: 图片后缀名(jpg, png, jpeg等)
        sample: 样本数量，可以是整数或浮点数，如果为浮点数，则表示样本占比
    """
    if isinstance(data_path, str):
        data_path = Path(data_path)

    if isinstance(imgsz, int):
        imgsz = (imgsz, imgsz)
    
    img_list = list(data_path.glob(f'**/*.{img_prefix}'))
    if isinstance(sample, int):
        if sample < len(img_list):
            img_list = random.sample(img_list, sample)
    elif sample < 1.:
        sample = int(sample * len(img_list))
        img_list = random.sample(img_list, sample)

    result = np.stack(list(map(lambda x: read_img(x, imgsz), img_list)))
    mean = np.mean(result, axis=(0, 1, 2))
    std = np.std(result, axis=(0, 1, 2))
    return mean, std


def get_pretrained(model: nn.Module, weights: WeightsEnum, out_features: int = None, num_train_layers: int = 0):
	"""
	根据指定的模型和权重创建一个预训练的模型，并修改其全连接层以适应新的分类任务。
	能用的模型包括：
	- ResNet: resnet18, ResNet18_Weights
	- VGG: vgg16, VGG16_Weights, bgg16_bn, VGG16_BN_Weights
	- EfficientNet: efficientnet_v2_s, EfficientNet_V2_S_Weights
	- DenseNet: densenet121, DenseNet_121_Weights
	- ShuffleNet: shufflenet_v2_x1_0, ShuffleNet_V2_X1_0_Weights
	- MNASNet: mnasnet0_5, MNASNet_0_5_Weights
	- MobileNet: mobilenet_v3_small, MobileNet_V3_Small_Weights
	- SqueezeNet: squeezenet1_0, SqueezeNet_V1_0_Weights
	- GoogLeNet: googlenet, GoogLeNet_Weights
	- Inception3: inception_v3, Inception_V3_Weights
	- VisionTransformer: vit_b_16, ViT_B_16_Weights
	- SwinTransformer: swin_s, Swin_S_Weights

	参数:
	model: torch.nn.Module 类型的模型，表示基础模型架构。
	weights: WeightsEnum 预训练权重，通常来自ImageNet数据集，用于初始化模型。
	out_features: int 类型，表示全连接层的输出特征数量，默认值为256。
	num_train_layers: int 类型，表示要训练的层数，默认值为0。

	返回:
	一个预训练的模型，其全连接层被修改为指定的输出特征数量。

	示例:
	>>> from torchvision.models import resnet18, ResNet18_Weights, efficientnet_v2_s, EfficientNet_V2_S_Weights
	>>> model = get_pretrained(resnet18, ResNet18_Weights.DEFAULT, num_train_layers=2)
	"""
	# 使用指定的权重初始化预训练模型
	pretrained = model(weights=weights)

	# 根据num_train_layers参数决定是否冻结预训练模型的权重
	if num_train_layers <= 0:
		# 如果num_train_layers小于等于0，冻结所有预训练模型的权重
		for param in pretrained.parameters():
			param.requires_grad_(False)
	else:
		# 否则，只冻结指定数量的层
		parameters = list(pretrained.parameters())
		if num_train_layers < len(parameters):
			for param in parameters[:num_train_layers]:
				param.requires_grad_(False)
			for param in parameters[num_train_layers:]:
				param.requires_grad_(True)
		else:
			for param in parameters:
				param.requires_grad_(True)

	if out_features:
		name = pretrained.__class__.__name__
		if name == 'DenseNet' and out_features != pretrained.classifier.out_features:
			pretrained.classifier = nn.Linear(pretrained.classifier.in_features, out_features)
		elif name in ('EfficientNet', 'MNASNet', 'MobileNetV2') and out_features != pretrained.classifier[1].out_features:
			pretrained.classifier[1] = nn.Linear(pretrained.classifier[1].in_features, out_features)
		elif name in ('MobileNetV3', 'SqueezeNet') and out_features != pretrained.classifier[3].out_features:
			pretrained.classifier[3] = nn.Linear(pretrained.classifier[3].in_features, out_features)
		elif name in ('ResNet', 'Inception3', 'GoogLeNet', 'ShuffleNetV2') \
			and out_features != pretrained.fc.out_features:
			pretrained.fc = nn.Linear(pretrained.fc.in_features, out_features)
		elif name == 'VGG' and out_features != pretrained.classifier[6].out_features:
			pretrained.classifier[6] = nn.Linear(pretrained.classifier[6].in_features, out_features)
		elif name == 'VisionTransformer' and out_features != pretrained.heads.head.out_features:
			pretrained.heads.head = nn.Linear(pretrained.heads.head.in_features, out_features)
		elif name == 'SwinTransformer' and out_features != pretrained.head.out_features:
			pretrained.head = nn.Linear(pretrained.head.in_features, out_features)

	# 返回经过修改的预训练模型
	return pretrained

# PIL图像转tensor
def pil_to_tensor(img: Image.Image, imgsz: Union[int, tuple[int, int]] = None):
	"""
	将PIL图像转换为tensor，并调整其尺寸。
	"""
	return _get_transforms(imgsz)(img)


@lru_cache(maxsize=1)
def _get_transforms(imgsz: Union[int, tuple[int, int]] = None):
	if imgsz is None:
		return transforms.ToTensor()  # PIL图像转tensor, (H,W,C) ->（C,H,W）,像素值[0,1]
	
	if isinstance(imgsz, int):
		imgsz = (imgsz, imgsz)

	return transforms.Compose([
		transforms.Resize(imgsz),  # PIL图像尺寸统一
		transforms.ToTensor()  
	])

# tensor转PIL图像
tensor_to_pil = transforms.Compose([
	transforms.Lambda(lambda t: t * 255),  # 像素还原
	transforms.Lambda(lambda t: t.type(torch.uint8)),  # 像素值取整
	transforms.ToPILImage(),  # tensor转回PIL图像, (C,H,W) -> (H,W,C)
])

def auto_pad(k, p=None, d=1):  # kernel, padding, dilation
	"""Pad to 'same' shape outputs."""
	if d > 1:
		k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
	if p is None:
		p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
	return p


def random_perspective(im, degrees=10, translate=0.1, scale=0.1, shear=10, perspective=0.0, border=(0, 0)):
	# torchvision.transforms.RandomAffine(degrees=(-10, 10), translate=(0.1, 0.1), scale=(0.9, 1.1), shear=(-10, 10))
	# https://blog.csdn.net/weixin_46334272/article/details/135420634
	"""Applies random perspective transformation to an image, modifying the image and corresponding labels."""
	height = im.shape[0] + border[0] * 2  # shape(h,w,c)
	width = im.shape[1] + border[1] * 2
	
	# Center
	C = np.eye(3)
	C[0, 2] = -im.shape[1] / 2  # x translation (pixels)
	C[1, 2] = -im.shape[0] / 2  # y translation (pixels)
	
	# Perspective
	P = np.eye(3)
	P[2, 0] = random.uniform(-perspective, perspective)  # x perspective (about y)
	P[2, 1] = random.uniform(-perspective, perspective)  # y perspective (about x)
	
	# Rotation and Scale
	R = np.eye(3)
	a = random.uniform(-degrees, degrees)
	# a += random.choice([-180, -90, 0, 90])  # add 90deg rotations to small rotations
	s = random.uniform(1 - scale, 1 + scale)
	# s = 2 ** random.uniform(-scale, scale)
	R[:2] = cv2.getRotationMatrix2D(angle=a, center=(0, 0), scale=s)
	
	# Shear
	S = np.eye(3)
	S[0, 1] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # x shear (deg)
	S[1, 0] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # y shear (deg)
	
	# Translation
	T = np.eye(3)
	T[0, 2] = random.uniform(0.5 - translate, 0.5 + translate) * width  # x translation (pixels)
	T[1, 2] = random.uniform(0.5 - translate, 0.5 + translate) * height  # y translation (pixels)
	
	# Combined rotation matrix
	M = T @ S @ R @ P @ C  # order of operations (right to left) is IMPORTANT
	if (border[0] != 0) or (border[1] != 0) or (M != np.eye(3)).any():  # image changed
		if perspective:
			im = cv2.warpPerspective(im, M, dsize=(width, height), borderValue=(114, 114, 114))
		else:  # affine
			im = cv2.warpAffine(im, M[:2], dsize=(width, height), borderValue=(114, 114, 114))
	
	return im
