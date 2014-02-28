#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import re
from copy import deepcopy
import json as JSON
import collections as CL
from operator import itemgetter
import itertools as IT
import functools as FT
from functools import partial
from functools import wraps



def get_configs(config_fname):
	config_file = os.path.expanduser(config_fname)
	with open(config_file, 'r', encoding='utf-8') as fh:
		return JSON.load(fh)


def load_data(dfile=None, max_transactions=250):
	import random as RND
	if dfile:
		with open(dfile, "r", encoding="utf-8") as fh:
			data = [ line.strip().split(' ') for line in fh.readlines()
				if not line.startswith('#') ]
			RND.shuffle(data)
			data = data[:max_transactions]
	else:
		import string
		import random as RND
		p = list(string.ascii_uppercase[:20])
		fnx = lambda: RND.randint(2, 10)
		data = [ RND.sample(p, fnx()) for c in range(100000) ]
		RND.shuffle(data)
		if max_transactions & max_transactions < len(data):
			return data[:max_transactions]
		else:
			return data



dataset = [
	['B', 'D', 'A', 'E'],
	['B', 'D', 'A', 'E', 'C'],
	['B', 'A', 'E', 'C'],
	['B', 'D', 'A'],
	['D'],
	['B', 'D'],
	['D', 'A', 'E'],
	['B', 'C']
]

MIN_SPT = 0.3
MIN_ITEMSET_LENGTH = 2

configs_filename = "~/Projects/fp-growth-for-frequent-itemsets/config.json"
configs = get_configs(configs_filename)
# MIN_SPT = configs['min_support']
# MIN_ITEMSET_LENGTH = configs['min_itemset_length']
# dataset = load_data()
# dataset = load_data(configs['data_file'])
TRANS_COUNT = len(dataset)



#---------------------- building the fp-tree -----------------------#


def item_counter(dataset):
    """
    returns: a dict whose keys are the unique items comprising the
		transactions & whose values are the integer counts
	pass in: raw data (nested list)
    """
    # flatten the data (from list of sets to list of items)
    trans_flat = [item for trans in dataset for item in trans]
    ic = CL.defaultdict(int)
    for item in trans_flat:
        ic[item] += 1
    return ic


def get_items_below_min_spt(dataset, min_spt, trans_count):
    """
    returns: list of the unique items whose frequency over the
		dataset is below some min_spt (float between 0 and 1,
		('decimal percent')
	pass in:
		(i) dataset (original dataset or conditional pattern bases)
		(ii) min_spt (float, eg, 0.03 means each item must appear in
		    at least 3% of the dataset)
		(iii) number of transactions in dataset or "conditional pattern
			bases"
    """
    item_count = item_counter(dataset)
    ic = {k:v for k, v in item_count.items() if (v/trans_count) < min_spt}
    return list(ic.keys())


def build_min_spt_filter_str(dataset, min_spt, trans_count):
	"""
	returns: a str which, when 'eval' is called on it, is a
		a valid arg for 'IT.filterfalse' which is used in
		'filter_by_min_spt' to remove items below min_spt
	pass in: list of excluded items (returned by
		 'get_items_below_min_spt')
	"""
	excluded_items_expr = []
	str_templ = '(q=="{0}")'
	excluded_items = get_items_below_min_spt(dataset, min_spt, trans_count)
	for item in excluded_items:
	    excluded_items_expr.append(str_templ.format(item))
	return " | ".join(excluded_items_expr)


def filter_by_min_spt(dataset, item_count, min_spt, trans_count):
	"""
	returns:
		(i) filterd dataset (remove items w/ freq < min_spt)
		(ii) filtered item counter
	pass in:
		(i) dataset (the raw dataset)
		(ii) dict w/ items for keys, values are item frequency,
			returned by call to item_counter, for queries this
			is probably an f-list, built by item_counter
		(iii) min_spt (float, eg, 0.03 means each item must appear in
			at least 3% of the dataset)
		(iv) total number of transactions
	removes any item from every transaction if that item's total freq
	is below min_spt
	to call this fn, bind the call to two variables, like so:
	filtered_trans, item_count_dict = filter_by_min_spt(...)
	"""
	excluded_items = get_items_below_min_spt(dataset, min_spt, trans_count)
	if not excluded_items:
		# if all items are above min_spt, ie, there are no items to exclude
		# so just return original args
		return dataset, item_count
	else:
		# there is at least one item to exclude
		# now build the expression required by 'IT.filterfalse' from the
		# list of excluded items
		filter_str = build_min_spt_filter_str(dataset, min_spt, trans_count)
		# remove those items below min_spt threshold items
		tx = [IT.filterfalse(lambda q: eval(filter_str), trans)
				for trans in dataset]
		ic = {k:v for k, v in item_count.items() if (v/trans_count) >= min_spt}
		return list(map(list, tx)), ic


def get_sort_key(dataset):
	"""
	returns: sort key as a dict whose keys are the unique trans
		items and whose values are the sort order for that item
	pass in:
		original dataset only (not conditional pattern bases)
	sorts by decr frequency, then secondary sort by incr. alpha
	t/4, sorts first by secondary key, then by primary key
	"""
	item_count = item_counter(dataset)
	ic = sorted(((k, v) for k, v in item_count.items()), key=itemgetter(0))
	ic = sorted(ic, key=itemgetter(1), reverse=True)
	return {t[0]: i for i, t in enumerate(ic)}


def reorder_items(dataset, sort_key):
	"""
	returns: list of lists sorted by item frequency
	pass in:
		(i) nested list, either original dataset or conditional pattern bases
		(ii) sort_key, (dict) return value from call to 'get_sort_key
	"""
	fnx = lambda q: sorted(q, key=sort_key.__getitem__)
	return map(fnx, dataset)


def config_fptree_builder(dataset, trans_count, min_spt, sort_key):
	"""
	returns: header table & sorted dataset for input to build_tree
		(latter returned as generator)
	pass in:
		(i) raw data (nested list of dataset)
		(ii) transaction count (length of original dataset)
		(iii) sort_key, value returned from call to 'get_sort_key'
		(iv) min_spt (float) fraction of total dataset in which an item
			must appear to be included in the fptree
	"""
	# dataset = [ set(trans) for trans in dataset ]
	item_count = item_counter(dataset)
	dataset, item_count = filter_by_min_spt(dataset, item_count,
		min_spt, trans_count)
	sort_key = get_sort_key(dataset)
	dataset_sorted = reorder_items(dataset, sort_key)
	# build header table from freq_items w/ empty placeholders for node pointer
	htable = CL.defaultdict(list)
	for k in item_count.keys():
	    htable[k].append(item_count[k])
	return htable, dataset_sorted


class TreeNode:

	def __init__(self, node_name, parent_node, node_count=1):
		self.name = node_name
		self.node_link = None
		self.count = node_count
		self.parent = parent_node
		self.children = {}

	def incr(self, freq=1):
		self.count += freq


def add_nodes(trans, header_table, parent_node):
	"""
	pass in:
		a transaction (list),
		header table (dict)
		parent_node (instance of class TreeNode)
	returns: nothing, converts a single transaction to
		nodes in an fp-tree (or increments counts if exists)
		and updates the companion header table
	"""
	while len(trans) > 0:
		item = trans.pop(0)
		# does this item appear in the same route?
		# if so it will have to be upsteam & adjacent given how the items
		# are sorted prior to tree building & given that the fp-tree is
		# built from the top down
		# if item in parent_node.children.keys():
			# parent_node.children[item].incr()
		if item == parent_node.name:
			parent_node.incr()
			add_nodes(trans, header_table, parent_node)

		elif item in parent_node.children:
			parent_node.children[item].incr()
			parent_node = parent_node.children[item]
			add_nodes(trans, header_table, parent_node)

		else:
			# create the node & add it to the tree
			parent_node.children[item] = TreeNode(item, parent_node)
			this_node = parent_node.children[item]
			# now update the node_links in the header table:
			try:
				# is there at least one node pointer for this item
				# in the header table?
				# ie, does this item appear in another route, or
				header_table[item][1]
				# if so:
				header_table[item][-1].node_link = this_node
				header_table[item].append(this_node)
			except IndexError:
				# this is the 1st time this item is seen by this fn
				# ie, no node pointer for this item in h/t, so add it
				header_table[item].append(this_node)
			this_node = parent_node.children[item]
			add_nodes(trans, header_table, this_node)


def build_fptree(dataset, min_spt, trans_count, sort_key, root_node_name="root"):
	"""
	pass in:
		(i) raw data (list of lists; one transcation per list)
		(ii) transaction count in original dataset
		(iii) minimum support (0=<min_spt>1)
		(iv) name of root node (str)
	returns: fptree
	the 'main' fn in this module instantiates fptree and builds it
	by calling 'add_node' when called, bind result to 2 variables:
	one for the tree, the second for the header table
	"""
	fptree = TreeNode(root_node_name, None)
	root = fptree
	header_table, dataset = config_fptree_builder(dataset, trans_count,
		min_spt, sort_key)
	for trans in dataset:
		add_nodes(trans, header_table, root)
	# trim the headertable so it includes just the first node_link
		# of each item type which can then be used to find all other
		# nodes of same type
	header_table = {k:v[:2] for k, v in header_table.items()}
	return fptree, header_table



#---------------- mine the fp-tree for frequent itemsets -----------------#

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


def like_item_traversal(item, header_table):
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


def get_conditional_pattern_bases(item, header_table):
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
	ic = item_counter(cpb_all_expanded)
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
	return reorder_items(cpb_all, sort_key=get_sort_key(dataset))


# recursively find frequent itemsets

# call build_conditional_fptree, once for each unique item in htab.keys(),
# then if cfptree has more than one node in it:
# repeat the mining loop; else: exit


def sort_fis(path_str, sort_key=get_sort_key(dataset)):
	fnx = lambda q: sorted(q, key=sort_key.__getitem__)
	return ''.join(fnx(list(path_str)))


def cpbs(k, header_table, min_spt=MIN_SPT, trans_count=TRANS_COUNT):
	cpb_all = get_conditional_pattern_bases(k, header_table)
	if len(cpb_all) == 0:
		return None
	else:
		f_list = create_flist(cpb_all, min_spt, trans_count)
		cpb_all = filter_cpb_by_flist(cpb_all, f_list)
		cpb_all = sort_cpb_by_freq(cpb_all)
		cpb_all = deepcopy(list(cpb_all))
	return cpb_all, f_list


def mine_tree(header_table, p=CL.deque([]), min_spt=MIN_SPT,
	trans_count=len(dataset), f_list=None, min_fis_length=MIN_ITEMSET_LENGTH,
	debug=1):
	if not f_list:
		f_list = header_table
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
			if len(q) >= min_fis_length:
				fis = q + ':' + str(header_table[k][0])
				if debug:
					print('fis: {}: {}'.format(q, f_list[k]))
				FIS.append(fis)
			cfptree, chtab = build_fptree(cpb_all_, len(cpb_all_),
				min_spt, k)
			mine_tree(p=p1, header_table=chtab, min_spt=min_spt,
				trans_count=trans_count, f_list=f_list_)
		elif not x:
			q = ''.join(p1)
			if len(q) >= min_fis_length:
				fis = q + ':' + str(header_table[k][0])
				if debug:
					print('fis: {}: {}'.format(q, header_table[k][0]))
				FIS.append(fis)
			continue

#---------------- query the frequent itemsets containers ----------------#


def create_fis_containers(freq_item_sets):
	""""
	returns: two containers that store the same data, all freq
		itemsets for a given dataset, nested list of freq itemsets
		is returned then a dict where each key is a fis, value is
		count
	pass in: sequence of all frequent itemsets, each fis is
		a string of the form fis:count, eg, 'xyz:99'
	recommend when calling this function, bind the result to
	two variables, like so: fis, fis_cnt = create_fis_containers()
	"""
	fis_all = [itm.strip().split(':') for itm in freq_item_sets]
	fis =  [list(t[0]) for t in fis_all]
	fis_cnt = {k:int(v) for k, v in fis_all}
	return fis, fis_cnt


def all_itemsets_that_begin_with(query, fis):
	query_str = r'{}'.format(query)
	return [ line for line in fis if line.startswith(query_str) ]


def itemset_begins_with(probe, fis):
    p = r" " + re.escape(probe) + r""
    p = r"{} {} {} ".format(a, b, c)
    po = re.compile(p)
    po.findall



#------------------------ example usage --------------------#

SORT_KEY=get_sort_key(dataset)

fptree, htab = build_fptree(
							dataset=dataset,
							min_spt=MIN_SPT,
							trans_count=TRANS_COUNT,
							sort_key=SORT_KEY,
							root_node_name='root',
)

FIS = []
mine_tree(htab)