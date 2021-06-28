---
title: 牛客网SQL第5题-含有关键字exists查找未分配具体部门的员工的所有信息
date: 2021-05-10 14:50:52
tags:
  - SQL
categories:
  - SQL 
---

# 题目描述

[原始链接](https://www.nowcoder.com/practice/c39cbfbd111a4d92b221acec1c7c1484?tpId=82&tqId=29825&rp=1&ru=%2Factivity%2Foj&qru=%2Fta%2Fsql%2Fquestion-ranking&tab=answerKey)
使用含有关键字exists查找未分配具体部门的员工的所有信息。

# 输入

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));
```

# 输出

输出格式

```txt
emp_no	birth_date	first_name	last_name	gender	hire_date
10011	1953-11-07	Mary	Sluis	F	1990-01-22
```

# 解题

```sql
select
      *
from
    employees
where 
    not exists (
        select 
            emp_no
        from 
            dept_emp
        where 
            dept_emp.emp_no = employees.emp_no -- 这里是核心
    )
```

# exists使用

Exists的用法：

1. exists对外表用loop逐条查询，每次查询都会查看exists的条件语句，当
2. exists里的条件语句能够返回记录行时(无论记录行是的多少，只要能返回)，条件就为真，返回当前loop到的这条记录;
3. 反之如果exists里的条 件语句不能返回记录行，则当前loop到的这条记录被丢弃，
4. exists的条件就像一个bool条件，当能返回结果集则为true，不能返回结果集则为 false。