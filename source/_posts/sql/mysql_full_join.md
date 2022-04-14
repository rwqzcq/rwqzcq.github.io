---
title: mysql full join实现
date: 2021-08-10 09:23:42
tags:
 - SQL
categories:
 - SQL
---

# 例题

2020年小红书秋招真题
现有订单表orders
![](https://uploadfiles.nowcoder.com/images/20200511/310337_1589206392072_D14D623C67A16FBAD14E33D7B879D9D8)

收藏表favorites
![](https://uploadfiles.nowcoder.com/images/20200511/310337_1589206410906_AC83D60FDAB846B94A070DF06682323C)

请用一句SQL取出所有用户对商品的行为特征，特征分为已购买、购买未收藏、收藏未购买、收藏且购买（输出结果如下表）

![](https://uploadfiles.nowcoder.com/images/20200511/310337_1589206444944_94E7A8251F79FE6C6E288DCCE1DF1F0C)

# 解题

> oracle支持full join, 而mysql则不支持，mysql中full join的实现方式为`left join + rightjoin + union`

也就是左连接+右链接+去重

```SQL
SELECT
	a.user_id,
	a.item_id,
CASE
		
		WHEN a.pay_time IS NOT NULL THEN
		1 ELSE 0 
	END AS `已购买`,
CASE
		
		WHEN a.pay_time IS NOT NULL 
		AND b.fav_time IS NULL THEN
			1 ELSE 0 
			END AS `购买未收藏`,
	CASE
			
			WHEN b.fav_time IS NOT NULL 
			AND a.pay_time IS NULL THEN
				1 ELSE 0 
				END AS `收藏未购买`,
		CASE
				
				WHEN b.fav_time IS NOT NULL 
				AND a.pay_time IS NOT NULL THEN
					1 ELSE 0 
					END AS `收藏且购买` 
			FROM
				`小红书2020_orders` AS a
				LEFT JOIN `小红书2020_favorites` AS b ON a.user_id = b.user_id 
				AND a.item_id = b.item_id UNION
			SELECT
				b.user_id,
				b.item_id,
			CASE
					
					WHEN a.pay_time IS NOT NULL THEN
					1 ELSE 0 
				END AS `已购买`,
			CASE
					
					WHEN a.pay_time IS NOT NULL 
					AND b.fav_time IS NULL THEN
						1 ELSE 0 
						END AS `购买未收藏`,
				CASE
						
						WHEN b.fav_time IS NOT NULL 
						AND a.pay_time IS NULL THEN
							1 ELSE 0 
							END AS `收藏未购买`,
					CASE
							
							WHEN b.fav_time IS NOT NULL 
							AND a.pay_time IS NOT NULL THEN
								1 ELSE 0 
								END AS `收藏且购买` 
						FROM
							`小红书2020_orders` AS a
						RIGHT JOIN `小红书2020_favorites` AS b ON a.user_id = b.user_id 
	AND a.item_id = b.item_id
```

![left join](0.png)

![right join](1.png)

![full join](2.png)