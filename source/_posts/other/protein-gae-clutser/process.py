# encoding=utf-8
import pandas as pd
import os
import networkx as nx
import torch
from torch_geometric.utils import convert
import pickle as pkl

input_data_path = r'E:\work\gae\data'
output_path = r'E:\work\gae\data'
dataset = 'DIP'

# 找到所有的节点
nodes_path = os.path.join(input_data_path, f'{dataset}_PPIs_protein_set.txt')
all_nodes = set()
with open(nodes_path, encoding='utf-8') as fp:
    for line in fp.readlines()[1:]:
        all_nodes.add(line.strip())
nodes_df = pd.DataFrame({'node': list(all_nodes), 'node_id': list(range(0, len(all_nodes)))}) # 编号
print('node_df', nodes_df.shape)

# 找到所有的节点的向量
nodes_vec_path = os.path.join(input_data_path, f'{dataset}_PPIs_protein_ex_3431.txt')
nodes_vec_df = pd.read_csv(nodes_vec_path, sep='\t', header=None, encoding='utf-8')
nodes_vec_df = nodes_vec_df.dropna(axis=1)
print('nodes_vec_df', nodes_vec_df.shape)
# 构造图
G = nx.Graph()
graph_path = os.path.join(input_data_path, f'{dataset}_PPIs.txt')
graph_df = pd.read_csv(graph_path, sep='\t', header=None, encoding='utf-8')
graph_df.columns = ['src', 'dst']
print('graph_df', graph_df.shape)
t_nodes_df = nodes_df.copy()
t_nodes_df.columns = ['src', 'src_node_id']
graph_df = graph_df.merge(t_nodes_df, on='src', how='left')
t_nodes_df = nodes_df.copy()
t_nodes_df.columns = ['dst', 'dst_node_id']
graph_df = graph_df.merge(t_nodes_df, on='dst', how='left')
graph_df = graph_df[['src_node_id', 'dst_node_id']]
graph_df.columns = ['src', 'dst']
print('graph_df', graph_df.shape)
nx_data = graph_df.values.tolist()
G.add_edges_from(nx_data)


# 找到时刻T下面活跃的节点
active_path = os.path.join(input_data_path, f'{dataset}_active_protein_vectors.txt')
active_df = pd.read_csv(active_path, header=None, sep=' ', encoding='UTF-8')
active_df = active_df.dropna(axis=1)

# 构造12张图
train_datas = []
for index in range(12):
    t = active_df.loc[index] # 0时刻
    del_nodes = t.where(t < 1).dropna().index.tolist()
    print('del nodes', len(del_nodes))
    TG = G.copy()
    TG.remove_nodes_from(del_nodes)
    # 从0开始编号
    nodes = list(TG.nodes)
    print(len(nodes), len(TG.edges))
    nodes_map = {n:i for i, n in enumerate(nodes)}
    x = torch.tensor(nodes_vec_df.loc[nodes, ].values, dtype=torch.float32)
    edges = list(TG.edges)
    edges = [[nodes_map[s], nodes_map[d]] for s, d in edges]
    del TG
    TG = nx.Graph()
    TG.add_nodes_from(list(nodes_map.values()))
    TG.add_edges_from(edges)
    print(len(edges))
    print(len(TG.nodes), len(TG.edges))
    # 转化成pytorch_geometric的data
    pg_data = convert.from_networkx(TG)
    pg_data.x = x
    pg_data.num_nodes_features = x.size()[1] # 数据的维度
    pg_data.edge_index = pg_data.edge_index.long()
    pg_data.train_pos_edge_index = pg_data.edge_index
    print(pg_data.num_nodes)
    print(x.size())
    assert x.size(0) == pg_data.num_nodes
    item = {
        'nodes_name_map': {index: nodes_df.loc[node_id, 'node'] for node_id, index in nodes_map.items()},
        'nodes_map': nodes_map, # 保存每一个节点的映射
        'pg_data': pg_data  # 保存的训练用的data
    }
    train_datas.append(item)

# 保存数据
with open(os.path.join(output_path, f'{dataset}_train_datas.pkl'), 'wb') as wp:
    pkl.dump(train_datas, wp)