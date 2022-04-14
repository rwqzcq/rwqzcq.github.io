---
title: 就业信息爬取与分析
date: 2022-01-10 13:32:31
tags:
 - 其他
categories:
 - 其他
---

# 爬虫

数据源为`51job`，通过指定的城市代码与岗位名称来构造请求的url，核心的构造url的代码如下:

```python
city_config = {
    'shenzhen': '040000',
    'guangzhou': '030200'
}
city = ''
def gen_url(self, i=1):
    """
    生成待爬虫的Url
    params: i为页码
    """
    self.url = f'https://search.51job.com/list/{self.city_config[self.city]},000000,0000,00,9,99,' + self.keyword + ",2," + str(i) + ".html"
```

爬取的就业信息存储到JSON文件中，核心代码如下:
```python
def write_json(self, data):
    """写入文件"""
    path = self.data_dir + f'/{self.keyword}_{self.city}_{time.time()}.json'
    with open(path, 'w', encoding='UTF-8') as wp:
        json.dump(data, wp, ensure_ascii=False)
```
数据格式如下所示:
```JSON
{
    "type": "engine_jds",
    "jt": "0_0",
    "tags": [],
    "ad_track": "",
    "jobid": "98192508",
    "coid": "4865021",
    "effect": "1",
    "is_special_job": "",
    "job_href": "https://jobs.51job.com/guangzhou-hpq/98192508.html?s=sou_sou_soulb&t=0_0",
    "job_name": "Python全栈开发",
    "job_title": "Python全栈开发",
    "company_href": "https://jobs.51job.com/all/co4865021.html",
    "company_name": "广东珺桦能源科技有限公司",
    "providesalary_text": "0.6-1.2万/月",
    "workarea": "030206",
    "workarea_text": "广州-黄埔区",
    "updatedate": "12-24",
    "iscommunicate": "",
    "companytype_text": "民营公司",
    "degreefrom": "6",
    "workyear": "4",
    "issuedate": "2021-12-24 09:05:24",
    "isFromXyz": "",
    "isIntern": "",
    "jobwelf": "五险一金 员工旅游 绩效奖金 年终奖金 定期体检 餐饮补贴",
    "jobwelf_list": [
        "五险一金",
        "员工旅游",
        "绩效奖金",
        "年终奖金",
        "定期体检",
        "餐饮补贴"
    ],
    "isdiffcity": "",
    "attribute_text": [
        "广州-黄埔区",
        "2年经验",
        "本科",
        "招2人"
    ],
    "companysize_text": "少于50人",
    "companyind_text": "电气/电力/水利",
    "adid": ""
}
```

# 算法

## 决策树

使用决策树进行薪资的预测，本研究将薪资预测转化成一个`回归任务`，即根据一系列的`特征`来取预测具体的`薪资`。其中选择的特征主要包括：

- 城市
- 公司类型
- 公司规模
- 学历
- 工作年限
- 福利待遇
- 工作经验
主要涉及的工作为对针对这些特征进行预处理->转化成向量->数据切分->决策树模型训练
其核心的代码如下图所示:

```python
from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor()
regressor.fit(X_train, y_train)
```

其中反映模型拟合度的图如下所示：

![模型拟合度](0_decision_tree_pred.png)

## Aprori

使用关联规则来挖掘企业用人单位对于薪资、岗位要求、福利待遇的相似点，通过选择一系列特征数据来构造数据集，如下所示：

```txt
[['薪资: 0.8万-1.0万', '深圳-南山区', '无需经验', '大专', '招2人', '民营公司'],
 ['薪资: 2.5万-3.0万',
  '深圳-福田区',
  '5-7年经验',
  '本科',
  '招1人',
  '民营公司',
  '150-500人',
  '五险一金'],
 ['薪资: 2.5万-5.0万',
  '深圳-南山区',
  '5-7年经验',
  '本科',
  '招1人',
  '上市公司',
  '500-1000人',
  '五险一金',
  '员工旅游',
  '年终奖金',
  '定期体检'],
 ['薪资: 2.5万-3.0万',
  '深圳',
  '3-4年经验',
  '本科',
  '招1人',
  '民营公司',
  '50-150人',
  '五险一金',
  '年终奖金',
  '绩效奖金',
  '年底双薪',
  '交通补贴',
  '餐饮补贴',
  '股票期权',
  '员工旅游'],
```

然后设置关联规则的`最小支持度`以及`置信度`可以得到频繁项集，如下图所示：

![频繁项集](1_频繁项集.png)

最后的关联规则如下图所示:

![关联规则](2_关联规则.png)

可以看到的是:

> 薪资在`1万到1.5万之间`的学历要求均为`本科`，同时需要`1年经验`，在福利待遇上面，都会提供`绩效奖金`与`五险一金`。

核心代码如下:

```python
te = TransactionEncoder()
te_ary = te.fit(train_data).transform(train_data)
train_df = pd.DataFrame(te_ary,columns=te.columns_)
frequent_itemsets = apriori(train_df,min_support=0.01,use_colnames=True)
association_rule = association_rules(frequent_itemsets,metric='confidence',min_threshold=0.95)	# metric可以有很多的度量选项，返回的表列名都可以作为参数
association_rule.sort_values(by='leverage',ascending=False,inplace=True)    #关联规则可以按leverage排序
```

# Django可视化展示

```python

# settings.py
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['薪资统计', '工作经验要求统计', '学历统计', '公司类型统计', '福利统计', '岗位要求统计'],      # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True, 
    'menus': [
        {
            'name': '薪资统计',
            'icon': 'fa fa-chart-bar',
            'url': '/bar/?type=salary'
        },
        {
            'name': '工作经验要求统计',
            'icon': 'fa fa-chart-pie',
            'url': '/bar/?type=avg_exp'
        },
        {
            'name': '学历统计',
            'icon': 'fa fa-chart-pie',
            'url': '/bar/?type=degree'
        },
        {
            'name': '公司类型统计',
            'icon': 'fa fa-chart-pie',
            'url': '/bar/?type=companytype_text'
        },
        {
            'name': '福利统计',
            'icon': 'fa fa-chart-bar',
            'url': '/wordcloud/?type=welf'
        },
        {
            'name': '岗位要求统计',
            'icon': 'fa fa-chart-bar',
            'url': '/wordcloud/?type=attribute'
        }
    ]
}

# views.py

from django.shortcuts import render
from mysite.settings import BASE_DIR
import json
import pandas as pd

# Create your views here.
data_df = pd.read_csv(BASE_DIR / 'app' / 'train_data.csv')
# 薪资
def process_salary(salary):
    if salary < 0.5:
        return '<0.5万'
    if 0.5 <= salary < 1.0:
        return '0.5万-1万'
    if 1.0 <= salary < 1.5:
        return '1万-1.5万'
    if 1.5 <= salary <= 2:
        return '1.5万-2万'
    if 2 <= salary < 2.5:
        return '2万-2.5万'
    if 2.5 <= salary < 3:
        return '2.5万-3万'
    if 3 < salary:
        return '>3万'
data_df['salary'] = data_df['mean_y'].apply(process_salary)

# 工作经验
def process_exp(exp):
    if exp == 0:
        return '无经验要求'
    return f'{int(exp)}年经验'
data_df['avg_exp'] = data_df['avg_exp'].apply(process_exp)

def group_count(key):
    """
    分组统计
    """
    return data_df[key].groupby(data_df[key]).count().to_frame().to_dict()[key]

def bar_plot(request):
    """
    
    """
    _type = request.GET.get('type', '')
    template = 'bar.html'

    if _type == '':
        key = 'salary'
        title = '薪资范围统计'
    else:
        key = _type

    data = group_count(key)

    if _type == 'salary': # 薪资统计
        title = '薪资范围统计'
        template = 'bar.html'
    elif _type == 'degree':
        title = '学历要求统计'
        template = 'pie.html'
    elif _type == 'companytype_text':
        title = '公司类型统计'
        template = 'pie.html'
    elif _type == 'avg_exp':
        title = '工作经验要求统计'
        template = 'pie.html'

    
    x = list(data.keys())
    y = list(data.values())
    x = json.dumps(x, ensure_ascii=False)
    y = json.dumps(y, ensure_ascii=False)

    return render(request, f'app/{template}', {'x': x, 'y': y, 'title': title})

orignal_data_df = pd.read_csv(BASE_DIR / 'app/data.csv')
welfs = []
attributes = []
for _, row in orignal_data_df.iterrows():
    try:
        attributes += eval(row["attribute_text"])
    except:
        continue
    try:
        welfs += row['jobwelf'].split(' ')
    except:
        continue

from collections import Counter
welfs = dict(Counter(welfs).most_common())
welfs = [{"name": k, "value": v} for k, v in welfs.items()]

attributes = dict(Counter(attributes).most_common())
attributes = [{"name": k, "value": v} for k, v in attributes.items()]

def word_cloud(request):
    """
    词云图
    """
    _type = request.GET.get('type', '')
    if _type == 'welf':
        data = welfs
    elif _type == 'attribute':
        data = attributes
    else:
        data = welfs
        
    data = json.dumps(data, ensure_ascii=False)
    return render(request, 'app/wordcloud.html', {'data': data})

```

<!-- 
# 参考链接

1. mlxtend文档. http://rasbt.github.io/mlxtend/api_subpackages/mlxtend.frequent_patterns/
2. 利用mlxtend进行数据关联分析. https://blog.csdn.net/qq_36523839/article/details/83960195
3. 

-->

