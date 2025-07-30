import copy
import os
from typing import Optional, List, Dict

import pandas as pd
import torch
import wandb
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, classification_report


def make_save_dirs(root_dir):
    img_dir = os.path.join(root_dir, 'images')
    model_dir = os.path.join(root_dir, 'checkpoints')
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    print(f'The output folder:{img_dir},{model_dir} has been created.')
    return img_dir, model_dir


def calculate_metric(all_labels, all_predictions, classes, class_metric=False, average='macro avg'):
    metric = classification_report(y_true=all_labels, y_pred=all_predictions, target_names=classes
                                   , digits=4, output_dict=True)
    if not class_metric:
        metric = {
            'accuracy': metric.get('accuracy'),
            'precision': metric.get(average).get('precision'),
            'recall': metric.get(average).get('recall'),
            'f1-score': metric.get(average).get('f1-score'),
        }
        return metric
    else:
        return metric


def plot_confusion_matrix(all_labels,
                          all_predictions,
                          classes,
                          name='confusion_matrix.png',
                          normalize=None,
                          cmap=plt.cm.Blues,
                          ):
    ConfusionMatrixDisplay.from_predictions(all_labels,
                                            all_predictions,
                                            display_labels=classes,
                                            cmap=cmap,
                                            normalize=normalize,
                                            xticks_rotation=45
                                            )
    plt.savefig(name, dpi=500)
    plt.close()

def get_wandb_runs(
        project_path: str,
        default_name: str = "未命名",
        api_key: Optional[str] = None,
        per_page: int = 1000
) -> List[Dict[str, str]]:
    """
    获取指定 WandB 项目的所有运行信息（ID 和 Name）

    Args:
        project_path (str): 项目路径，格式为 "username/project_name"
        default_name (str): 当运行未命名时的默认显示名称（默认："未命名"）
        api_key (str, optional): WandB API 密钥，若未设置环境变量则需传入
        per_page (int): 分页查询每页数量（默认1000，用于处理大量运行）

    Returns:
        List[Dict]: 包含运行信息的字典列表，格式 [{"id": "...", "name": "..."}]

    Raises:
        ValueError: 项目路径格式错误
        wandb.errors.UsageError: API 密钥无效或未登录
    """
    # 参数校验
    if "/" not in project_path or len(project_path.split("/")) != 2:
        raise ValueError("项目路径格式应为 'username/project_name'")

    # 登录（仅在需要时）
    if api_key:
        wandb.login(key=api_key)
    elif not wandb.api.api_key:
        raise wandb.errors.UsageError("需要提供API密钥或预先调用wandb.login()")

    # 初始化API
    api = wandb.Api()

    try:
        # 分页获取所有运行（自动处理分页逻辑）
        runs = api.runs(project_path, per_page=per_page)
        print(f'共获取{len(runs)}个run')
        return [
            {
                "id": run.id,
                "name": run.name or default_name,
                "url": run.url,  # 增加实用字段
                "state": run.state  # 包含运行状态
            }
            for run in runs
        ]

    except wandb.errors.CommError as e:
        raise ConnectionError(f"连接失败: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"获取运行数据失败: {str(e)}") from e

def get_id(target_name, res):
    df = pd.DataFrame.from_records(res)
    # 筛选状态既不是 'finished' 也不是 'running' 的记录
    filtered = df[(df['name'] == target_name) & ~df['state'].isin(['finished', 'running'])]['id']

    if not filtered.empty:
        # 存在符合条件的记录，返回第一个 id
        return filtered.iloc[0]
    else:
        # 无符合条件的记录，获取该 name 最新的 id（按 id 降序排列取第一个）
        name_df = df[df['name'] == target_name]
        if name_df.empty:
            return '001'  # 无该 name 的任何记录时返回 None
        latest_id_str = name_df['id'].sort_values(ascending=False).iloc[0]
        # 转为数值加 1 后再格式化为三位字符串
        new_id_num = int(latest_id_str) + 1
        return f"{new_id_num:03d}"
















def auto_batch_size(
    model,
    criterion,
    optimizer,
    dataset_sample,
    device,
    max_possible=1024,
    memory_ratio=0.98
):
    """
    Automatically find the maximum feasible batch size based on GPU memory.

    Args:
        model:
        criterion:
        optimizer:
        dataset_sample:  (input_sample, label_sample)
        device:
        max_possible:
        memory_ratio:

    Returns:
    """
    model.to(device)
    if not (0 < memory_ratio <= 1):
        raise ValueError("memory_ratio must be between 0 and 1.")
    total_memory = torch.cuda.get_device_properties(device).total_memory
    allowed_memory = total_memory * memory_ratio
    print(f"Total GPU Memory: {total_memory / 1024**3:.2f} GB")
    print(f"Allowed Memory ({memory_ratio*100}%): {allowed_memory / 1024**3:.2f} GB")

    model.train()
    input_sample, label_sample = dataset_sample
    input_sample = input_sample.to(device)
    label_sample = label_sample.to(device)

    model_init = copy.deepcopy(model.state_dict())
    optimizer_init = copy.deepcopy(optimizer.state_dict())

    def try_batch_size(batch_size):

        model.load_state_dict(model_init)
        optimizer.load_state_dict(optimizer_init)
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(device)

        try:
            inputs = input_sample.unsqueeze(0).expand(batch_size, *input_sample.shape).contiguous()
            labels = label_sample.unsqueeze(0).expand(batch_size, *label_sample.shape).contiguous()
        except RuntimeError as e:
            print(f"Error generating batch size {batch_size}: {e}")
            return False

        try:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            peak_memory = torch.cuda.max_memory_allocated(device)
            if peak_memory > allowed_memory:
                print(f"Batch size {batch_size} exceeds allowed memory: {peak_memory / 1024**3:.2f} GB > {allowed_memory / 1024**3:.2f} GB")
                return False

            del inputs, outputs, loss
            torch.cuda.empty_cache()
            return True

        except RuntimeError as e:
            if 'CUDA out of memory' in str(e):
                del inputs, labels
                torch.cuda.empty_cache()
                return False
            else:
                raise e

    batch_size = 1
    while batch_size <= max_possible:
        if try_batch_size(batch_size):
            batch_size *= 2
        else:
            break

    if batch_size == 1 and not try_batch_size(1):
        raise RuntimeError("Even batch size 1 causes OOM.")

    low = batch_size // 2
    high = min(batch_size, max_possible)
    best = low
    while low <= high:
        mid = (low + high) // 2
        if try_batch_size(mid):
            best = mid
            low = mid + 1
        else:
            high = mid - 1

    # print(f'try_batch_size {best}')
    # test_batch = try_batch_size(best)
    # while not test_batch:
    #     best = best - 1
    #     print(f'try_batch_size {best}')
    #     test_batch = try_batch_size(best)
    #     print(f'{test_batch} and {not test_batch}')
    # if not try_batch_size(best):
    #     raise RuntimeError("Validation failed after finding the best batch size.")

    final_peak = torch.cuda.max_memory_allocated(device)
    print(f"Maximum feasible batch size: {best}")
    print(f"Peak memory used: {final_peak / 1024**3:.2f} GB / {allowed_memory / 1024**3:.2f} GB")
    return best