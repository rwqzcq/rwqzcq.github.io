---
title: 服务器上配置jupyter lab远程访问
date: 2022-01-03 14:43:04
tags:
 - 其他
categories:
 - 其他
---

# 基本环境配置

- 操作系统: ubuntu18.4
- node.js
- npm

> npm node.js是必须的，否则在`Jupyter build`的时候就会报错。可以在conda里面安装nodejs

```shell
conda install nodejs
```

# jupyter相关配置

生成配置文件

```shell
jupyter lab --generate-config
```

生成密码

```python
from notebook.auth import passwd
passwd()
```

修改配置文件

```shell
vim /root/.jupyter/jupyter_lab_config.py
```

需要修改的信息如下：

```python
c.ServerApp.allow_root = True # 允许以root的方式运行jupyter
c.ServerApp.allow_remote_access = True # 允许远程访问
c.ServerApp.open_browser = False # 启动Jupyter的是不自动开启浏览器
c.ServerApp.ip = '*' # 允许所有的ip访问
c.ServerApp.port = 8888 # 访问端口
c.ServerApp.password = '' # 之前生成的密码
c.ServerApp.notebook_dir = '/home/hengd/container/workspace/RWQ' # 根目录
c.ServerApp.root_dir = '/home/hengd/container/workspace/RWQ' # 根目录
```

`build`jupyter

```shell
jupyter lab build
```

> 在build的时候发现了服务器上没有安装`nodejs`


# 关于外网访问问题

如果访问不了的话最有可能还是`没有放行对应的端口`。使用`iptables`来完成相应的操作：

```shell
apt-get install iptables
iptables -I INPUT -p tcp --dport 9200 -j ACCEPT
iptables-save
```

在学院的服务器上由于无法切换到`root`用户因此无法开发端口，所以目前没有解决外网访问配置的问题。


# 参考链接
- 云服务器搭建神器JupyterLab（多图）. https://blog.csdn.net/ds19991999/article/details/83663349
- Ubuntu20.04开放指定端口. https://blog.csdn.net/lianghecai52171314/article/details/113813826
- 远程访问服务器JupyterLab的配置方法. https://blog.csdn.net/GouGe_CSDN/article/details/104567559
