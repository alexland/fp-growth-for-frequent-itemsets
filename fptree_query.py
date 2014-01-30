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
		inserts original element(s) back into itemset, sorts by alpha,
		then stringifies
		"""
		item_set.extend(item)
		item_set.sort()
		return ''.join(item_set)
	fis = deepcopy(cpb_all)
	for item_set, cnt in fis:
		frequent_itemsets[fnx(item_set, item)] += cnt
	return None


def build_conditional_fptree(cpb_all, min_spt, item):
	"""
	returns: conditional fptree & header table
	pass in:
	"""
	len_cpbs = len(list(cpb_all))
	cfptree, cheader_table = FPT.build_fptree(dataset=cpb_all,
		trans_count=len_cpbs, min_spt=min_spt, root_node_name=item)
	return cfptree, cheader_table


def find_frequent_itemsets(item, fptree, min_spt, trans_count,
	header_table=FPT.htab):
	"""
	returns:
	pass in:
	"""
	cpb_all = FQU.get_conditional_pattern_bases(item[0], header_table)
	if cpb_all == []:
		return None
	else:
		f_list = FQU.p_create_flist(cpb_all)
		cpb_all = FQU.filter_cpb_by_flist(cpb_all, f_list)
		persist_frequent_itemsets(item, cpb_all, frequent_itemsets)
		cpb_all = FQU.sort_cpb_by_freq(cpb_all)
		# if max(map(len, cpb_all)) > 1:
		if len(f_list.items()) > 1:
			cpb_all = deepcopy(list(cpb_all))
			cfptree, cheader_table = build_conditional_fptree(cpb_all,
				min_spt, item)
			for k in cheader_table.keys():
				item += k
				item = item[::-1]
				return find_frequent_itemsets(item, cfptree, min_spt,
					len(list(cpb_all)), header_table=cheader_table)
		else:
			return None


# item = 'E'
fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data0
min_spt = 0.3
trans_count = len(dataset)

frequent_itemsets = CL.defaultdict(int)

p_find_frequent_itemsets = partial(find_frequent_itemsets,
	min_spt=min_spt, trans_count=len(dataset))


unique_transaction_items = list(header_table.keys())

for item in unique_transaction_items:
	find_frequent_itemsets(item, fptree, min_spt, trans_count)

