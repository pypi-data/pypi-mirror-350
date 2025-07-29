import argparse
import os
import warnings

import pandas as pd
import torch
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision import transforms

from zsl_ma.dataset import create_dataloaders
from zsl_ma.model import ZeroShotModel
from zsl_ma.tools import calculate_metric, make_save_dirs
from zsl_ma.train_val_until import val_one_epoch, train_one_epoch

warnings.filterwarnings("ignore")
def main(configs, run=None):
    save_dir = configs.save_dir
    img_dir, model_dir = make_save_dirs(save_dir)
    device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
    print("Using {} device training.".format(device.type))
    transform = transforms.Compose([transforms.Resize((64, 64)),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    train_loader, val_loader = create_dataloaders(configs.seen_data,
                                                  configs.batch_size,
                                                  configs.seen_att,
                                                  transform=transform,
                                                  )
    metrics = {'epoch': [], 'train_loss': [], 'val_loss': [], 'accuracy': [], 'precision': [], 'recall': [],
               'f1-score': [],
               'lr': []}
    model = ZeroShotModel(attribute_dims=[3, 4, 4]).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=configs.lr)
    lr_scheduler = ReduceLROnPlateau(optimizer, 'min', factor=0.1, patience=5, min_lr=1e-9)
    criterion = CrossEntropyLoss()
    best = -1
    epochs = configs.epochs
    for epoch in range(epochs):
        training_lr = lr_scheduler.get_last_lr()[0]
        train_loss = train_one_epoch(model, train_loader, optimizer, device, criterion, epoch)
        val_loss, all_predictions, all_labels = val_one_epoch(model, val_loader, device, criterion,
                                                              val_loader.dataset.get_true_attributes(), epoch)
        result = calculate_metric(all_labels, all_predictions, train_loader.dataset.classes)
        print(result)
        lr_scheduler.step(val_loss)
        result.update({'train_loss': train_loss, 'val_loss': val_loss.item(), 'lr': training_lr})
        if run is not None:
            run.log(result)
        metrics['train_loss'].append(train_loss)
        metrics['val_loss'].append(val_loss.item())
        metrics['accuracy'].append(result['accuracy'])
        metrics['precision'].append(result['precision'])
        metrics['recall'].append(result['recall'])
        metrics['f1-score'].append(result['f1-score'])
        metrics['lr'].append(training_lr)
        metrics['epoch'].append(epoch)

        if best < result['f1-score']:
            best = result['f1-score']
            torch.save(model, os.path.join(model_dir, 'best.pth'))

    df = pd.DataFrame(metrics)
    df.to_csv(os.path.join(save_dir, '训练日志.csv'), index=False)
    if run is not None:
        run.finish()


def parse_args(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lr', type=float, default=0.1, help='learning rate')
    parser.add_argument('--epochs', type=int, default=100, help='number of epochs')
    parser.add_argument('--batch_size', type=int, default=30)
    parser.add_argument('--seen_data', type=str, default=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\B\seen')
    parser.add_argument('--save_dir', type=str, default=r'./../output')
    parser.add_argument('--seen_att', type=str, default=r'D:\Code\2-ZSL\Zero-Shot-Learning\data\B\seen\seen_att.npz')
    return parser.parse_args(args if args else [])


if __name__ == '__main__':
    opts = parse_args()
    print(opts)
    main(opts)
