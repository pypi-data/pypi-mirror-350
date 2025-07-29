import sys

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm


def train_one_epoch(model, train_loader, optimizer, device, criterion, epoch):
    train_loss = torch.zeros(1).to(device)
    model.train()
    train_iterator = tqdm(train_loader, file=sys.stdout, colour='blue', desc=f'the {epoch + 1} epoch is training....')
    for step, (images, attributes, _) in enumerate(train_iterator):
        images = images.to(device)
        attributes = attributes.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, attributes)

        loss.backward()
        optimizer.step()
        train_loss = (train_loss * step + loss.detach()) / (step + 1)
        train_iterator.set_postfix(loss=loss.item(), mean_loss=train_loss.item())

    return train_loss.item()


@torch.no_grad()
def val_one_epoch(model, val_loader, device, criterion, true_att, epoch):
    val_loss = torch.zeros(1).to(device)
    model.eval()
    all_predictions = []
    all_labels = []
    true_att = true_att.to(device)
    test_iterator = tqdm(val_loader, file=sys.stdout, colour='blue', desc=f'the {epoch + 1} epoch is val....')
    for step, (images, attributes, label) in enumerate(test_iterator):
        images, label = images.to(device), label.to(device)
        attributes = attributes.to(device)
        outputs = model(images)
        loss = criterion(outputs, attributes)

        val_loss = (val_loss * step + loss.detach()) / (step + 1)
        distances = torch.cdist(outputs, true_att, p=2)
        _, predicted = torch.min(distances, dim=1)
        test_iterator.set_postfix(loss=loss.item(), mean_loss=val_loss.item())
        all_predictions.extend(predicted.cpu().numpy())
        all_labels.extend(label.cpu().numpy())
    return val_loss, all_predictions, all_labels

@torch.no_grad()
def unseen_predict(model, test_loader, device, true_att, n, idx_to_labels, classes):
    """
    模型预测函数，返回DataFrame格式的预测结果（n行×m列）

    参数:
    - n: 取top-n预测结果
    - idx_to_labels: 类别索引到名称的映射字典
    - classes: 所有类别名称列表
    """
    model.eval()
    all_samples = []  # 存储所有样本的预测结果，每个样本是一个字典

    test_iterator = tqdm(test_loader, file=sys.stdout, colour='blue', desc=f'testing...')

    for step, (images, labels, img_path) in enumerate(test_iterator):
        images = images.to(device)
        outputs = model(images)

        # 处理模型输出
        # pred_attributes = torch.tensor(np.hstack([
        #     sublist.cpu().detach().numpy() for sublist in outputs
        # ]))

        # 计算距离和置信度
        distances = torch.cdist(outputs, true_att, p=2)
        pred_softmax = torch.softmax(-distances, dim=1)

        # 获取top-n预测结果
        top_n = torch.topk(pred_softmax, n)
        pred_indices = top_n.indices.cpu().detach().numpy()  # [batch_size, n]
        pred_confidences = top_n.values.cpu().detach().numpy()  # [batch_size, n]

        # 处理每个样本
        for i in range(len(images)):
            sample_data = {}  # 当前样本的所有预测结果
            sample_label = labels[i].item()

            # 1. 标注信息
            sample_data['图像路径'] = img_path[i]
            sample_data['标注类别ID'] = sample_label
            sample_data['标注类别名称'] = idx_to_labels[sample_label]

            # 2. top-n预测结果
            for j in range(n):
                pred_id = pred_indices[i, j]
                pred_name = idx_to_labels[pred_id]
                pred_conf = pred_confidences[i, j]

                sample_data[f'top-{j + 1}-预测ID'] = pred_id
                sample_data[f'top-{j + 1}-预测名称'] = pred_name
                sample_data[f'top-{j + 1}-置信度'] = pred_conf

                # top-1预测正确性
                if j == 0:
                    sample_data['top-1-预测正确'] = int(pred_id == sample_label)

            # 3. top-n整体预测正确性
            sample_data['top-n预测正确'] = int(sample_label in pred_indices[i])

            # 4. 各类别置信度（限制为前10个类别，避免列数过多）
            for idx, each in enumerate(classes):
                sample_data[f'{each}-预测置信度'] = pred_softmax[i, idx].cpu().detach().numpy()

            all_samples.append(sample_data)  # 添加当前样本到列表

        test_iterator.set_postfix()

    # 转换为DataFrame（n行×m列）
    df = pd.DataFrame(all_samples)

    # 确保列顺序符合要求
    required_columns = [
        '图像路径',
        '标注类别ID', '标注类别名称',
        'top-1-预测ID', 'top-1-预测名称', 'top-1-预测正确',
    ]

    # 添加top-2到top-n的列
    for j in range(2, n + 1):
        required_columns.extend([
            f'top-{j}-预测ID',
            f'top-{j}-预测名称',
            f'top-{j}-置信度'
        ])

    # 添加top-n预测正确性和类别置信度
    required_columns.append('top-n预测正确')
    for each in classes:
        required_columns.append(f'{each}-预测置信度')

    # 按指定顺序排列列
    df = df[required_columns]

    return df  # 返回n行×m列的DataFrame

def get_true_attributes(attributes_path):
    flattened_arrays = []
    attributes = np.load(attributes_path, allow_pickle=True)
    for file in attributes.files:
        flattened_arrays.append(attributes[file].tolist())
    return torch.tensor(flattened_arrays).float()

