---
title: 查询员工累计薪水
date: 2021-08-11 21:26:48
tags:
 - SQL
 - leetcode
categories:
 - leetcode
---


# 题目链接

https://leetcode-cn.com/problems/find-cumulative-salary-of-an-employee/

# 题目描述

Employee 表保存了一年内的薪水信息。

请你编写 SQL 语句，对于每个员工，查询他除最近一个月（即最大月）之外，剩下`每个月的近三个月的累计薪水`（不足三个月也要计算）。

结果请按 Id 升序，然后按 Month 降序显示。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-cumulative-salary-of-an-employee
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

![输入输出](0.png)

# 解题难点

> 剩下的近三个月的累计薪水，比如7月份，那就是`5+6+7`

而不是因为数据表中的记录如下所示：

```TXT

month salary
1       3
3       5
7       5
```
由于`月份没有连续出现`所以选择求和的是按照该月份排序后该月份之前的累计求和。



# SQL

```sql
with base as (
select
    Id,
    Month,
    Salary
from (
    select
        *,
        row_number() over (partition by Id order by Month desc) as ranking 
    from
        Employee  
) as a
where
    a.ranking > 1 -- 去除最大的月份
)

select 
    a.Id,
    a.Month,
    sum(b.Salary) as Salary
from
    base as a
left join 
    base as b
on
    a.Id = b.Id and
    a.Month >= b.Month and -- 这里是关键,不加这里会导致左表为4，右表为7
    a.Month <= b.Month + 2 -- 近3个月的
group by 
    a.Id,
    a.Month
order by    
    Id,
    Month desc
```