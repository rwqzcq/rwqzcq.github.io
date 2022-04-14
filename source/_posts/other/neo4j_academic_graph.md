---
title: neo4j做学术文献数据库
date: 2021-05-21 11:40:15
tags:
 - 其他
categories:
 - 其他
---

# 下载neo4j

- neo4j 14.1 https://we-yun.com/doc/neo4j/1.4.1/neo4j-community-1.4.1-windows.zip
- neo4j desktop https://we-yun.com/doc/neo4j-desktop/1.4.1/neo4j-desktop-1.4.1-x86_64.AppImage

- 全部链接 https://we-yun.com/index.php/blog/releases-56.html

# windows下安装neo4j

1. 安装JDK11
2. 配置JDK的环境变量
3. 下载neo4j社区版
4. 进入`bin`目录，输入`neo4j console`启动服务。

# python操作neo4j

# 业务分析

构造学术文献数据库,涉及到的实体与属性有

1. 论文 paper
 - name
 - englist_title
 - year
 - abstract
 - english_abstract
 - link

2. 学位 degree
 - name

2. 作者 author
 - name

3. 学位授予单位 school
 - name

4. 关键词 keyword
 - name

5. teacher
 - name

涉及到的关系有
1. (paper) (belongs_to_author) (author)
2. (author) (belongs_to_school) (school)
3. (author) (has_degree) (degreee)
4. (paper) (has_keywords) (keyword)
5. (author) (is_student_of) (teacher)


# 代码

## 1. 导入数据到neo4j中

## 2. Cpher查询语言


# 参考链接

1. windows下安装配置neo4j. https://blog.csdn.net/jing_zhong/article/details/112557084
2. JDK配置环境变量. https://www.runoob.com/w3cnote/windows10-java-setup.html

