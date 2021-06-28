# encoding=utf-8
import pickle as pkl
import pandas as pd
import os.path as op
from sklearn import cluster
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA # 降维
from matplotlib import pyplot as plt
import seaborn as sns


input_data_path = r'E:\work\gae\data'
output_path = r'E:\work\gae\data'
dataset = 'DIP'

# 加载向量
with open(op.join(input_data_path, f'{dataset}_Z.pkl'), 'rb') as fp:
    Z = pkl.load(fp)

# 加载训练数据
with open(op.join(input_data_path, f'{dataset}_train_datas.pkl'), 'rb') as fp:
    train_datas = pkl.load(fp)

# 对不同时刻进行聚类
time_index = 0
for z, train_data in zip(Z, train_datas):
    df = pd.DataFrame(data=z)
    df['node'] = list(train_data['nodes_name_map'].values())
    # 聚类
    x = df.values[:, 0:-1]
    n_clutsers = 3 # 聚类个数为3
    km = KMeans(n_clusters=n_clutsers, max_iter=1000).fit(x)
    # 降维
    pca = PCA(n_components=2)
    x_ = pca.fit_transform(x)
    # 保存数据
    cluster_df = pd.DataFrame(data=x_, columns=['x', 'y'])
    cluster_df['label'] = km.labels_
    cluster_df['node'] = df['node']
    # 画散点图
    title=f'Time-{time_index}'
    fig = sns.scatterplot(x='x', y='y', hue='label', data=cluster_df)
    fig.set_title(title)
    plot = fig.get_figure()
    plot.savefig(op.join(output_path, f'{dataset}_{time_index}.png'), dpi=300)
    plot.clf() # 清除
    cluster_df.to_csv(op.join(output_path, f'{dataset}_{time_index}_聚类结果.csv'), index=False)
    time_index += 1
    # distortions = []
    # for i in range(1, 20):
    #     km = KMeans(n_clusters=i, max_iter=1000).fit(x)
    #     distortions.append(km.inertia_)
    # plt.plot(range(1,20), distortions, marker='o')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Distortion')
    # plt.show()
    # break

    
    
