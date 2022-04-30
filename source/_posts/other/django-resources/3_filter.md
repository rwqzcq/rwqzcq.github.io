# 1. 定义

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

# 2. views中使用

```python
f = BoothFilter(request.GET, queryset=qs)
return render(request, 'booth/search.html', {'filter': f})
```

# 3. 模板中使用

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

