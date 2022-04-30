---
title: 体育馆人流量-连续区间问题
date: 2021-08-12 14:45:08
tags:
 - leetcode
 - SQL
categories:
 - leetcode
---

# 题目描述

编写一个 SQL 查询以找出每行的人数大于或等于 100 且 `id 连续的三行或更多行记录`。
返回按 visit_date 升序排列的结果表。

https://leetcode-cn.com/problems/human-traffic-of-stadium/

![](0.png)

> 遇到这种问题按照哪一个字段来连续就row_number() over (partition by )谁

# SQL

```sql
select
    id,
    visit_date,
    people
from (
    select
    -- 分组统计
        *,
        count(1) over (partition by next_id_gap) as counting -- 按照差值统计
    from
    (
        select
            *,
            id - (row_number() over (order by id))  as next_id_gap -- 排序求差值
        from
            stadium
        where
            people >= 100
    ) as a
) as a
where 
    counting >= 3 -- 过滤统计后的差值

```