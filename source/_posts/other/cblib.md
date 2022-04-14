---
title: 社区重叠算法包cdlib
date: 2021-10-28 19:43:49
tags:
 - 其他
categories:
 - 其他
---

# 安装

需要`python3.8`。

```shell
brew install libomp
pip install cdlib
```

# 算法运行

## ASLPAW

报错：

```shell
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
/var/folders/cf/_jypt9xj1v5gcwgkt_92l0700000gn/T/ipykernel_41399/3731462195.py in <module>
      1 for oa in overlapping_algorithms:
----> 2     pred_com_obj = eval(f'algorithms.{oa}(G)')

<string> in <module>

~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/cdlib/algorithms/overlapping_partition.py in aslpaw(g_original)
   1221 
   1222     if ASLPAw is None:
-> 1223         raise ModuleNotFoundError(
   1224             "Optional dependency not satisfied: install gmpy (conda install gmpy2) and ASLPAw (pip install shuffle_graph>=2.1.0 similarity-index-of-label-graph>=2.0.1 ASLPAw>=2.1.0). If using a notebook, you need also to restart your runtime/kernel."
   1225         )

ModuleNotFoundError: Optional dependency not satisfied: install gmpy (conda install gmpy2) and ASLPAw (pip install shuffle_graph>=2.1.0 similarity-index-of-label-graph>=2.0.1 ASLPAw>=2.1.0). If using a notebook, you need also to restart your runtime/kernel.
```

解决:

```shell
brew install gmp
brew install libmpc
pip install gmpy2
pip install shuffle_graph similarity-index-of-label-graph ASLPAw
```

## ebgc

```shell
---------------------------------------------------------------------------
NetworkXUnfeasible                        Traceback (most recent call last)
~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/networkx/relabel.py in _relabel_inplace(G, mapping)
    134         try:
--> 135             nodes = reversed(list(nx.topological_sort(D)))
    136         except nx.NetworkXUnfeasible as e:

~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/networkx/algorithms/dag.py in topological_sort(G)
    245     """
--> 246     for generation in nx.topological_generations(G):
    247         yield from generation

~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/networkx/algorithms/dag.py in topological_generations(G)
    176     if indegree_map:
--> 177         raise nx.NetworkXUnfeasible(
    178             "Graph contains a cycle or graph changed during iteration"

NetworkXUnfeasible: Graph contains a cycle or graph changed during iteration

The above exception was the direct cause of the following exception:

NetworkXUnfeasible                        Traceback (most recent call last)
/var/folders/cf/_jypt9xj1v5gcwgkt_92l0700000gn/T/ipykernel_45586/1767744134.py in <module>
----> 1 algorithms.ebgc(G) # nx.convert_node_labels_to_integers(G)

~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/cdlib/algorithms/overlapping_partition.py in ebgc(g_original)
   2047     dmap = {n: i for i, n in enumerate(g.nodes)}
   2048     reverse_map = {i: n for n, i in dmap.items()}
-> 2049     nx.relabel_nodes(g, dmap, False)
   2050 
   2051     EBGC_cluster = EBGC()

~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/networkx/relabel.py in relabel_nodes(G, mapping, copy)
    121         return _relabel_copy(G, m)
    122     else:
--> 123         return _relabel_inplace(G, m)
    124 
    125 

~/opt/anaconda3/envs/rjl/lib/python3.8/site-packages/networkx/relabel.py in _relabel_inplace(G, mapping)
    135             nodes = reversed(list(nx.topological_sort(D)))
    136         except nx.NetworkXUnfeasible as e:
--> 137             raise nx.NetworkXUnfeasible(
    138                 "The node label sets are overlapping and no ordering can "
    139                 "resolve the mapping. Use copy=True."

NetworkXUnfeasible: The node label sets are overlapping and no ordering can resolve the mapping. Use copy=True.
```

解决：

```shell
# https://www.osgeo.cn/networkx/_modules/networkx/relabel.html
algorithms.ebgc(nx.convert_node_labels_to_integers(G))
```