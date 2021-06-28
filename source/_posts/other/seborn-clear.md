---
title: 在for循环中seaborn画图去重重复标签
date: 2021-05-13 15:28:15
tags:
categories:
 - 其他
---

# 描述

在利用seborn在一个循环中生成多张图片的时候，需要注意的是使用的的是需要清楚本步骤留下的痕迹，否则就容易出现下面的问题
![](DIP_1.png)

![](DIP_2.png)

在上面的图片中出现了`label`还有`点`的重复。

# 解决方式

## 1. matplotlib的`clf`
```python
from matplotlib import pyplot as plt
import seaborn as sns

sns.scatterplot()
plt.clf() # 这里清除

```

## 2. seaborn的`clf`
```python
from matplotlib import pyplot as plt
import seaborn as sns

fig = sns.scatterplot()
plot = fig.get_figure()
plot.clf() # 这里清楚
```


# 参考链接
1. https://stackoverflow.com/questions/36018681/stop-seaborn-plotting-multiple-figures-on-top-of-one-another