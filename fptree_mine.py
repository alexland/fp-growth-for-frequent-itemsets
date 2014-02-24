#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import collections as CL
import itertools as IT
import functools as FT
from functools import partial
from functools import wraps

import fptree as FPT



def flatten(nested_seq, ignore_seq=(str, bytes)):
	"""
	flattens a nested sequence
	"""
	import collections as CL
	for itm in nested_seq:
		if isinstance(itm, CL.Iterable) and not isinstance(itm, ignore_seq):
			yield from flatten(itm)
		else:
			yield itm


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
		if len(route) > 2:
			cnt = route[0].count
			cpb = route[1:-1][::-1]
			cpb_all.append((list(map(fnx, cpb)), cnt))
	return cpb_all


def create_flist(cpb_all, trans_count, min_spt):
	"""
	returns: f-list, a dict whose keys are the items comprising the
		  conditional pattern bases & whose values are the frequency
		  of the nodes ('count' attr) in the conditional fptree;
		  items in the f-list are filtered against min_spt before returned
	pass in:
		(i) conditional pattern bases for a given unique item in the
			transacdtions, this nested list is the value returned
			from calling get_conditional_pattern_bases
		(ii) min_spt
	"""
	import math
	min_spt_ct = math.ceil(min_spt * trans_count)
	cpb_all_expanded = [(route * count) for route, count in cpb_all]
	cpb_all_expanded = list(flatten(cpb_all_expanded))
	ic = FPT.item_counter(cpb_all_expanded)
	# filter by min_spt translated to actual count, abs_ms
	return {k:v for k,v in ic.items() if v >= min_spt_ct}


def filter_cpb_by_flist(cpb_all, f_list):
	"""
	returns:
	pass in:
	"""
	fnx = lambda q: q in list(f_list.keys())
	return [ (list(filter(fnx, cpb)), cnt) for cpb, cnt in cpb_all ]


def sort_cpb_by_freq(cpb_all):
	"""
	returns: generator obj (call 'list' to recover conditional pattern bases)
		 (list of lists) each list re-orderdered by item frequency
		 from original dataset
	pass in:
		(i) filtered conditional pattern bases (list of lists),
			returned from call to filterd_cpbs_by_flist
		(ii) original dataset
	"""
	# expand each [cpb, count]
	cpb_all = [ list(IT.repeat(cpb, cnt)) for cpb, cnt in cpb_all ]
	# flatten one level
	cpb_all = [itm for inlist in cpb_all for itm in inlist]
	return FPT.c_reorder_items(cpb_all)


#------------------ recursively find frequent itemsets  --------------------#

# call build_conditional_fptree, once for each unique item in htab.keys(),
# then if cfptree has more than one node in it:
# repeat the mining loop; else: exit

FIS = []
fis = []


def sort_fis(path_str, sort_key=FPT.SORT_KEY):
	fnx = lambda q: sorted(q, key=sort_key.__getitem__)
	return ''.join(fnx(list(path_str)))


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


def cpbs(k, header_table, min_spt=FPT.MIN_SPT, trans_count=FPT.TRANS_COUNT):
	cpb_all = FQU.get_conditional_pattern_bases(k, header_table=header_table)
	if len(cpb_all) == 0:
		return None
	else:
		f_list = FQU.create_flist(cpb_all, min_spt, trans_count)
		cpb_all = FQU.filter_cpb_by_flist(cpb_all, f_list)
		cpb_all = FQU.sort_cpb_by_freq(cpb_all)
		cpb_all = deepcopy(list(cpb_all))
	return cpb_all, f_list


def mine_tree(p=CL.deque([]), header_table=FPT.htab, min_spt=FPT.MIN_SPT, trans_count=len(FPT.dataset), c=0, f_list=FPT.htab, debug=1):
	for k in f_list.keys():
		p1 = deepcopy(p)
		p1.appendleft(k)
		q = ''.join(p1)
		x = cpbs(k, header_table, min_spt, trans_count)
		if x:
			cpb_all_, f_list_ = x
			q = ''.join(p1)
			if debug:
				print('path: {}'.format(q))
			if len(q) > 1:
				fis = q + ':' + str(header_table[k][0])
				if debug:
					print('fis: {}: {}'.format(q, f_list[k]))
				FIS.append(fis)
			cfptree, chtab = FPT.build_fptree(cpb_all_, len(cpb_all_),
				min_spt, k)
			mine_tree(p=p1, header_table=chtab, min_spt=min_spt,
				trans_count=trans_count, f_list=f_list_)
		elif not x:
			q = ''.join(p1)
			if len(q) > 1:
				fis = q + ':' + str(header_table[k][0])
				if debug:
					print('fis: {}: {}'.format(q, header_table[k][0]))
				FIS.append(fis)
			continue


def create_fis_containers(FIS):
	""""
	returns: two containers that store the same data, all freq
		itemsets for a given dataset, nested list of freq itemsets
		is returned then a dict where each key is a fis, value is
		count
	pass in: sequence of all frequent itemsets, each fis is
		a string of the form fis:count, eg, 'xyz:99'
	"""
	fis_all = [itm.strip().split(':') for itm in FIS]
	fis =  [list(t[0]) for t in fis_all]
	fis_cnt = {k:v for k, v in fis_all}
	return fis, fis_cnt
