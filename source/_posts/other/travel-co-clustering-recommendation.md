---
title: 协同过滤-景点推荐
date: 2021-05-17 14:32:08
tags:
 - 其他
categories:
 - 其他
---

# 基于用户的协同过滤

```python
import pandas as pd
from surprise import NormalPredictor
from surprise import Reader
from surprise import Dataset, KNNBaseline, SVD, accuracy, Reader
from surprise.model_selection import cross_validate


# Creation of the dataframe. Column names are irrelevant.
ratings_dict = {'itemID': [1, 1, 1, 2, 2],
                'userID': [9, 32, 2, 45, 'user_foo'],
                'rating': [3, 2, 4, 3, 1]}
df = pd.DataFrame(ratings_dict)

# A reader is still needed but only the rating_scale param is requiered.
reader = Reader(rating_scale=(1, 5))

# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

trainset = data.build_full_trainset()

# user-based
user_based_sim_option = {'name': 'pearson_baseline', 'user_based': True}
algo = KNNBaseline(sim_option = user_based_sim_option)
algo.fit(trainset)

# pred
uid = 'user_foo'
inner_id = algo.trainset.to_inner_uid(uid)
neighbors = algo.get_neighbors(inner_id, k=10)
neighbors_uid = (algo.trainset.to_raw_uid(x) for x in neighbors )

```

# 安装surprise

```shell
conda install -c conda-forge scikit-surprise
```

# 参考链接
1. https://www.jianshu.com/p/898cc4443add
2. https://surprise.readthedocs.io/en/stable/getting_started.html#load-dom-dataframe-py

