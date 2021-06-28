---
title: 牛客网70题-求每一天新用户的留存率
date: 2021-05-10 15:55:06
tags:
 - SQL
categories:
 - SQL
---

# 题目描述

[https://www.nowcoder.com/practice/ea0c56cd700344b590182aad03cc61b8?tpId=82&tqId=35088&rp=1&ru=%2Factivity%2Foj&qru=%2Fta%2Fsql%2Fquestion-ranking&tab=answerKey](原始链接)
牛客每天有很多人登录，请你统计一下牛客每个日期新用户的次日留存率。
有一个登录(login)记录表，简况如下:
![](https://uploadfiles.nowcoder.com/images/20200820/557336_1597903752757_A02F3DF1419BC2D3D4EE9B2B4557053B)
第1行表示user_id为2的用户在2020-10-12使用了客户端id为1的设备登录了牛客网，因为是第1次登录，所以是新用户
。。。
第4行表示user_id为2的用户在2020-10-13使用了客户端id为2的设备登录了牛客网，因为是第2次登录，所以是老用户
。。
最后1行表示user_id为4的用户在2020-10-15使用了客户端id为1的设备登录了牛客网，因为是第2次登录，所以是老用户



请你写出一个sql语句查询每个日期新用户的次日留存率，结果保留小数点后面3位数(3位之后的四舍五入)，并且查询结果按照日期升序排序，上面的例子查询结果如下:
![](https://uploadfiles.nowcoder.com/images/20200820/557336_1597903761838_F734DB69B9941F0DF86776922B0CF347)
查询结果表明:
2020-10-12登录了3个(user_id为2，3，1)新用户，2020-10-13，只有2个(id为2,1)登录，故2020-10-12新用户次日留存率为2/3=0.667;
2020-10-13没有新用户登录，输出0.000;
2020-10-14登录了1个(user_id为4)新用户，2020-10-15，user_id为4的用户登录，故2020-10-14新用户次日留存率为1/1=1.000;
2020-10-15没有新用户登录，输出0.000;
(注意:sqlite里查找某一天的后一天的用法是:date(yyyy-mm-dd, '+1 day')，sqlite里1/2得到的不是0.5，得到的是0，只有1*1.0/2才会得到0.5)

# 输入

```sql
drop table if exists login;
CREATE TABLE `login` (
`id` int(4) NOT NULL,
`user_id` int(4) NOT NULL,
`client_id` int(4) NOT NULL,
`date` date NOT NULL,
PRIMARY KEY (`id`));


INSERT INTO login VALUES
(1,2,1,'2020-10-12'),
(2,3,2,'2020-10-12'),
(3,1,2,'2020-10-12'),
(4,2,2,'2020-10-13'),
(5,1,2,'2020-10-13'),
(6,3,1,'2020-10-14'),
(7,4,1,'2020-10-14'),
(8,4,1,'2020-10-15');
```
# 输出

```sql
2020-10-12|0.667
2020-10-13|0.000
2020-10-14|1.000
2020-10-15|0.000
```

# 解题

> 注意是查找每一个日期`新用户`的留存

## 错误写法

```sql

select
    a.date
    round(
        count(distinct b.user_id) / count(distinct a.user_id),
        3
    ) as p
from
    user_login as a
left join 
    user_login as b
on 
    a.user_id = b.user_id and
    datediff(b.date, a.date) = 1 -- 相隔1天
group by a.date
order by date

```

> 这里写的错误的原因在于没有在日期中区分出来新的用户

## 正确写法1

### 查询出每一个用户的最早登录日期

```sql

with user_first_login as (
    select
        user_id,
        min(date) as date
    from 
        user_login
    group by user_id
)

```

### 查询出所有日期

```sql
with all_date as (
    select
        distinct date
    from
        user_login
    order by 
        date 
)
```

### 在每一个日期中过滤掉老用户

```sql
with date_retention as (
    select
        a.date
        round(
            count(distinct b.user_id) / count(distinct a.user_id),
            3
        ) as p
    from
        user_login as a
    left join 
        user_login as b
    on 
        a.user_id = b.user_id and
        datediff(b.date, a.date) = 1 -- 相隔1天
    where 
        exists (
            select
                *
            from 
                user_first_login as c
            where 
                c.user_id = a.user_id and
                c.date = a.date
        )
    group by 
        a.date
    order by date
)


```

### 合并所有日期

```sql
select
    a.date,
    case when b.p is null then 0.000 else b end as p
from 
    all_date as a
left join 
    date_retention  as b
on 
    a.date = b.date
```

## 正确解法2

### 找到所有新用户与首次登录日期

```sql
with user_first_login as (
    select
        user_id,
        min(date) as date
    from 
        login
    group by user_id
)
```

### 原表与新用户表链接(这是最巧妙的地方)

```sql
with date_retention as (
    select
        a.date,
        round(
            count(b.user_id) / count(a.user_id),
            3
        )
    from 
        user_first_login as a
    left join 
        login as b
    on 
        a.user_id = b.user_id and
        datediff(b.date, a.date) = 1
    group by 
        a.date
)

```

### 利用union 补全日期

```sql

select
    *
from date_retention
union all
(
    select
        distinct date,
        0.000 as p
    from 
        user_login
    where
        date not in (select date from user_first_login)
)
order by
    date
```


