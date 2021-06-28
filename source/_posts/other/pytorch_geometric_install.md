---
title: pytorch_geometric安装
date: 2021-05-12 11:48:01
tags:
 - 其他
categories:
 - 其他
---


1. 安装torch1.7.0

```
pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
```

2. 安装其他包

```
pip install torch-scatter -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
pip install torch-sparse -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
pip install torch-cluster -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
pip install torch-spline-conv -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
pip install torch-geometric
```

# requirements.txt

```TXT
torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
torch-scatter -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
torch-sparse -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
torch-cluster -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
torch-spline-conv -f https://pytorch-geometric.com/whl/torch-1.7.0+cpu.html
torch-geometric
```

# 淘宝镜像 

https://mirrors.aliyun.com/pypi/simple


# 参考链接

1. https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html
