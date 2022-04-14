---
title: windows上配置大数据相关组件
date: 2022-01-05 12:45:59
tags:
 - 大数据
categories:
 - 大数据
---

| 组件                 | 下载链接                                                     |
| -------------------- | ------------------------------------------------------------ |
| hadoop3.2.3          | [下载](https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz) |
| hadoop-winutils      | [下载](https://github.com/cdarlint/winutils)                 |
| hive3.1.2            | [下载](https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz) |
| hive2.1.1            | [下载](http://archive.apache.org/dist/hive/hive-2.1.1/apache-hive-2.1.1-bin.tar.gz) |
| flume1.9.0           | [下载](https://mirrors.tuna.tsinghua.edu.cn/apache/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz) |
| mysql8.0             | [下载](https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-community-8.0.27.1.msi) |
| mysql-connector-java |                                                              |
| mysql-workbench | [下载](https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-8.0.27-winx64.msi)

> windows上全套环境推荐这一篇[博客](https://www.cnblogs.com/throwable/p/13917379.html)<sup>3</sup>，帮助我们踩了很多坑。

# hadoop

参考这一篇[博客](https://zhuanlan.zhihu.com/p/111844817)

> 需要使用`管理员权限`来打开`cmd`

# hive

## 初始化metastore

```cmd
hive --service schematool -initSchema -dbType mysql
```

## 启动Metastore

```cmd
hive --service metastore
```

## 启动hiveserver2

```cmd
hive --service hiveserver2
```

## 在windows电脑上可能出现的问题

1. `select`可以查询出数据，但是在`group by`的时候直接卡死，hadoop显示`JAVA-IOError 强制关闭链接`，可能的原因在于：
    - 内存太小，做不了这样的运算
    - 因为hive的优化，使得没有进行MapReduce任务，而是在那个hiveserver2本地机器上启动fetch task，数据量巨大的时候，就可能使它崩溃了<sup>2</sup>

# 清理Hadoop Hive 然后重来
1. 重新初始化hadoop
```cmd
hdfs namenode -format
```
2. 清空hadoop data文件夹
3. 删除metastore数据库
4. 建立metastore数据库
5. 初始化Hadoop
```cmd
hdfs namenode -format
```

# 参考链接

1. WIN10安装配置Hadoop. https://zhuanlan.zhihu.com/p/111844817
2. hive强制select * 进行MapReduce任务. https://blog.csdn.net/u010936936/article/details/86578106
3. Windows10系统下Hadoop和Hive开发环境搭建填坑指南. https://www.cnblogs.com/throwable/p/13917379.html
4. windows平台下安装配置Hive. https://blog.csdn.net/qinlan1994/article/details/90524484
5. windows10部署hive-3.1.2. https://blog.csdn.net/yamaxifeng_132/article/details/102633264
6. 
