---
title: 基于GAE的蛋白质网络聚类
date: 2021-05-12 15:24:32
tags:
categories:
 - 其他
---

# 数据读取与预处理

1. 读取所有的蛋白质数据并为其附上编号

2. 找到所有蛋白质的特征向量

3. 根据txt文件构造图

4. 读取所有时刻下的活跃节点

5. 根据时刻切分成12个图

6. 保存文件

[文件下载](process.py)

# 模型训练并保存向量Z

1. 定义device
2. 构建模型
3. 读取上一步生成的数据
4. 训练生成Z
5. 保存Z

[文件下载](train.py)

# 3. 利用Z聚类

[文件下载](cluster.py)

# 4. 参考链接

- hexo 添加静态图片
http://abonege.github.io/2016/05/25/%E5%A6%82%E4%BD%95%E5%9C%A8hexo%E4%BD%BF%E7%94%A8%E5%9B%BE%E7%89%87/

# 5. requirements.txt

[下载](requirements.txt)
