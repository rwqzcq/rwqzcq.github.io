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
db_path = os.path.join(os.path.dirname(os.getcwd()), 'db.sqlite3')

# 创建链接引擎
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')
# 链接数据库
conn = engine.connect()
# CODE

# 关闭数据库
conn.close()
```

# sqlalchemy链接mysql

> 20230205更新，sqlalchemy需要安装`1.4.35`版本

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

# 清空数据

sql = f'''delete from table
        '''
with engine.connect() as conn:
    conn.execute(sql)

# 导入数据库
# 链接数据库
conn = engine.connect()
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

## 训练

```python

import pandas as pd
from tqdm import tqdm
from sklearn.utils import shuffle
import jieba
import joblib
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import *
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import pickle as pkl

def load_stopwords():
    stopwords = set()
    with open('./stopwords.txt', encoding='UTF-8') as fp:
        for line in fp:
            stopwords.add(line.strip())
    return stopwords


# 加载停用词
stopwords = load_stopwords()


def token_filter(token):
    """
    关键词过滤
    """
    token = token.strip()
    if len(token) in [0, 1]:
        return False
    if token in stopwords:
        return False
    return True


# 读取数据
pos_df = pd.read_csv('./data/pos.txt', header=None, sep='    ')
print(pos_df)
pos_df.columns = ['label', 'content']
neg_df = pd.read_csv('./data/neg.txt', header=None, sep='    ')
neg_df.columns = ['label', 'content']
# 合并数据
df = pd.concat([pos_df, neg_df])
# 去重
df = df.drop_duplicates()
df = df.dropna()
df['label'] = df['label'].replace(-1, 0)

# 分词 去除停用词
X = []
y = []
for label, content in tqdm(df.values):
    y.append(label)
    tokens = list(jieba.cut(content))
    tokens = ' '.join(
        [token for token in tokens if token_filter(token) is True]
    )
    X.append(tokens)

# 打散数据
X, y = shuffle(X, y)

# 数据切分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print('splited ok!')
# 训练模型
clf = Pipeline([
    ('word_count', CountVectorizer()),
    ('tfidf', TfidfTransformer()),  
    ('svm', SVC())
])
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))  # 评测指标

with open('./models/clf.svm.pkl', 'wb') as wp:
    pkl.dump(clf, wp)


```

## 预测

```python

import pickle as pkl
import jieba

def load_stopwords():
    stopwords = set()
    with open('./stopwords.txt', encoding='UTF-8') as fp:
        for line in fp:
            stopwords.add(line.strip())
    return stopwords


# 加载停用词
stopwords = load_stopwords()

def token_filter(token):
    """
    关键词过滤
    """
    token = token.strip()
    if len(token) in [0, 1]:
        return False
    if token in stopwords:
        return False
    return True

clf = None
with open('models/clf.svm.pkl', 'rb') as fp:
    pkl.load(fp)

def predict(sentence):
    tokens = list(jieba.cut(sentence))
    tokens = ' '.join(
        [token for token in tokens if token_filter(token) is True]
    )
    tokens = [tokens, ]
    y_pred = clf.predict(tokens)
    return y_pred


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

```python

from surprise import BaselineOnly
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise.model_selection import cross_validate
from surprise.model_selection import KFold
from surprise.model_selection import train_test_split
import pandas as pd

# 生成一个dataframe，需要3列，分别是用户id(userId)、物品Id(itemId)、评分(rating)
df = pd.DataFrame(data=[])
df.columns = ['userId', 'itemId', 'rating']

# 1. 生成reader
reader = Reader(rating_scale=(1, 5))

# 2. 构造data
# The columns must correspond to user id, item id and ratings (in that order).
dataset = Dataset.load_from_df(df[['userId', 'itemId', 'rating']], reader)
trainset = dataset.build_full_trainset()

# 3. 训练基于物品的协同过滤模型，把user_based值设置为false
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBasic(sim_options=sim_options)
algo.fit(trainset)

# 4. 预测
item_id = 57641555
# 转化为Inner_id
inner_id = algo.trainset.to_inner_iid(item_id)
sim_inner_ids = algo.get_neighbors(inner_id, k=10) # 找到10个相似的item
# 找到推荐的商品
recommend_items = [algo.trainset.to_raw_iid(i) for i in sim_inner_ids]
```

# 基于用户的协同过滤

```python

from surprise import BaselineOnly
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise.model_selection import cross_validate
from surprise.model_selection import KFold
from surprise.model_selection import train_test_split
import pandas as pd

# 生成一个dataframe，需要3列，分别是用户id(userId)、物品Id(itemId)、评分(rating)
df = pd.DataFrame(data=[])
df.columns = ['userId', 'itemId', 'rating']

# 1. 生成reader
reader = Reader(rating_scale=(1, 5))

# 2. 构造data
# The columns must correspond to user id, item id and ratings (in that order).
dataset = Dataset.load_from_df(df[['userId', 'itemId', 'rating']], reader)
trainset = dataset.build_full_trainset()

# 3. 训练基于物品的协同过滤模型，把user_based值设置为True
sim_options = {'name': 'pearson_baseline', 'user_based': True}
algo = KNNBasic(sim_options=sim_options)
algo.fit(trainset)

# 4. 预测
user_id = 57641555
# 转化为Inner_id
inner_user_id = algo.trainset.to_inner_uid(user_id)
sim_inner_user_ids = algo.get_neighbors(inner_id, k=10) # 找到10个相似的item
# 找到推荐的用户
recommend_users = [algo.trainset.to_raw_uid(i) for i in sim_inner_user_ids]

# 与django结合
recom_qs = []
for nuid in recommend_users:
    # 找到用户评分最高的对象
    m = Rating.objects.filter(user__id=nuid).order_by('-rating')[0].movie
    recom_qs.append(m)

```

# LDA主题分析

## sklearn版

## gensim版

# pandas.to_html与bootstrap结合，table左右浮动

```html

<style>
    table {
        font-size:0.75rem;
    }
    .table-area {
        white-space: nowrap; 
        overflow: hidden; 
        overflow-x: scroll; 
        overflow-y: scroll; 
        -webkit-backface-visibility: hidden; 
        -webkit-overflow-scrolling: touch;
        height: 700px;
    }
</style>
<div class="table-area text-center">
    {{ table|safe }}
</div>
<script>
    $(function(){
        $('table').addClass('table table-borderd table-striped');
        $('table thead tr').attr('style', '');
    });
</script>

```

# django发送email

## mysite/settings.py

```python
# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
#发送邮件的邮箱
EMAIL_HOST_USER = 'rwqccnuimd@mails.ccnu.edu.cn'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = ''
#收件人看到的发件人
EMAIL_FROM = 'rwqccnuimd@mails.ccnu.edu.cn'
EMAIL_USE_SSL = True
```

## views.py

```python
from django.core.mail import send_mail
from mysite.settings import *

subject = '郑州道路拥堵预警'	#主题
message = '我是内容'	#内容
sender = EMAIL_FROM		#发送邮箱，已经在settings.py设置，直接导入
email = '2667743665@qq.com'
# email = '1024749861@qq.com'
receiver = [email, ]	#目标邮箱 切记此处只能是列表或元祖
html_msg = '<h1>Hello World</h1>'
send_mail(subject, message, sender, receiver, html_message=html_message)
```

# pyecharts饼图带上比例

```python
plot.set_series_opts(
    label_opts=opts.LabelOpts(formatter="{b}: {d}%")
)
```

# pyecharts折线图去掉label

```python
plot.set_series_opts(
    label_opts=opts.LabelOpts(is_show=False)
)
```

# pyecharts关系图变成有向图

```python
c = (
    Graph(init_opts=opts.InitOpts(chart_id='myChart', height="800px"))
    .add(
        "",
        echarts_nodes_data,
        echarts_edge_data,
        repulsion=4000,
        # 参考：https://blog.csdn.net/hj009zzh/article/details/114928411
        edge_symbol=['circle', 'arrow'] # 这里控制是否显示
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Attack Path"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False), tooltip_opts=opts.TooltipOpts())
    .render("攻击路径可视化.html")
)
```

# 关联规则

```python

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_csv('./data.csv', header=0)
data = []
for i in df.groupby(['读者ID']):
    i = i[1]
    if i.shape[0] >= 2:
        data.append(i['图书ID'].tolist())

records = data
te = TransactionEncoder()
#进行 one-hot 编码
te_ary = te.fit(records).transform(records)
df = pd.DataFrame(te_ary, columns=te.columns_)

freq = apriori(df, min_support=0.001, use_colnames=True)
#计算关联规则
result = association_rules(freq, metric="confidence", min_threshold=0.05)
result.to_excel('./结果.xlsx', index=False)

```

# 通用程序启动流程

```shell
# 创建venv环境
python -m venv venv
# 激活venv环境
Source venv\Script\activate
# 安装依赖
pip install -r requirements.txt
# 初始化数据库与表
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
# 导入数据
python setup.py
# 启动网站
python manage.py runserver
```

# scrapy新闻爬虫

# scrapy插入mysql的pipeline