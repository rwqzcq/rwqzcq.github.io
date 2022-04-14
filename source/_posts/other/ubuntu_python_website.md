---
title: ubuntu部署python网站
date: 2021-12-03 15:50:03
tags:
 - 其他
categories:
 - 其他
---

# 安装相关组件

1. nginx
2. uwsgi

```shell
sudo conda install -c conda-forge uwsgi 
sudo conda install -c conda-forge libiconv
```

如果没有`sudo`命令的话可能会出现`perssion deny`.

# uwsgi编辑

```ini

[uwsgi]                                                                        
                                                                               
socket = 127.0.0.1:5000                                           
                                                                               
plugins = python                                                  
                                                                               
chdir = /python_work/websites/2_flask_estore/scripts                                       
                                                                               
wsgi-file = manage.py                                          
                                                                     
callable = app

processes = 1

threads = 1

buffer-size = 32768

master = true

```

> 以上不要出现任何注释

启动uwsgi

```shell
uwsgi --ini uwsgi.ini &
```

查看uwsgi进程

```shell
ps aux|grep uwsgi
```

杀死相关uwsgi进程

```shell
sudo killall uwsgi
```

# nginx

```shell
server {
    listen 80;
    server_name a.ozflhnb.top;
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5000;
     }
}
```

# django部署

## 1. uwsgi.ini配置

```ini
[uwsgi]
    plugins = python
    socket = 127.0.0.1:8881
    master = true
    enable-threads = true
    workers = 1
    wsgi-file = /python_work/websites/3_pxy_termite_detect/scripts/mysite/wsgi.py
    chdir = /python_work/websites/3_pxy_termite_detect/scripts
    buffer-size = 32768
    pidfile = %(chdir)/uwsgi.pid
```

## 2. 编辑`settings.py`文件

```python

ALLOWED_HOSTS = ['*']
# STATICFILES_DIRS = [BASE_DIR / 'static', ] # 部署的时候这个需要注释掉
STATIC_ROOT = BASE_DIR / 'static'

```

## 4. 收集静态文件

```shell
python manage.py collectstatic
```

## 开启uwsgi

```shell

uwsgi --ini uwsgi.ini

```

## 4. nginx.cof文件配置

```txt

server {
  listen 81;
  server_name localhost;
  location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:8881;
  }
  location /static {
    alias /python_work/websites/3_pxy_termite_detect/scripts/static;
  }
  location /media {
    alias /python_work/websites/3_pxy_termite_detect/scripts/media;
  }
}

```

## 5. 重启nginx

# 参考链接

- conda安装`uwsgi`. https://www.cnblogs.com/jiaxiaoxin/p/10642263.html
- ubuntu下`sudo`没有用. https://blog.csdn.net/jiangjiang_jian/article/details/88933530
- uwsgi+nginx. https://www.cnblogs.com/sdadx/p/10360208.html
