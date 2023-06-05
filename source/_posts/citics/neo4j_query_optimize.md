---
title: neo4j查询调优
date: 2022-05-20 21:31:19
tags:
 - 工作
 - 中信证券
categories:
 - 中信证券
---

在使用`py2neo`库中涉及到`多跳查询`的时候，速度很慢，也别是涉及到`10跳`以上遍历的话速度会很慢，因此需要进行查询上优化。目前优化的思路主要有：

1. 建立索引
2. 硬件优化
3. 使用其他包

在python包上，python操作neo4j的主流的包有2个，分别是:
- py2neo
- neo4j-driver

其中`neo4j-driver`是neo4j推出的官方包。
在这一篇[博客](https://www.cnblogs.com/angdh/p/10315877.html)中，作者比较了`neo4j-driver`、`py2neo`、`neo4jrestclient`三个库在运行cypher查询上的速度差异。作者的核心结论如下:

> My recommendation? Definitely **py2no is not an option**. Although it is user-friendly in many respects, it is too slow for counting queries. Neo4jrestclient is not bad, but sometimes it returns nested list structure which we have to deal with using some trick (e.g. “sum(temp,[])” which I want to avoid. So I think I would go with the Neo4j Python driver. After all it is the only official release supported by Neo4j. What is your recommendation?

在[neo4j官方社区](https://community.neo4j.com/)中这一篇[博客](https://community.neo4j.com/t/barebones-http-requests-much-faster-than-python-neo4j-driver-and-py2neo/3932)作者比较了`neo4j-rest-server`、`py2neo`以及`neo4j-driver`三种方式进行cypher查询速度的测试。

> 需要注意的是`neo4j-rest-server`在`neo4j4.x版本`被移除，因此该方式不在本次优化范围内。

测试结果如下:

![测试结果](0.png)


# 参考链接
- 对比python 链接 neo4j 驱动,py2neo 和 neo4j-driver 和 neo4jrestclient: https://www.cnblogs.com/angdh/p/10315877.html
- Barebones HTTP requests much faster than python neo4j-driver and py2neo?: https://community.neo4j.com/t/barebones-http-requests-much-faster-than-python-neo4j-driver-and-py2neo/3932
