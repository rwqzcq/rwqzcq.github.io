---
title: Spark3.1.1使用教程
date: 2022-01-01 16:44:17
tags:
 - 大数据
categories:
 - 大数据
---

# 启动spark

```shell
source ~/.bash_profile
satrt-all.sh # 启动hadoop
cd $SPARK_HOME
./sbin/start-all.sh # 启动spark
```

# 安装pyspark

> 注意pyspark与spark的版本对应关系

```shell
sudo pip install pyspark==3.1.1
```

# pyspark链接Hive

1. hive中的`hive-site.xml`放到spark安装目录下面的`conf`文件夹下
3. hive中的`hive-site.xml`放到pyspark安装目录下面的`conf`文件夹下(没有的话就创建)
2. 将`mysql-connector-java.jar`包移动到`/Users/renweiqiang/opt/anaconda3/lib/python3.7/site-packages/jars`文件夹中。

```shell
cd /Library/Hive/apache-hive-3.1.2-bin/conf
sudo mkidr /Users/renweiqiang/opt/anaconda3/lib/python3.7/site-packages/pyspark/conf
sudo cp hive-site.xml /Users/renweiqiang/opt/anaconda3/lib/python3.7/site-packages/pyspark/conf
sudo cp hive-site.xml $SPARK_HOME/conf
cd /Library/Hive/apache-hive-3.1.2-bin/lib
sudo cp mysql-connector-java-8.0.27.jar /Users/renweiqiang/opt/anaconda3/lib/python3.7/site-packages/pyspark/jars
```

# pyspark做文本分类

## spark链接mysql

将jdbc链接mysql的驱动放入到`spark`的`jar`目录。



# 参考链接

1.Jupyter中通过pyspark连接Hive数据库. https://blog.csdn.net/Albert_Fang/article/details/107932131
2.pyspark环境搭建,连接hive. https://blog.csdn.net/l752820681/article/details/114482873
3. pyspark链接mysql. https://zhuanlan.zhihu.com/p/136777424
