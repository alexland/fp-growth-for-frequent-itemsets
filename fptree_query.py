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
# repeat the mining loop; ELSE: exit

def persist_frequent_itemsets(item, cpb_all, frequent_itemsets):
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
	def fnx(item_set, item=item):
		"""
		inserts original element back into itemset then stringy
		"""
		item_set.append(item)
		item_set.sort()
		return ''.join(item_set)
	fis = deepcopy(cpb_all)
	for item_set, cnt in fis:
		frequent_itemsets[fnx(item_set)] += cnt
	return None


def find_frequent_itemsets(item, fptree, dataset, min_spt, trans_count, header_table=FPT.htab):
    cpb_all = FQU.get_conditional_pattern_bases(item, header_table)
    if cpb_all == []:
    	return None
    f_list = FQU.create_flist(dataset, cpb_all, min_spt)
    cpb_all = FQU.filter_cpb_by_flist(cpb_all, f_list)
    persist_frequent_itemsets(item, cpb_all, frequent_itemsets)
    cpb_all = FQU.sort_cpb_by_freq(cpb_all, dataset)
    return None


def build_conditional_fptree(cpb_all, min_spt, item):
	"""
	returns: conditional fptree & header table
	pass in:
	"""
	len_cpbs = len(list(cpb_all))
	return build_fptree(dataset=cpb_all, trans_count=len_cpbs, min_spt=min_spt,
		root_node_name=item)


all_items = ['D', 'E', 'B', 'C', 'A']
correct_items = ['C']

# item = 'B'
fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data0
min_spt = 0.3
trans_count = len(dataset)

p_find_frequent_itemsets = partial(find_frequent_itemsets,
	min_spt=min_spt, trans_count=len(dataset))

unique_transaction_items = list(FPT.htab.keys())

frequent_itemsets = CL.defaultdict(int)

for item in unique_transaction_items:
	p_find_frequent_itemsets(item, fptree, dataset)


build_conditional_fptree(cpb_all, min_spt, item)

