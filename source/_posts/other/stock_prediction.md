---
title: 基于机器学习的股价预测
date: 2022-05-02 15:24:55
tags:
 - 其他
categories:
 - 其他
---

# 使用LinearSVR来预测股价的涨跌幅

> X, y 都要做标准化才能有着好的推荐结果

```python

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR, SVR
from sklearn.metrics import *
from matplotlib import pyplot as plt

# 准备数据
df = pd.DataFrame(data=None, columns=['open', 'high', 'low', 'close', 'date'])
# 收盘价涨跌幅
df['change'] = df['close'].diff().fillna(0)
# 数据集切分
train_num = int(df.shape[0] * 0.8) # 80%作为训练集
test_num = df.shape[0] - train_num # 剩下的20%作为测试集
X = df[['open', 'high', 'low', 'close']].astype('float').values
y = df[['change']].values
# 标准化处理特征值与y
X_scaler = StandardScaler()
X_ = X_scaler.fit_transform(X)

y_scaler = StandardScaler()
y_ = y_scaler.fit_transform(y)

X_train = X_[0:train_num]
y_train = y_[0:train_num]
X_test = X_[train_num: ]
y_test = y_[train_num: ]

# 建立模型
model = LinearSVR()

# 模型训练
model.fit(X_train, y_train)

# 模型预测
y_pred = model.predict(X_test)
# 模型评价指标
mse = mean_squared_error(y_test, y_pred)
print(mse)

# 股价变动可视化
plt.plot(y_test, label='y_test_change')
plt.plot(y_pred, label='y_pred_change')
plt.legend()
plt.title('Price Change Prediction')
plt.show()

# 预测收盘价
y_pred_close = np.round(X[train_num: , 3] + y_scaler.inverse_transform(y_pred.reshape((-1, 1))).squeeze(), 2)
y_test_close = X[train_num: , 3]

# 收盘价可视化
plt.plot(y_test_close, label='y_test_close')
plt.plot(y_pred_close, label='y_pred_close')
plt.legend()
plt.title('Closed Price Prediction')
plt.show()

```

> 该方法比较鸡肋的是需要提供今天的开盘价、收盘价等4个特征来去预测明天的，没法预测未来N天的。

# 使用LSTM预测股价

> 核心是构造滑动窗口

# 股价预测包


