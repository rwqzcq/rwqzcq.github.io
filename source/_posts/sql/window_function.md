---
title: 窗口函数
date: 2021-09-15 14:57:15
tags:
 - SQL
categories:
 - SQL
---

# 窗口函数是什么


# 窗口函数的一般形式

```txt
window_function_name (expression)
over(
	[partition_definition]
	[order_definition]
	[frame_definition]
)
```
> 之前只是复习到了`partition by`、`order by`，但是并没有学到`frame_definition`，而在`leetcode 1321题`中则是典型的滑动窗口的使用案例。

# 窗口函数中的滑动窗口

滑动窗口有两大类别，分别是基于`行`的与基于`范围`的。

## 基于行的滑动窗口

基于`行`的滑动窗口包括的语法形式为:

> rows between frame_start and frame_end

`frame_start`和`frame_end`可以支持如下关键字，来确定不同的动态行记录：

- current row 边界是当前行，一般和其他范围关键字一起使用
- unbounded preceding 边界是分区的第一行
- unbounded following 边界是分区的最后一行
- expr preceding 边界是当前行减去expr行
- expr following 边界是当前行加上expr行

比如:

- rows between 1 preceding and 1 following: 窗口的范围就是3行，即：当前行、上一行、后一行
- rows between unbounded preceding and unbounded following: 全部分区

## 基于范围的滑动窗口

不是以行数来衡量，比如希望窗口范围是一周前的订单开始，截止到当前行。此时可以使用`range`来完成。比如

> `range between 10 preceding and 5 following`表示值在[n-10,n+5]范围内的所有值

需要注意的有:

> mysql8.0中目前不支持`following`相关的操作

> 窗口函数中使用`range`，则`order`中需要指定的列的类型为`数字`或者`时间差`

![](https://img-blog.csdnimg.cn/20201121171300979.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMzODY3Ng==,size_16,color_FFFFFF,t_70#pic_center)

> range中order的为`datetime`类型，那么需要加`interval`

![](https://img-blog.csdnimg.cn/20201121172449842.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMzODY3Ng==,size_16,color_FFFFFF,t_70#pic_center)

# 参考链接

- mysql窗口函数中的滑动窗口. https://blog.csdn.net/weixin_46338676/article/details/109899748