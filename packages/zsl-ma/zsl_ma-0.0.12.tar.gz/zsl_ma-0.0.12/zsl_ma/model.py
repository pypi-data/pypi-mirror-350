import torch
import torch.nn as nn


class ConvResBlock(nn.Module):
    """严格匹配图示尺寸的Conv-Res-Block"""

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        # 主分支卷积序列
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, stride, 1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1),
            nn.BatchNorm2d(out_channels)
        )

        # 残差捷径
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride),
                nn.BatchNorm2d(out_channels)
            )

        # 将ReLU作为模块成员
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(self.conv(x) + self.shortcut(x))  # 使用模块定义的ReLU


class ResBlock(nn.Module):
    """保持尺寸不变的Res-Block"""

    def __init__(self, channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, 3, 1, 1),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(channels, channels, 3, 1, 1),
            nn.BatchNorm2d(channels)
        )

    def forward(self, x):
        return x + self.block(x)


class ZeroShotModel(nn.Module):
    """严格对应图示结构的实现"""

    def __init__(self, attribute_dims=None):
        super().__init__()
        # --------------------- 阶段A ---------------------
        if attribute_dims is None:
            attribute_dims = [3, 4, 4]
        self.num = sum(attribute_dims)
        self.A = nn.Sequential(
            nn.Conv2d(3, 32, 3, 1, 1),  # 3x64x64 → 32x64x64
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )

        # --------------------- 阶段B1 ---------------------
        self.B1 = ConvResBlock(32, 64, stride=2)  # → 64x32x32

        # --------------------- 阶段B2 ---------------------
        self.B2 = ConvResBlock(64, 64, stride=2)  # → 64x16x16

        # --------------------- 阶段Cx3 ---------------------
        self.C3 = nn.Sequential(
            ResBlock(64), ResBlock(64), ResBlock(64))  # → 64x16x16

        # --------------------- 阶段B3 ---------------------
        self.B3 = ConvResBlock(64, 128, stride=2)  # → 128x8x8

        # --------------------- 阶段C4 ---------------------
        self.C4 = ResBlock(128)  # → 128x8x8

        # --------------------- 阶段B4 ---------------------
        self.B4 = ConvResBlock(128, 256, stride=2)  # → 128x4x4

        # --------------------- 阶段C5 ---------------------
        self.C5 = ResBlock(256)  # → 128x4x4

        # --------------------- 阶段D ---------------------
        self.D = nn.Sequential(
            nn.Flatten(),  # → 128
            nn.Linear(256*4*4, 4095),  # 保持维度
            nn.ReLU(inplace=True),
        )

        # 多属性分类器
        # self.classifiers = nn.ModuleList([
        #     nn.Sequential(
        #         nn.Dropout(0.5),
        #         nn.Linear(4095, 2730),
        #         nn.ReLU(inplace=True),
        #         nn.Dropout(0.5),
        #         nn.Linear(2730, 1365),
        #         nn.ReLU(inplace=True),
        #         nn.Dropout(0.5),
        #         nn.Linear(1365, 1),
        #     ) for _ in range(self.num)
        # ])
        self.classifiers = nn.ModuleList([
            nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(4095, 2730),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(2730, 1365),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(1365, dim),
            ) for dim in attribute_dims
        ])

    def forward(self, x):
        x = self.A(x)  # [B,3,64,64] → [B,32,64,64]
        x = self.B1(x)  # → [B,64,32,32]
        x = self.B2(x)  # → [B,64,16,16]
        x = self.C3(x)  # → [B,64,16,16]
        x = self.B3(x)  # → [B,128,8,8]
        x = self.C4(x)  # → [B,128,8,8]
        x = self.B4(x)  # → [B,128,4,4]
        x = self.C5(x)  # → [B,128,4,4]
        features = self.D(x)  # → [B,128]
        outputs = [cls(features) for cls in self.classifiers]

        return torch.cat(outputs, dim=1)


class CNN(nn.Module):
    def __init__(self, attribute_dims=None):
        super().__init__()
        if attribute_dims is None:
            attribute_dims = [3, 3, 3]
        self.num = sum(attribute_dims)
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Linear(256 * 8 * 8, 4096),
            nn.ReLU(),
            # nn.Linear(4096, 2048),
        )
        self.classifiers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(4096, 2048),
                nn.ReLU(inplace=True),
                nn.Linear(2048, 1024),
                nn.ReLU(inplace=True),
                nn.Linear(1024, 1),
            ) for _ in range(self.num)
        ])

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        features = self.fc(x)
        outputs = [cls(features) for cls in self.classifiers]
        return torch.cat(outputs, dim=1)



# 定义残差块
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.res = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
            nn.Conv2d(channels, channels, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
        )

    def forward(self, x):
        residual = x
        out = self.res(x)
        return out + residual


# 编码器
class Encoder(nn.Module):
    def __init__(self, attribute_dims=None):
        super().__init__()
        if attribute_dims is None:
            attribute_dims = [3, 3, 3]
        self.num = sum(attribute_dims)
        # Conv1 + ResidualBlock1
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            ResidualBlock(16)
        )
        # Conv2 + ResidualBlock2
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            ResidualBlock(32)
        )
        # Conv3 + ResidualBlock3
        self.conv3 = nn.Sequential(
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            ResidualBlock(64)
        )
        # Conv4 + ResidualBlock4
        self.conv4 = nn.Sequential(
            nn.Conv2d(64, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            ResidualBlock(128)
        )
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(128 * 4 * 4, 2048)
        self.classifiers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(2048, 2048),
                nn.ReLU(inplace=True),
                nn.Linear(2048, 1024),
                nn.ReLU(inplace=True),
                nn.Linear(1024, 1),
            ) for _ in range(self.num)
        ])


    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.flatten(x)
        features = self.fc(x)
        outputs = [cls(features) for cls in self.classifiers]
        return torch.cat(outputs, dim=1)
# --------------------- 尺寸验证 ---------------------
if __name__ == "__main__":

    model = ZeroShotModel(attribute_dims=[3, 4, 4])
    test_input = torch.randn(1, 3, 64, 64)

    print("输入尺寸:", test_input.shape)
    outputs = model(test_input)

    for i, out in enumerate(outputs):
        print(f"属性{i + 1}输出尺寸: {out.shape}")  # 应为 [2,3]
