---
title: 基于sklearn的文本分类通用流程
date: 2021-05-21 10:59:30
tags:
 - 其他
categories:
 - 其他
---

# 以垃圾邮件数据集为例，做文本分类的通用流程

## 1. 数据预处理

- 数据载入
- 停用词载入
- 文本分词
- 形成X Y

## 2. 模型训练与保存

- 载入X Y
- train_test_split
- 利用sklearn的pipeLine完成模型搭建
- 保存模型

## 3. 模型测试
- 加载模型
- 输入句子
- 得到结果

# 代码

```python

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import *
import joblib
from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

class DenseTransformer(TransformerMixin):
	"""
	变换数据
	"""
	def fit(self, X, y=None, **fit_params):
		return self

	def transform(self, X, y=None, **fit_params):
		return X.todense()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print('splited ok!')

clf = Pipeline([('word_count', CountVectorizer()), ('tfidf', TfidfTransformer()),  ('lr', LogisticRegression())])
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred)) # 评测指标

x1 = '陕西略阳钢铁有限责任公司'
tokens = list(jieba.cut(x1))
t1 = [token for token in tokens if token_filter(token) is True]
t1 = ' '.join(t1)
y_pred = clf.predict_proba([t1, ])
y_pred

```