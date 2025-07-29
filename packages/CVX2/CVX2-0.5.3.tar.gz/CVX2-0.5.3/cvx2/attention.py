import math
import torch
from torch import nn


# 定义SE注意力机制的类(Squeeze and Excitation)
class SE(nn.Module):
    """主要思想是通过对输入特征进行压缩和激励，来提高模型的表现能力"""
    def __init__(self, channel: int, ratio: int = 16):
        super(SE, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // ratio, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // ratio, channel, bias=False),
            nn.Sigmoid()
        )
 
    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y


# 通道注意力模块
class ChannelAttention(nn.Module):
    def __init__(self, in_planes: int, ratio = 16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)  # 自适应平均池化
        self.max_pool = nn.AdaptiveMaxPool2d(1)  # 自适应最大池化

        # 两个卷积层用于从池化后的特征中学习注意力权重
        self.fc = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // ratio, 1, bias=False),  # 第一个卷积层，降维
            nn.ReLU(),  # ReLU激活函数
            nn.Conv2d(in_planes // ratio, in_planes, 1, bias=False)  # 第二个卷积层，升维
        )
        self.sigmoid = nn.Sigmoid()  # Sigmoid函数生成最终的注意力权重

    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x)) # 对平均池化的特征进行处理
        max_out = self.fc(self.max_pool(x))  # 对最大池化的特征进行处理
        out = avg_out + max_out  # 将两种池化的特征加权和作为输出
        return self.sigmoid(out)  # 使用sigmoid激活函数计算注意力权重


# 空间注意力模块
class SpatialAttention(nn.Module):
    def __init__(self, kernel_size: int = 7):
        super(SpatialAttention, self).__init__()

        assert kernel_size in (3, 7), 'kernel size must be 3 or 7'  # 核心大小只能是3或7
        padding = 3 if kernel_size == 7 else 1  # 根据核心大小设置填充

        # 卷积层用于从连接的平均池化和最大池化特征图中学习空间注意力权重
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()  # Sigmoid函数生成最终的注意力权重

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)  # 对输入特征图执行平均池化
        max_out, _ = torch.max(x, dim=1, keepdim=True)  # 对输入特征图执行最大池化
        x = torch.cat([avg_out, max_out], dim=1)  # 将两种池化的特征图连接起来
        x = self.conv1(x)  # 通过卷积层处理连接后的特征图
        return self.sigmoid(x)  # 使用sigmoid激活函数计算注意力权重


# CBAM模块
class CBAM(nn.Module):
    def __init__(self, in_planes: int, ratio: int = 16, kernel_size: int = 7):
        super(CBAM, self).__init__()
        self.ca = ChannelAttention(in_planes, ratio)  # 通道注意力实例
        self.sa = SpatialAttention(kernel_size)  # 空间注意力实例

    def forward(self, x):
        out = x * self.ca(x)  # 使用通道注意力加权输入特征图
        result = out * self.sa(out)  # 使用空间注意力进一步加权特征图
        return result  # 返回最终的特征图
    

# 定义ECA注意力机制的类(Efficient Channel Attention)
class ECA(nn.Module):
    """主要是通过对图像通道进行注意力调控，提高图像特征表示的有效性"""
    def __init__(self, channel: int, b=1, gamma=2):
        super(ECA, self).__init__()
        kernel_size = int(abs((math.log(channel, 2) + b) / gamma))
        kernel_size = kernel_size if kernel_size % 2 else kernel_size + 1
 
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.conv = nn.Conv1d(1, 1, kernel_size=kernel_size, padding=(kernel_size - 1) // 2, bias=False)
        self.sigmoid = nn.Sigmoid()
 
    def forward(self, x):
        y = self.avg_pool(x)
        y = self.conv(y.squeeze(-1).transpose(-1, -2)).transpose(-1, -2).unsqueeze(-1)
        y = self.sigmoid(y)
        return x * y.expand_as(x)
    

# 定义CA注意力机制的类(Coordinate attention)
class CA(nn.Module):
    """CA可以避免全局pooling-2D操作造成的位置信息丢失，将注意力分别放在宽度和高度两个维度上，有效利用输入特征图的空间坐标信息"""

    def __init__(self, channel: int, reduction=16):
        super(CA, self).__init__()
 
        self.conv_1x1 = nn.Conv2d(in_channels=channel, out_channels=channel // reduction, kernel_size=1, stride=1,
                                  bias=False)
 
        self.relu = nn.ReLU()
        self.bn = nn.BatchNorm2d(channel // reduction)
 
        self.F_h = nn.Conv2d(in_channels=channel // reduction, out_channels=channel, kernel_size=1, stride=1,
                             bias=False)
        self.F_w = nn.Conv2d(in_channels=channel // reduction, out_channels=channel, kernel_size=1, stride=1,
                             bias=False)
 
        self.sigmoid_h = nn.Sigmoid()
        self.sigmoid_w = nn.Sigmoid()
 
    def forward(self, x):
        _, _, h, w = x.size()
 
        x_h = torch.mean(x, dim=3, keepdim=True).permute(0, 1, 3, 2)
        x_w = torch.mean(x, dim=2, keepdim=True)
 
        x_cat_conv_relu = self.relu(self.bn(self.conv_1x1(torch.cat((x_h, x_w), 3))))
 
        x_cat_conv_split_h, x_cat_conv_split_w = x_cat_conv_relu.split([h, w], 3)
 
        s_h = self.sigmoid_h(self.F_h(x_cat_conv_split_h.permute(0, 1, 3, 2)))
        s_w = self.sigmoid_w(self.F_w(x_cat_conv_split_w))
 
        out = x * s_h.expand_as(x) * s_w.expand_as(x)
        return out


# 示例使用
if __name__ == '__main__':
    channels = 32
    input = torch.rand(2, channels, 64, 64)  # 随机生成一个输入特征图

    # 模型实例化
    model = SE(channels, ratio=16)
    # 前向传播查看输出结果
    outputs = model(input)
    print('SE:', outputs.shape)  #[2, 32, 64, 64]

    block = ChannelAttention(channels, 16)  
    output = block(input)  
    print('ChannelAttention:', input.size(), output.size())  # 打印输入和输出的
    # ChannelAttention: torch.Size([1, 32, 64, 64]) torch.Size([1, 32, 1, 1])

    block = SpatialAttention(7)  
    output = block(input)  
    print('SpatialAttention:', input.size(), output.size())  # 打印输入和输出的
    # SpatialAttention: torch.Size([1, 32, 64, 64]) torch.Size([1, 1, 64, 64])

    block = CBAM(channels, 8)  # 创建一个CBAM模块，输入通道为64
    output = block(input)  # 通过CBAM模块处理输入特征图
    print('CBAM:', input.size(), output.size())  # 打印输入和输出的
    # CBAM: torch.Size([1, 32, 64, 64]) torch.Size([1, 32, 64, 64])

    # 模型实例化
    model = ECA(channels)
    # 前向传播查看输出结果
    outputs = model(input)
    print('ECA:', outputs.shape)  #[2, 32, 64, 64]

    # 模型实例化
    model = CA(channels, reduction=16)
    # 前向传播查看输出结果
    outputs = model(input)
    print('CA:', outputs.shape)  #[2, 32, 64, 64]
