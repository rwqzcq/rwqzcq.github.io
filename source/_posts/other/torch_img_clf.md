---
title: 基于pytorch的图像分类算法
date: 2021-10-18 01:07:51
tags:
 - 其他
categories:
 - 其他
---

# 基于DenseNet的图像分类算法

```python
import pandas as pd
import torch
import torchvision
import os
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from skimage import io,transform
from PIL import Image
from torchvision import datasets, models, transforms
import torch.nn as nn
import torch.optim as optim
import time
from tqdm import tqdm
from sklearn.metrics import classification_report

from utils import * # 引入自己的类库

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def load_model(num_classes):
    """
    加载模型
    """
    densenet = models.densenet121(pretrained=True)
    for param in densenet.parameters():
        param.requires_grad = False # 冻结参数

    fc_inputs = densenet.classifier.in_features
    densenet.classifier = nn.Sequential( # 设置分类算法
        nn.Linear(fc_inputs, 512),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(512, num_classes)
#         nn.Softmax(dim=1)
    )
    return densenet.to(device)

train_data, valid_data, train_data_size, valid_data_size = load_dataset(batch_size=64)

def train_and_valid(model, loss_function, optimizer, epochs=25):
    """
    训练测试
    """
    
    history = []
    best_acc = 0.0
    best_epoch = 0
 
    for epoch in range(epochs):
        epoch_start = time.time()
        print("Epoch: {}/{}".format(epoch+1, epochs))
 
        model.train()
 
        train_loss = 0.0
        train_acc = 0.0
        valid_loss = 0.0
        valid_acc = 0.0


        for (inputs, labels) in tqdm(train_data):
            inputs = inputs.to(device)
            labels = labels.to(device)
 
            #因为这里梯度是累加的，所以每次记得清零
            optimizer.zero_grad()
 
            outputs = model(inputs)
 
            loss = loss_function(outputs, labels)
 
            loss.backward()
 
            optimizer.step()
 
            train_loss += loss.item() * inputs.size(0)
 
            ret, predictions = torch.max(outputs.data, 1)
            correct_counts = predictions.eq(labels.data.view_as(predictions))
 
            acc = torch.mean(correct_counts.type(torch.FloatTensor))
 
            train_acc += acc.item() * inputs.size(0)

        with torch.no_grad():
            model.eval()
 
            for j, (inputs, labels) in enumerate(valid_data):
                inputs = inputs.to(device)
                labels = labels.to(device)
 
                outputs = model(inputs)
 
                loss = loss_function(outputs, labels)
 
                valid_loss += loss.item() * inputs.size(0)
 
                ret, predictions = torch.max(outputs.data, 1)
                correct_counts = predictions.eq(labels.data.view_as(predictions))
 
                acc = torch.mean(correct_counts.type(torch.FloatTensor))
 
                valid_acc += acc.item() * inputs.size(0)

        avg_train_loss = train_loss/train_data_size
        avg_train_acc = train_acc/train_data_size
 
        avg_valid_loss = valid_loss/valid_data_size
        avg_valid_acc = valid_acc/valid_data_size
 
        history.append([avg_train_loss, avg_valid_loss, avg_train_acc, avg_valid_acc])
 
        if best_acc < avg_valid_acc:
            best_acc = avg_valid_acc
            best_epoch = epoch + 1
 
        epoch_end = time.time()
 
        print("Epoch: {:03d}, Training: Loss: {:.4f}, Accuracy: {:.4f}%, \n\t\tValidation: Loss: {:.4f}, Accuracy: {:.4f}%, Time: {:.4f}s".format(
            epoch+1, avg_valid_loss, avg_train_acc*100, avg_valid_loss, avg_valid_acc*100, epoch_end-epoch_start
        ))
        print("Best Accuracy for validation : {:.4f} at epoch {:03d}".format(best_acc, best_epoch))
 
        torch.save(model, f'./models/densenet/{epoch+1}.pt')
    return model, history

model = load_model(num_classes=281)
loss_func = nn.CrossEntropyLoss() # 交叉熵自带了softmax
optimizer = torch.optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)
trained_model, history = train_and_valid(model, loss_func, optimizer, 40)

# TODO do other things

```

> 在进行`281`分类任务的时候在模型定义部分最后加上了`nn.Softmax(dim=1)`导致了`loss一直没有变化`，也就是没有收敛，所以如果使用了交叉熵作为损失函数，则在模型定义部分不用`softmax`

参考链接: https://blog.csdn.net/RH_Wang/article/details/110229268
