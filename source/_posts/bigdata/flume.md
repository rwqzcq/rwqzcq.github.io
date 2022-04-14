---
title: Flume使用教程
date: 2021-12-17 15:22:24
tags:
 - 大数据
 - Flume
categories:
 - 大数据
 - Flume
---

# 核心架构图

![核心架构图](https://flume.liyifeng.org/_images/UserGuide_image00.png)

# 1. Spooldir对接HDFS

`flume-conf.properties`文件配置

```conf
a1.sources = r1
a1.sinks = k1
a1.channels = c1

a1.sources.r1.type = spooldir # 定义source的类型为spooldir，也就是文件
a1.sources.r1.spoolDir = /Users/renweiqiang/outSource/进行中/Hadoop_日志用户挖掘_1700/scripts/dataset/flume_data

a1.sources.r1.fileSuffix = .ok # 数据传输完成之后文件名后缀更改为.ok
a1.sources.r1.decodeErrorPolicy = IGNORE # 当从文件读取时遇到不可解析的字符时如何处理。IGNORE ：忽略无法解析的字符。

a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = hdfs://0.0.0.0:9000/flume/logs/%Y%m%d # 这里要与hadoop里面的core-site.xml保持一致

a1.sinks.k1.hdfs.fileType = DataStream
a1.sinks.k1.hdfs.filePrefix = events # 文件名前缀
a1.sinks.k1.hdfs.writeFormat = Text
a1.sinks.k1.hdfs.useLocalTimeStamp = true
a1.sinks.k1.hdfs.fileSuffix = .log # 文件名后缀
a1.sinks.k1.hdfs.batchSize = 100
a1.sinks.k1.hdfs.rollSize = 1024000 # 这里一定要调大，不然不行
a1.sinks.k1.hdfs.rollCount = 0
a1.sinks.k1.hdfs.rollInterval = 10 # 每10秒产生一个文件


a1.channels.c1.type = file
a1.channels.c1.checkpointDir = /Library/Hadoop/flume/apache-flume-1.9.0-bin/filechannel/checkpoint
a1.channels.c1.dataDirs = /Library/Hadoop/flume/apache-flume-1.9.0-bin/filechannel/data

a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

启动

```shell
flume-ng agent --conf conf --conf-file conf/flume-conf.properties --name a1 -Dflume.root.logger=INFO, console
```

hadoop中查看数据

```shell
hadoop fs -ls /flume/logs/
```


# 2. Spooldir对接hive

## 2.1 Hive相关配置

### 2.1.1 拷贝相关jar

hive根目录下的`/hcatalog/share/hcatalog`文件夹中的如下三个文件夹添加到`flume的lib`目录下

### 2.1.2 hive-site.xml

```xml
   <property>
     <name>hive.metastore.port</name>
     <value>9083</value>
   </property>
               <!-- 指定存储元数据要连接的地址 -->
   <property>
       <name>hive.metastore.uris</name>
       <value>thrift://127.0.0.1:9083</value>
   </property>
   <!-- 元数据存储授权  -->
   <property>
       <name>hive.metastore.event.db.notification.api.auth</name>
       <value>false</value>
   </property>
   <!-- Hive元数据存储版本的验证 -->
   <property>
       <name>hive.metastore.schema.verification</name>
       <value>false</value>
   </property>

    <property>
      <name>hive.support.concurrency</name>
      <value>true</value>
   </property>
   <property>
      <name>hive.exec.dynamic.partition.mode</name>
      <value>nonstrict</value> 
   </property>
   <property>
      <name>hive.txn.manager</name>
      <value>org.apache.hadoop.hive.ql.lockmgr.DbTxnManager</value>
   </property> 
   <property>
      <name>hive.compactor.initiator.on</name>
      <value>true</value> 
   </property>
   <property>
      <name>hive.compactor.worker.threads</name>
      <value>1</value> <!--这里的线程数必须大于0 :理想状态和分桶数一致--> 
   </property>
   <property>
      <name>hive.enforce.bucketing</name> 
      <value>true</value>
   </property>
   <property>
      <name>hive.server2.authentication</name> 
      <value>NOSASL</value>
   </property>

```

### 2.1.3 创建数据库


```shell
CREATE DATABASE IF NOT EXISTS sougou;
```

### 2.1.4 创建数据表

> Hive建表需要开启的策略 - ORC 格式存储 - 分桶 - 支持事务性 - 显式声明 transtions

```shell
use sougou;

CREATE TABLE IF NOT EXISTS log(
    create_at String,
    uid bigint,
    keywords String,
    rank String,
    click_url String,
    tokens String,
    token_num int,
    hour int,
    minute int,
    second int
) 
partitioned by(`time` string) clustered by(uid) into 3 buckets 
row format delimited fields terminated by ',' 
stored as orc tblproperties('transactional'='true');

```

## 2.2 Hadoop相关配置

文件夹赋权

```shell
hdfs dfs -chmod 777 /user/hive/warehouse/
```



## 2.3 Flume相关配置

### 2.3.1 创建flume的conf文件

```conf
a1.sources = r1
a1.sinks = k1
a1.channels = c1

a1.sources.r1.type = spooldir
a1.sources.r1.spoolDir = /Users/renweiqiang/outSource/进行中/Hadoop_日志用户挖掘_1700/scripts/dataset/flume_data

a1.sources.r1.fileSuffix = .ok
a1.sources.r1.decodeErrorPolicy = REPLACE

a1.sinks.k1.type = hive
a1.sinks.k1.hive.metastore = mysql://127.0.0.1:3306
a1.sinks.k1.hive.database = sougou
a1.sinks.k1.hive.table = log
a1.sinks.k1.hive.serializer = DELIMITED
a1.sinks.k1.serializer.delimiter = "\t"
a1.sinks.k1.serializer.serdeSeparator = "\t"


a1.channels.c1.type = file
a1.channels.c1.checkpointDir = /Library/Hadoop/flume/apache-flume-1.9.0-bin/filechannel/checkpoint
a1.channels.c1.dataDirs = /Library/Hadoop/flume/apache-flume-1.9.0-bin/filechannel/data

a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

### 2.3.2 启动hive-metastore

```
hive --service metastore
```


### 2.3.3 启动

```shell
cd /Library/Hadoop/flume/apache-flume-1.9.0-bin
flume-ng agent --conf conf --conf-file conf/sougou-hive-conf.properties --name a1
```

> 所有的结果都会放到`logs/flume.log`文件夹里面去！

### 2.3.4 py脚本

```python
# put the csv file into the flume_data dir
```

# 参考链接

- Flume实时监控目录Spooldir: https://blog.csdn.net/weixin_41209740/article/details/111378804
- 关于flume 中spooldir传输数据报出HDFS IO error ..... File type DataStream not supported 错误解决: https://blog.csdn.net/hui_2016/article/details/70255820
- Flume+HDFS实战及遇到的坑: https://blog.csdn.net/a_drjiaoda/article/details/84975690
- https://zhuanlan.zhihu.com/p/62904645
