#!/usr/bin/env python3
# encoding: utf-8

import fptree_query_utils as FPTU


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


def find_frequent_itemsets(fptree, header_table=FPT.htab, frequent_itemsets=[]):
	"""
	returns: None, recursively builds conditional fptrees, mines
		them for frequent item sets then adds them to frequent_itemsets
	pass in:
	"""
	# get unique transaction items & select 1 to begin with


	# mine tree for frequent itemsets
	cpb_all = get_conditional_pattern_bases()

	f_list = create_flist(dataset, cpb_all, min_spt)


	# add filtered conditional pattern bases to a temp container
	fis = count_frequent_itemsets(cpb_all_filtered)
	frequent_itemsets.append(fis)

	# examine cfptree to determine which case below applies

	# base case:
	return

	# recursive case:
	return find_frequent_itemsets(cfptree, frequent_itemsets=frequent_itemsets)

