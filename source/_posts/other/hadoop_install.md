---
title: MAC上hadoop全家桶安装
date: 2021-07-28 17:39:21
tags:
 - 其他
categories:
 - 其他
---

# 版本对应问题

- hadoop==3.2.2
- java=1.8

# 1. 安装jdk1.8

下载链接: http://www.oracle.com/technetwork/java/javasebusiness/downloads/

> mac在安装java的时候会默认把java添加进环境变量

除此之外，还需要自己去配置环境变量。


# 2. 安装hadoop3.2.2

下载链接: https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz
或者从清华镜像里面去下载：https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz

运行wordcount程序的时候报错如下：

```TXT
[2021-12-15 23:57:46.370]Container exited with a non-zero exit code 127. Error file: prelaunch.err.
Last 4096 bytes of prelaunch.err :
Last 4096 bytes of stderr :
/bin/bash: /Library/Internet: No such file or directory
```

原因在于hadoop默认使用的java_home是环境变量为`/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home`，我们需要指定我们使用的是自己`设定的JAVA_HOME`，具体需要做的是修改`etc/hadoop/hadoop-env.sh`里面的`JAVA_HOME`，然后cd到这个目录里面去`sh hadoop-env.sh`，最后重启即可完成！

`hadoop-env.sh`修改如下:
```shell
# 54行
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_311.jdk/Contents/Home

```

# 3. 运行hadoop

```shell
start-all.sh
jps # 查看是否已经启动
```

# 4. 安装Hive

## 4.1 下载Hive

注意版本：`3.1.2`与hadoop3.2.2对应，下载地址为: https://dlcdn.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz
也可以使用清华镜像，地址为https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-3.1.2/

下载好之后放到`/Library/Hive`文件夹里面，然后添加环境变量:

```shell
export HIVE_HOME=/Library/Hive/apache-hive-3.1.2-bin
export PATH=$HIVE_HOME/bin:$PATH
```

在命令行中输入`hive`后报错信息如下：

```shell
SLF4J: Found binding in [jar:file:/Library/Hive/apache-hive-3.1.2-bin/lib/log4j-slf4j-impl-2.10.0.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/Library/Hadoop/hadoop-3.2.2/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Exception in thread "main" java.lang.NoSuchMethodError: com.google.common.base.Preconditions.checkArgument(ZLjava/lang/String;Ljava/lang/Object;)V
    at org.apache.hadoop.conf.Configuration.set(Configuration.java:1357)
    at org.apache.hadoop.conf.Configuration.set(Configuration.java:1338)
    at org.apache.hadoop.mapred.JobConf.setJar(JobConf.java:536)
    at org.apache.hadoop.mapred.JobConf.setJarByClass(JobConf.java:554)
    at org.apache.hadoop.mapred.JobConf.<init>(JobConf.java:448)
    at org.apache.hadoop.hive.conf.HiveConf.initialize(HiveConf.java:5141)
    at org.apache.hadoop.hive.conf.HiveConf.<init>(HiveConf.java:5099)
    at org.apache.hadoop.hive.common.LogUtils.initHiveLog4jCommon(LogUtils.java:97)
    at org.apache.hadoop.hive.common.LogUtils.initHiveLog4j(LogUtils.java:81)
    at org.apache.hadoop.hive.cli.CliDriver.run(CliDriver.java:699)
    at org.apache.hadoop.hive.cli.CliDriver.main(CliDriver.java:683)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:483)
    at org.apache.hadoop.util.RunJar.run(RunJar.java:323)
    at org.apache.hadoop.util.RunJar.main(RunJar.java:236)
```

这个原因是在于hive中的包与hadoop中的包没有对应上所导致的，解决方法是:

1. com.google.common.base.Preconditions.checkArgument这个类所在的jar包为：guava.jar

2. hadoop-3.2.2（路径：hadoop\share\hadoop\common\lib）中该jar包为 cd ；而hive-3.1.2(路径：hive/lib)中该jar包为guava-19.0.1.jar

3. 将jar包变成一致的版本：删除hive中低版本jar包，将hadoop中高版本的复制到hive的lib中。同时也需要把这个放到flume的lib文件夹。

以上内容复制自该博客[hive启动报错](https://www.cnblogs.com/syq816/p/12632028.html)

## 4.2 下载Mysql驱动

下载地址: https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.27.tar.gz

然后放到`lib`目录下。

## 4.3 在mysql中创建`metastore`数据表


## 4.4 创建conf/hive-site.xml

```xml
<configuration>
   <!-- 配置mysql -->
    <property>
       <name>javax.jdo.option.ConnectionURL</name>
       <value>jdbc:mysql://localhost:3306/metastore?createDatabaseIfNotExist=true</value>
    </property>
  
    <property>
       <name>javax.jdo.option.ConnectionDriverName</name>
       <value>com.mysql.cj.jdbc.Driver</value>
    </property>
    <property>
       <name>javax.jdo.option.ConnectionUserName</name>
       <value>hive</value>
    </property>

    <property>
       <name>javax.jdo.option.ConnectionPassword</name>
       <value>hive</value>
    </property>
</configuration>
```

## 4.4 初始化schema

```shell
schematool -initSchema -dbType mysql
```


## 4.5 创建一个表来测试

```shell
hive
create table test(a string, b int);
show databases;

```

# 5. flume

## 5.1 下载链接

可以使用官方的：https://dlcdn.apache.org/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz

也可以使用清华镜像: https://mirrors.tuna.tsinghua.edu.cn/apache/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz

## 5.2 安装

编辑`.bash_profile`

```shell
# add flume
export FLUME_HOME=/Library/Hadoop/Flume/apache-flume-1.9.0-bin
export FLUME_CONF_DIR=$FLUME_HOME/conf
export PATH=$FLUME_HOME/bin:$PATH
```

## 5.3 配置`conf/flume-env.sh`

```shell
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_141.jdk/Contents/Home
export JAVA_OPTS="-Xms100m -Xmx2000m -Dcom.sun.management.jmxremote"
```

## 5.4 测试

```TXT
flume-ng version

Source code repository: https://git-wip-us.apache.org/repos/asf/flume.git
Revision: d4fcab4f501d41597bc616921329a4339f73585e
Compiled by fszabo on Mon Dec 17 20:45:25 CET 2018
From source with checksum 35db629a3bda49d23e9b3690c80737f9
```

> windows电脑上如果需要hive的话需要将hive加入到环境变量

# 6. Spark

Spark与Hadoop是一脉相承的，可以认为是MapReduce2.0。使用spark之前首先需要安装`scala`。

## 6.1 下载安装scala

下载`scala2.12.13`(https://downloads.lightbend.com/scala/2.12.13/scala-2.12.13.tgz))，然后放到`/usr/local`文件夹里面去。

```shell
cd /usr/local
sudo mkdir scala
mv ~/Downloads/scala-2.12.13.tgz ./
sudo tar -zxvf scala-2.12.13.tgz
sudo rm scala-2.12.13.tgz
```

编辑`.bash_profile`:
```shell
SCALA_HOME=/usr/local/scala/scala-2.12.13
export PATH=$PATH:$SCALA_HOME/bin
```

## 6.2 下载安装spark

下载[`spark-3.1.1`](https://www.apache.org/dyn/closer.lua/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz) <!-- 官方网站上没有找到3.1.1的 -->
然后执行下面的操作:

```shell
cd /Library/Hadoop
mkdir Spark
cd Spark
mv ~/.spark-3.1.1-bin-hadoop3.2.tgz ./
sudo tar -zvxf spark-3.1.1-bin-hadoop3.2.tgz
sudo rm spark-3.1.1-bin-hadoop3.2.tgz
```

编辑`.bash_profile`:
```shell
SPARK_HOME=/Library/Hadoop/Spark/spark-3.1.1-bin-hadoop3.2
export PATH=$PATH:$SPARK_HOME/bin
```
`source ~/.bash_profile`使环境变量生效。

## 6.3 启动spark

```shell
cd $SPARK_HOME
./sbin/start-master.sh # 启动master
./sbin/start-worker.sh spark://renweiqiangdeMacBook-Pro.local:7077 # 启动slave
./sbin/start-all.sh # 启动所有
```

`jsp`查看情况

```txt
(base) renweiqiang@renweiqiangdeMacBook-Pro spark-3.1.1-bin-hadoop3.2 % jps
8132 NameNode
9974 Master
8232 DataNode
10026 Jps
10011 Worker
8556 ResourceManager
8652 NodeManager
8366 SecondaryNameNode
```

访问`localhost:8080`就能看到相应的信息





# 参考链接
- mac安装jdk1.8: https://www.jianshu.com/p/26db5674d1f9
- mac卸载java: https://www.jianshu.com/p/3ab3fcfb8bcd
- mac配置java Home: https://www.jianshu.com/p/27e494e45f78
- naco mac 启动报错 /Library/Internet: No such file or directory: https://blog.csdn.net/fynzhy/article/details/118148883
- hadoop执行wordcount报错: https://blog.csdn.net/qq_33609401/article/details/80912808
- jdk和hadoop和hbase的版本对应: https://blog.csdn.net/weixin_43582443/article/details/115140601
- hive启动报错-java.lang.NoSuchMethodError: com.google.common.base.Preconditions.checkArgument: https://www.cnblogs.com/syq816/p/12632028.html
- Hive环境搭建-Mac、Hadoop、Yarn、Hive、MySQL: https://zhuanlan.zhihu.com/p/65825211
- Hive与Hbase的区别: https://zhuanlan.zhihu.com/p/30023920
- mac配置Flume: https://blog.csdn.net/vbirdbest/article/details/104479258
- mac安装Flume: https://blog.csdn.net/qq_38262266/article/details/108628496
- Flume1.9中文文档. https://flume.liyifeng.org/#agent
- hadoop. https://towardsdatascience.com/installing-hadoop-on-a-mac-ec01c67b003c
- Spark. https://blog.csdn.net/qq_42855570/article/details/115146839
- Hive. https://blog.csdn.net/vbirdbest/article/details/104139457
- Hadoop安装教程Mac版. https://blog.csdn.net/qq_42855570/article/details/115146839


