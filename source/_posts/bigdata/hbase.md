---
title: Hbase使用教程
date: 2022-01-17 11:01:16
tags:
 - 大数据
 - Hbase
categories:
 - 大数据
---

# Hbase2.3.7安装

## 版本对应关系

https://hbase.apache.org/book.html#hadoop

> Hadoop2.X是Hbase推荐的版本，本次使用`Hadoop3.2`搭配`Hbase2.3`

## 下载地址

https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.3.7/hbase-2.3.7-bin.tar.gz   


## 修改`conf/hbase-env.sh`

```sh
# 配置JDK
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_311.jdk/Contents/Home
# 开启Zookeeper
export HBASE_MANAGES_ZK=true
```

## 修改`conf/hbase-site.xml`

```XML
<property>
    <!-- 单机配置 -->
    <name>hbase.cluster.distributed</name>
    <value>false</value>
</property>
<property>
    <!-- 临时文件夹 -->
    <name>hbase.tmp.dir</name>
    <value>./tmp</value>
</property>
<property>
    <name>hbase.unsafe.stream.capability.enforce</name>
    <value>false</value>
</property>
<property>
    <!-- Hbase数据存储位置 -->
    <name>hbase.rootdir</name>
    <value>/Library/Hadoop/Hbase/hbase-2.3.7/data/hbase</value>
</property>
<property>
    <!-- zookeeper数据存储位置 -->
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/Library/Hadoop/Hbase/hbase-2.3.7/data/zookeeper</value>
</property>
<property>
    <!-- Zookeeper地址 -->
    <name>hbase.zookeeper.quorum</name>
    <value>localhost:2181</value>
</property> 

```

在`/Library/Hadoop/Hbase/hbase-2.3.7`文件夹下:

```shell
cd /Library/Hadoop/Hbase/hbase-2.3.7
mkdir data
cd data
mkdir hbase
mkdir zookeeper
```

## Hbase启动

```sh
# 启动Hadoop
start-all.sh 
# 启动Hbase
cd /Library/Hadoop/Hbase/hbase-2.3.7/bin
./start-hbase.sh
```

验证是否安装成功：

```shell
jps

3440 Jps
3362 HMaster # 有HMaster则说明安装成功
1885
```

# Phoenix安装

## Phoenix简介

> Phoenix是一个HBase框架，可以通过SQL的方式来操作HBase。
>Phoenix是构建在HBase上的一个SQL层，是内嵌在HBase中的JDBC驱动，能够让用户使用标准的JDBC来操作HBase。
>Phoenix使用JAVA语言进行编写，其查询引擎会将SQL查询语句转换成一个或多个HBase Scanner，且并行执行生成标准的JDBC结果集。

## Phoenix与Hbase版本对应关系

https://phoenix.apache.org/download.html

> Current release 4.16.1 can run on Apache HBase 1.3, 1.4, 1.5 and 1.6. Current release `5.1.2` can run on Apache HBase 2.1, 2.2, `2.3` and 2.4 CDH HBase 5.11, 5.12, 5.13 and 5.14 is supported by 4.14.0.

## 下载地址

https://www.apache.org/dyn/closer.lua/phoenix/phoenix-5.1.2/phoenix-hbase-2.3-5.1.2-bin.tar.gz

## 配置

- 复制`phoenix-server-hbase-2.3-5.1.2.jar`放到`hbase/lib`目录下
- 复制`hase/conf/hbase-site.xml`到`bin`目录下

## 初始化

```shell
# 进入目录
cd /Library/Hadoop/Hbase/phoenix/phoenix-hbase-2.3-5.1.2-bin/bin
# 启动
python sqlline.py 127.0.0.1:2181
# 初始化表
> !tables
```

>20220414更新：启动该服务报错，报错信息如下:

```
java.net.UnknownHostException: bogon: bogon: nodename nor servname provided, or not known--异常
```
此时需要修改`/etc/hosts`文件，在最后一行添加:

```shell
# vim /etc/hosts
127.0.0.1 localhost bogon
```

运行[demo](https://phoenix.apache.org/installation.html):

```shell
# 创建一张表然后倒入数据
python sqlline.py 127.0.0.1:2181 ../examples/stock_symbol.sql
```

可以使用一个GUI工具[squirrel-sql](https://sourceforge.net/projects/squirrel-sql/)来去操作:

![](https://phoenix.apache.org/images/squirrel.png)

# 使用python api去链接

安装`phoenixdb`

```shell
pip install phoenixdb
```

开启`queryserver`服务:

> phoenix5.1不包含内置的`queryserver`，需要额外下载，地址为:
https://dlcdn.apache.org/phoenix/phoenix-queryserver-6.0.0/phoenix-queryserver-6.0.0-bin.tar.gz

- 将phoenix中的`phoenix-client-hbase-2.3-5.1.2.jar`以及`phoenix-server-hbase-2.3-5.1.2.jar`放到queryserver的bin目录
- 将`phoenix/bin/hbase-site.xml`放到`queryserver/bin`目录下

配置queryserver的原文如下:

> The server is packaged in a standalone jar, `phoenix-queryserver-<version>.jar`. This jar, the `phoenix-client.jar` and `HBASE_CONF_DIR` on the classpath are all that is required to launch the server.



开启queryserver服务:

```sh
cd bin
python2 queryserver.py 
```
> 需要使用`python2`开启

使用python测试

```python
import phoenixdb
import phoenixdb.cursor
database_url = "http://localhost:8765/"

conn = phoenixdb.connect(database_url, autocommit=True, cursor_factory=phoenixdb.cursor.DictCursor)
cursor = conn.cursor() 
sql = "select * from STOCK_SYMBOL"  
cursor.execute(sql)
cursor.fetchall()
```







# 参考链接
- Mac下安装HBase及详解. https://www.jianshu.com/p/510e1d599123
- 本地模式下搭建Hbase（使用自带的zookeeper）. https://blog.csdn.net/weixin_42369418/article/details/99440946
- bogon: nodename nor servname provided, or not known--异常. https://blog.uproject.cn/articles/2016/07/16/1468684624515.html



