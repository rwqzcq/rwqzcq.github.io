---
title: 牛客SQL-找到积分最高的人
date: 2021-04-25 17:28:16
tags:
  - SQL
categories:
  - SQL
---

## 题目描述

[原始链接](https://www.nowcoder.com/practice/d2b7e2a305a7499fb310dc82a43820e8?tpId=82&tqId=38361&rp=1&ru=%2Fta%2Fsql&qru=%2Fta%2Fsql%2Fquestion-ranking&tab=answerKey)

牛客每天有很多用户刷题，发帖，点赞，点踩等等，这些都会记录相应的积分。
积分表如下:

![avatar](https://uploadfiles.nowcoder.com/images/20210328/301499_1616896023720/B9EE61A3CF7F34EF411FE1A9C6B86FBC)

还有一个积分表(grade_info)，简况如下:

![avatar](https://uploadfiles.nowcoder.com/images/20210328/301499_1616905385537/13C8EB67E494299F9396F462A8D0728D)

第1行表示，user_id为1的用户积分增加了3分。
第2行表示，user_id为2的用户积分增加了3分。
第3行表示，user_id为1的用户积分减少了1分。
.......
最后1行表示，user_id为3的用户积分减少了1分。

请你写一个SQL查找积分增加最高的用户的id，名字，以及他的总积分是多少(可能有多个)，查询结果按照id升序排序，以上例子查询结果如下:

![avatar](https://uploadfiles.nowcoder.com/images/20210328/301499_1616905506009/26B900CFF8FB6BE2B2077D494CA1F237)

## 输入的SQL

```SQL
drop table if exists user;
drop table if exists grade_info;

CREATE TABLE user (
id  int(4) NOT NULL,
name varchar(32) NOT NULL
);

CREATE TABLE grade_info (
user_id  int(4) NOT NULL,
grade_num int(4) NOT NULL,
type varchar(32) NOT NULL
);

INSERT INTO user VALUES
(1,'tm'),
(2,'wwy'),
(3,'zk'),
(4,'qq'),
(5,'lm');

INSERT INTO grade_info VALUES
(1,3,'add'),
(2,3,'add'),
(1,1,'reduce'),
(3,3,'add'),
(4,3,'add'),
(5,3,'add'),
(3,1,'reduce');

```

## 预期输出的SQL

```sql
2|wwy|3
4|qq|3
5|lm|3
```

## 解题

### 1. 根据type找到每一个用户最终的积分

> sum函数的参数不仅可以接受字段，里面还可以针对该字段施加各种函数

```SQL
select
    user_id,
    sum(if(type = 'reduce', -1 * grade, grade)) as total_grade
from grade_info
group by user_id
order by total_grade desc
```

### 2. 利用窗口函数dense_rank根据total_grade为1中的表添加排序编号

> dense_rank窗口函数可以使数值相同的行拥有同一个编号

<b>他的总积分是多少(可能有多个)</b>，遇到这个的时候可以使用`dense_rank`或者`rank`

```sql
select
    user_id,
    total_grade,
    dense_rank(order by total_grade desc) as 'ranking'
from (
    select
        user_id,
        sum(if(type = 'reduce', -1 * grade, grade)) as total_grade
    from grade_info
        group by user_id
        order by total_grade desc
) as a
```

### 3. 找到总积分最高的用户Id,名字与积分

接着2，利用`where`找到`ranking = 1`就可以

```sql
select
    a.user_id,
    a.name as user_name,
    a.total_grade
from (
    select
        user_id,
        total_grade,
        dense_rank(order by total_grade desc) as 'ranking'
    from (
        select
            user_id,
            sum(if(type = 'reduce', -1 * grade, grade)) as total_grade
        from grade_info
            group by user_id
            order by total_grade desc
    ) as a
) as a
left join user as u
on a.user_id = u.id
where a.ranking = 1
order by a.user_id
```
