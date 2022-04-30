---
title: 求中位数
date: 2021-07-22 15:53:41
tags:
 - SQL
categories:
 - SQL
---

# 题目描述

![](./0.png)

# 解题思路

- 使用`row_number`窗口函数对公司薪资进行分组排序，得到序号
- 使用`count`窗口函数统计公司内员工的数量
- 判断当前记录的序号是否在`数量 / 2`与`数量 / 2 + 1`之间

# SQL

```sql
select
    Id,
    Company,
    Salary
from (
    select
        *,
        row_number() over (partition by Company order by Salary) as ranking,
        count(*) over (partition by Company) as num
    from 
        Employee
) as a
where
    ranking between num / 2 and num / 2 + 1 -- 核心
```


# 题目描述

[牛客网SQL88题](https://www.nowcoder.com/practice/165d88474d434597bcd2af8bf72b24f1?tpId=82&tags=&title=&difficulty=0&judgeStatus=0&rp=1)

[leetcode](https://leetcode-cn.com/problems/find-median-given-frequency-of-numbers/submissions/)

# 解题思路

这里题目使用的不是单纯得从1开始排序的，而是每一个阶段的综合数量，配合sum窗口函数累积求和问题，再加上求解中位数的一个技巧即可完成，技巧为：

> 当某一数的正序和逆序累计均大于整个序列的数字个数的一半即为中位数

比如:
A A B B C C D D 
1 2 3  4  5 6  7 8
8 7 6  5  4  3 2 1
那么上面的4，5以及5，4就是中位数，如果是奇数的话，就只有1个
再比如
A2个，B3个，C5个，D2个，
正序2，5，10，12
倒序12，10，7，2
正序和12，大于等于6的，为C,D，
逆序和为12，大于等于6的为ABC，所以最后中位数为C

```sql
-- 当某一数的正序和逆序累计均大于整个序列的数字个数的一半即为中位数
WITH base AS (
	SELECT
		*,
		( SELECT sum( number ) FROM class_grade ) AS total,
		sum( number ) over ( ORDER BY grade ) AS ranking,
		sum( number ) over ( ORDER BY grade DESC ) AS r_ranking 
	FROM
		class_grade 
	ORDER BY
		grade 
	) 
SELECT
	avg(grade)
FROM
	base 
WHERE
	ranking >= total / 2 
	AND r_ranking >= total / 2
```

# 另一种巧妙的解题思路

> 一个序列的正序与倒叙的index要么相等，要么相差为1

还是第一题，那么这个时候优化的写法为：

```sql
select
	Company,
	Salary
from (
	SELECT
		*,
		cast(ROW_NUMBER() over (PARTITION by Company ORDER BY Salary) as SIGNED) as ranking, -- 显示类型转换
		cast(ROW_NUMBER() over (PARTITION by Company ORDER BY Salary desc) as SIGNED) as reverse_ranking
	FROM
		`牛客_employee_中位数`
) as a
where
	ranking = reverse_ranking or abs(ranking - reverse_ranking) = 1 -- 接受相减是负数的结果
```

这个里面需要注意的是`SIGNED INT`与`UNSIGNED INT`的区别。

`unsigned` 是mysql自定义的类型，表示`无符号数值即非负数`。signed为整型默认属性。
由于`ranking-reverse_ranking`的结果可能为负数，因此需要转化成`signed`。

> 上面的这种写法不太适合于[leetcode569题](https://leetcode-cn.com/problems/median-employee-salary/)

比如最后的结果需要加上`id`的话还需要在`窗口函数里面加上id`，比如`order by id`以及`order by id desc`

```sql
select
    Id,
    Company,
    Salary
from (
    select
        *,
        cast(row_number() over (partition by Company order by Salary, id) as signed) as ranking,
        cast(row_number() over (partition by Company order by Salary desc, id desc) as signed) as reverse_ranking
    from
        Employee
) as a
where
    ranking = reverse_ranking or abs(ranking - reverse_ranking) = 1
order by
    Company, Salary


```

# 参考链接

- https://blog.csdn.net/qq_45445841/article/details/104002092
- 
