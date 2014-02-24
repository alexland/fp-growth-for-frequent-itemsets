#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import collections as CL
from functools import partial

import fptree as FPT
import fptree_query_utils as FQU


#------------------ recursively find frequent itemsets  --------------------#

# call build_conditional_fptree, once for each unique item in htab.keys(),
# then if cfptree has more than one node in it:
# repeat the mining loop; else: exit

FP = []


def gather_nodes(node, N=[]):
    nx = node.children
    if len(nx) == 0:
        return N
    else:
        for n in nx.keys():
            N.append(n)
            gather_nodes(node.children[n], N)
    return N


def persist_freq_patterns(path, f_list):
    k = ''.join(path)
    q = path[-1]
    v = f_list[q]
    return {k:v}


def cpbs(k, header_table, MIN_SPT, trans_count):
	cpb_all = get_conditional_pattern_bases(k, header_table=header_table)
	if len(cpb_all) == 0:
		return None
	else:
		f_list = create_flist(cpb_all=cpb_all, min_spt=MIN_SPT,trans_count=trans_count)
		cpb_all = filter_cpb_by_flist(cpb_all, f_list)
		cpb_all = sort_cpb_by_freq(cpb_all)
		cpb_all = deepcopy(list(cpb_all))
	return cpb_all, f_list

FIS = []



def mine_tree(p=CL.deque([]), header_table=FPT.htab, min_spt=FPT.MIN_SPT, trans_count=len(FPT.dataset),
              c=0, f_list=FPT.htab):
    for k in f_list.keys():
        p1 = deepcopy(p)
        p1.appendleft(k)
        q = ''.join(p1)
        x = cpbs(k, header_table, MIN_SPT, trans_count)
        if x:
            cpb_all_, f_list_ = x
            q = ''.join(p1)
            print('path: {}'.format(q))
            if len(q) > 1:
                fis = q + ':' + str(header_table[k][0])
                print('fis: {}: {}'.format(q, f_list[k]))
                FIS.append(fis)
            cfptree, chtab = build_fptree(cpb_all_, len(cpb_all_), MIN_SPT, k)
            mine_tree(p=p1, header_table=chtab, min_spt=MIN_SPT, trans_count=trans_count,
                      c=c+5, f_list=f_list_)
        elif not x:
            q = ''.join(p1)
            if len(q) > 1:
                fis = q + ':' + str(header_table[k][0])
                print('fis: {}: {}'.format(q, header_table[k][0]))
                FIS.append(fis)
            continue