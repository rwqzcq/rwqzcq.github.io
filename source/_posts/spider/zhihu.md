---
title: 知乎爬虫
date: 2022-02-10 11:12:37
tags:
 - 爬虫
categories:
 - 爬虫
---

# 爬取某一个问题ID下面的所有答案

知乎为了反爬取采取了相关的加密机制，其中在请求头中最核心的三个参数为:
1. cookie
2. user-agent
3. x-zse-93
4. x-zse-96

其中`x-zse-93`的值固定为`101_3_2.0`。而`x-zse-96`是最核心的加密后的字符串，关于解密，参考[这一篇博客](https://zhuanlan.zhihu.com/p/419576219)。

> 核心的就是通过浏览器调试JS代码，然后定位到代码：`signature: a()(l()(s))`，其中的参数`s`就是原始的字符串，然后通过知乎自己的加密方式形成`x-zse-96`这个参数。

核心代码为：

```python
def get_x_zse_96(d_c0, uri, x_zse_93='101_3_2.0'):
    """
    解密x-zse-96这个参数
    """
    f = "+".join([x_zse_93, uri, d_c0])
    fmd5 = hashlib.new('md5', f.encode()).hexdigest()
    with open('g_encrypt.js', 'r') as f:
        ctx1 = execjs.compile(f.read(), cwd='/usr/local/lib/node_modules')
    encrypt_str = "2.0_%s" % ctx1.call('b', fmd5)
    return encrypt_str
```


# 参考链接

1. 分析 分析 知乎加密算法 最新 x-zse-96. https://zhuanlan.zhihu.com/p/419576219
2. 知乎爬虫. https://github.com/nanodog/zhihuspider
3. 知乎x-zse-96参数解密. https://blog.csdn.net/weixin_54506550/article/details/121195805
4. 各大网站逆向demo. https://github.com/leishufei/JS-Crack-Records/tree/608224c5d2b16912ebbc63fd7002148571ea0708



