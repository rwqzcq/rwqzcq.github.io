---
title: 用户价值分析
date: 2023-05-01 15:20:13
tags:
 - 其他
categories:
 - 其他
---

# 1. 客户终身价值CLV Customer Lifetime Value

```shell

sudo pip install lifetimes
```

```python
"""
代码来自： https://zhuanlan.zhihu.com/p/139510382
"""

# 编造数据
from faker import Faker   # 1
from tqdm import tqdm
import pandas as pd
fake = Faker()  

base_clv_df = data_features[['ZF', 'member_no']]
clv_data = []
for index, row in tqdm(base_clv_df.iterrows()):
    num = row['ZF']
    member_no = row['member_no']
    # 随机生成数据
    for _ in range(num):
        date = fake.date_time_between(start_date="-720d", end_date="now")
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        price = fake.pyfloat(min_value=200, max_value=10000)        # Python浮点数 
        clv_data.append([member_no, date, price])


clv_data_df = pd.DataFrame(data=clv_data, columns=['member_no', 'order_time', 'price'])

from lifetimes.utils import summary_data_from_transaction_data
summary = summary_data_from_transaction_data(clv_data_df, 'member_no', 'order_time','price',observation_period_end='2023-05-01')
summary = summary[summary['frequency']>0]

# 导入BG/NBD模型，通过模型拟合，得到4个参数（r， ，a，b）。
from lifetimes import BetaGeoFitter
bgf = BetaGeoFitter(penalizer_coef=0.0)#L2正则项
bgf.fit(summary['frequency'], summary['recency'], summary['T'])
print(bgf)

# 预测客户预期的lifetime value
from lifetimes import GammaGammaFitter
ggf = GammaGammaFitter(penalizer_coef = 0.5)
ggf.fit(summary['frequency'],
        summary['monetary_value'])
print(ggf)

# refit the BG model to the summary_with_money_value dataset
# bgf.fit(summary['frequency'], summary['recency'], summary['T'])

clv_result_df = ggf.customer_lifetime_value(
    bgf, #the model to use to predict the number of future transactions
    summary['frequency'],
    summary['recency'],
    summary['T'],
    summary['monetary_value'],
    time=4, # months
    discount_rate=0.01
)

clv_result_df = clv_result_df.to_frame().reset_index()

clv_result_df.head()
```

## 参考链接

1. https://blog.csdn.net/tonydz0523/article/details/86256803
2. https://zhuanlan.zhihu.com/p/139510382
3. https://lifetimes.readthedocs.io/en/latest/Quickstart.html

# 2. 航空客户价值因素分析

```python

```