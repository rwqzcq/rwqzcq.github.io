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

##  pyspark做文本分类

> TODO 

## spark链接mysql

将jdbc链接mysql的驱动放入到`spark`的`jar`目录。

## spark链接sqlite

```python
import pandas as pd
from django.db import connection as dbconn
from app.eplots import *
import pyspark
import pyspark.sql
from pyspark.sql import SparkSession
import os
import traceback

"""
How To Use
1. cd mysite
2. python spark_sql.py
"""

# 这里可以选择本地win系统的PySpark环境执行pySpark代码，也可以使用虚拟机中PySpark环境，通过os可以配置。
os.environ['SPARK_HOME'] = r'D:\Hadoop\spark-3.1.1-bin-hadoop3.2'
# TODO python安装的路径
PYSPARK_PYTHON = r"D:\Anaconda\python"
# 当存在多个python版本环境时，不指定很可能会导致出错
os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
os.environ["PYSPARK_DRIVER_PYTHON"] = PYSPARK_PYTHON

BASE_DIR = os.getcwd()

jar_path = os.path.join(BASE_DIR, 'sqlite-jdbc-3.34.0.jar')
SPARK = SparkSession.builder.appName("SQLite").config("spark.driver.extraClassPath", jar_path).getOrCreate()

jdbc_url = 'jdbc:sqlite:' + os.path.join(BASE_DIR, 'db.sqlite3')
table_name = 'app_data'
DF = SPARK.read.format("jdbc").option("url", jdbc_url).option("dbtable", table_name).load()
DF.createOrReplaceTempView("app_data")
print('spark load success')

def load_data_from_spark(sql):
    try:
        result = SPARK.sql(sql)
        data = result.toPandas()
    except:
        traceback.print_exc()
        data = pd.read_sql(sql, dbconn)
    pdata = data
    return pdata

def spark_plot():
    page = Page(layout=Page.SimplePageLayout)
    sql = f'''
        select t.city as x,
               avg(t.price_per_meter) as y
          from app_data t
        where t.city is not null and t.price_per_meter is not null
        group by t.city
    '''
    pdata = load_data_from_spark(sql)
    x = pdata['x'].tolist()
    y = [round(float(i), 2) for i in pdata['y'].values]
    plot = simple_bar(x=x, y=y, title='城市对房均价影响', y_axis_name='平均价格(元/平方米)')
    plot.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    page.add(plot)

    page.render(os.path.join(BASE_DIR, 'templates/spark_plot.html'))
    print('gen plot success')

if __name__ == '__main__':
    spark_plot()

```

核心是：`SPARK = SparkSession.builder.appName("SQLite").config("spark.driver.extraClassPath", jar_path).getOrCreate()`

## pyspark协同过滤算法

### mysql版本

```python
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import SparkSession

# spark 初始化
spark = SparkSession.\
        Builder().\
        appName('sql').\
        master('local').\
        config('spark.executor.memory','8g').\
        config('spark.driver.memory','8g').\
        config('spark.driver.maxResultsSize','0').\
        getOrCreate()

# mysql 配置(需要修改)
prop = {
    'user': 'tianjin', 
    'password': 'tianjin', 
    'driver': 'com.mysql.cj.jdbc.Driver'
}
# database 地址(需要修改)
url = 'jdbc:mysql://localhost:3306/django_wxapp_food_recommendation'
# 读取表
data = spark.read.jdbc(url=url, table='app_usercomment', properties=prop)

# 开始算法训练
from pyspark.ml.recommendation import ALS
# 设置参数
alsExplicit  = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="good_id", ratingCol="score")
# 训练
modelExplicit = alsExplicit.fit(data)

# 预测
# spark.createDataFrame([(0, 2), (1, 0), (2, 0)], ["user", "item"])
recom = modelExplicit.transform(data).orderBy('prediction', ascending=False)
# 写到数据库
import datetime
from pyspark.sql import functions as F

def set_now(_):
    return datetime.datetime.now()

recom = recom.select('user_id', 'good_id', 'prediction')
recom = recom.withColumnRenamed('prediction', 'score')
recom = recom.withColumn('create_at', F.lit(datetime.datetime.now()))

# 存到数据库
recom.write.jdbc(url=url, table='app_userrecommend', mode='overwrite', properties=prop)

```

### sqlite版本

```python
import pyspark
import pandas as pd
import pyspark.sql
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import SparkSession
import os

# spark 初始化
# spark = SparkSession.\
#         Builder().\
#         appName('sql').\
#         master('local').\
#         config('spark.executor.memory','8g').\
#         config('spark.driver.memory','8g').\
#         config('spark.driver.maxResultsSize','0').\
#         getOrCreate()
print('spark init success')

BASE_DIR = os.getcwd()

jar_path = os.path.join(BASE_DIR, 'sqlite-jdbc-3.34.0.jar')
SPARK = SparkSession.builder.appName("SQLite").config("spark.driver.extraClassPath", jar_path).getOrCreate()

print('spark init success')

jdbc_url = 'jdbc:sqlite:' + os.path.join(BASE_DIR, 'db.sqlite3')
table_name = 'app_userrank'

data = SPARK.read.format("jdbc").option("url", jdbc_url).option("dbtable", table_name).load()
print('评分表加载成功')

# 开始算法训练
from pyspark.ml.recommendation import ALS
# 设置参数
alsExplicit  = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="book_id", ratingCol="score")
# 训练
modelExplicit = alsExplicit.fit(data)
print('模型训练成功')

# 预测
recom = modelExplicit.transform(data).orderBy('prediction', ascending=False)

# 写到数据库
import datetime
from pyspark.sql import functions as F

def set_now(_):
    return datetime.datetime.now()

recom = recom.select('user_id', 'book_id', 'prediction')
recom = recom.withColumnRenamed('prediction', 'score')
recom = recom.withColumn('create_at', F.lit(datetime.datetime.now()))
# 存到数据库
recom.write.format("jdbc").option("url", jdbc_url).option("dbtable", table_name).mode('overwrite')
print("模型运算完成!")

```

# 参考链接

1.Jupyter中通过pyspark连接Hive数据库. https://blog.csdn.net/Albert_Fang/article/details/107932131
2.pyspark环境搭建,连接hive. https://blog.csdn.net/l752820681/article/details/114482873
3. pyspark链接mysql. https://zhuanlan.zhihu.com/p/136777424
