---
title: 排序算法
date: 2021-09-15 01:21:39
tags:
 - 数据结构
categories:
 - 数据结构
---

# 冒泡排序

```python
def bubble_sort(arr):
    """
    从小到大排序
    https://www.cnblogs.com/qlshine/p/6017957.html
    """
    l = len(arr)
    for i in range(l):
        for j in range(i, l): # 从小到大排序，每一轮最小的已经排到i的位置了
            if arr[j] < arr[i]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
    return arr
```

# 快速排序

采用`分治策略`将一个序列切分成较小和较大的两个子序列，然后`递归`地排序两个子序列。
步骤：
- 挑选基准值：从数列中挑出一个元素，称为"基准"（pivot）;
- 分割：重新排序数列，所有比基准值小的元素摆放在基准前面，所有比基准值大的元素摆在基准后面（与基准值相等的数可以到任何一边）
- 递归排序子序列：递归地将小于基准值元素的子序列和大于基准值元素的子序列排序。

> 递归到最底部的判断条件是`数列的大小是零或一`，此时该数列显然已经有序。