#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import collections as CL
from functools import partial
import fptree as FPT
import fptree_query_utils as FQU


frequent_itemsets = CL.defaultdict(int)

#------------------ recursively find frequent itemsets  --------------------#

# call build_conditional_fptree, once for each unique item in htab.keys(),
# then if cfptree has more than one node in it:
# repeat the mining loop; ELSE: exit

def persist_frequent_itemsets(route, cpb_all, frequent_itemsets,
	sort_key=FPT.sort_key):
	"""
	returns: None, populates frequent itemset container with
		filtered conditional pattern bases, to which the
		original transaction element (route start) is first appended,
		then pattern base is converted from list to string
	pass in:
		(i) unique transaction item
		(ii) filtered conditional pattern bases (returned from
			filter_cpbs_by_flist)
		(ii) container storing all frequent itemsets
	"""
	fnx = lambda q: sorted(q, key=sort_key.__getitem__)
	freq_itemset = list(route.item + route.prefix)
	freq_itemset = ''.join(fnx(freq_itemset))

	if cpb_all == []:
		frequent_itemsets[freq_itemset] = route.count
		return None
	else:
		fis = deepcopy(cpb_all)
		for item_set in fis:
			item_set = ''.join(fnx(freq_itemset))
			frequent_itemsets[freq_itemset] += 1

class Route:
	__slots__ = ['node', 'count', 'prefix']
	def __init__(self, node, count, prefix):
		self.node = node
		self.count = count
		self.prefix = prefix

def find_frequent_itemsets(route_tpl, fptree, min_spt=MIN_SPT, trans_count,
	header_table=FPT.htab):
	"""
	returns: None, recursive fn that populates a dict, frequent_itemsets
	pass in:
		(i) 	instance of the class Route, instantiated by calling
				the constructor and passing in a 3-tuple:
				(item, count, route)
		(ii)	fptree or conditional fptree
		(iii) 	minimum support (fixed)
		(iv)  	length of dataset
		(v) 	header table for fptree or conditional fptree
	"""
	cpb_all = FQU.get_conditional_pattern_bases(route.node, header_table)
	f_list = FQU.p_create_flist(cpb_all)
	cpb_all = FQU.filter_cpb_by_flist(cpb_all, f_list)
	cpb_all = FQU.sort_cpb_by_freq(cpb_all)
	cpb_all = deepcopy(list(cpb_all))
	if cpb_all == []:
		persist_frequent_itemsets(route, cpb_all, frequent_itemsets)
	else:
		tc = len(cpb_all)
		cfptree, cheader_table = FPT.build_fptree(cpb_all, tc, min_spt, route.node)
		if len(cheader_table) == 1:
			persist_frequent_itemsets(route, cpb_all, frequent_itemsets)
		else:
			print(f_list)
			for k, v in f_list.items():
				route.prefix += k
				find_frequent_itemsets(route, cfptree, MIN_SPT, tc, cheader_table)



# item = 'E'
fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data0
MIN_SPT = 0.3
trans_count = len(dataset)

frequent_itemsets = CL.defaultdict(int)

p_find_frequent_itemsets = partial(find_frequent_itemsets,
	min_spt=MIN_SPT, trans_count=len(dataset))


def mine_fptree(unique_transaction_items=list(header_table.keys()),
	fptree=fptree, min_spt=MIN_SPT, trans_count=trans_count):
	"""
	returns:
	pass in:
	"""
	for item in unique_transaction_items:
		find_frequent_itemsets(item, fptree, min_spt=MIN_SPT, trans_count)


unique_transaction_items=list(header_table.keys())

for item in unique_transaction_items:
	route = Route(item, 0, '')
	find_frequent_itemsets(route, fptree, min_spt=MIN_SPT, trans_count)

# find_frequent_itemsets('E', fptree, MIN_SPT, trans_count)