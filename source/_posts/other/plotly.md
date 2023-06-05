---
title: python动态可视化图-plotly
date: 2021-05-27 11:37:53
tags:
 - 其他
categories:
 - 其他
---

# 热力图/混淆矩阵

参考链接: https://plotly.com/python/heatmaps/

```python
import pandas as pd
import plotly.express as px

df = None
# 探求变量之间的相关性
data = pd.crosstab(cor_df['工作经验'], cor_df['薪资'])
plot = px.imshow(data)
return HttpResponse(plot.to_html())
```

# 地图

```python
# 最大经纬度
MAX_LON = 120.52
MIN_LON = 122.12
MAX_LAT = 31.53
MIN_LAT = 30.40

CEN_LON = 121.48
CEN_LAT = 31.22

PLOTLY_TOKEN = 'pk.eyJ1IjoiYmxhY2tzaGVlcHdhbGwwMzA1IiwiYSI6ImNrMHo5ZnQxYjBjbG8zbm84b3hrb25vb24ifQ.K8tcDjJDsPcjdYFTSVgTxw'
# pk.eyJ1IjoiYmxhY2tzaGVlcHdhbGwwMzA1IiwiYSI6ImNrMHo5ZnQxYjBjb

import plotly.express as px
import plotly.graph_objects as go
# from mysite.settings import PLOTLY_TOKEN, CEN_LON, CEN_LAT
from .models import Car

def one_car_plot(x, y, car: Car):
    """
    一辆车停放位置
    参考链接: https://zhuanlan.zhihu.com/p/87163211
    """
    hovertext = str(car)
    fig = go.Figure(go.Scattermapbox(mode='markers',
                                    lon=[x],
                                    lat=[y],
                                    hovertext=hovertext,
                                    hoverinfo='text',
                                    marker = dict(color='yellow', size=12)
                                ))

    fig.update_layout(mapbox = {'accesstoken': PLOTLY_TOKEN,
                                # 'style':'satellite',
                                'center': {'lon': CEN_LON, 'lat': CEN_LAT}, 
                                'zoom': 10,
                            },
                    margin = {'l': 0, 'r': 0, 't': 0, 'b': 0})
    return fig

def multi_cars_plot(xs, ys, car: Car):
    """
    一辆车停放位置
    参考链接: https://zhuanlan.zhihu.com/p/87163211
    """
    hovertext = str(car)
    fig = go.Figure(go.Scattermapbox(mode='markers',
                                    lon=xs,
                                    lat=ys,
                                    hovertext=hovertext,
                                    hoverinfo='text',
                                    marker = dict(color='red', size=5)
                                ))

    fig.update_layout(mapbox = {'accesstoken': PLOTLY_TOKEN,
                                # 'style':'satellite',
                                'center': {'lon': CEN_LON, 'lat': CEN_LAT}, 
                                'zoom': 10,
                            },
                    margin = {'l': 0, 'r': 0, 't': 0, 'b': 0})
    return fig
```

