---
title: 累计求和问题与滑动求和问题
date: 2021-07-28 17:44:50
tags:
 - SQL
categories:
 - SQL
---

# 题目1

## 描述
已知数据表`Activity`
![](https://img-blog.csdnimg.cn/20200717211034388.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RocjIyMw==,size_16,color_FFFFFF,t_70)
每一行是一个玩家的记录，他在某一天使用某个设备注销之前登录并玩了很多游戏（可能是 0 ）。
编写一个 SQL 查询，同时报告每组玩家和日期，以及玩家到目前为止玩了多少游戏。也就是`在此日期之前玩家所玩的游戏总数`。
查询结果如下:
![](https://img-blog.csdnimg.cn/20200717211232404.png)

对于 ID 为 1 的玩家，2016-05-02 共玩了 5+6=11 个游戏，2017-06-25 共玩了 5+6+1=12 个游戏。
对于 ID 为 3 的玩家，2018-07-03 共玩了 0+5=5 个游戏。
请注意，对于每个玩家，我们只关心玩家的登录日期。

## 解析

### 使用自链接来解决问题

```sql
select
	a.player_id,
	a.event_date,
	sum(b.games_played)
from
	`累计求和_activity` as a
left join
	`累计求和_activity` as b
on 
	a.player_id = b.player_id
	and a.event_date >= b.event_date
group by
	a.player_id,
	a.event_date
```

类似于求留存率，自己与自己连接之后的结果为:
![](https://img-blog.csdnimg.cn/20200717212814624.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RocjIyMw==,size_16,color_FFFFFF,t_70)

然后求出来截止到某一个日期话就需要再次过滤，也就是
> 左表的日期要大于等于右表
最后进行分组聚合对右表进行sum

### 使用窗口函数

核心的要点在于:

> order by：表面是排序功能，实际是累计功能！！！


所以当一些聚合函数（sum、avg、min、max等）和窗口函数连用的时候，`order by 就是起累计作用的`。

```sql
select
	player_id,
	event_date,
	sum(games_played) over (partition by player_id order by event_date) -- 截止到event_date来做累计求和
from
	`累计求和_activity`
```

# 参考链接
- hive中over来完成累计求和. https://www.codenong.com/cs105190396/
- (超详细一文看懂）MySQL累计求和问题及窗口函数order by的原理. https://blog.csdn.net/dhr223/article/details/107413344
