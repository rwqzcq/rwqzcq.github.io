---
title: 兴业数金面试
date: 2021-05-25 13:48:50
tags:
 - 面试
categories:
 - 面试
---

# 暑期实习

## 一面

进入腾讯会议室，发现第一个面试就是我哈哈哈，好尴尬。

- 介绍在金山的实习
- SQL left join
- 聚集函数
- 窗口函数
- having where的区别
- 算法的了解
- 有写过什么开发语言

## 二面

常规面试

# 秋招

## 兴业银行总行-数据类管培生

### 笔试

- 牛客网常规数理统计题
- 如何让4个人在17分钟内过桥
- 蛇形填数

```python
def genMatrix(rows,cols):  
    #用二维数组来代表矩阵
    matrix = [[0 for col in range(cols)] for row in range(rows)]  
    for i in range(rows):  
        for j in range(cols):  
            matrix[i][j]
    return matrix

#构造蛇形填数函数
def testSnake():
    #调用genMatrix函数
    matrix = genMatrix(number, number)
    i = j = 0
    total = matrix[i][j] = 1
    while(total < number * number):
        #向右填数
        while(j + 1 < number and matrix[i][j + 1] == 0): 
            total += 1
            j += 1
            matrix[i][j] = total
        #向下填数
        while(i + 1 < number and matrix[i + 1][j] == 0):
            total += 1
            i += 1
            matrix[i][j] = total
        #向左填数
        while(j > 0 and matrix[i][j - 1] == 0): 
            total += 1
            j -= 1
            matrix[i][j] = total
        #向上填数
        while(i + 1 > 0 and matrix[i - 1][j] == 0): 
            total += 1
            i -= 1
            matrix[i][j] = total

```