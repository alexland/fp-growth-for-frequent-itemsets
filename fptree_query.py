#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import collections as CL
from functools import partial
import fptree as FPT
import fptree_query_utils as FQU


frequent_itemsets = CL.defaultdict(int)

S = []

#------------------ recursively find frequent itemsets  --------------------#

# call build_conditional_fptree, once for each unique item in htab.keys(),
# then if cfptree has more than one node in it:
# repeat the mining loop; else: exit

def prep_persist(route, sort_key=FPT.sort_key):
	"""
	returns: frequent itemset as a string
	pass in: instance of Class Route
	"""
	fnx = lambda q: sorted(q, key=sort_key.__getitem__)
	route.prefix.append(route.node)
	root = route.prefix.popleft()
	freq_itemset = fnx(list(route.prefix))
	freq_itemset.append(root)
	return ''.join(freq_itemset)


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
	freq_itemset = prep_persist(route)
	if cpb_all == []:
		frequent_itemsets[freq_itemset] = route.count
		return None
	else:
		fis = deepcopy(cpb_all)
		for item_set in fis:
			item_set = ''.join(fnx(freq_itemset))
			frequent_itemsets[freq_itemset] += 1

class Route:
	__slots__ = ['prefix_path', 'count']
	def __init__(self, prefix_path, count):
		self.prefix_path = CL.deque(prefix_path)
		self.count = count


S = []

def find_frequent_itemsets(route, fptree, trans_count, min_spt=FPT.MIN_SPT, header_table=FPT.htab):
	"""
	returns: None, recursive fn that populates frequent_itemsets (dict)
	pass in:
		(i) 	instance of the class Route, instantiated by calling
				the constructor and passing in a 3-tuple:
				(node/item, count, prefix); node + prefix = complete route
		(ii)	fptree or conditional fptree
		(iii) 	minimum support (fixed)
		(iv)  	length of dataset
		(v) 	header table for fptree or conditional fptree
	"""
	for k, v in header_table.items():
		route.prefix_path.appendleft(k)
		route.count = v[0]
		# print(route.node)
		# print(route.prefix)
		cpb_all = FQU.get_conditional_pattern_bases(k, header_table)
		f_list = FQU.p_create_flist(cpb_all)
		cpb_all = FQU.filter_cpb_by_flist(cpb_all, f_list)
		cpb_all = FQU.sort_cpb_by_freq(cpb_all)
		cpb_all = deepcopy(list(cpb_all))
		if cpb_all == []:
			print( "{0}\t{1}".format(route.prefix_path, route.count) )

		else:
			cfptree, cheader_table = FPT.build_fptree(cpb_all, len(cpb_all),
				min_spt, k)
			find_frequent_itemsets(route, cfptree, len(cpb_all), min_spt,
				cheader_table)





		# print(cpb_all)
		# if (cpb_all == []) | (len(f_list) == 1):
		# 	print(prep_persist(route))

		# 	persist_frequent_itemsets(route, cpb_all, frequent_itemsets)
		# else:
		# 	cfptree, cheader_table = FPT.build_fptree(cpb_all, len(cpb_all),
		# 		min_spt, route.node)
		# 	find_frequent_itemsets(route, cfptree, len(cpb_all), min_spt, cheader_table)

#print( "node: {0} \t count: {1} \t prefix: {2}".format(route.node,
				#route.count, route.prefix) )


# item = 'E'
fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data0
MIN_SPT = 0.3
trans_count = len(dataset)

frequent_itemsets = CL.defaultdict(int)



find_frequent_itemsets(
						Route([], 0),
						fptree,
						trans_count,
						min_spt=MIN_SPT,
						header_table=FPT.htab
						)
