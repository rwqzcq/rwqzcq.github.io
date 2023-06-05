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
df = df.drop_duplicates()
df.to_csv('boss_游戏公司岗位汇总.csv', index=False)
