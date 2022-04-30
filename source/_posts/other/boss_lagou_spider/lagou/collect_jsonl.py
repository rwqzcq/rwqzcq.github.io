import os
import json
import pandas as pd
from tqdm import tqdm

data = []
for file in tqdm(os.listdir('./')):
    if file.find('.jsonl') > 0:
        with open(file) as fp:
            for line in fp:
                try:
                    item = json.loads(line.strip())
                    data.append(item)
                except:
                    print(line)
df = pd.DataFrame(data=data)
selected_columns = ['positionName', 'companyShortName', 'city', 'salary', 'salaryMonth', 'workYear']
df = df[selected_columns]
df.to_csv('拉钩_游戏公司岗位汇总.csv', index=False)
