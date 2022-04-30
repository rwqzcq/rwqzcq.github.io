# 1. 建立tables

```python

```class InfoTable(tables.Table):
    """
    定义Modeltable
    https://django-tables2.readthedocs.io/en/latest/pages/table-data.html#table-data
    """
    class Meta:
        model = HealthInfo # 指定模型
        attrs = {"class": "table table-striped"} # 自定义属性
```
# 2. views中使用

```python
def my_info(request):
    """
    个人信息填报
    """
    qs = HealthInfo.objects.filter(user=request.user)
    table = InfoTable(qs)

    return render(request, 'health/my_info.html', {'table': table})
```

# 3. 模板中使用

```html
{% load render_table from django_tables2 %}
<h4>我的填报</h4>
<div>
    {% render_table table %}
</div>
```

# 4. 自定义字段

```python
from django_tables2 import tables
from django_tables2.utils import A

detail = tables.columns.LinkColumn('detail', args=[A('pk')], orderable=False, empty_values=(), verbose_name='操作')

def render_detail(self):
        return '查看详情'
```

# 5. 显示图片

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

