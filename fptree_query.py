#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import collections as CL
from functools import partial
import fptree as FPT
import fptree_query_utils as FQU


frequent_itemsets = []


def count_frequent_itemsets(frequent_itemsets):
	"""
	returns:
	pass in:
	"""
	cx = CL.defaultdict(int)
	for s in frequent_itemsets:
		cx[s] += 1
	return cx

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
	fnx = lambda g: ''.join(g)
	fis = deepcopy(cpb_all)
	for item_set in fis:
		item_set.append(item)
		item_set = fnx(item_set)
		frequent_itemsets.append(item_set)
	return None


def find_frequent_itemsets(item, fptree, dataset, min_spt, trans_count, header_table=FPT.htab):
    cpb_all = FQU.get_conditional_pattern_bases(item, header_table)
    f_list = FQU.create_flist(dataset, cpb_all, min_spt)
    cpb_all = FQU.filter_cpbs_by_flist(cpb_all, f_list)
    persist_frequent_itemsets(item, cpb_all, frequent_itemsets)
    cpb_all = FQU.sort_cpbs_by_freq(cpb_all, dataset)
    return frequent_itemsets


item = 'C'
fptree = FPT.fptree
dataset = FPT.data0
min_spt = 0.3
trans_count = len(dataset)

p_find_frequent_itemsets = partial(find_frequent_itemsets,
	min_spt=min_spt, trans_count=len(dataset))




unique_transaction_items = list(FPT.htab.keys())

for item in unique_transaction_items:
	p_find_frequent_itemsets(item, fptree, dataset)


FIS = frequent_itemsets
header_table FPT.htab
