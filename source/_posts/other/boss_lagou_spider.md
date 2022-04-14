---
title: Boss/拉勾网爬虫
date: 2021-07-30 10:40:41
tags:
 - 其他
categories:
 - 其他
---


需要帮助女朋友统计市面上游戏公司的薪资水平，因此需要从`boss`以及`拉钩`上爬取给定的游戏公司内发布的所有职位的招聘信息，通过从Github上clone下来的一些代码以及CSDN上的博客，发现总体上爬取方式有两种：
1. requests构造请求头，携带上cookie发送请求，从而返回一个JSON，进而去取数据。
2. 使用`selenium`控制浏览器爬取。

但是自己在实操中发现了以下的问题:
1. 挂上cookie爬取很容易遇到反爬的问题。
2. 由于拉勾网在打开网页的时候在加载完`doc`会加载ajax请求，因此selenium设置的`等待时间`不可控，经常会闪退。

通过看这位[大神](https://github.com/xianyunyh/spider_job)的代码发现可以通过以下的方式来解决问题:
1. 用`手机端`的拉钩接口。
2. 用代理IP,我用的是快代理，还可以。
3. 每一轮爬取都`sleep`5到20秒钟。
通过使用浏览器调试手机端的拉钩，可以看到手机端API的一个demo:

```TXT
https://gate.lagou.com/v1/entry/position/queryByCompany?companyId=451&showId=null&positionType=&city=&pageNo=1&pageSize=10&workYear=&salary=&_t=1627612742833
```
上面的demo为查看某一个公司发布的岗位。

> 凡是碰到有封锁IP的网站都可以使用谷歌浏览器调试，尝试使用手机端的接口



# 参考网站
1. https://github.com/xianyunyh/spider_job