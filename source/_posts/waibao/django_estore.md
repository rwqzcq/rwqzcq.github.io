---
title: Django电商系统通用数据表结构
date: 2022-02-15 00:05:00
tags:
 - django
categories:
 - django
---

# 引入基本的包

```python
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
```

# 分类表

```python
class Category(models.Model):
    """
    分类表
    """
    name = models.CharField(max_length=25, verbose_name='分类名称')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间 默认为当前时间

    class Meta:
        verbose_name = "商品分类管理"  # 设置模型的别名
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)  # 设置排序的字段

    def __str__(self):  # 定义在下拉列表中的显示的名字
        return self.name
```

# 商品表

```python
class Good(models.Model):
    """
    商品表
    """
    name = models.CharField(max_length=25, verbose_name='商品名')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', default=1)
    description = RichTextUploadingField(verbose_name='商品描述')
    img = models.ImageField(upload_to='img', verbose_name='商品图片')
    amount = models.IntegerField(verbose_name='库存量', default=1)
    price = models.FloatField(verbose_name='价格')
    STATUS_CHOICES = (
        ('正常', '正常'),
        ('已下架', '已下架')
    )
    status = models.CharField(verbose_name='状态', default='正常', choices=STATUS_CHOICES, max_length=32)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间 默认为当前时间
    add_user = models.ForeignKey(User, verbose_name='卖家', on_delete=models.CASCADE) # 多卖家的时候有这个字段
    
    @property
    def remain(self):
        return self.amount - self.has_sell

    @property
    def has_sell(self):
        sum_ = self.order_set.aggregate(sum=Sum('amount'))['sum']
        if sum_ is None:
            return 0
        else:
            return sum_

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

    def __str__(self):
        return self.name
```

# 购物车表
> 一个购物车里面只有一种商品
```python
class Cart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='商品')
    amount = models.IntegerField(verbose_name='数量', default=1)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @property
    def total_price(self):
        return self.good.price * self.amount

    class Meta:
        verbose_name = "购物车管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

    def __str__(self):
        return self.user.username
```

# 收货地址表

```python
class Address(models.Model):
    """
    收货地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    province = models.CharField(verbose_name='省份', max_length=255)
    city = models.CharField(verbose_name='市', max_length=255)
    area = models.CharField(verbose_name='区', max_length=255)
    address = models.CharField(verbose_name='详细地址', max_length=255)
    contact_user = models.CharField(verbose_name='收货人', max_length=255)
    phone = models.CharField(verbose_name='手机号', max_length=12)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

    def __str__(self):
        return '''
            {}-{}-{}-{}-{}-{}
        '''.format(self.province, self.city, self.area, self.address, self.contact_user, self.phone)
```

# 订单表

```python
class Order(models.Model):
    """
    订单表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='商品')
    amount = models.IntegerField(default='1', verbose_name='数量')
    total_price = models.FloatField(default='0', verbose_name='总价')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='收货地址')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_price = self.amount * self.good.price
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    STATUS_CHOICES = (
        ('已下单', '已下单'),
        ('已发货', '已发货'),
        ('已收货', '已收货'),
        ('已申请退货', '已申请退货'),
        ('已退货', '已退货'),
    )
    status = models.CharField(verbose_name='订单状态', max_length=32, choices=STATUS_CHOICES, default='已下单')

    DELATE_CHOICES = (
        ('正常', '正常'),
        ('已删除', '已删除'),
    )
    is_delete = models.CharField(verbose_name='是否删除', max_length=32, choices=DELATE_CHOICES, default='正常')

    def delete_order(self):
        self.is_delete = '已删除'
        self.save()
        return True

    def tuihuo(self):
        """
        退货
        :return:
        """
        self.status = '已申请退货'
        self.save()
        return True


    def shuohuo(self):
        self.status = '已收货'
        self.save()
        return True


    class Meta:
        verbose_name = "订单管理"  # 设置模型的别名
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

    def __str__(self):
        return str(self.user) + '-' + str(self.good) + '-' + str(self.amount)
```

# 评论表

```python
class Comment(models.Model):
    """
    评论表
    """
    order = models.ForeignKey(Order, verbose_name='订单', on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name='评分', default=1)
    content = models.TextField(verbose_name='评论内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "评论管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

    def __str__(self):
        return str(self.order)
```