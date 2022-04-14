---
title: 1127-用户购买平台
date: 2021-09-02 16:35:48
tags:
 - leetcode
 - sql
categories:
 - leetcode
 - sql
---

# 题目描述

```markdown
支出表: Spending

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| user_id     | int     |
| spend_date  | date    |
| platform    | enum    | 
| amount      | int     |
+-------------+---------+
这张表记录了用户在一个在线购物网站的支出历史，该在线购物平台同时拥有桌面端（'desktop'）和手机端（'mobile'）的应用程序。
这张表的主键是 (user_id, spend_date, platform)。
平台列 platform 是一种 ENUM ，类型为（'desktop', 'mobile'）。
 

写一段 SQL 来查找每天 仅 使用手机端用户、仅 使用桌面端用户和 同时 使用桌面端和手机端的用户人数和总支出金额。

查询结果格式如下例所示：

Spending table:
+---------+------------+----------+--------+
| user_id | spend_date | platform | amount |
+---------+------------+----------+--------+
| 1       | 2019-07-01 | mobile   | 100    |
| 1       | 2019-07-01 | desktop  | 100    |
| 2       | 2019-07-01 | mobile   | 100    |
| 2       | 2019-07-02 | mobile   | 100    |
| 3       | 2019-07-01 | desktop  | 100    |
| 3       | 2019-07-02 | desktop  | 100    |
+---------+------------+----------+--------+

Result table:
+------------+----------+--------------+-------------+
| spend_date | platform | total_amount | total_users |
+------------+----------+--------------+-------------+
| 2019-07-01 | desktop  | 100          | 1           |
| 2019-07-01 | mobile   | 100          | 1           |
| 2019-07-01 | both     | 200          | 1           |
| 2019-07-02 | desktop  | 100          | 1           |
| 2019-07-02 | mobile   | 100          | 1           |
| 2019-07-02 | both     | 0            | 0           |
+------------+----------+--------------+-------------+ 
在 2019-07-01, 用户1 同时 使用桌面端和手机端购买, 用户2 仅 使用了手机端购买，而用户3 仅 使用了桌面端购买。
在 2019-07-02, 用户2 仅 使用了手机端购买, 用户3 仅 使用了桌面端购买，且没有用户 同时 使用桌面端和手机端购买。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/user-purchase-platform
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```

# 解题

```sql

with to_join as (
    -- 建立底表
    select
        distinct spend_date, 'desktop' as platform
    from
        Spending
    union
    select
        distinct spend_date, 'mobile' as platform
    from
        Spending
    union
    select
        distinct spend_date, 'both' as platform
    from
        Spending
),
base as (
    -- 统计每一个日期每一个用户登录的平台类型以及开销
    select
        spend_date,
        user_id,
        sum(amount) as amount,
        if(count(*) = 1, platform, 'both') as platform -- 判断平台类型
    from
        Spending
    group by
        spend_date,
        user_id
)

select
    a.spend_date,
    a.platform,
    ifnull(sum(b.amount), 0) as total_amount,
    ifnull(count(distinct b.user_id), 0) as total_users
from
    to_join as a
left join
    base as b
on
    a.spend_date = b.spend_date and
    a.platform = b.platform
group by
    a.spend_date,
    a.platform
```

> `if(count(*) = 1, platform, 'both')`,这个用来判断平台类型是核心的要求

# 原来写的代码

```sql
with whole_date as (
    -- 所有日期
    select
        distinct spend_date
    from
        Spending
), 
base as (
    -- 手机端
    select
        *,
        count(platform) over (partition by spend_date, user_id) as platform_num -- 这一天根据当前的platform分组后的数量
    from
        Spending
),
mobile as (
    select
        spend_date,
        'mobile' as platform,
        sum(amount) as total_amount,
        count(distinct user_id) as total_users
    from
        base
    where
        platform = 'mobile' and platform_num = 1
    group by
        spend_date
),
desktop as (
    select
        spend_date,
        'desktop' as platform,
        sum(amount) as total_amount,
        count(distinct user_id) as total_users
    from
        base
    where
        platform = 'desktop' and platform_num = 1
    group by
        spend_date   
)

select
    a.spend_date,
    b.platform,
    ifnull(b.total_amount, 0) as total_amount,
    ifnull(b.total_users, 0) as total_users
from    
    whole_date as a
left join
    mobile as b
on
    a.spend_date = b.spend_date
union
select
    a.spend_date,
    b.platform,
    ifnull(b.total_amount, 0) as total_amount,
    ifnull(b.total_users, 0) as total_users
from    
    whole_date as a
left join
    desktop as b
on
    a.spend_date = b.spend_date
union
select
    a.spend_date,
    ifnull(b.platform, 'both'),
    ifnull(b.total_amount, 0) as total_amount,
    ifnull(b.total_users, 0) as total_users
from    
    whole_date as a
left join (
    select
        spend_date,
        'both' as platform,
        sum(amount) as total_amount,
        count(distinct user_id) as total_users
    from
        base
    where   
        platform_num = 2
    group by
        spend_date
) as b
on
    a.spend_date = b.spend_date
order by
    spend_date,
    field(platform, 'desktop', 'mobile', 'both')
```

> 过于臃肿，计算麻烦，很容易出错，出错也不容易去修改



# Write your MySQL query statement below

--报告为垃圾广告的帖子
with base as (
    select
        a.*,
        if(b.remove_date is null, 0, 1) as if_remove
    from
        Actions as a
    left join
        Removals as b
    on
        a.post_id = b.post_id
)



select
    round(avg(p) * 100, 4)
from (
    select
        action_date,
        sum(if_remove) / count(distinct post_id) as p
    from
        base
    where
        action = 'report' and
        extra = 'spam'
    group by
        action_date
) as a