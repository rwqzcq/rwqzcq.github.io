---
title: 上海心愿盒笔试
date: 2021-05-17 09:36:13
tags:
 - 笔试
categories:
 - 笔试
---

# 题目内容

1. 定义一个python方程将邮件里面的raw.xlsx清理并转化成sample.xlsx的格式，表头与sample一致，
清理规则如下：
- 删除types为空并移除
- 剔除明显outlier

2. 利用commodity = 52的数据进行以下分析：
    - 定义一个方程计算receive_time和comment_time的时间差(以天计算)，并在原表生成新的列，列名为`time_difference`
    - 将数据可视化，生成两个图表
        - 定义一个方程用柱状图展示每一个time_difference的count
        - 定义一个方程用comment_time生成曲线图，x轴为日期，颗粒度为天，y轴为每一个日期的count

3. 提出有意思的想法

通过多个角度分析用户的评论内容，分析其再次购买的意愿。

1. 首先进行总体统计：
```TXT
               time_difference
comment_value
不感兴趣                       242
已经下单                       245
还想再试                       646
```
57%的用户还想再次尝试，可以发现，总体上，该店铺内的产品用户比较满意。

2. 总体上看用户从下单到评论的时间间隔。
```TXT
mean       12.253310
std         7.442732
min         0.000000
25%         6.000000
50%        12.000000
75%        16.000000
max        56.000000
```
用户平均的时间间隔为12天，标准差为7天，大部分集中在16天之内。

3. 重点分析还想再试的用户，该类型用户有较大的价值。
与总体差别不大，所以较难根据用户评论反馈时间来分析用户的下单意愿。
```TXT
mean      12.159443
std        7.226199
min        0.000000
25%        6.000000
50%       12.000000
75%       16.000000
max       47.000000
```

4. 寻求更多的特征分析用户的下单意愿。

从用户的评论来看，主要的评论的角度包括了`包装`,`大小`,`气味`, `口味`, `外观`，因此这些角度可以当作特征，而最后的下单意愿可以作为`目标值`，再加上评论间隔时间这一特征，
可以利用`决策树`构建分类模型，以此来判断，哪一些特征对于`用户的下单意愿`影响较大，以此作为产品改进的方向。



# 评价

1. 较为简单，不涉及到很复杂的知识点

# 相关知识点

1. pandas用`apply`扩展多列

```python
raw_df[['comment_type', 'comment_value']] = raw_df.apply(lambda x: x['types'].split(':'), axis=1, result_type="expand")
```
定义`axis=1`,以及`result_type=expand`

2. 找到离群点

```python
print(raw_df['receive_time'].describe())
```
`describe`方法来看总体的数据分布

3. pandas一行拆分成多行

```python
# https://zhuanlan.zhihu.com/p/124242604
#一、先将‘爱好’字段拆分
df['爱好']=df['爱好'].map(lambda x:x.split(','))
#二、然后直接调用explode()方法
df_new=df.explode('爱好')
```

[py文件下载](main.py)