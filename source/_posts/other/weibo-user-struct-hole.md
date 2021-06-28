---
title: 微博用户结构洞分析
date: 2021-05-13 17:56:59
tags:
 - 其他
categories:
 - 其他
---

# 1. 数据预处理

- 读取数据

- 解析每一个微博，利用textrank提取出关键词

- 建立用户-关键词映射

- 建立用户-用户关系网络，以共现次数作为边的权重

- 生成networkx的Graph对象

- 生成gaphei对象供gephi来画图


# 2. 结构洞分析

# 3. 节点重要性排序

- 读取networkx文件

- pagerank排序

- 输出到csv文件

# 4. requirements.txt
```TXT
networkx
pandas
jieba
tqdm
``` 



# 参考链接

1. pajek https://blog.csdn.net/qq_34322002/article/details/102565747