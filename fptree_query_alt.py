#!/usr/bin/env python3
# encoding: utf-8


import itertools as IT
from copy import deepcopy
import collections as CL
ddir = "/Users/dougybarbo/Projects/fp-growth-for-frequent-itemsets"
import os
os.chdir(ddir)

%run fptree
%run fptree_query_utils
%run fptree_query

route = Route('', '', '', 0)

fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data0
MIN_SPT = 0.3
trans_count = len(dataset)

k = 'A'
route.prefix_path.appendleft(route.root)
route.root = route.node
route.node = k
route.count = header_table[k][0]

# print(route)

S = []

def persist(route, sort_key=FPT.sort_key):
    fnx = lambda q: sorted(q, key=sort_key.__getitem__)
    freq_itemset = route.node + ''.join(route.prefix_path) + route.root
    freq = route.count
    return {freq_itemset: freq}

def update_route(route, f_list, k):
    route.prefix_path.appendleft(route.root)
    route.root = route.node
    route.node = k
    route.count = f_list[k]

def get_cpbs(route, header_table):
    cpb_all = get_conditional_pattern_bases(route.node, header_table=FPT.htab)
    f_list = p_create_flist(cpb_all)
    cpb_all = filter_cpb_by_flist(cpb_all, f_list)
    cpb_all = sort_cpb_by_freq(cpb_all)
    cpb_all = deepcopy(list(cpb_all))
    if cpb_all == []:
        print(persist(route))
    else:
        cfptree, cheader_table = FPT.build_fptree(cpb_all, len(cpb_all), min_spt, route.node)
        # for k in cheader_table.keys():
            # update_route(route, f_list, k)
            # cpb_all, f_list = get_cpbs(route, cheader_table)

cpb_all, f_list = get_cpbs(route, header_table)