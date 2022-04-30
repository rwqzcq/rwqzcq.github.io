---
title: SQL笔试题集合
date: 2021-07-22 16:21:10
tags:
 - SQL
categories:
 - SQL
---

# 网易春招-题目1

## 题目描述

![](./0.png)

## 来源

https://zhuanlan.zhihu.com/p/368947628


## SQL

```sql
with base as (
    select
        a.goods_id,
        b.name,
        a.count,
        b.weight
    from
        trans as a
    left join
        goods as b
    on a.goods_id = b.goods_id
)

select
    name
from
    base
where
    weight between 30 and 50
group by
    goods_id
having
    sum(count) > 50
```

# 网易春招-题目2

## 题目描述

![](./1.png)

## 来源

https://zhuanlan.zhihu.com/p/368947628

## SQL

```SQL
-- 取出该用户喜欢并关注的人所喜欢的音乐
with follow_like as (
    select
        distinct b.music_id
    from
        follow as a
    left join
        music_likes as b
    on
        a.follower_id = b.user_id
    where
        b.music_id not in (
            select
                music_id
            from
                music_likes
            where
                user_id = 1
        ) 
)
-- 向user_id为1的用户推荐
select
    b.music_name
from
    follow_like as a
left join
    music as b
on a.music_id = b.music_id
```


# 完美世界春招-题目1

## 题目描述

![](./2.png)

## 来源

https://zhuanlan.zhihu.com/p/367773231

## SQL1

```sql
select
    date(log_time) as '日期',
    count(distinct user_id) as '访客次数', -- 注意去重
    count(opr_id) / count(distinct user_id) as '平均操作次数'
from
    tracking_log
group by
    date(log_time)
```

## SQL2

```sql
-- 统计每天符合以下条件的用户数：A操作之后是B操作，AB操作必须相邻
with base as (
    select
        user_id,
        opr_id,
        date(log_time) as log_date, -- 日期转化
        LEAD(opr_id, 1) over (partition by user_id order by log_time) as next_opr_id -- 下一次的操作id 记得加order_by
    from
        tracking_log        
)
select
    log_date,
    count(distinct user_id) as '用户数'
from
    base
where
    opr_id = 'A' and next_opr_id = 'B'
group by
    log_date
order by
    log_date
```


# 网易互娱-题目1

## 题目描述

![](./4.png)

## 题目来源

https://zhuanlan.zhihu.com/p/366090074

## SQL1

### 错误写法

为了省事写了一个错误的写法，因为一个用户在一天内可能登录不止一次，因此不是PV，而是UV
```sql
-- 使用sql语句取出每个产品的登录人数，有效登录人数，官方渠道有效登录人数，再按产品顺序排序（从小到大）

with base as (
    select
        *,
        case when online_second >= 5*60 then 1 else 0 end as '有效登录',
        case when right(user_id, 8) = '@163.com' then 1 else 0 end as '官方渠道',
        case when online_second >= 5*60 and right(user_id, 8) = '@163.com' then 1 else 0 as '官方渠道有效登录渠道'
    from
        user_login_table
)
select
    product,
    count(user_id) as '登陆人数',
    sum(`有效登录`) as '有效登陆人数', -- 这里出错
    sum(`官方有效登录渠道`) as '官方有效登录渠道' -- 这里出错
from
    base
group by
    product
order by
    product
```

### 正确写法

```SQL
with login as (
    select
        product,
        count(distinct user_id) as '登陆人数'
    from
        user_login_table
    group by
        product
),
youxiao_login as (
    select
        product,
        count(distinct user_id) as '有效登陆人数'
    from
        user_login_table
    where
        online_second >= 5*60
    group by
        product
),
guanfangqudao_youxiao_login as (
    select
        product,
        count(distinct user_id) as '官方渠道有效登陆人数'
    from
        user_login_table
    where
        online_second >= 5*60 and
        right(user_id, 8) = '@163.com'
    group by
        product
)

select
    a.product,
    `登陆人数`,
    `有效登陆人数`,
    `官方渠道有效登陆人数`
from
    login as a
left join
    youxiao_login as b
on
    a.product = b.product
left join 
    guanfangqudao_youxiao_login as c
on 
    a.product = c.product
order by 
    product
```

或者简单写法
```sql
    select
        product,
        count(distinct user_id) as '登陆人数'
        count(distinct if(online_second >= 5*60, user_id, null)) as '有效登录', -- 聚合函数忽略NULL
        count(distinct if(online_second >= 5*60 and right(user_id, 8) = '@163.com', user_id, null)) as '官方渠道有效登录'
    from
        user_login_table
    group by
        product
    order by
        product
```


## SQL2

### 不准确写法

```SQL
-- 取出有效登录用户数前2，的产品，其总在线时长前5的用户。按照产品id顺序（从小到大），在线时长倒序（从大到小）排序

with youxiao as (
    -- 有效登录数前2的产品
    select
        product,
        count(distinct user_id) as num
    from
        user_login_table
    where
        online_second >= 5*60
    group by
        product
    order by
        num desc
    limit 2
    
),
user_online as (
    select
        *
    from (
        select
            *,
            dense_rank() over (partition by product order by num) as ranking
        from (
            select
                user_id,
                product,
                sum(online_second) as num
            from
                user_login_table
            where
                online_second >= 50
            group by
                user_id,
                product
        ) as a
    ) as a
    where
        ranking <= 5
)

select
    a.product,
    b.user_id,
    b.num
from
    youxiao as a
left join
    user_online as b
on a.product = b.product
order by
    product,
    num desc
```

这里需要注意的是

> 取出前几名的话需要用到`dense_rank`函数，因为按照数量排序的话可能会出现排名相同的情况,dense_rank函数不会跳跃

### 正确写法

```sql

with youxiao as (
    -- 有效登录数前2的产品
    select
        product,
        num
    from (
        select
            *,
            dense_rank() over (order by num) as ranking
        from (
            select
                product,
                count(distinct user_id) as num
            from
                user_login_table
            where
                online_second >= 5*60
            group by
                product
        ) as a
    )  as a
    where
        ranking = 1  
),
user_online as (
    select
        *
    from (
        select
            *,
            dense_rank() over (partition by product order by num) as ranking
        from (
            select
                user_id,
                product,
                sum(online_second) as num
            from
                user_login_table
            where
                online_second >= 50
            group by
                user_id,
                product
        ) as a
    ) as a
    where
        ranking <= 5
)

select
    a.product,
    b.user_id,
    b.num
from
    youxiao as a
left join
    user_online as b
on a.product = b.product
order by
    product,
    num desc
```

# 网易互娱-题目2

## 题目描述

![](./5.png)

## 题目来源

https://zhuanlan.zhihu.com/p/366090074

## SQL

```SQL  
-- 每个产品最后一次付款记录。然后按照最后一条付款记录时间从大到小排序（若同产品最后相同时间存在多条记录，则返回多条）
with base as (
    select
        product,
        pay_time
    from (
        select
            *,
            dense_rank() over (partition by product order by pay_time desc) as ranking -- 使用这个窗口函数
        from
            user_pay_table
    ) as a
    where 
        ranking = 1
    order by
        pay_time
)
```

# 抖音春招-题目1

## 题目描述

![](./6.png)

## 题目来源

https://zhuanlan.zhihu.com/p/361870962

## SQL1

```sql
-- 计算2020年每个月，每个用户连续签到的最多天数
with base as (
    select
        uid,
        imp_month,
        date_sub(imp_date, interval ranking day) as gap,
        count(1) as num
    from (
        select
            *,
            row_number() over (partition by uid, imp_month order by imp_date) as ranking -- 每一个用户每一个月的登录时间排序
        from (
            select
                *,
                month(imp_date) as imp_month
            from
                t_act_records
            where
                imp_date between '2020-01-01' and '2020-12-31'
        ) as a
    ) as a
    group by
        uid,
        imp_month,
        date_sub(imp_date, interval ranking day) -- 根据这个往前推的日期排序，核心就在这里
)

select
    uid,
    imp_month,
    max(num) as '最大连续登录天数'
from 
    base
group by
    uid,
    imp_month
order by
    uid,
    imp_month
```

## SQL2

```sql
-- 计算2020年每个月，连续2天都有登陆的用户名单

select
    distinct imp_month, uid
from (
    select
        *,
        datediff(next_login_day, imp_date) as diff -- 求日期差
    from (
        select
            *,
            LEAD(imp_date, 1) over (partition by uid, imp_month order by imp_date) as next_login_day -- 下一次登录日期
        from (
            select
                *,
                month(imp_date) as imp_month
            from
                t_act_records
            where
                imp_date between '2020-01-01' and '2020-12-31'
        ) as a
    ) as a
) as a
where
    diff >= 1 -- 日期差大于等于1

```

优化写法，还是按照`连续时间`的问题来看待

```sql
with base as (
    select
        uid,
        imp_month,
        date_sub(imp_date, interval ranking day) as gap
    from (
        select
            *,
            row_number() over (partition by uid, imp_month order by imp_date) as ranking -- 每一个用户每一个月的登录时间排序
        from (
            select
                *,
                month(imp_date) as imp_month
            from
                t_act_records
            where
                imp_date between '2020-01-01' and '2020-12-31'
        ) as a
    ) as a
)

select
    imp_month,
    uid
from
    base
group by
    imp_month, 
    uid
having
    count(gap) >= 2 -- 连续两天登录

```

## SQL3

```SQL
-- 计算2020年每个月，连续5天都有登陆的用户数
with base as (
	select
		*,
		date_sub(imp_date, interval gap day) as next_login_day
	from (
		select
			*,
			month(imp_date) as imp_month,
			row_number() over (partition by month(imp_date), uid order by imp_date) as gap
		from
			`抖音_t_act_records`
		where
			imp_date between '2020-01-01' and '2020-12-31'
	) as a
)

select
    imp_month,
    count(distinct uid) as user_num
from (
	select
		imp_month,
		uid,
		max(num) as max_login_days
	from (
		select
			-- 每一个月每一个用户的连续登录天数(可能有很多)
			imp_month,
			uid,
			next_login_day,
			count(1) as num
		from
			base
		group by
			imp_month,
			uid,
			next_login_day
	) as a
	group by
		imp_month,
		uid
) as a
where
	max_login_days >= 5 -- 最高连续登录天数
group by
	imp_month
order by
	imp_month
```
精简写法

```sql
select
	month(imp_date) as 'month',
	count(distinct uid) as num -- 统计用户id
from (
	select
		uid,
		imp_date,
		date_sub(imp_date, interval gap day) as diff
	from (
		select
			*,
			row_number() over (partition by month(imp_date), uid order by imp_date) as gap
		from
			`抖音_t_act_records`
		where
			imp_date between '2020-01-01' and '2020-12-31'
	) as a
) as a
group by
	month(imp_date) -- 以月份来分组
having
	count(diff) >= 5 -- 登录天数大于等于5，不管什么Uid
```


# 抖音春招-题目2

## 题目描述

![](7.png)

## 题目来源

https://zhuanlan.zhihu.com/p/361870962

## SQL1 

求出每个用户第一个订单的记录，如果同时下单了包含多个课程的订单，则按照：语文、数学、英语顺序排。

以下为错误写法：
```SQL
select
	order_id,
	uid,
	order_time,
	subject
from (
	select
		*,
		row_number() over (partition by uid order by order_time, subject_ranking) as ranking
	from (
		select
			*,
			case subject when '语文' then 1 when '数学' then 2 when '英语' then 3 end as subject_ranking
		from 
			`抖音_t_order_records`
	) as a
) as a
where
	ranking = 1
```

一个订单可能包括多个课程，所以上面的写法是错误的

优化写法，主要用到了`field`函数。

```sql
select
	uid,
	subject,
	min(order_time) as time
from
	`抖音_t_order_records`
group by -- 每一个用户每一科目的最早下单时间
	uid,
	subject
order by
	field(subject, '语文', '数学', '英语')
```

## SQL2

运行不出来


# 抖音春招-题目3

## 题目描述

![](8.png)

## 题目来源

https://zhuanlan.zhihu.com/p/361870962

## SQL1

```SQL
-- 求出每个学生成绩最高的三条记录
select
    student_id,
    course_id,
    score
from (
    select
        *,
        row_number() over (partition by student_id order by score desc) as ranking
    from
        t_student_score
) as a
where
    ranking <= 3
order by
    student_id,
    score
```

## SQL2

```SQL  
-- 求出每个班，每个课程，高于课程平均分的学生
select
    class_id,
    course_id,
    student_id
from(
    select
        *,
        avg(score) over (partition by class_id, course_id) as class_course_avg_score
    from
        t_student_score
) as a
where
    score > class_course_avg_score
group by
    class_id,
    course_id,
    student_id
```


# 快手春招-题目1

## 题目描述

![](9.png)

## 题目来源

https://zhuanlan.zhihu.com/p/364317753

## SQL1

经典的计算留存的问题，之前写过博客介绍过，核心在于自连接。

```sql
with base as (
	select
		a.device_id,
		a.app_id,
		a.login_day as login_day,
		b.login_day as next_login_day,
		datediff(b.login_day, a.login_day) as gap
	from
		`快手_user_log` as a
	left join -- 这里要注意
		`快手_user_log` as b
	on
		a.device_id = b.device_id and
		a.app_id = b.app_id and
		a.login_day <= b.login_day -- 这里要注意
	order by
		device_id,
		app_id,
		gap
)

select
	login_day,
	day1 / num  as 次日留存率
from (
	select
		login_day,
		count(distinct device_id, app_id) as num,
		count(case when gap = 1 then 1 else null end) as day1
	from
		base
	group by
		login_day
) as a
```

## 快手春招-题目2

## 题目描述

![](10.png)

## 题目来源

https://zhuanlan.zhihu.com/p/364317753

## SQL1

mysql没有split函数


# 网易

## 题目描述

现在数据库中有一张用户交易表 netease_order，其中有orderid（订单ID）、userid（用户ID）、amount（消费金额）、paytime（支付时间）。

1. 请写出对应的SQL语句，查出每个用户第一单的消费金额。
2. 请写出对应的SQL语句，查出每个月的新客数（新客指在严选首次支付的用户），当月有复购的新客数，新客当月复购率（当月有复购的新客数/月总新客数）。

## SQL1

```sql
SELECT
    userid,
    amount 
FROM
    ( SELECT *, row_number() over ( PARTITION BY userid ORDER BY paytime ) AS ranking FROM netease_order ) AS a 
WHERE
ranking = 1 
```

## SQL2

```sql
with -- 查出每个月的新客数（新客指在严选首次支付的用户）
new_user as (
	select
		userid,
		date_format(min(paytime), '%Y-%m') as first_order_date
	FROM
		netease_order
	group by
		userid
),
xinke as (
	select
		first_order_date,
		count(userid) as user_num
	from
		new_user
	group by
		first_order_date
),
fugou as (
-- 	select
-- 		DATE_FORMAT(a.paytime, '%Y-%m') as order_date,
-- 		count(distinct a.userid) as user_num
-- 	from
-- 		netease_order as a
-- 	left join 
-- 		netease_order as b
-- 	on 
-- 		a.userid = b.userid and
-- 		DATE_FORMAT(a.paytime, '%Y-%m') = DATE_FORMAT(b.paytime, '%Y-%m')
-- 	where
-- 		(a.userid, DATE_FORMAT(a.paytime, '%Y-%m')) in (select * from new_user)
-- 	group by 
-- 		DATE_FORMAT(a.paytime, '%Y-%m')
	select
		DATE_FORMAT(a.paytime, '%Y-%m') as order_date,
		count(distinct a.userid) as user_num
	from
		netease_order as a
	inner join 
		new_user as b
	on 
		a.userid = b.userid and
		DATE_FORMAT(a.paytime, '%Y-%m') = b.first_order_date
	group by 
		DATE_FORMAT(a.paytime, '%Y-%m')
)

select
	b.order_date,
	a.user_num as '新客数',
	b.user_num as '复购数',
	b.user_num / a.user_num as '复购率'
from
	xinke as a
left join
	fugou as b
on 
	a.first_order_date = b.order_date
```
