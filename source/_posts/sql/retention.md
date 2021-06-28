---
title: 计算各种留存
date: 2021-05-10 10:01:05
tags:
 - SQL
categories:
 - SQL
---

# 概念解析

留存是以某日期为基准，如果该用户在该基准日期的后N天再次登录系统，则记录为一次N日留存。

留存包括：普通用户留存与新用户留存。新用户留存如[牛客网第70题](/2021/05/10/sql/niuke-70/)

# 解题1-以日为单位计算留存

## 题目描述

![](https://pic2.zhimg.com/80/v2-17ef440668a922929e48cf784b5224b9_720w.jpg)
这是一个APP的用户活跃日期表。
有两个字段： user_id 当日活跃用户的ID，dates用户活跃的日期。
最终我们想要得到如下留存表：
![](https://pic3.zhimg.com/80/v2-d93075ba8bcf738ba584781748ad20b6_720w.jpg)
dates1计算留存的基准日日期。
day0基准日当日的活跃用户数。

## 解题思路

1. 左连接自己

```sql
with all as (
    select
        a.user_id,
        a.dates as d1,
        b.dates as d2
    from
        temp_user_act as a,
    left join 
        temp_user_act as b
    on a.user_id = b.user_id
)

```
2. 找出右表日期大于等于左表日期的内容（排除基准日之前的数据）

```sql
with filer_all as (
    select
        *
    from
        all
    where
        d2 >= d1 -- 这里需要注意，要等于
)

```
3. 计算以左表日期为基准日的当日用户数，第二日、第三日、第四日、第八日回访用户数

```sql
with retention_num as (
    select
        d1,
        count(distinct case when d1 = d2 then user_id else null end) as day0, -- 一定要加上distinct，因为用户一天之内可能会登录很多次
        count(distinct case when datediff(d2, d1) = 1 then user_id else null end) as day1 -- 次日
        -- .....N日
    from
        filter_all
    group by 
        d1
)
```

4. 计算留存率
```sql
select
    d1, 
    day0,
    CONCAT( CAST( ( day1 / day0 ) * 100 as DECIMAL(18,2)) , '%' ) '次日留存率',
from
    retention_num
order by d1
```

## 优化写法

```sql

select
    a.login_date,
    count(distinct a.user_id) as dau, -- daliy active user
    count(distinct case when date_diff('day', b.login_date, a.login_date) = 1 then a.user_id else null end) /
        count(distinct a.user_id) as day1_retention_rate
from
    temp_user_act as a
left join 
    temp_user_act as b
on 
    a.user_id = b.user_id and 
    a.login_date <= b.login_date -- 这里可以这样写
group by 
    a.login_date
order by
    login_date
```

# 要点

1. 自连接
    - user_id相同
    - 日期比较

2. distinct
一个用户可能在同一天登录多个系统，需要去去重

# 参考链接

1. 留存的概念. https://zhuanlan.zhihu.com/p/49050001
2. 计算日留存. https://zhuanlan.zhihu.com/p/359336858