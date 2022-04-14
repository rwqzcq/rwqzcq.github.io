---
title: 2016年投资
date: 2021-08-12 13:49:59
tags:
 - leetcode
categories:
 - leetcode
---

# 题目描述

写一个查询语句，将 2016 年 (TIV_2016) 所有成功投资的金额加起来，保留 2 位小数。

对于一个投保人，他在 2016 年成功投资的条件是：

他在 2015 年的投保额 (TIV_2015) 至少跟一个其他投保人在 2015 年的投保额相同。
他所在的城市必须与其他投保人都不同（也就是说维度和经度不能跟其他任何一个投保人完全相同）。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/investments-in-2016
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

![输入输出](0.png)

# 解题思路

为了判断一个值在某一列中是不是唯一的，我们可以使用`GROUP BY`和`COUNT`。
最开始自己想的是使用`join`操作，但是往往会把`3月份`带入到结果中。

![](1.png)

leetcode官方的解答:

> 注意：这两条要求`需要不分顺序同时满足`，所以如果你想要先用规则 1 来筛选一遍数据，然后再用规则 2 来筛选，会得到错误的结果。

# SQL

```SQL
select
    round(sum(TIV_2016), 2) as TIV_2016
from
    insurance
where
    TIV_2015 in (
        select
            TIV_2015
        from
            insurance
        group by
            TIV_2015
        having count(1) > 1
    ) and
    (LAT, LON) in (
        select
            LAT,
            LON
        from
            insurance
        group by
            LAT, LON
        having
            count(1) = 1
    )
```

> where中的条件在原表中要`同时满足`而没有`先后顺序`，注意是同时!不是是先筛选了`TIV2015`后拿着筛选后的结果再去筛选`LAT LON`