---
title: pytorch语义分割
date: 2021-10-19 14:11:27
tags:
 - 其他
categories:
 - 其他
---

# segmentation_models_pytorch包

这个包中封装了一系列经典的语义分割算法，比如`Unet`。语义分割是对像素点的分割，核心的问题是`如何组织输入的数据符合其格式要求`。



# 使用案例-sui数据集

## 输入的尺寸的维度

参考这个链接https://cuijiahua.com/blog/2019/11/dl-14.html中所提到的

其中核心的解释为:

> 与标准分类值（standard categorical values）的做法相似，这里也是创建一个one-hot编码的目标类别标注——本质上即为每个类别创建一个输出通道。因为上图有5个类别，所以网络输出的通道数也为5。

因此pytorch中的输入的数据的形状为`[width, height, num_classes]`

![](https://cuijiahua.com/wp-content/uploads/2019/11/dl-14-2.jpg)

```python
num_classes = 11
base_dir = './CamVid'
test_mask = f'{base_dir}/trainannot/0001TP_006690.png'
mask = cv2.imread(test_mask, 0)
masks = [(mask == v) for v in range(num_classes)] # 这里是核心
mask = np.stack(masks, axis=-1).astype('float')
mask.shape
# (360, 480, 11)
```

TODO



