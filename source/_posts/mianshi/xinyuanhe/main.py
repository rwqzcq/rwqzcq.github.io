import pandas as pd
import os
from matplotlib import pyplot as plt
import seaborn as sns

def clean(filename):
    """
    定义一个python方程将邮件里面的raw.xlsx清理并转化成sample.xlsx的格式，表头与sample一致，
    清理规则如下：
        - 删除types为空并移除
        - 剔除明显outlier
    """
    base_dir = r'e:\\work\\心盒笔试\\'
    filename = os.path.join(base_dir, filename)

    raw_df = pd.read_excel(filename, header=0)
    raw_df = raw_df.dropna(subset=['types'])

    raw_df['types'] = raw_df['types'].apply(lambda x: x.strip().split(' '))
    raw_df = raw_df.explode('types')
    raw_df[['comment_type', 'comment_value']] = raw_df.apply(lambda x: x['types'].split(':'), axis=1, result_type="expand")

    sample_df = pd.read_excel(os.path.join(base_dir, 'sample.xlsx'), header=0)
    raw_df = raw_df[sample_df.columns]
    raw_df['receive_time'] = pd.to_datetime(raw_df['receive_time'])
    raw_df['comment_time'] = pd.to_datetime(raw_df['comment_time'])
    raw_df = raw_df.sort_values(by=['userid', 'commodityid', 'wishid', 'receive_time', 'comment_time'])

    # 找到离群点
    print(raw_df['receive_time'].describe())
    print(raw_df['comment_time'].describe())
    raw_df = raw_df[raw_df['receive_time'].dt.year > 1970]

    # 日期格式化
    raw_df['receive_time'] = raw_df['receive_time'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M"))
    raw_df['comment_time'] = raw_df['comment_time'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M"))
    
    raw_df.to_excel(os.path.join(base_dir, 'sample.xlsx'), index=False)
    print('column_names: ', list(raw_df.columns))

def getTimeDifference(df):
    """
    2. 利用commodity = 52的数据进行以下分析：
        - 定义一个方程计算receive_time和comment_time的时间差(以天计算)，并在原表生成新的列，列名为`time_difference`
    """
    df = df[df['commodityid'] == 52]
    df['time_difference'] = df.apply(lambda x: (x['comment_time'] - x['receive_time']).days, axis=1)
    return df

def makePlot(df):
    """
    - 将数据可视化，生成两个图表
        - 定义一个方程用柱状图展示每一个time_difference的count
        - 定义一个方程用comment_time生成曲线图，x轴为日期，颗粒度为天，y轴为每一个日期的count
    """
    td_df = df.groupby(df['time_difference']).count()['userid'].to_frame()
    td_df.columns = ['time_difference']
    td_df.plot(kind='bar')
    plt.show()

    plf.clf()
    df['comment_time'] = df['comment_time'].apply(lambda x: x.date())
    ct_df = df.groupby(df['comment_time']).count()['userid'].to_frame()
    ct_df.columns = ['comment_time']
    ct_df.plot(kind='bar')
    plt.show()

def part3():
    """
    意愿
    """
    base_dir = r'e:\\work\\心盒笔试\\'
    df = pd.read_excel(os.path.join(base_dir, 'sample.xlsx'))
    df = df[df['comment_type'] == '意愿']
    df['time_difference'] = df.apply(lambda x: (x['comment_time'] - x['receive_time']).days, axis=1)
    df = df[['time_difference', 'comment_value']]

if __name__ == '__main__':
    clean(filename='raw.xlsx')
    base_dir = r'e:\\work\\心盒笔试\\'
    filename = 'raw.xlsx'
    filename = os.path.join(base_dir, filename)
    raw_df = pd.read_excel(filename, header=0)
    raw_df = raw_df.dropna(subset=['types'])
    raw_df['receive_time'] = pd.to_datetime(raw_df['receive_time'])
    raw_df['comment_time'] = pd.to_datetime(raw_df['comment_time'])
    raw_df = raw_df[raw_df['receive_time'].dt.year > 1970]
    raw_df = getTimeDifference(raw_df)

