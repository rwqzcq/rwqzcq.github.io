---
title: 新冠肺炎数据统计API
date: 2022-01-23 17:04:57
tags:
 - 其他
categories:
 - 其他
---

调研了现有的一些开源的新冠肺炎API

# 1. django_covid19

## 地址

http://ncov.leafcoder.cn/docs/#/?id=country-daily

## 特点

- 以`丁香园`作为数据源
- 可以部署到本地运行，提供一个可视化大屏
- API比较丰富，可以分`国家`分`省市`查看

> 最新的数据是`2021年1月11号`，时效性较差

# 2. akshare

## 地址

https://akshare-4gize6tod19f2d2e-1252952517.tcloudbaseapp.com/data/event/event.html

## 特点

- 接口齐全
- 返回最新的数据，返回的是最近`60天`的数据，并不能返回从疫情爆发以来的全部数据

> 有一些接口不能用，比如`covid_19_baidu`



