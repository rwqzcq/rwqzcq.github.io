---
title: 微博数据集
date: 2022-03-30 17:38:06
tags:
 - 数据集
categories:
 - 数据集
---

# 微博社交网络数据集总结

| 数据集名称 | 下载地址 | 用途 | 总结 |
| - | - | - | - |
| MicroblogPCU | [下载](https://archive.ics.uci.edu/ml/machine-learning-databases/00323/) | 探索微博中的spammers（发送垃圾信息的人） | 数据量适中；适合做小项目，是一个比较理想的数据集 | 
| WeiboSpammer | [下载](https://github.com/WxxShirley/WeiboSpammer) | 异常粉丝 | 数据量较少，但是是一个完整的项目 | 
微博数据集 | 链接：https://pan.baidu.com/s/1tStvmHwRcXsGxiUh8SbI9A 提取码：n3hl | 数据量很大，对机器要求高 | 
北京大学新浪微博用户关系数据 | [下载](https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/KVBL82) | 数据量小，只有id编号，没有其他数据 | 


# MicroblogPCU

## 数据集信息

### weibo_user.csv  
- user_id: 用户ID
- user_name: 用户昵称
- gender:性别，male，female，other
- class:账户级别
- message:账户注册位置或其他个人信息
- post_num: 邮政编码
- follower_num: followers的数量
- followee_num: followee的数量
- follow ratio: followee_num/follower_num;
- is_spammer: manually annotated label, 1 表示 spammer，0 表示 non-spammer;

### user_post.csv 
- post_id:微博的ID
- post_time:发布时间
- poster_id: 发布用户的ID
- repost_num:转发数量
- commnet_num: 评论数量

### followe-followee.csv 
- follower: the nickname of follower;
- follower_id: the user ID of follower;
- followee: the nickname of followee;
- followee_id: the user ID of followee;


# 参考链接

- 新浪微博数据集MicroblogPCU. https://blog.csdn.net/scythe666/article/details/51872882
- 