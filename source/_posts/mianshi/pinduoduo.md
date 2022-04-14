---
title: 拼多多
date: 2021-08-01 21:41:19
tags:
 - 秋招
categories:
 - 面试
---

# 提前批

## 一面

1. SQL题

- 任意两个月份的销售额大于某一个值
> 用`case when`

```sql
    select
        mallid,
        ordertime
    from (
        select
            *,
            case when amt >= 100000 then 1 else 0 end as if_ok
        from (
            select
                mallid,
                month(ordertime) as ordertime,
                sum(amt) as amt
            from
                base
            group by
                mallid,
                month(ordertime)
        ) as a
    ) as a 
    group by
        mallid,
        ordertime
    having
        sum(amt) >= 2


    
    


    

```

2. 自己做得项目
3. 假设检验
4. 大数定理
5. 决策树确定最大的子树
6. 开放题
    - 确定今年的GDP为6%，如何规划
> 强调的是指标的拆解，比如按照地区、按照产业细分


