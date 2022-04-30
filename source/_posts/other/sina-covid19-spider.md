---
title: 新浪网新冠肺炎数据爬取
date: 2022-03-03 23:49:10
tags:
 - 其他
categories:
 - 其他
---

本博客针对新浪网的疫情实时播报网页(https://news.sina.cn/zt_d/yiqing0121)进行数据采集，主要采集的指标分别`国内`、`国外`两个部分。采集的数据维度包括：
- 新增确诊
- 累计确诊
- 新增死亡
- 累计死亡
- 新增治愈
- 累计治愈
- 各省数据
- 全国数据

# 相关API

| API | 请求方式 | 解释 | 返回示例
| - | - | - | - |
| https://gwpre.sina.cn/ncp/get_data?type=1&callback=dynamicData | GET | 获取包含所有国家的历史数据的csv文件 | try{dynamicData({"result":{"status":{"code":0,"msg":"succ"},"timestamp":"Thu Mar 03 23:53:07 +0800 2022","data":{"csv_url":"https:\/\/comment.sinaimg.cn\/ncp\/all_country_history_1646321400.csv"}}});}catch(e){}; |
| https://comment.sinaimg.cn/ncp/all_country_history_1646321400.csv | GET | 获取所有国家的历史数据 | 美国,SCUS0001,1646236800,80770604,0,53945789,979725,72680,0,214984,2323,25845090,-144627,324024,936375.88,246,878.50,536.90 | 
| https://gwpre.sina.cn/interface/news/ncp/data.d.json?mod=province&province=hebei | GET | 获取中国某一个省份的所有历史数据 | 
| https://gwpre.sina.cn/interface/news/ncp/data.d.json?mod=city&citycode=CN61010000000000&_=1647186530303&callback=jsoncallback | GET | 获取中国某一个城市的所有历史数据 | 
