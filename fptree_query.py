#!/usr/bin/env python3
# encoding: utf-8

import fptree as FPT
import fptree_query_utils as FQU


# temporary container for frequent itemsets
frequent_itemsets = []


def count_frequent_itemsets(freq_itemsets):
	"""
	returns:
	pass in:
	"""
	fnx = lambda g: ''.join(g)
	tx = map(fnx, freq_itemsets)
	cx = CL.defaultdict(int)
	for s in tx:
		cx[s] += 1
	return cx



#------------------ recursively find frequent itemsets  --------------------#

# call build_conditional_fptree, once for each unique item in htab.keys(),
# then if cfptree has more than one node in it:
# repeat the mining loop; ELSE: exit

def find_frequent_itemsets(item, fptree, dataset, min_spt, trans_count,
	header_table=FPT.htab, frequent_itemsets=[]):
	"""
	returns: None, recursively builds conditional fptrees, mine
		them for frequent item sets then adds them to frequent_itemsets
	pass in:
		(i) empty container (frequent_itemsets)
	"""
	# mine tree for frequent itemsets
	cpb_all = FQU.get_conditional_pattern_bases(item, header_table)
	f_list = FQU.create_flist(dataset, cpb_all, min_spt)
	cpb_all = FQU.filter_cpbs_by_flist(cpb_all, f_list, min_spt, trans_count,
		header_table)
	# add frequent pattern bases to container
		# after the cpbs are filtered but *before* they are re-ordered:
	for fi in cpb_all:
		fi.append(item)
		frequent_itemsets.append(fi)

	cpb_all = FQU.sort_cpbs_by_freq(cpb_all, dataset)
	return frequent_itemsets



# examine cfptree to determine which case below applies

# base case:
# return

# recursive case:
# return find_frequent_itemsets(cfptree, frequent_itemsets=frequent_itemsets)


unique_transaction_items = list(FPT.htab.keys())

item = 'E'
min_spt = 0.3
header_table = FPT.htab
dataset = FPT.data0
trans_count = len(dataset)

cpb_all = FQU.cpb_all
f_list = FQU.f_list
cpb_all_filtered = FQU.cpb_all_filtered
cpb_all_filtered_sorted = FQU.cpb_all_filtered_sorted

# find_frequent_itemsets('E', FPT.fptree, dataset, min_spt, trans_count, FPT.htab)

# for t in unique_transaction_items:
# 	find_frequent_itemsets()

# add filtered conditional pattern bases to a temp container
	# count_frequent_itemsets(cpb_all_filtered)