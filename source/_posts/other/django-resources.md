---
title: Django相关扩展资源
date: 2021-05-21 18:07:17
tags:
 - 其他
 - Django
categories:
 - 其他
---

这里收录了平常自己看到的有用的Django相关的博客、第三方库等。

# Django-Forms

## 1. 建立modelForm

```python
from django.forms import ModelForm
from .models import HealthInfo

class MyForm(ModelForm):
  class Meta:
    """
    规定了要为哪一个model创建表单
    """
    model = HealthInfo # 指定模型
    fields = '__all__' # 指定字段
    exclude = ['user', 'create_at'] # 指定排除的字段
    

```

## 2. views中使用-添加数据

```python
def add_info(request):
    """
    填报信息
    """
    if request.method == 'GET':
        user_form = InfoForm() # 生成form
        return render(request, 'health/add_info.html', {'user_form': user_form})
    else:
        user_form = InfoForm(request.POST) # 把Post中的数据添加到form中
        if user_form.is_valid():
            user_form.save()
            # TODO
        else:
            return render(request, 'health/add_info.html', {'user_form': user_form})
```

## 3. template中加载form

```html
{% extends 'base.html' %}
{% block content %}
    {% for key, error in user_form.errors.items %}
             <div class="alert alert-danger">{{ key }} - {{ error}}</div>
    {% endfor %}
    <form class="form-horizontal" method="post" action="">
        {% csrf_token %}
        <h2 class="form-signin-heading text-center">Title</h2>
        {% for user in user_form %}
            <div class="form-group">
                <label class="col-md-2" class="sr-only">{{ user.label }}</label>
                <div class="col-md-10">
                    {{ user }}
                </div>
            </div>
        {% endfor %}
        <div class=" text-center">
            <button type="submit" class="btn btn-primary">提交</button>
        </div>
      </form>
      <script>
          $(function(){
              $('input').addClass('form-control');
              $('select').addClass('form-control');
          });
      </script>
{% endblock %}
```

[原始链接](1_form.md)

# Django_tables2

## 1. 建立tables

```python

class InfoTable(tables.Table):
    """
    定义Modeltable
    https://django-tables2.readthedocs.io/en/latest/pages/table-data.html#table-data
    """
    class Meta:
        model = HealthInfo # 指定模型
        attrs = {"class": "table table-striped"} # 自定义属性
```
## 2. views中使用

```python
def my_info(request):
    """
    个人信息填报
    """
    qs = HealthInfo.objects.filter(user=request.user)
    table = InfoTable(qs)

    return render(request, 'health/my_info.html', {'table': table})
```

## 3. 模板中使用

```html
{% load render_table from django_tables2 %}
<h4>我的填报</h4>
<div>
    {% render_table table %}
</div>
```

## 4. 自定义字段

```python
from django_tables2 import tables
from django_tables2.utils import A

detail = tables.columns.LinkColumn('detail', args=[A('pk')], orderable=False, empty_values=(), verbose_name='操作')

def render_detail(self):
    return '查看详情'
```

## 5. 显示图片

```python

from django.utils.html import format_html


class ImageColumn(tables.columns.Column):
    """
    自定义图片
    """
    def render(self, value):
        return format_html(
            '<img src="/media/{url}" class="center-block" height="20px", width="20px">',
            url=value
            )
    
```

## 6. 前台分页显示

https://django-tables2.readthedocs.io/en/latest/pages/pagination.html

```python
def index(request):
    qs = News.objects.all()
    table = NewsTable(qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10) # 这里是核心
    return render(request, 'app/index.html', {'table': table})
```

> 用了bootstrap4版本需要在前台加上JS代码以修正其样式的显示

```html
<script>
$(function(){
    $('ul.pagination li').addClass('page-item');
    $('ul.pagination li > a').addClass('page-link');
});
</script>
```

## 7. Models中自定义了property

```python

class Movie(models.Model):
    """
    电影表
    """
    movie_id = models.IntegerField(verbose_name='电影id', primary_key=True)
    name = models.CharField(verbose_name='电影名称', max_length=128)
    release_date = models.CharField(verbose_name='上映日期', max_length=128, null=True, blank=True)

    @property
    def release_days(self, ):
        """
        上映天数
        """
        release_date = datetime.datetime.strptime(self.release_date, '%Y-%m-%d')
        today = datetime.datetime.now()
        release_days = (today - release_date).days
        return release_days  

```

可以直接在tables中去使用

```python

class MovieTable(tables.Table):
    """
    定义Modeltable
    https://django-tables2.readthedocs.io/en/latest/pages/table-data.html#table-data
    """
    total_piaofang = tables.columns.Column(verbose_name='总票房(万)') # 在这里更换别名
    release_days = tables.columns.Column(verbose_name='上映天数(天)')
    class Meta:
        model =  Movie # 指定模型
        attrs = {"class": "table table-striped"} # 自定义属性
        fields = ('name', 'release_date', 'release_days', 'total_piaofang', )

```

[原始链接](2_tables2.md)

# Django_filter

## 1. 定义

```python
class BoothFilter(django_filters.FilterSet):
    """
    摊位过滤器
    """
    status = django_filters.ChoiceFilter(choices=Booth.STATUS_CHOICES)

    class Meta:
        model = Booth
        # fields = ['name', 'location', 'price', 'area']
        fields = {
            'name': ['contains'],
            'position': ['contains', ],
            'area': ['lt', 'gt'],
            'price': ['lt', 'gt'],
            # 'status': ['choices', ]

        }

        @property
        def qs(self):
            parent = super().qs
            return parent
```

## 2. views中使用

```python
f = BoothFilter(request.GET, queryset=qs)
return render(request, 'booth/search.html', {'filter': f})
```

## 3. 模板中使用

```html
<form method="get" class="form form-horizontal">
  {% for exp in filter.form %}
  <div class="form-group">
    <label class="col-md-2" class="sr-only">{{ exp.label }}</label>
    <div class="col-md-10">
      {{ exp }}
    </div>
  </div>
  {% endfor %}
  <div class=" text-center">
    <button type="submit" class="btn btn-primary">Search</button>
  </div>
</form>
{% if filter.qs.count > 0 %}
	循环
{% endif %}
```

[原始链接](3_filter.md)

# django_filter与tables2结合使用

```python
def index(request):
    qs = News.objects.all()
    f = NewsFilter(request.GET, queryset=qs)
    table = NewsTable(f.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, 'app/index.html', {'table': table, 'filter': f})
```

模板中的写法

```html
{% load bootstrap4 %}
{% load render_table from django_tables2 %}
    <form method="get" >
    {% bootstrap_form filter.form  %}
    <div class=" text-center">
        <button type="submit" class="btn btn-primary">Search</button>
    </div>
    </form>
    {% if filter.qs.count > 0 %}
        {% render_table table %}
    {% endif %}

<script>
    $(function(){
        $('ul.pagination li').addClass('page-item');
        $('ul.pagination li > a').addClass('page-link');
        $('#id_create_at__lt').attr('type', 'date');
        $('#id_create_at__gt').attr('type', 'date');
    });
</script>
```

# django中执行原生SQL

https://docs.djangoproject.com/zh-hans/3.2/topics/db/sql/

```python
from django.db import connection

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row
```

# Django-mptt

> 无限极分类插件
https://django-mptt.readthedocs.io/en/latest/install.html


# Django Filter结合分页

## views.py

```python

import django_filters
from .models import *

class PaperFilter(django_filters.FilterSet):
    class Meta:
        model = Paper
        fields = {
            'title': ['contains']  
        }

# Create your views here.
def paper_list(request):
    """
    论文管理
    """
    qs = Paper.objects.all().order_by('-year', '-n_citation')
    f = PaperFilter(request.GET, queryset=qs)
    # 每页展示的数量
    per_page = 10 
    # 实例化一个分页器对象
    paginator = Paginator(f.qs, per_page)
    # 获取当前页码数
    page_number = request.GET.get('page', 1)
    # 获取当前页面的对象列表
    page_obj = paginator.page(page_number)
    return render(request, 'paper/list.html', {'filter': f, 'page_obj': page_obj})
```

## templates

```html
{% extends 'base.html' %}
{% block content %}
<div class="container">
    {% load bootstrap4 %}
    <form action="" method="GET">
        {% bootstrap_form filter.form  %}
        <div class="text-center">
            {% buttons submit='提交' %}
            {% endbuttons %}
        </div>  
    </form>
</div>
<hr>
{% if filter.qs.count > 0 %}
    {% for obj in page_obj %}
        <div class="card" style="margin-top:5px;">
            <div class="card-header">
                <a href="{% url 'paper_detail' obj.id %}" target="_blank">{{ obj.title }}</a>
                {% if request.user.id in obj.fav_user_ids %}
                    <span class="float-right">
                        <button class="btn btn-sm btn-success" disabled="disabled">已收藏</button>
                        <a href="{% url 'do_cancel_fav' obj.id %}" class="btn btn-sm btn-danger" target="_blank">取消收藏</a>
                    </span>
                {% else %}
                    <span class="float-right">
                        <a href="{% url 'do_fav' obj.id %}" class="btn btn-sm btn-primary" target="_blank">收藏</a>
                    </span>
                {% endif %}
            </div>
            <div class="card-body">
                <p>{{ obj.authors }}</p>
                <p>{{ obj.venue }}</p>
                <p>
                    Publish at: {{ obj.year }}
                </p>
                <p>
                    Citation Number: 
                    <span class="text-success">{{ obj.n_citation }}</span>
                </p>
                <p>
                    {{ obj.fos_show }}
                </p>
                <hr>
                <p class="text-sm">
                    {{ obj.abstract }}
                </p>
            </div>
        </div>
    {% endfor %}
    <!-- 分页 -->
    <div style="margin-top:10px">
        <!--extra=request.GET.urlencode 可以保证分页的时候带上其他的request的参数 -->
        {% bootstrap_pagination page_obj extra=request.GET.urlencode %}
    </div>

{% endif %}

{% endblock %}
```

# 相关资源

- Django相关资源大集合. https://github.com/wsvincent/awesome-django#ecommerce
- Django博客. https://github.com/liangliangyy/DjangoBlog
- 非常好看的Admin后台. https://github.com/geex-arts/django-jet
- django-bootstrap-modal-forms. https://github.com/trco/django-bootstrap-modal-forms
- Django packages. https://djangopackages.org/
