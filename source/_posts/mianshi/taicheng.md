---
title: 上海-泰诚科技笔试题目
date: 2021-05-14 11:16:15
tags:
 - 面试
 - 笔试
categories:
 - 面试
---

# 1.用python进行数据整理及分析：
a)打开“inputs.csv”筛选出2019年全年，type=DAID的数据

b)检查数据是否有缺失值，是否每半小时都有数据，并用上一时刻的值补齐数据
c)做一些简单的visualization，分析2019年DAID的走势（任何角度都可以，并配合简单的语言解释）
d)将得到的图和解释写在下面：

# 2.蒙特卡洛模拟：
a)还是使用上题的数据集，使用蒙特卡洛模拟，模拟出2021年2月的DANF和DATF的半小时颗粒度的数据。

b)简单描述模拟过程和注意事项：

# 3.排序算法：给你一个整数数组alist，请你将该数组升序排列。

a)编写以上算法；

写出该算法的空间复杂度。

# 4.编写一个SQL查询，获取Employee表中第n高的薪水（Salary）

例如上述Employee表，n = 2 时，应返回第二高的薪水 200。如果不存在第 n 高的薪水，那么查询应返回 null。

```sql
select
    case when Salary is null then null else Salary end as max_salary
from (
    select
        *,
        row_number() over(order by Salary desc) as 'ranking'
    from Employee
) as a
where a.ranking = n
```

# 参考链接

1. 蒙特卡洛. https://zhuanlan.zhihu.com/p/342624971
2. pandas时间日期操作. https://www.pypandas.cn/docs/user_guide/timeseries.html#%E8%BD%AC%E6%8D%A2%E6%97%B6%E9%97%B4%E6%88%B3
3. seaborn折线图. https://seaborn.pydata.org/examples/errorband_lineplots.html 
