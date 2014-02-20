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

def persist(route, header_table, sort_key=FPT.sort_key):
    fnx = lambda q: sorted(q, key=sort_key.__getitem__)
    freq_itemset = route.node + ''.join(list(route.path))
    freq = header_table[route.node]
    return {freq_itemset: freq}

def update_route(route, k):
    new_route = Route('', '')
    new_route.path.appendleft(route.node)
    new_route.node = k
    return new_route

# def get_cpbs(route, header_table=FPT.htab):
# 	cpb_all = get_conditional_pattern_bases(route.node, header_table=FPT.htab)
# 	f_list = p_create_flist(cpb_all)
# 	cpb_all = filter_cpb_by_flist(cpb_all, f_list)
# 	cpb_all = sort_cpb_by_freq(cpb_all)
# 	cpb_all = deepcopy(list(cpb_all))
# 	if cpb_all == []:
# 		print(persist(route))
# 		return None
# 	else:
# 		cpb_all, f_list
# 		for k in f_list.keys():
# 			cfptree, cheader_table = build_fptree(cpb_all, len(cpb_all), min_spt,
# 				route.node)
# 			udpate_route()
# 			return get_cpbs(route, cheader_table)

#----------------#

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


def mine_tree(route=Route(), f_list=FPT.htab):
	for k in f_list.keys():
		r1 = update_route(route, k)
		print(r1)
		x = get_cpbs(r1, header_table)
		if not x:
			print(persist(r1, f_list, sort_key=FPT.sort_key))
			continue
		else:
			cpb_all, f_list = x
			cfptree, cheader_table = build_fptree(cpb_all, len(cpb_all),
				min_spt, k)
			mine_tree(route=r1, f_list)




# updating the route (using example of 'A'):
	# begin at top level
	# loop initialized for its context (loop)
	r_init = Route('', '', '', 0)
	k = 'A'					#  a unique transaction item
	rA = update_route(route_init, k)

		# next level
		# init set to route's val when exit enclosing loop
		r_init = rA
		for k in f_list.keys():
			# loops twice once for 'B', once for 'D', but
			rAB = update_route(rA, 'B', f_list)
