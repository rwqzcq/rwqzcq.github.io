# 1. 建立modelForm

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

# 2. views中使用-添加数据

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

# 3. template中加载form

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

