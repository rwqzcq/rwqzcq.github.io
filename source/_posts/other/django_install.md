---
title: django通用安装配置
date: 2021-08-02 21:10:00
tags:
 - 其他
categories:
 - 其他
---

# 1. 安装anaconda

> 32位的电脑就下载32位的安装包，64位电脑就下载64位的安装包

[32位下载](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2019.10-Windows-x86.exe
)

[64位下载](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2019.10-Windows-x86_64.exe
)

# 2. 安装phpstudy

> 32位的电脑就下载32位的安装包，64位电脑就下载64位的安装包

[32位下载](http://public.xp.cn/upgrades/phpStudy_32.zip)

[64位下载](http://public.xp.cn/upgrades/phpStudy_64.zip)

# 3. 配置淘宝源

打开`anaconda prompt powershell`

![](0.png)

输入:

```shell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
```

# 4. 安装相关包

## 4.1 django

```shell
pip install django==3.1.2
```

## 4.2 mysqlclient

```shell
pip install mysqlclient
```

## 4.3 simpleui

```shell
pip install django-simpleui
```

## 4.4 ckeditor

```shell
pip install django-ckeditor
```

# 5. 配置phpstudy

## 5.1 安装数据库相关软件

![](1.png)

## 5.2 启动数据库服务

![](2.png)

## 5.3 打开数据库管理软件

![](3.png)

<<<<<<< HEAD
## 6. 安装安装代码编辑器 Vs Code

[下载](http://vscode.cdn.azure.cn/stable/78a4c91400152c0f27ba4d363eb56d2835f9903a/VSCodeUserSetup-x64-1.43.0.exe)

下载地址: http://vscode.cdn.azure.cn/stable/78a4c91400152c0f27ba4d363eb56d2835f9903a/VSCodeUserSetup-x64-1.43.0.exe

## 7. 下载向日葵

[下载](https://sunlogin.oray.com/download)

下载地址: https://sunlogin.oray.com/download

## 8. 观看视频，了解django
=======
## 6. 安装Vs code

[下载](http://vscode.cdn.azure.cn/stable/78a4c91400152c0f27ba4d363eb56d2835f9903a/VSCodeUserSetup-x64-1.43.0.exe)

## 7. 观看视频，了解django
>>>>>>> a0f0c488d8e95c86febe7c323b7e22d38991a299

<iframe src="//player.bilibili.com/player.html?aid=16957624&bvid=BV1GW411Y7EU&cid=27721310&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="400" width="100%"> </iframe>