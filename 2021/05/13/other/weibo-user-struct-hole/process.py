# encoding=utf-8
import jieba
import jieba.analyse
import pandas as pd
import os
from tqdm import tqdm
import itertools
import networkx as nx

# 读取数据
input_base_dir = r'E:\\work\\weibo-struct-hole'
output_base_dir = r'E:\\work\\weibo-struct-hole'

df_path = os.path.join(input_base_dir, 'weibo.csv')
df = pd.read_csv(df_path, encoding='GBK')
df = df[['名字', '题目']]
df = df.dropna() # 去除空的

# 建立作者ID-映射
authors = {name: index for index, name in enumerate(df['名字'].unique())}
df['author_id'] = df['名字'].apply(lambda name: authors[name])

# 提取关键词并构造关键词-作者映射
contents = df['题目']
all_keywords_set = set()
keywords_author = {}
for i in tqdm(df.values):
    author = i[2]
    c = i[1]
    keywords = jieba.analyse.extract_tags(c, 5)
    keywords = [k for k in keywords if len(k) >= 2] # TODO stopwords
    for k in keywords:
        if keywords_author.get(k, '-1') == '-1':
            keywords_author[k] = set([author])
        else:
            keywords_author[k].add(author)

# 构造网络
edges_weight = {

}
G = nx.Graph()
for k, a_s in tqdm(keywords_author.items()):
    a_s = list(a_s)
    #edges = itertools.combinations(a_s, 2)
    edges = itertools.permutations(a_s, 2)
    # for (i, j) in edges:
    #     G.add_edge(i, j)
    e0 = [f'{i}#{j}' for i, j in edges]
    #e1 = [f'{j}-{i}' for i, j in edges]
    for e in e0:
        if edges_weight.get(e, 0) == 0:
            edges_weight[e] = 1
        else:
            edges_weight[e] = edges_weight[e] + 1

for e, w in edges_weight.items():
    try:
        src, dst = e.split('#')
        G.add_edge(src, dst, weight=w)  
    except:
        print(e)
    

# 保存网络
import pickle as pkl
with open(os.path.join(output_base_dir, 'garph.pkl'), 'wb') as wp:
    pkl.dump(G, wp)

# 生成Gephi
nx.write_gexf(G, os.path.join(output_base_dir, 'garph.gexf'))

# 生成pajek
# https://blog.csdn.net/qysh123/article/details/77506427
nx.write_pajek(G, os.path.join(output_base_dir, 'garph.net'))

print('生成网络: ok')

# pagerank
pr = nx.pagerank(G, alpha=0.85)
authors_map = {v: k for k, v in authors.items()}
pr = [[authors_map[int(k)], v] for k, v in pr.items()]
pr_df = pd.DataFrame(data=pr, columns=['作者', 'pr值'])
pr_df = pr_df.sort_values(by=['pr值'], ascending=False)
pr_df.to_csv(os.path.join(output_base_dir, '作者重要性.csv'), index=False, encoding='UTF-8')

print('pagerank: ok')

# 结构洞
constraint = nx.constraint(G)
constraint = [[authors_map[int(k)], v] for k, v in constraint.items()]
constraint_df = pd.DataFrame(data=constraint, columns=['作者', 'constraint值'])
constraint_df = constraint_df.sort_values(by=['constraint值'], ascending=False)
constraint_df.to_csv(os.path.join(output_base_dir, '结构洞-constraint.csv'), index=False, encoding='UTF-8')

# eff = nx.effective_size(G)
# eff = [[authors_map[int(k)], v] for k, v in eff.items()]
# eff_df = pd.DataFrame(data=eff, columns=['作者', 'effective_size值'])
# eff_df = eff_df.sort_values(by=['effective_size值'], ascending=False)
# eff_df.to_csv(os.path.join(output_base_dir, '结构洞-effective_size.csv'), index=False, encoding='UTF-8')

print('结构洞: ok')

# https://blog.csdn.net/banshao5453/article/details/101770966
# https://networkx.org/documentation/stable/reference/algorithms/structuralholes.html?highlight=struct%20hole


