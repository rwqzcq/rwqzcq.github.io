---
title: 常用代码集合
date: 2022-04-26 16:32:20
tags:
 - 其他
categories:
 - 其他
---

# sqlalchemy链接sqlite

```python

import sqlalchemy
db_path = '/Users/renweiqiang/outSource/进行中/0430_22682_空气质量指数/mysite/db.sqlite3'
# 创建链接引擎
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')
# 链接数据库
conn = engine.connect()
# CODE

# 关闭数据库
conn.close()
```

# sqlalchemy链接mysql

```python

import sqlalchemy
import pymysql

host = '127.0.0.1'
port = '3306'
username = 'tianjin'
password = 'tianjin'
db_name = 'disk_3256'

engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}",echo=True)
conn = engine.connect()

```

# pandas to_sql

## 慢速

```python
import sqlalchemy
import pandas as pd

db_path = '/Users/renweiqiang/outSource/进行中/0430_22682_空气质量指数/mysite/db.sqlite3'
# 创建链接引擎
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')
# 链接数据库
conn = engine.connect()

# 导入数据库
df = None
df.to_sql('table_name', conn, if_exists='append', index=False, chunksize=2000)

```

## 快速导入

```python
import sqlalchemy
import pandas as pd
import cStringIO

db_path = '/Users/renweiqiang/outSource/进行中/0430_22682_空气质量指数/mysite/db.sqlite3'
# 创建链接引擎
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')

output = cStringIO.StringIO()
# ignore the index
df_a.to_csv(output, sep='\t',index = False, header = False)
output.getvalue()
# jump to start of stream
output.seek(0)
 
connection = engine.raw_connection() #engine 是 from sqlalchemy import create_engine
cursor = connection.cursor()
# null value become ''
cursor.copy_from(output, table_name, null='')
connection.commit()
cursor.close()

"""
————————————————
版权声明：本文为CSDN博主「Lenskit」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/chenkfkevin/article/details/72911525
"""
```

# 停用词过滤

```python

```

# scikit-learn文本分类

```python

```

# requests爬虫

```python

import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}
url = ''
try:
    response = requests.get(url, headers=headers)
except: 
    print(url, '请求失败')
    return False

if response.status_code != 200:
    print('响应码: ', response.status_code)
    return False

response.encoding = 'UTF-8'
html = response.text

# 解析

```

# scikit-surprise协同过滤

# select2插件使用

```html
<!-- 引入资源 -->
<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

<script>
    $(function(){
        // 启动该插件
        $('selector').select2();
    });
</script>
```
# layui弹窗

```html
<!-- 引入资源 -->
<script src="https://cdn.bootcdn.net/ajax/libs/layer/3.5.1/layer.min.js"></script>

<script>
    $(function(){
        // layui弹窗
        layer.open({
            type: 2,
            title: title,
            content: url,
            area:['95%', '700px'],
        });
    });
</script>

```

# table 左右滑动

```html
    <style>
        div.table-area {
            white-space: nowrap; 
            overflow: hidden; 
            overflow-x: scroll; -webkit-backface-visibility: hidden; -webkit-overflow-scrolling: touch;
        }
    </style>
```

# 基于物品的协同过滤

# 基于用户的协同过滤