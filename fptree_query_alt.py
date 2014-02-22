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


fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data
MIN_SPT = 0.3
trans_count = len(dataset)

frequent_itemsets = CL.defaultdict(int)
unique_items = header_table.keys()





class Route:
	__slots__ = ['node', 'path']
	def __init__(self, node, path):
		self.node = node
		self.path = CL.deque(path)

	def __repr__(self):
		return "node: {0}  path: {1}".format(self.node, self.path)





#----- top level: iterating over unique transaction items ------#

# initialize the route:
r1 = Route()
for k in header_table.keys():
	# update the route:
	r1k = update_route(r1, k)
	# calculate conditional pattern bases:
	x = get_cpbs(r1k, header_table)
	if not x:
		# persist frequent itemsets & 'continue', ie break out of this loop &
		# go to next key in header_table.keys()
		persist(r1k, header_table, sort_key=FPT.sort_key)
		print("recursion path terminated; frequent itemsets persisted")
		continue
	else:
		cpb_all, f_list = x
		print("continue recursion")
		for k in f_list.keys():
			# build fptree from conditional pattern bases:
			cfptree, cheader_table = build_fptree(cpb_all, len(cpb_all), min_spt, k)
			# update the route:
			r2k = update_route(r1k, k)
			# get conditional pattern bases of new conditional fptree:
			x = get_cpbs(r2k, cheader_table)
			if not x:
				persist(r2k, sort_key=FPT.sort_key)
				print("recursion path terminated AND frequent itemsets persisted")
			else:
				cpb_all, f_list = x
				print("continue recursion")



def get_cpbs(k, trans_count=len(dataset), min_spt=MIN_SPT, header_table=FPT.htab):
	def is_empty(alist):
		if len(alist) == 0:
			return True
	cpb_all = get_conditional_pattern_bases(k, header_table=FPT.htab)
	if is_empty(cpb_all):
		return None
	else:
		f_list = create_flist(cpb_all=cpb_all, min_spt=MIN_SPT, trans_count=trans_count)
		cpb_all = sort_cpb_by_freq(cpb_all)
		cpb_all = deepcopy(list(cpb_all))
		return cpb_all, f_list


def mine_tree(p=[], f_list=FPT.htab, c=0):
	for k in f_list.keys():
		p1 = deepcopy(p)
		print('{0:>{1}}'.format(path, c))
		x = get_cpbs(r1, header_table)
		if not x:
			print(persist(r1, f_list, sort_key=FPT.sort_key))
			continue
		else:
			cpb_all, f_list = x
			cfptree, cheader_table = build_fptree(cpb_all, len(cpb_all),
				min_spt, k)
			p.append(k)
			mine_tree(p, f_list, c=c+5)




#------------------ latest iteration ---------#

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

def mine_tree(p=CL.deque([]), header_table=FPT.htab, min_spt=MIN_SPT, trans_count=len(dataset),
              c=0, f_list=FPT.htab):
    for k in f_list.keys():
        p1 = deepcopy(p)
        p1.appendleft(k)
        q = ''.join(p1)
        x = cpbs(k, header_table, MIN_SPT, trans_count)
        if len(q) > 1:
            fis = q + str(header_table[k][0])
            # print('fis: {}: {}'.format(q, f_list[k]))
            FIS.append(fis)
        if x:
            cpb_all_, f_list_ = x
            q = ''.join(p1)
            print('path: {}'.format(q))
            # print('f_list {}'.format(f_list))
            if len(q) > 1:
                fis = q + str(header_table[k][0])
                print('fis: {}: {}'.format(q, f_list[k]))
            cfptree, chtab = build_fptree(cpb_all_, len(cpb_all_), MIN_SPT, k)
            mine_tree(p=p1, header_table=chtab, min_spt=MIN_SPT, trans_count=trans_count,
                      c=c+5, f_list=f_list_)
        elif not x:
            q = ''.join(p1)
            if len(q) > 1:
                fis = q + str(header_table[k][0])
                print('fis: {}: {}'.format(q, header_table[k][0]))
                FIS.append(fis)
            # q1 = q[1:]
            # fis = q1
            # if len(fis) > 1:
                # print('fis: {}: '.format(q1))
                # FIS.append(fis)
            # k = 'key: ' + k
            print("\n")
            continue