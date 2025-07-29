import os

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

from zsl_ma.train_val_until import get_true_attributes


class CustomDataset(Dataset):
    def __init__(self, img_dir, att_path, transform, class_to_label=None):
        self.flattened_arrays = None
        self.root_dir = img_dir
        self.transform = transform
        self.class_to_label = class_to_label if class_to_label is not None else {}
        self.images = [f for f in os.listdir(img_dir) if f.endswith(('.bmp', '.jpg', '.png'))]
        self.attributes = np.load(att_path, allow_pickle=True)

        # 如果没有提供class_to_label字典，我们在这里创建它
        if not self.class_to_label:
            self._create_class_to_label_mapping()
            # self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.class_to_label)}
            self.idx_to_labels = {value: key for key, value in self.class_to_label.items()}

    def _create_class_to_label_mapping(self):
        # 假设类别是从0开始编号的连续整数
        self.classes = sorted(file for file in self.attributes.files)
        self.class_to_label = {cls: i for i, cls in enumerate(self.classes)}

    def get_true_attributes(self):
        self.flattened_arrays = []
        for file in self.attributes.files:
            self.flattened_arrays.append(self.attributes[file].tolist())
        return torch.tensor(np.array(self.flattened_arrays)).float()

    def get_class_to_label(self):
        return self.class_to_label

    def save_label_mapping(self):
        save_dir = os.path.join(os.path.dirname(self.root_dir))
        np.save(os.path.join(save_dir, 'idx_to_labels.npy'), self.idx_to_labels)
        np.save(os.path.join(save_dir, 'classes_to_idx.npy'), self.class_to_label)
        np.save(os.path.join(save_dir, 'classes.npy'), self.classes)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        # 获取图片路径
        image_path = os.path.join(self.root_dir, self.images[idx])
        # 打开图片并转换为RGB格式
        image = Image.open(image_path)
        # 如果有变换，则进行变换
        if self.transform:
            image = self.transform(image)

        # 提取文件名中的类别
        base_filename = os.path.splitext(self.images[idx])[0]
        class_name = base_filename.split('_')[0]
        # 将类别转换为标签
        attributes = torch.tensor(self.attributes[class_name].tolist()).float()
        label = self.class_to_label[class_name]

        return image, attributes, label


class TestDataset(Dataset):
    def __init__(self, img_dir, class_to_label, transform):
        self.flattened_arrays = None
        self.root_dir = img_dir
        self.transform = transform
        self.class_to_label = class_to_label
        self.images = [f for f in os.listdir(img_dir) if f.endswith(('.bmp', '.jpg', '.png'))]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        # 获取图片路径
        image_path = os.path.join(self.root_dir, self.images[idx])
        # 打开图片并转换为RGB格式
        image = Image.open(image_path)
        # 如果有变换，则进行变换
        # if self.transform:
        image = self.transform(image)
        # 提取文件名中的类别
        base_filename = os.path.splitext(self.images[idx])[0]
        class_name = base_filename.split('_')[0]
        label = self.class_to_label[class_name]

        return image, label, image_path


def create_dataloaders(data_dir, batch_size, att_path, transform=transforms.ToTensor(), num_workers=0,
                       train_shuffle=True):
    # 训练集数据加载器
    train_dir = os.path.join(data_dir, 'train')
    train_dataset = CustomDataset(img_dir=train_dir, att_path=att_path, transform=transform)
    # 初始化验证集Dataset
    validation_dir = os.path.join(data_dir, 'val')  # 替换为你的验证集图片目录
    validation_dataset = CustomDataset(img_dir=validation_dir, transform=transform, att_path=att_path)
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=train_shuffle,
                              num_workers=num_workers)
    val_loader = DataLoader(dataset=validation_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader


if __name__ == '__main__':
    print()
    # transform = transforms.Compose([transforms.ToTensor()])
    # train_data = CustomDataset(img_dir=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\seen\train',
    #                            att_path=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\seen\seen_att.npz',
    #                            transform=transform)
    # unseen_data = CustomDataset(img_dir=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\unseen\images',
    #                             att_path=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\unseen\unseen_att.npz',
    #                             transform=transform)
    # train_data.save_label_mapping()
    # unseen_data.save_label_mapping()
    # un = unseen_data.get_true_attributes()

    # val_data = CustomDataset(img_dir=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\seen\val',
    #                          att_path=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\seen_att.npz',
    #                          transform=transform)
    # print(train_data.classes == val_data.classes)
#     train_loader = DataLoader(dataset=train_data, batch_size=1, shuffle=False)
#     for img, att in train_loader:
#         print(att)
#     un = get_true_attributes(r'D:\Code\2-ZSL\Zero-Shot-Learning\data\A\unseen\unseen_att.npz')
#     print()
