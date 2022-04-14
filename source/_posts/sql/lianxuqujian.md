---
title: 连续区间问题
date: 2021-07-22 14:05:09
tags:
 - SQL
categories:
 - SQL
---

# 连续出现数字

![题目描述](./0.png)

## 思路

- 使用`lag`窗口函数来求当前行的前N行数据
- 根据Id来过滤

## SQL

```SQL
select
	distinct num as '连续出现3次的数字'
from (
	select
		*,
		lag(id, 2) over (partition by Num order by id) as prev
	from
		`logs`
) as a
where 
	id = prev + 2
```

核心在：

> lag(id, 2) over (partition by num order by id) as prev

lag往前推2个：根据num来分组，根据Id来排序，将id作为prev

# 参考链接

1. lag函数. https://www.begtut.com/mysql/mysql-lag-function.html 