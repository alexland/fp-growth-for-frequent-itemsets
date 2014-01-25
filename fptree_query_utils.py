#!/usr/bin/env python3
# encoding: utf-8

"""
steps to query fp-tree:

	for a given item (any atomic element comprising the transactions):

		(i) 	get conditional pattern bases
		(ii) 	get F-list (filtered against min spt)
		(iii)	sort each cpb by item frequency
		(v) 	build conditional fp-tree
		(vi)	place results in container for fast, intuitive retrieval

"""

# TODO: *** refactor 'create_flist' so that it returns res filtered by min spt
# TODO: if 2 items have same freq, sort by alpha/numeric order
# TODO: eliminate the "sort header table" from mineTree
# TODO: to exemplary queries below, add frequency (refactor mineTree)
# TODO: refactor variable names: distinguish: 'item' to itemset and 'item to item
# TODO: add frequency to 'frequent_items' so i can sort the results
# TODO: get rid of 'min_spt' in place of something more appropriate
# TODO: fix f-list calculation (use htab for counts)
# TODO: fix 'get_conditional_pattern_bases' so count also returned is flag set to True
# TODO: need to collect frequent itemsets during recursive cfptree building

data0 = [
	['B', 'E', 'B', 'D', 'A'],
	['E', 'A', 'D', 'C', 'B'],
	['C', 'E', 'B', 'A'],
	['A', 'B', 'D'],
	['D'],
	['D', 'B'],
	['D', 'A', 'E'],
	['B', 'C'],
]


import itertools as IT
import collections as CL
from functools import wraps

import fptree as FPT
# import exception_handling as EX



def like_item_traversal(item, header_table=FPT.htab):
	"""
	returned: dict of pointers to node objects having the same
		'name' attribute as 'item' keys are the node's name attribute w/
		incremented integer appended (to ensure unique), values are the
		node pointers that correspond to that node
	pass in:
		(i) str/int representation of a given unique transaction item
		(ii) header table (from fptree built from original transaction data)
	"""
	linked_nodes = {}
	keys = []
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(item, next(c))
	node = header_table[item][-1]
	while node != None:
		linked_nodes[fnx(item)] = node
		node = node.node_link
	return linked_nodes


def flatten(nested_seq, ignore_seq=(str, bytes)):
	import collections as CL
	for itm in nested_seq:
		if isinstance(itm, CL.Iterable) and not isinstance(itm, ignore_seq):
			yield from flatten(itm)
		else:
			yield itm


def ascend_route(node, string_repr=False):
	"""
	returns: all nodes in a given route from the node passed in
		to the root
	pass in: a single node in an fp-tree
	note: setting 'string_repr to True will return 'node.name' attribute
		rather than the node pointer itself
	"""
	node_route = []
	while node != None:
		if string_repr:
			node_route.append(node.name)
		else:
			node_route.append(node)
		node = node.parent
	return node_route


def get_conditional_pattern_bases(item, header_table=FPT.htab):
	"""
	returns: a list of tuples, each tuple comprised of a conditional pattern base
	(node route) and the count for that cpb
	pass in:
		(i) str/int representation of a given unique transaction item
		(ii) header table
	this fn transforms a raw 'route' from 'ascend_tree' into a cpb in 2
		steps:
			(i) remove start & terminus
			(ii) reverse the order of the items
	'string_repr' flag should be set to 'False', *except*
	for use in de-bugging, unit test, etc.

	"""
	cpb_all = []
	fnx = lambda n: n.name
	linked_nodes = like_item_traversal(item, header_table)
	for node in linked_nodes.values():
		route = ascend_route(node, string_repr=False)
		cnt = route[0].count
		cpb = route[1:-1][::-1]
		cpb_all.append((list(map(fnx, cpb)), cnt))
	return cpb_all


def create_flist(dataset, cpb_all, min_spt):
	"""
	returns: f-list, a dict whose keys are the items comprising the
		  conditional pattern bases & whose values are the frequency
		  of the nodes ('count' attr) in the conditional fptree;
		  items in the f-list are filtered against min_spt before returned
	pass in:
		(i) original dataset
		(ii) conditional pattern bases for a given unique item in the
			transacdtions, this nested list is the value returned
			from calling get_conditional_pattern_bases
		(iii) min_spt
	"""
	import math
	min_spt = math.ceil(min_spt * len(dataset))
	cpb_all_expanded = [(route * count) for route, count in cpb_all]
	# restore string representation of nodes?
	ic = FPT.item_counter(cpb_all_expanded)
	# now filter by min spt
	# translate mnin_spt to actual count (eg, 3)
	return {k:v for k,v in ic.items() if v >= min_spt}


def filter_cpbs_by_flist(cpb_all, f_list):
	"""
	returns:
	pass in:
	"""
	fnx = lambda q: q in list(f_list.keys())
	return [ list(filter(fnx, cpb[0])) for cpb in cpb_all ]


def sort_cpbs_by_freq(cpb_all, dataset):
	"""
	returns: generator obj (call 'list' to recover conditional pattern bases)
		 (list of lists) each list re-orderdered by item frequency
		 from original dataset
	pass in:
		(i) filtered conditional pattern bases (list of lists),
			returned from call to filterd_cpbs_by_flist
		(ii) original dataset
	"""
	return FPT.reorder_items(cpb_all, sort_key=FPT.get_sort_key(dataset))


def build_conditional_fptree(dataset, item, min_spt, trans_count,
	header_table=FPT.htab):
	"""
	thin wrapper over 'build_fptree'
	"""
	cpb_all_filtered, _ = filter_cpbs_by_flist(item, min_spt, trans_count, header_table)
	cpb_all_filtered_sorted = sort_cpbs_by_freq(cpb_all_filtered, dataset)
	cfptree, htab = FPT.build_fptree(cpb_all_filtered_sorted, trans_count, min_spt, root_node_name=item)
	return cfptree, htab



# returns a conditional fptree for unique item 'C'
# the usable result needs to return something like ([C, B], 3)
#cfptree_c = build_conditional_fptree(data0, 'C', 0.3, len(data0))


# returns a conditional fptree for unique item 'E'
# cfptree_e = build_conditional_fptree(data0, 'E', 0.3, len(data0))

# frequent_itemsets = []

min_spt = 0.3
item = 'C'

cpb_all = get_conditional_pattern_bases(item, FPT.htab)
f_list = create_flist(data0, cpb_all, min_spt)
cpb_all_filtered = filter_cpbs_by_flist(cpb_all, f_list)
cpb_all_filtered_sorted = sort_cpbs_by_freq(cpb_all_filtered, data0)
cpb_all = cpb_all_filtered_sorted
# frequent_itemsets.append(cpb_all_filtered)



# cpb_all_filtered_sorted = sort_cpbs_by_freq(cpb_all, data0)

# cfptree, _ = FPT.build_fptree(list(cpb_all_filtered_sorted), len(data0), 0.3, 'E')
