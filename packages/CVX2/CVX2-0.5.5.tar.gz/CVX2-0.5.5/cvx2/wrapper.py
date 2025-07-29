import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report
import torch
from torch import nn
from torch import optim
from torch.utils.data import random_split
from typing import List, Optional, Union, Tuple, Collection, Callable
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import Dataset, Sampler
from torchvision import transforms
from torchvision.datasets import ImageFolder

from model_wrapper.utils import acc_predict
from model_wrapper import (
    ModelWrapper,
    FastModelWrapper,
    ClassifyModelWrapper,
    FastClassifyModelWrapper,
    SplitClassifyModelWrapper,
    RegressModelWrapper,
    FastRegressModelWrapper,
    SplitRegressModelWrapper,
    log_utils,
    acc_predict_dataset
)

__all__ = [
    "ModelWrapper",
    "FastModelWrapper",
    "ClassifyModelWrapper",
    "FastClassifyModelWrapper",
    "SplitClassifyModelWrapper",
    "ImageClassifyModelWrapper",
    "SplitImageClassifyModelWrapper",
    "RegressModelWrapper",
    "FastRegressModelWrapper",
    "SplitRegressModelWrapper",
]


def get_base_transform(imgsz: Union[int, tuple, list]):
    """
    根据给定的图像大小参数，返回一系列数据预处理变换。

    参数:
    imgsz (Union[int, tuple, list]): 图像大小参数。如果为整数，则图像将被调整为该大小的正方形；
                                     如果为元组或列表，则图像将被调整为指定的宽高比。

    返回:
    transforms.Compose: 包含图像大小调整和图像到张量转换的预处理步骤。
                        如果imgsz为None，则只返回图像到张量的转换。
    """
    # 检查imgsz是否提供了图像大小参数
    if imgsz:
        # 如果imgsz是整数，创建一个正方形尺寸的元组
        if isinstance(imgsz, int):
            imgsz = (imgsz, imgsz)
        # 返回一系列预处理变换，首先调整图像大小，然后将图像转换为张量
        return transforms.Compose([transforms.Resize(imgsz), transforms.ToTensor()])
    else:
        # 如果没有提供图像大小参数，仅返回将图像转换为张量的预处理步骤
        return transforms.ToTensor()


def get_train_transform(imgsz: Union[int, tuple, list]):
    """
    获取训练数据的转换器。

    如果提供了imgsz参数，根据其类型调整图像大小。总是应用一系列转换以增强训练数据的多样性。
    
    参数:
    imgsz (Union[int, tuple, list]): 图像大小。如果是整数，则将其转换为方形尺寸的元组。如果是元组或列表，则直接使用。

    返回:
    transforms.Compose: 一系列转换的组合。
    """
    if imgsz:
        # 如果imgsz是整数，将其转换为方形尺寸的元组
        if isinstance(imgsz, int):
            imgsz = (imgsz, imgsz)
        # 构建并返回一系列转换的组合，包括调整大小、颜色抖动、仿射变换、转换为张量和随机擦除
        return transforms.Compose(
            [
                transforms.Resize(imgsz),
                transforms.ColorJitter(
                    brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
                ),  # 亮度、对比度、饱和度和色相
                transforms.RandomAffine(
                    degrees=(-10, 10),
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1),
                    shear=(-10, 10),
                ),
                transforms.ToTensor(),
                transforms.RandomErasing(
                    p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)
                ),  # 遮挡
            ]
        )
    else:
        # 如果没有提供imgsz参数，返回不包括调整大小的转换组合
        return transforms.Compose(
            [
                transforms.ColorJitter(
                    brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
                ),  # 亮度、对比度、饱和度和色相
                transforms.RandomAffine(
                    degrees=(-10, 10),
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1),
                    shear=(-10, 10),
                ),
                transforms.ToTensor(),
                transforms.RandomErasing(
                    p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)
                ),  # 遮挡
            ]
        )
        return transforms.Compose(
            [
                transforms.ColorJitter(
                    brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
                ),  # 亮度、对比度、饱和度和色相
                transforms.RandomAffine(
                    degrees=(-10, 10),
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1),
                    shear=(-10, 10),
                ),
                transforms.ToTensor(),
                transforms.RandomErasing(
                    p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)
                ),  # 遮挡
            ]
        )


class ImageClassifyModelWrapper(ClassifyModelWrapper):
    """
    根文件下包含train(必须)，test(可选), val(可选)文件夹

    Examples
    --------
    >>> model_wrapper = ImageClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    0.9876
    """

    test_dir: Path

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)
        self.test_dir = None
        self.imgsz = None
        self.transform = None

    def train(
        self,
        data: Union[str, Path],
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        train_transform=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if isinstance(data, str):
            data = Path(data)

        assert data.exists(), f"Data directory {data} does not exist"

        train_dir = data / "train"
        test_dir = data / "test"
        val_dir = data / "val"
        if not val_dir.exists():
            val_dir = data / "valid"

        assert train_dir.exists(), f"Train directory {train_dir} does not exist"
        train_transform = train_transform or transform or get_train_transform(imgsz)
        self.transform = transform or get_base_transform(imgsz)
        train_set = ImageFolder(train_dir, train_transform)
        self.classes = train_set.classes
        if sampler is not None and isinstance(sampler, bool):
            if sampler:
                if weight is None:
                    sampler, weight = self.get_balance_sampler(np.array(train_set.targets), return_weights=True)
                else:
                    sampler = self.get_balance_sampler_from_weights(np.array(train_set.targets), weight)
            else:
                sampler = None
        log_utils.info(f"Classes: {self.classes}")

        if val_dir.exists():
            val_set = ImageFolder(val_dir, self.transform)
            result = super().train(
                train_set,
                val_set,
                epochs=epochs,
                optimizer=optimizer,
                scheduler=scheduler,
                lr=lr,
                T_max=T_max,
                batch_size=batch_size,
                eval_batch_size=eval_batch_size,
                sampler=sampler,
                weight=weight,
                num_workers=num_workers,
                num_eval_workers=num_eval_workers,
                pin_memory=pin_memory,
                pin_memory_device=pin_memory_device,
                persistent_workers=persistent_workers,
                early_stopping_rounds=early_stopping_rounds,
                print_per_rounds=print_per_rounds,
                drop_last=drop_last,
                checkpoint_per_rounds=checkpoint_per_rounds,
                checkpoint_name=checkpoint_name,
                show_progress=show_progress,
                eps=eps,
            )
            if test_dir.exists():
                self.test_dir = test_dir
                test_set = ImageFolder(val_dir, self.transform)
                preds, targets = acc_predict_dataset(self.best_model, test_set, eval_batch_size, 0.5, num_eval_workers, None, self.device)
                preds, targets = preds.ravel(), targets.ravel()
                metrics = self._cal_metrics(preds, targets, len(self.classes))
                self._print_metrics(metrics, targets, preds, "Test")
            else:
                preds, targets = acc_predict_dataset(self.best_model, val_set, eval_batch_size, 0.5, num_eval_workers, None, self.device)
                preds, targets = preds.ravel(), targets.ravel()
                metrics = self._cal_metrics(preds, targets, len(self.classes))
                self._print_metrics(metrics, targets, preds, "Valid")
            return result
        elif test_dir.exists():
            self.test_dir = test_dir
            test_set = ImageFolder(test_dir, self.transform)
            result = super().train(
                train_set,
                test_set,
                epochs=epochs,
                optimizer=optimizer,
                scheduler=scheduler,
                lr=lr,
                T_max=T_max,
                batch_size=batch_size,
                eval_batch_size=eval_batch_size,
                sampler=sampler,
                weight=weight,
                num_workers=num_workers,
                num_eval_workers=num_eval_workers,
                pin_memory=pin_memory,
                pin_memory_device=pin_memory_device,
                persistent_workers=persistent_workers,
                early_stopping_rounds=early_stopping_rounds,
                print_per_rounds=print_per_rounds,
                drop_last=drop_last,
                checkpoint_per_rounds=checkpoint_per_rounds,
                checkpoint_name=checkpoint_name,
                show_progress=show_progress,
                eps=eps,
            )
            preds, targets = acc_predict_dataset(self.best_model, test_set, eval_batch_size, 0.5, num_eval_workers, None, self.device)
            preds, targets = preds.ravel(), targets.ravel()
            metrics = self._cal_metrics(preds, targets, len(self.classes))
            self._print_metrics(metrics, targets, preds, "Test")
            return result
        
        return super().train(
            train_set,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            sampler=sampler,
            weight=weight,
            num_workers=num_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor,
        )
    
    def train_evaluate(
        self,
        data: Union[str, Path],
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        train_transform=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if isinstance(data, str):
            data = Path(data)

        test_dir = data / "test"
        val_dir = data / "val"
        assert test_dir.exists() or val_dir.exists() or (data / "valid").exists()
        return self.train(data, imgsz, transform, train_transform, epochs, optimizer, scheduler, lr, T_max,
                          batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory, pin_memory_device, 
                          persistent_workers, early_stopping_rounds, print_per_rounds, drop_last,
                          checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)

    def predict(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> np.ndarray:
        """
        :param source:
        :param imgsz: 图片大小
        """
        logits = self.logits(source, imgsz, batch_size)
        return acc_predict(logits.cpu())

    def predict_classes(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> list:
        """
        :param source:
        :param imgsz: 图片大小
        """
        pred = self.predict(source, imgsz, batch_size)
        return self._predict_classes(pred.ravel())

    def predict_proba(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param source:
        :param imgsz: 图片大小
        """
        logits = self.logits(source, imgsz, batch_size)
        return self._proba(logits)

    def predict_classes_proba(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> Tuple[list, np.ndarray]:
        """
        :param source:
        :param imgsz: 图片大小
        """
        indices, values = self.predict_proba(source, imgsz, batch_size)
        return self._predict_classes(indices.ravel()), values

    def logits(
        self,
        source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
        imgsz: Union[int, tuple, list] = None,
        batch_size: int = 64,
    ) -> torch.Tensor:
        imgsz = imgsz or self.imgsz 
        if imgsz:
            transform = transforms.Compose(
                [transforms.Resize(imgsz), transforms.ToTensor()]
            )
        else:
            if self.transform:
                transform = self.transform
            else:
                raise ValueError("Expected 'imgsz', but None")

        if isinstance(source, str):
            source = Path(source)
        if isinstance(source, Path):
            if source.is_file():
                source = Image.open(source)
            elif source.is_dir():
                source = (
                    img
                    for img in source.rglob("*")
                    if img.suffix in (".png", ".jpg", "jpeg") and img.is_file()
                )
                source = [transform(Image.open(s)).unsqueeze(0) for s in source]
                source = torch.cat(source, dim=0)
        if isinstance(source, Image.Image):
            source = transform(source)
            source = source.unsqueeze(0)

        return super().logits(source, batch_size)

    def acc(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        batch_size: int = 64,
        num_workers: int = 0,
    ) -> float:
        """return accuracy"""
        dataset = self._to_dataset(data, imgsz, transform)
        return super().acc(dataset, batch_size, num_workers)
    
    def confusion_matrix(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        batch_size: int = 64,
        num_workers: int = 0,
        verbose: bool = True,
    ) -> float:
        """return confusion matrix"""
        dataset = self._to_dataset(data, imgsz, transform)
        return super().confusion_matrix(dataset, batch_size, num_workers, verbose=verbose)

    def evaluate(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        batch_size: int = 64,
        num_workers: int = 0,
        verbose: bool = True,
    ) -> float:
        """return metrics"""
        dataset = self._to_dataset(data, imgsz, transform)
        return super().evaluate(dataset, batch_size, num_workers, verbose=verbose)     
    
    def classification_report(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        batch_size: int = 64,
        num_workers: int = 0,
        target_names: Optional[List] = None,
        verbose: bool = True,
    ) -> Union[str, dict]:
        dataset = self._to_dataset(data, imgsz, transform)
        return super().classification_report(dataset, batch_size, num_workers, target_names=target_names, verbose=verbose)
        
    def _to_dataset(
        self,
        data: Union[str, Path, Dataset] = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
    ) -> Dataset:
        data = data or self.test_dir
        if isinstance(data, (str, Path)):
            transform = transform or get_base_transform(imgsz)
            return ImageFolder(data, transform)
        elif isinstance(data, ImageFolder):
            data.transform = data.transform or get_base_transform(imgsz)

        return data

    def _print_metrics(self, metrics: dict, labels: np.ndarray, preds: np.ndarray, dataset_type: str) -> None:
        print()
        print("==", f"{dataset_type} Dataset Metrics", "==")
        print(f"Accuracy: {metrics['accuracy']:.2%}")
        print(f"Precision: {metrics['precision']:.2%}")
        print(f"Recall: {metrics['recall']:.2%}")
        print(f"F1: {metrics['f1']:.2%}")
        print(f"AUC: {metrics['auc']:.2%}\n")

        self._print_classification_report(classification_report(labels, preds, target_names=self.classes))
        

class SplitImageClassifyModelWrapper(ImageClassifyModelWrapper):
    """
    根文件下是分类文件夹

    Examples
    --------
    >>> model_wrapper = SplitImageClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    0.9876
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        data: Union[str, Path, ImageFolder],
        val_size=0.2,
        random_state: int = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        train_transform=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        train_set, val_set = self._before(data, val_size, random_state, imgsz, transform, train_transform)

        # 调用的是ImageClassifyModelWrapper父类ClassifyModelWrapper的train方法
        return super(ImageClassifyModelWrapper, self).train(
            train_set,
            val_set,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            sampler=sampler,
            weight=weight,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor
        )
    
    def train_evaluate(
        self,
        data: Union[str, Path, ImageFolder],
        val_size=0.2,
        random_state: int = None,
        imgsz: Union[int, tuple, list] = None,
        transform=None,
        train_transform=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose: bool = True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None
    ) -> Tuple[dict, dict]:
        train_set, val_set = self._before(data, val_size, random_state, imgsz, transform, train_transform)

        # 调用的是ImageClassifyModelWrapper父类ClassifyModelWrapper的train_evaluate方法
        return super(ImageClassifyModelWrapper, self).train_evaluate(
            train_set,
            val_set,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            sampler=sampler,
            weight=weight,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor,
            verbose=verbose,
            threshold=threshold,
            target_names=target_names,
            num_classes=num_classes
        )

    def _before(self, data, val_size: float, random_state, imgsz, transform, train_transform):
        assert 0.0 <= val_size < 1.0
        if val_size > 0.0:
            train_transform = train_transform or transform or get_train_transform(imgsz)
            if isinstance(data, (str, Path)):
                # (PIL.Image.Image, int)
                dataset = ImageFolder(root=data)
                self.transform = transform or get_base_transform(imgsz)
            elif isinstance(data, ImageFolder):
                dataset = data
                self.transform = (
                    transform or dataset.transform or get_train_transform(imgsz)
                )
            else:
                raise TypeError(
                    f"Expected str or Path or ImageFolder, but {type(data)}"
                )

            self.classes = dataset.classes
            # dataset.transform = None
            train_size = 1 - val_size
            if random_state is None:
                train_set, val_set = random_split(dataset, [train_size, val_size])
            else:
                generator = torch.Generator().manual_seed(random_state)
                train_set, val_set = random_split(dataset, [train_size, val_size], generator)
            train_set.dataset.transform = train_transform
            val_set.dataset.transform = self.transform
        else:
            val_set = None
            if isinstance(data, (str, Path)):
                train_set = ImageFolder(root=data, transform=train_transform)
            elif isinstance(data, ImageFolder):
                train_set = data
                train_set.transform = (
                    train_transform
                    or train_set.transform
                    or transform
                    or get_train_transform(imgsz)
                )
            self.classes = train_set.classes

        log_utils.info(f"Classes: {self.classes}")

        return train_set, val_set
