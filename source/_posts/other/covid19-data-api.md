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

# 3. covid-19

数据源来自`https://github.com/CSSEGISandData/COVID-19 dataset`。

主页为:https://pypi.org/project/covid-19/。

主要使用命令行的形式得到世界各国的历史数据。使用如下:

```shell
pip install covid-19
pip install gunicorn
covid serve
```
> 需要开启`VPN`才能使用，因为会直接访问github的CSV文件。

# 4. covid19-api

数据源来自:https://virusncov.com/以及https://epidemic-stats.com/coronavirus/

使用如下:

```python
# sudo pip install covid19-api

import coroapi

instance = coroapi.Corona()
country = 'china' 
instance.country_stats(country)   
```

> 该API只能获取当天的情况，不能获取到历史数据

# 5. covid

pypi地址: https://pypi.org/project/covid/
官方主页: https://nf1s.github.io/covid/worldometers/

# 6. covid-tracking-project

pypi地址:https://pypi.org/project/covid-tracking-project/

> 该包能够追溯到的日期为`2021年3月7日`，因此该包已经过时了。
代码使用如下:

```python
import ctp
data = ctp.us().history()
```
