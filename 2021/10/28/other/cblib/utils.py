import networkx as nx
from cdlib import algorithms


def methodFactory(method, G, kwargs={}):
    com = None
    if method == 'aslpaw':
        com = algorithms.aslpaw(G, **kwargs)
    if method == 'angel':
        com = algorithms.angel(G, **kwargs)
    if method == 'big_clam':
        com = algorithms.big_clam(G, **kwargs)
    if method == 'coach':
        com = algorithms.coach(G, **kwargs)
    if method == 'conga':
        # number_communities必须写
        com = algorithms.conga(G, **kwargs)
    if method == 'congo':
        # number_communities必须写
        com = algorithms.conga(G, **kwargs)
    if method == 'core_expansion':
        com = algorithms.core_expansion(G, **kwargs)
    if method == 'danmf':
        com = algorithms.danmf(G, **kwargs)
    if method == 'dcs':
        com = algorithms.dcs(G, **kwargs)
    if method == 'demon':
        # epsilon 必须
        com = algorithms.demon(G, **kwargs)
    if method == 'dpclus':
        com = algorithms.dpclus(G, **kwargs)
    if method == 'ebgc':
        com = algorithms.ebgc(nx.convert_node_labels_to_integers(G), **kwargs)
    if method == 'ego_networks':
        com = algorithms.ego_networks(G, **kwargs)
    if method == 'egonet_splitter':
        com = algorithms.egonet_splitter(G, **kwargs)
    if method == 'graph_entropy':
        com = algorithms.graph_entropy(G , **kwargs)
    if method == 'ipca':
        com = algorithms.ipca(G , **kwargs)
    if method == 'lais2':
        com = algorithms.lais2(G , **kwargs)
    if method == 'lemon':
        com = algorithms.lemon(G , **kwargs)
    if method == 'lpam':
        com = algorithms.lpam(G, **kwargs)
    if method == 'lpanni':
        com = algorithms.lpanni(G, **kwargs)
    if method == 'multicom':
        com = algorithms.multicom(G, **kwargs)
    if method == 'mnmf':
        com = algorithms.mnmf(G, **kwargs)
    if method == 'nnsed':
        com = algorithms.nnsed(G, **kwargs)
    if method == 'node_perception':
        com = algorithms.node_perception(G, **kwargs)
    if method == 'overlapping_seed_set_expansion':
        com = algorithms.overlapping_seed_set_expansion(G, **kwargs)
    if method == 'umstmo':
        com = algorithms.umstmo(G, **kwargs)
    if method == 'percomvc':
        com = algorithms.percomvc(G, **kwargs)
    if method == 'slpa':
        com = algorithms.slpa(G, **kwargs)
    if method == 'symmnmf':
        com = algorithms.symmnmf(G, **kwargs)
    if method == 'walkscan':
        com = algorithms.walkscan(G, **kwargs)
    if method == 'wCommunity':
        nx.set_edge_attributes(G, values=1, name='weight')
        com = algorithms.wCommunity(G, **kwargs)
    if method == 'lfm':
        com = algorithms.lfm(G, **kwargs)
    return com