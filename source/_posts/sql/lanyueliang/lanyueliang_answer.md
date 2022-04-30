-- 查出2020年高于订单平均金额的订单数量、订单总金额
select
	count(1) as '订单数量',
	sum(order_payment) as '订单总金额'
from 
	mall_unit_order
where
	order_payment > (select avg(order_payment) from mall_unit_order)


/*
	定义：
		购买两单以及以上的用户为复购用户，同一用户相邻两单的支付间隔天数为复购间隔天数。
	计算每一个复购用户在2020年的平均复购间隔天数
	解题：
		当初被“同一用户相邻两单的支付间隔天数为复购间隔天数”给迷惑了，计算复购天数的逻辑就是计算首次下单时间与最后一次下单时间的差值然后除以订单的数量
	
*/

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




/*

 按月查出2020年3月份各个省份支付金额排在前3的城市在哪里

*/
with base as (
	select
		province,
		city,
		sum(order_payment) as pay_num
	from
		mall_unit_order
	where month(pay_time) = 7
	group by
		province, city
)
select
	province,
	city
from (

select
	*,
	row_number() over (partition by province order by pay_num desc) as ranking
from base
) as a
where ranking <= 3
order by province, ranking


/*
	假设下单渠道有京东、天猫、淘宝，查出2020年3月份各个渠道订单支付总金额
*/

select
	order_source,
	sum(order_payment) as '支付总金额'
from
	mall_unit_order
where
	pay_time between '2020-07-01' and '2020-07-31'
group by
	order_source


/*
	查出最近三个月内有购买行为的用户信息，包括字段：
		唯一用户ID，
		用户号码，
		支付订单数，
		支付总金额，
		支付总件数，
		最近一次购买时间
		常用收货省份，
		常用收货城市，
	用户ID中间5位数用*代替
*/
with base as (
	select
		*
	from 
		mall_unit_order	
), 
user_province as (
	select
		buyer_nick,
		province
	from (
		select
			buyer_nick,
			province,
			row_number() over (partition by buyer_nick order by num desc) as ranking
		from (
			select
				buyer_nick,
				province,
				count(*) as num
			from
				base
			group by 
				buyer_nick, province
			order by 
				buyer_nick, num desc
		) as a
	) as a
	where ranking = 1	
),
user_city as (
	select
		buyer_nick,
		city
	from (
		select
			buyer_nick,
			city,
			row_number() over (partition by buyer_nick order by num desc) as ranking
		from (
			select
				buyer_nick,
				city,
				count(*) as num
			from
				base
			group by 
				buyer_nick, city
			order by 
				buyer_nick, num desc
		) as a
	) as a
	where ranking = 1	
)

select
	a.*,
	b.province as '省份',
	c.city as '城市'
from (
	select	
		buyer_nick,
		concat(left(buyer_mobile, 3), '*****', right(buyer_mobile, 3)) as '手机号',
		count(*) as '支付订单数',
		sum(order_payment) as '支付总金额',
		sum(buy_num)  as '支付总件数',
		max(pay_time) as '最近一次购买时间'
	from
		base
	group by 
		buyer_nick
) as a
left join user_province as b
on b.buyer_nick = a.buyer_nick 

left join user_city as c 
on c.buyer_nick = a.buyer_nick