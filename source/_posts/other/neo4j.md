---
title: neo4j学习
date: 2022-03-26 15:44:53
tags:
 - 其他
categories:
 - 其他
---

# Neo4j安装

> jdl8 + neo4j3.5

## mac

## windows
安装好需要先`./neo4j.bat install-service`才能启动

# Neo4j导入csv文件

使用`LOAD CSV WITH HEADERS FROM file_path as line`进行导入，其中`with headers`是将第一行作为key，需要注意的是这个csv文件里面不要出现`空值`,否则会报错：

> Cannot merge the following node because of null property value for 'name':

使用`merge`而不是使用`create`来创建节点与边，以免出现重复的问题。
代码如下：

```cypher
LOAD CSV WITH HEADERS FROM 'file:///imdb_top_1000_movies.csv' AS line
with line as line where line.Title is not null and line.Certificate is not null

// 创建电影节点
merge (movie: Movie { title: line.Title, year: line.Released_Year, rating: line.IMDB_Rating, runtime: line.Runtime, overview: line.Overview})

// 创建题材节点
merge (genre: Genre { category: line.Genre})

// 创建关系: 电影-题材
merge (movie)-[: CATEGORIZATION]->(genre)

// 创建Certificate节点
merge (certificate: Certificate {type: line.Certificate})

// 创建关系: 电影-Certificate
merge (movie)-[: CERTIFICATION]->(certificate)

// 创建导演节点
merge (director: Director {name: line.Director})

// 创建关系: 电影-导演
merge (director)-[: DIRECTED]->(movie)

// 创建演员节点, 创建关系: 电影-演员

merge(actor1: Actor {name: line.Star1})
merge (actor1)-[: ACTED_ID]->(movie)

// 创建演员节点, 创建关系: 电影-演员
merge(actor2: Actor {name: line.Star2})
merge (actor2)-[: ACTED_ID]->(movie)

// 创建演员节点, 创建关系: 电影-演员
merge(actor3: Actor {name: line.Star3})
merge (actor3)-[: ACTED_ID]->(movie)
```

# Neo4j图算法

## 社群划分算法

https://neo4j.com/docs/graph-data-science/1.1/algorithms/louvain/

# Nneo4j前端可视化组件

> 官方文档: https://neo4j.com/developer/tools-graph-visualization/

## popoto.js

https://github.com/Nhogs/popoto

## Neovis.js

- https://github.com/neo4j-contrib/neovis.js
- https://www.bilibili.com/video/av201105891/


