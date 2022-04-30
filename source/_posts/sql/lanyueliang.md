---
title: 蓝月亮SQL笔试题
date: 2021-07-18 10:09:38
tags:
 - SQL
categories:
 - SQL
---

# 蓝月亮数据分析师SQL笔试题

## 文件下载

1. [题目描述](sql.pdf)
2. [SQL文件](lanyueliang.sql)

## 具体题目

### 1. 查出2020年高于订单平均支付金额的订单数量、订单金额

解题思路：
- 计算订单的平均支付金额：

> 平均支付金额 = 订单总额 / 订单数

```sql
select avg(order_payment) from mall_unit_order
```

- 找到订单金额高于平均支付金额的所有订单数量、订单金额

```sql
select
    count(order_id) as '订单数量',
    sum(order_payment) as '订单总金额'
from
    mall_unit_order
where
    order_payment > (
        select avg(order_payment) from mall_unit_order
    )
```

### 2. 定义：购买两单及以上的用户为复购用户，同一用户相邻两单的支付间隔天数为复购间隔天数，计算每一个用户在2020年的平均复购天数

解题思路：

- 计算2018年的所有订单

```sql
select
    *
from
    unit_mall_order
where
    pay_time >= '2020-01-01' and pay_time < '2021-01-01'
```

- 用窗口函数分组计算每一个用户的首次下单时间

```sql
select
    *,
    min(pay_time) over (partition by buyer_nick) as 'first_order_pay_time'
from
    unit_mall_order
where
    pay_time >= '2020-01-01' and pay_time < '2021-01-01'
```

- 计算本次下单时间与首次下单时间的天数差

```sql
    select
        date_diff(date(pay_time), date(first_order_pay_time)) as diff_days
    .....
```

- 根据用户分组计算平均天数

```sql
select
    buyer_nick,
    ceil(avg(diff_days)) as '平均天数'
from
    X
group by
    buyer_nick
order by 
    buyer_nick
```

> 当初被“同一用户相邻两单的支付间隔天数为复购间隔天数”给迷惑了，计算复购天数的逻辑就是计算`首次下单时间`与`最后一次下单时间`的差值然后除以订单的数量

完整的SQL

```sql
with base as (
	-- 2020年的所有订单信息
	select
		*
	from
		mall_unit_order
	where
		pay_time >= '2020-01-01' and pay_time < '2021-01-01'
	ORDER BY pay_time
),
user_filtered_base as (
	-- 购买两单以上的用户的信息
	select
		*,
		DATEDIFF(date(pay_time), first_pay_time) as diff -- 日期差
	from (
		select
			*,
			count(*) over (partition by buyer_nick) as order_num,
			min(date(pay_time)) over (partition by buyer_nick) as first_pay_time -- 第一次购买时间
		from 
			base
	) as a
	where 
		a.order_num >= 2	
)
select
	buyer_nick,
	ceil(max(diff) / (order_num - 1)) as '平均复购间隔天数' -- 向上取整
from 
	user_filtered_base
group by
	buyer_nick
```


### 3. 按月查出2020年3月份各个省份支付金额排在前3的城市在哪里

解题思路:
- 查出2020年3月的订单

```sql
select
    *
from
    mall_unit_order
where
    pay_time >= '2020-03-01' and pay_time < '2020-04-01'
```

- 查出各个省份各个城市的支付金额

```sql
select
    province,
    city,
    sum(order_payment) as payment
from
    X
group by
    province,
    city
```

- 找出各个省份排名前三的城市

```sql
select
    *,
    row_number() over (partition by province, city order by payment desc) as ranking

```

- 最终SQL

```sql
with base as (
    select
        province,
        city,
        sum(order_payment) as payment
    from
        mall_unit_order
    where
        pay_time >= '2020-03-01' and pay_time < '2020-04-01'
    group by
        province,
        city
)

select
    province,
    city
from (
    select
        *,
        row_number() over (partition by province, city order by payment desc) as ranking
    from
        base
) as a
where 
    ranking <= 3
order by
    province,
    ranking
```


### 4. 假设下单渠道有京东、天猫、淘宝，查出2020年3月份各个渠道订单支付总金额

```sql
select
    order_source,
	sum(order_payment) as '支付总金额'
from
    unit_mall_order
where
    pay_time >= '2020-03-01' and pay_time < '2020-04-01'
group by
    order_source
```

### 5. 查出最近三个月内有购买行为的用户信息，包括字段：唯一用户ID，用户号码，支付订单数，支付总金额，支付总件数，最近一次购买时间，常用收货省份，常用收货城市，手机号中间5位数用*代替

解题思路：
- 找到最近三个月的所有订单
```sql
select
    *
from
    unit_mall_order
where
    month(pay_time) >= (month(now()) - 3)
```

- 找到所有的用户基本信息

```sql
select
    buyer_nick,
    concat(left(buyer_mobile, 3), '*****', right(buyer_mobile, 3)) as '手机号',
    count(order_id) as '支付订单数',
    sum(order_payment) as '支付总金额',
    sum(buy_num) as '支付总件数',
    min(pay_time) as '最近一次购买时间'
from
    mall_unit_order
group by 
    buyer_nick,
    buyer_mobile
```

- 找到用户常用收货省份

```sql
select
    buyer_nick,
    province
from (
    select
        *
        row_number() over (partition by buyer_nick order by num desc) as ranking
    from (
        select
            buyer_nick,
            province,
            count(order_id) as num
        from
            mall_unit_order
        group by
            buyer_nick,
            province
    ) as a 
) as a
where
    ranking = 1
```

- 找到用户常用收货城市

```sql
select
    buyer_nick,
    city
from (
    select
        *
        row_number() over (partition by buyer_nick order by num desc) as ranking
    from (
        select
            buyer_nick,
            city,
            count(order_id) as num
        from
            mall_unit_order
        group by
            buyer_nick,
            city
    ) as a 
) as a
where
    ranking = 1

```

- join汇总

```sql
with
    base as (
        select
            *
        from
            mall_unit_order
        where
            month(pay_time) >= (month(now()) - 3)
    ),
    basic_info as (
        select
            buyer_nick,
            concat(left(buyer_mobile, 3), '*****', right(buyer_mobile, 3)) as '手机号',
            count(order_id) as '支付订单数',
            sum(order_payment) as '支付总金额',
            sum(buy_num) as '支付总件数',
            min(pay_time) as '最近一次购买时间'
        from
            base
        group by 
            buyer_nick,
            buyer_mobile
    ),
    user_province as (
        select
            buyer_nick,
            province
        from (
            select
                *,
                row_number() over (partition by buyer_nick order by num desc) as ranking
            from (
                select
                    buyer_nick,
                    province,
                    count(order_id) as num
                from
                    base
                group by
                    buyer_nick,
                    province
            ) as a 
        ) as a
        where
            ranking = 1
    ),
    user_city as (
        select
            buyer_nick,
            city
        from (
            select
                *,
                row_number() over (partition by buyer_nick order by num desc) as ranking
            from (
                select
                    buyer_nick,
                    city,
                    count(order_id) as num
                from
                    mall_unit_order
                group by
                    buyer_nick,
                    city
            ) as a 
        ) as a
        where
            ranking = 1
    )

select
    a.*,
	b.province as '省份',
	c.city as '城市'
from
    basic_info as a
left join
    user_province as b
on 
    a.buyer_nick = b.buyer_nick
left join
    user_city as c
on 
    a.buyer_nick = c.buyer_nick
```
