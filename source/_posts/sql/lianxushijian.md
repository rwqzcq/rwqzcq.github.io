---
title: 连续时间问题
date: 2021-07-22 10:42:38
tags:
 - SQL
categories:
 - SQL
---

# 问题1

已知日活表table如下图所示：

![](./0.png)

现在要计算出

## 日活表求每个用户一周内活跃天数

### 思路

1. 使用`timestampdiff`函数过滤出一周内有过登录的记录

2. 根据用户id分组统计计数

> row_number是求连续时间问题的第一步

### SQL

```SQL

with base as ( -- 计算一周内有过登录的记录
    select
        *
    from
        table
    where
        timestampdiff(day, time, now()) <= 7 -- 核心在这里
)

SELECT
	user_id,
	count(1) AS '登录天数'
FROM
	base
GROUP BY
	user_id
ORDER BY
	user_id
```

### timestampdiff函数解释

> timestampdiff(unit, datetime_1, datetime_2)

该函数用来计算两个时间的差，第一个参数是差值的单位，可以是`minute`,`day`,`hour`,`second`，后面两个参数是时间，需要注意的是`datetime_2`减去`datetime_1`，也就是后面的减前面的

## 日活表求每个用户一周内最大连续活跃天数

### 思路

1. 使用`timestampdiff`来过滤出最近一周的记录
2. 使用`row_number`函数来计算每一个用户登录日期的顺序
3. 利用`date_sub`函数来计算每一条记录在`登录顺序`天数之前的日期
4. 根据第4步的日期来分组计数，将最大值作为最大连续登录天数

> 判断是否连续的核心就是站在某一天往前推顺序的N天可以同步到同一日期，那么这个就是连续的

### SQL

```SQL
with base as (
    select
        *,
        row_number() over (partition by user_id order by date) as ranking
    from
        table
    where
        timestampdiff(day, time, now()) <= 7
)
select
    user_id,
    max(count) as '最大连续登录天数'
from (
    select
        user_id,
        date_sub(date, interval ranking day) as gap,
        count(1) as count
    from
        base
    group by
        user_id,
        date_sub(date, interval ranking day)
    order by
        user_id
) as a
group by
    user_id
order by
    user_id
```

# mysql常见的时间日期函数

![mysql时间日期函数](https://pic1.zhimg.com/v2-378511c14708de1ea5ea3fb5bb99ac08_r.jpg)

# 参考链接

- SQL笔试题（1）：求连续时间问题（必考难题）. https://zhuanlan.zhihu.com/p/349358841


```SQL
with base as (
    select
        user_id,
        date_sub(date, interval ranking day) as gap,
        count(*) as num
    from (
        select
            *,
            row_number() over (partition by user_id order by date) as ranking
        from
            user
        where
            date between '2020-01-01' and '2020-01-31'
    ) as a
    group by
        user_id,
        date_sub(date, interval ranking day)
)

select
    user_id,
    max(num) as '最大连续登录天数'
from 
    base
group by
    user_id  
order by
    user_id
```
