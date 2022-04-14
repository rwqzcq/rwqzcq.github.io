---
title: mysql简单题
date: 2021-08-12 12:45:51
tags:
 - SQL
 - leetcode
categories:
 - leetcode
---

# 

[题目链接](https://leetcode-cn.com/problems/count-student-number-in-departments/comments/)

```sql
select
    a.dept_name,
    -- if(count(b.student_id) is null, 0, count(b.student_id)) as student_number
    count(b.student_id) as student_number,
    -- count(null)返回0
    -- sum(null) 返回null
    -- avg(null) 返回null
from
    department as a
left join
    student as b
on 
    a.dept_id = b.dept_id
group by    
    a.dept_id
order by
    student_number desc,
    dept_name 
```


[题目链接](https://leetcode-cn.com/problems/find-customer-referee/solution/xun-zhao-yong-hu-tui-jian-ren-by-leetcode/)

```sql
select
    name
from
    customer
where
    referee_id != 2 or 
    referee_id is null
```

MySQL 使用三值逻辑 —— `TRUE`, `FALSE` 和 `UNKNOWN`。任何与 NULL 值进行的比较都会与第三种值 `UNKNOWN` 做比较。这个“任何值”包括 `NULL 本身`！这就是为什么 MySQL 提供 IS NULL 和 IS NOT NULL 两种操作来对 NULL 特殊判断。

作者：LeetCode
链接：https://leetcode-cn.com/problems/find-customer-referee/solution/xun-zhao-yong-hu-tui-jian-ren-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


# 612

表 point_2d 保存了所有点（多于 2 个点）的坐标 (x,y) ，这些点在平面上两两不重合。

 

写一个查询语句找到两点之间的最近距离，保留 2 位小数。

 

| x  | y  |
|----|----|
| -1 | -1 |
| 0  | 0  |
| -1 | -2 |
 

最近距离在点 (-1,-1) 和(-1,2) 之间，距离为 1.00 。所以输出应该为：

 

| shortest |
|----------|
| 1.00     |
 

注意：任意点之间的最远距离小于 10000 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shortest-distance-in-a-plane
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```sql
select
    round(sqrt(power(a.x-b.x, 2) + power(a.y-b.y, 2)), 2) as shortest
from
    point_2d as a
left join 
    point_2d as b
on
    (a.x, a.y) != (b.x, b.y)
order by 
    shortest
limit 1
```

