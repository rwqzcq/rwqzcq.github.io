---
title: 牛客SQL-第86题-简历分析(三)
date: 2021-04-25 17:48:46
tags:
  - SQL
categories:
  - SQL 
---

## 题目描述

[原始链接](https://www.nowcoder.com/practice/83f84aa5c32b4cf5a75558d02dd7743c?tpId=82&rp=1&ru=%2Fta%2Fsql&qru=%2Fta%2Fsql%2Fquestion-ranking&tab=answerKey)

在牛客实习广场有很多公司开放职位给同学们投递，同学投递完就会把简历信息存到数据库里。
现在有简历信息表(resume_info)，部分信息简况如下:

![avatar](https://uploadfiles.nowcoder.com/images/20210305/301499_1614930662852/E587507D0FC15C77027A0B0E39B12F10)

第1行表示，在2025年1月2号，C++岗位收到了53封简历
。。。
最后1行表示，在2027年2月6号，C++岗位收到了231封简历

请你写出SQL语句查询在2025年投递简历的每个岗位，每一个月内收到简历的数目，和对应的2026年的同一个月同岗位，收到简历的数目，最后的结果先按first_year_mon月份降序，再按job降序排序显示，以上例子查询结果如下:

![avatar](https://uploadfiles.nowcoder.com/images/20210305/301499_1614931927046/10AF6822A92E37CE34B3EFFF8522E033)

解析:

第1行表示Python岗位在2025年2月收到了93份简历，在对应的2026年2月收到了846份简历
。。。
最后1行表示C++岗位在2025年1月收到了107份简历，在对应的2026年1月收到了470份简历

## 输入的SQL

```sql
drop table if exists resume_info;
CREATE TABLE resume_info (
id int(4) NOT NULL,
job varchar(64) NOT NULL,
date date NOT NULL,
num int(11) NOT NULL,
PRIMARY KEY (id));

INSERT INTO resume_info VALUES
(1,'C++','2025-01-02',53),
(2,'Python','2025-01-02',23),
(3,'Java','2025-01-02',12),
(4,'C++','2025-01-03',54),
(5,'Python','2025-01-03',43),
(6,'Java','2025-01-03',41),
(7,'Java','2025-02-03',24),
(8,'C++','2025-02-03',23),
(9,'Python','2025-02-03',34),
(10,'Java','2025-02-04',42),
(11,'C++','2025-02-04',45),
(12,'Python','2025-02-04',59),
(13,'C++','2026-01-04',230),
(14,'Java','2026-01-04',764),
(15,'Python','2026-01-04',644),
(16,'C++','2026-01-06',240),
(17,'Java','2026-01-06',714),
(18,'Python','2026-01-06',624),
(19,'C++','2026-02-14',260),
(20,'Java','2026-02-14',721),
(21,'Python','2026-02-14',321),
(22,'C++','2026-02-24',134),
(23,'Java','2026-02-24',928),
(24,'Python','2026-02-24',525),
(25,'C++','2027-02-06',231);
```

## 预期输出的SQL

```sql
Python|2025-02|93|2026-02|846
Java|2025-02|66|2026-02|1649
C++|2025-02|68|2026-02|394
Python|2025-01|66|2026-01|1268
Java|2025-01|53|2026-01|1478
C++|2025-01|107|2026-01|470
```

## 解题

### 1. 将日期格式的date转化成年-月的格式

mysql内置函数`date_format`与`date_add`的使用。

> `date_format`函数接受的参数是一个`datetime`类型的数据，不是`date`类型的数据, 所以date(month('2019-11-13'), '%Y-%m')会返回`none`

```sql

select
    *,
    date_format(date, '%Y-%m') as first_year_month,
    date_format(date_add(date, interval 1 year), '%Y-%m') as second_year_date
from resume_info
where year(date) in (2025, 2026)

```

### 2. 根据年-月分组求和2025年

```sql

select
    job,
    first_year_month,
    date_add(first_year_month, interval 1 year) as second_year_month
    sum(id) as first_year_cnt
from (
    select
        *,
        date_format(date, '%Y-%m') as first_year_month,
        date_format(date_add(date, interval 1 year), '%Y-%m') as second_year_month
    from resume_info
    where year(date) = 2025
) as a
group by job, first_year_month

```

### 3. 根据年-月分组求和2026年

```sql

select
    job,
    second_year_month,
    sum(id) as second_year_cnt
from (
    select
        *,
        date_format(date, '%Y-%m') as sencond_year_month
    from resume_info
    where year(date) = 2026
) as a
group by job, second_year_month
```

### 4. 两者内连接

```sql

select
    a.job,
    a.first_year_month,
    a.first_year_cnt,
    b.second_year_month,
    b.second_year_cnt
from (
    -- 2015年
    select
        job,
        first_year_month,
        second_year_month,
        sum(num) as first_year_cnt
    from (
        select
            *,
            date_format(date, '%Y-%m') as first_year_month,
            date_format(date_add(date, interval 1 year), '%Y-%m') as second_year_month
        from resume_info
        where year(date) = 2025
    ) as a
    group by job, first_year_month  
) as a
inner join (
    -- 2016年
    select
        job,
        second_year_month,
        sum(num) as second_year_cnt
    from (
        select
            *,
            date_format(date, '%Y-%m') as second_year_month
        from resume_info
        where year(date) = 2026
    ) as a
    group by job, second_year_month
) as b
on a.job = b.job and a.second_year_month = b.second_year_month
order by a.first_year_month desc, a.job desc


```

## 优化写法

上一次写法用了5个select，比较耗时。参考牛客大神`牛客421553514号`的写法。
核心思想就是`group by`字句中使用的是`month(date)`，这样可以直接根据日期分组，不需要先将时间转化成日期。

### 1. 2025年分组求和

```sql
select
    job,
    date,
    sum(num) as first_year_cnt
from resume_info
where year(date) = 2025
group by job, month(date)

```

此时的输出如下:

```text
C++|2025-01-02|107
Python|2025-01-02|66
Java|2025-01-02|53
Java|2025-02-03|66
C++|2025-02-03|68
Python|2025-02-03|93
```

### 2. 2026年求和

```sql
select
    job,
    date,
    sum(sum) as sencond_year_cnt
from resume_info
where year(date) = 2026
group by job, month(date)
```

### 3. 两表连接

```sql
select
    a.job,
    date_format(a.date, '%Y-%m') as first_year_month,
    a.first_year_cnt,
    date_format(b.date, '%Y-%m') as second_year_month,
    b.second_year_cnt
from (
    select
        job,
        date,
        sum(num) as first_year_cnt
    from resume_info
    where year(date) = 2025
    group by job, month(date)  
) as a
inner join (
    select
        job,
        date,
        sum(num) as second_year_cnt
    from resume_info
    where year(date) = 2026
    group by job, month(date)
) as b
on a.job = b.job and month(a.date) = month(b.date)
order by first_year_month desc, job desc
```

## 两种方法比较

|     | 运行时间  | 占用内存 | select个数 | 
|  ----  | ----  | ---- | ---- | 
| 方法1  | 51ms | 6900kb | 5 | 
| 方法2  | 51ms | 6824kb | 3 | 


## 2021-08-03写法

```sql

select
    a.job,
    first_year_mon,
    first_year_cnt,
    second_year_mon,
    second_year_cnt
from (
    select
        DATE_FORMAT(date, '%Y-%m') as first_year_mon,
        job,
        sum(num) as first_year_cnt
    from
        resume_info
    where
        date between '2025-01-01' and '2025-12-31'
    group by
        job,
        DATE_FORMAT(date, '%Y-%m')
) as a
left join (
    select
        DATE_FORMAT(date, '%Y-%m') as second_year_mon,
        job,
        sum(num) as second_year_cnt
    from
        resume_info
    where
        date between '2026-01-01' and '2026-12-31'
    group by
        job,
        DATE_FORMAT(date, '%Y-%m')
) as b
on
    a.job = b.job
    and right(a.first_year_mon, 2) = right(b.second_year_mon, 2) -- 这里用上字符串或者
    -- date_format(a.first_year_mon, '%m') = date_format(b.second_year_mon, '%m') 保证月份相同
order BY
    first_year_mon desc,
    job desc

```