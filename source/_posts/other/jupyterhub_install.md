---
title: jupyterhub配置使用
date: 2022-05-11 21:49:19
tags:
 - 其他
categories:
 - 其他
---

官方文档: https://jupyterhub.readthedocs.io/en/latest/quickstart.html

# 机器基本配置

- ubuntu
- anaconda环境

# Jupyterhub多用户配置

要想实现`多用户互相隔离`需要满足以下条件：

1. 在ubuntu中需要新建用户。
2. ubuntu中为每一个用户编辑`.bashrc`，讲`anaconda`加入到环境变量中。
3. 为自己的用户目录配置`777权限`。
4. 编辑`jupyter-notebook`配置文件。

```python

c.LocalAuthenticator.create_system_users = True
c.Authenticator.whitelist = {'root', '用户1', '用户2'} 
c.Authenticator.admin_users = {'root', }
c.JupyterHub.admin_access = True

c.Spawner.args = ['--allow-root']
# 配置每一个用户的jupyter目录
c.Spawner.notebook_dir = '~/notebook'

```

# Jupyterhub + Django OAuth配置

参考本链接: https://vkaustubh.github.io/blog/geek/2020-02-08-integrating-jupytethub-with-django.html

jupyter-notebook文件配置

```python

# This is how we tell Jupyter to use OAuth instead of the default
# authentication which is done using local Linux user accounts.
c.JupyterHub.authenticator_class = 'oauthenticator.generic.GenericOAuthenticator'

# Where should Django pass the authentication results back to?
c.GenericOAuthenticator.oauth_callback_url = 'http://localhost:8010/hub/oauth_callback'

# What is the client ID and client secret for Jupyterhub provided Django?

c.GenericOAuthenticator.client_id = 'bzAVpy1Dm8xOrGjSBBganWWYeixGXPFY2YCelxld'
c.GenericOAuthenticator.client_secret = '3qdEs5SkyBXMhY3DLmLOWqGgiROl6uEi0jUm5ek80tYJh2hWA4GxNn0qQyEcKZyR5BWDhKwCH89vKRFShHCudhIRTzO4d6bMunS1wncYCr43n2Li5Z380Tu4WoTOCzS4'

# Where can Jupyterhub get the token from?
c.GenericOAuthenticator.token_url = 'http://localhost:8000/o/token/'

# Where can it get the user name from? What method shall it use?
# What key in the JSON output is the username?
c.GenericOAuthenticator.userdata_url = 'http://localhost:8000/userdata'
c.GenericOAuthenticator.userdata_method = 'GET'
c.GenericOAuthenticator.userdata_params = {}
c.GenericOAuthenticator.username_key = 'username'

# What address will Jupyterhub be accessed from?
c.JupyterHub.bind_url = 'http://localhost:8010'

# By default Jupyterhub requires that a Linux user exist for every
# authenticated user. For testing, we are going to trick JupyterHub
# to merely pretend that such a user exists and launch notebook servers
# for the same user running the hub process itself!
# from jupyterhub.spawner import LocalProcessSpawner

# class SameUserSpawner(LocalProcessSpawner):
#     """Local spawner that runs single-user servers as the same user as the Hub itself.

#     Overrides user-specific env setup with no-ops.
#     """

#     def make_preexec_fn(self, name):
#         """no-op to avoid setuid"""
#         return lambda : None

#     def user_env(self, env):
#         """no-op to avoid setting HOME dir, etc.""" 
#         return env

# c.JupyterHub.spawner_class = SameUserSpawner

c.LocalAuthenticator.create_system_users = True
c.Authenticator.whitelist = {'root', 'student1', 'lgc'} 
c.Authenticator.admin_users = {'root', }
c.JupyterHub.admin_access = True

c.Spawner.args = ['--allow-root']
c.Spawner.notebook_dir = '~/notebook'


```

# how to add an user to Ubuntu

```shell

# add username

adduser student1

# set paasword

passwd student1

# mkdir user dir

mkdir /home/student1

# auth the dir to the user

chown student1 /home/student1


```

# how to edit bashrc

```shell

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

```

# how to add an user to the jupyterhub

## user the root to create an user

## change to the user

## mkdir an dir named `notebook` to the added user

```shell

chmod -R 777 ~/notebook

```

## change the `.bashrc` in order to add the conda path 

```shell

gedit ~/.bashrc

# add conda path

source ~/.bashrc

```

## change `jupuyerhub_config.py`

```python

# add the username to the whitelist

c.Authenticator.whitelist = {'root', 'student1', 'lgc'} 

```

## restart the jupyterhub server
