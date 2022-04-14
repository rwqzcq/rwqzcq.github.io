import pandas as pd
import numpy as np
import os
import pandas as pd
import networkx as nx
from cdlib import algorithms, evaluation, readwrite
from utils import *
from tqdm import tqdm

base_dir = './cdlib_data/'

class ComEva():
    def __init__(self, network_id):
        com_path = os.path.join(base_dir, 'comminities', f'{network_id}.csv')
        network_path = os.path.join(base_dir, 'network', f'{network_id}.csv')

# 加载网络
network_id = 2806687306
df = pd.read_csv(f'./cdlib_data/networks/{network_id}.csv', header=None)
df.columns = ['src', 'dst']
print(df.shape)
df = df.drop_duplicates()
print(df.shape)

# 做映射
nodes = set(df['src'].tolist()) | set(df['dst'].tolist())
nodes_id_map = {v:index for index, v in enumerate(nodes)}

df['src_idx'] = df['src'].map(nodes_id_map)
df['dst_idx'] = df['dst'].map(nodes_id_map)

# 生成图
G = nx.Graph()
G.add_nodes_from(df['src_idx'].tolist())
G.add_nodes_from(df['dst_idx'].tolist())
G.add_edges_from(df[['src_idx', 'dst_idx']].values.tolist())

overlapping_algorithms = [
    'aslpaw', 'angel', 'big_clam', 'coach',
     'core_expansion', 'danmf', 'dcs',
    'demon', 'dpclus', 'ebgc', 'ego_networks', 
    'egonet_splitter', 'graph_entropy', 'ipca', 'lais2', 
    'lpam', 'lpanni', 'lfm', 
    'multicom',  'mnmf', 'nnsed', 'node_perception',
    'overlapping_seed_set_expansion', 'umstmo', 'percomvc', 'slpa', 
    'symmnmf', 'walkscan', 'wCommunity'
]

true_com_obj = readwrite.read_community_csv(f'./cdlib_data/communities/{network_id}.csv', ',', int)
true_com_obj.graph = G
true_com = true_com_obj.communities
true_com_idx = []
for item in true_com:
    item = [nodes_id_map[i] for i in item]
    true_com_idx.append(item)
true_com_obj.communities = true_com_idx

params = {
    'angel': dict(threshold=0.1),
    'conga': dict(number_communities=len(true_com_obj.communities)),
    'congo': dict(number_communities=len(true_com_obj.communities)),
    'demon': dict(epsilon=0.1),
    'lemon': dict(seeds=[1]),
    'lfm': dict(alpha=0.8),
    'multicom': dict(seed_node=0),
    'node_perception': dict(threshold=0.1, overlap_threshold=0.1),
    'overlapping_seed_set_expansion': dict(seeds=list(nodes_id_map.values())),
}

new_elist = ['nf1', 'f1', 'overlapping_normalized_mutual_information_LFK','overlapping_normalized_mutual_information_MGH']
metric_data = []
for method in tqdm(overlapping_algorithms):
    print(method)
    kwargs = {}
    if method in params:
        kwargs = params[method]
    G_ = G.copy()
    pred_com_obj = methodFactory(method, G_, kwargs)
    eva_results = []
    for eval_m in new_elist:
        eva_result = eval(f'evaluation.{eval_m}(pred_com_obj, true_com_obj)')
        eva_score = round(eva_result.score, 4)
        eva_score = str(eva_score)
        eva_results.append(eva_score)
    metric_data.append(eva_results)
    
