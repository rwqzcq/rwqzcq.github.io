---
title: 堡垒机使用技巧
date: 2022-05-20 19:49:36
tags:
 - 工作
 - 中信证券
categories:
 - 中信证券
---

由于堡垒机完全与外网隔绝，所以安装软件、调试代码方面有很多不便，因此总结一下堡垒机的一些使用的方法。

## 安装python包

由于一些包会依赖其他包，因此单独下载一个`whl`文件会导致安装不上的问题，因此比较合适的做法是：

> 在本地下载好依赖包之后再去上传到堡垒机上。

使用到了`pip download`这个指令，然后再通过`pip install`安装静态文件

本地`下载`包:

```shell
pip download -d 目录 -r requirements.txt
```

堡垒机上`安装`包

```shell
pip install --no-index --find-links=包目录 -r requirements.txt
```

# 参考链接
- windows server 2012桌面锁定在开始菜单那里什么都点不开 又没卡 怎么弄啊？: https://zhidao.baidu.com/question/1246627843100866579.html
- Windows server 2016 点开始无反应: https://jingyan.baidu.com/article/e75057f2e456c8ebc81a894d.html
- Pip 技巧 批量下载安装 WHL 文件: https://blog.csdn.net/Daphnisz/article/details/106390316
