import pandas as pd
import seaborn as sns

df = pd.read_csv(r'E:\\work\\sh\\inputs.csv')
df['date_time'] = pd.to_datetime(df['date_time'])
# 打开“inputs.csv”筛选出2019年全年，type=DAID的数据
daid_2019 = df[(df['type'] == 'DAID') & (df['date_time'].dt.year == 2019)]

# 检查数据是否有缺失值
print(df.isnull().any())

# 是否每半小时都有数据 并用上一时刻的值补齐数据
date_df = df.groupby(['settlement_date', 'type']).count()['date_time'].to_frame()
missing_df = date_df[date_df['date_time'] != 48]
print(missing_df)
append_dfs = []
for index in missing_df.index:
    date = index[0]
    type = index[1]
    item = df[(df['settlement_date'] == date) & (df['type'] == type)]
    last = item.tail(1)
    diff_num = 48 - item.shape[0] # 缺失的行数
    appends = []
    for i in range(1, diff_num + 1):
        row = last.copy()
        row['settlement_period'] = last['settlement_period'] + i
        row['date_time'] = row['date_time'] + pd.Timedelta(f'{30*i} minute')
        appends.append(row)
    append_df = pd.concat(appends)
    append_dfs.append(append_df)
append_df = pd.concat(append_dfs)
df = pd.concat([df, append_df])
df = df.sort_values(by=['settlement_date', 'type', 'settlement_period', 'date_time'])

# 做一些简单的visualization，分析2019年DAID的走势（任何角度都可以，并配合简单的语言解释）
# daid_2019 = None

# 月份总和来看
daid_2019['month'] = daid_2019['date_time'].apply(lambda x:x.date().month)
data = daid_2019.groupby(['month']).sum('value')['value'].to_frame()
sns.lineplot(data=data, x='month', y='value')

# 月份最大值
daid_2019['month'] = daid_2019['date_time'].apply(lambda x:x.date().month)
data = daid_2019.groupby(['month']).max('value')['value'].to_frame()
sns.lineplot(data=data, x='month', y='value')

# 季度总和来看
def get_season(month):
    if 1<=month<=3:
        return 1
    if 4<=month<=6:
        return 2
    if 7<=month<=9:
        return 3
    if 10<=month<=12:
        return 4
daid_2019['season'] = daid_2019['month'].apply(get_season)
data = daid_2019.groupby(['season']).sum('value')['value'].to_frame()
sns.lineplot(data=data, x='season', y='value')

# 季度最大值看来
data = daid_2019.groupby(['season']).max('value')['value'].to_frame()
sns.lineplot(data=data, x='season', y='value')