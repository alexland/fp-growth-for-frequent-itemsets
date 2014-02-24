#!/usr/bin/env python3
# encoding: utf-8

"""

"""

# TODO: refactor comprehensions as gen exp (check for 'list' calls)
# TODO: make build_tree a partial so 'htab' doesn't have to passed in
# TODO: above: add_nodes_ = partial(add_nodes, header_table=header_table)
# TODO: create variable to avoid repeated lookups for 'parent_node.children[item]'
# TODO: use CL.deque() where appropriate (in lieu of lists for htab.values() ?)
# TODO: write viz module comprised of python obj --> JSON translator + pygraphviz render
# TODO: a few of these fns i think are memoizable
# TODO: *** create tests for duplicate items in trans
# TODO: in TreeNode, create 'repr' fn so node pointers print like 'name' attr


import collections as CL
from operator import itemgetter
import functools as FT
import itertools as IT


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


def get_items_below_min_spt(dataset, item_count, min_spt, trans_count):
    """
    returns: list of the unique items whose frequency over the
		dataset is below some min_spt (float between 0 and 1,
		('decimal percent')
	pass in:
		(i) dataset
		(ii) dict w/ items for keys, values are item frequency
		(iii) min_spt (float, eg, 0.03 means each item must appear in
		    at least 3% of the dataset)
	        calls 'item_counter'
    """
    ic = {k:v for k, v in item_count.items() if (v/trans_count) < min_spt}
    return list(ic.keys())


def build_min_spt_filter_str(excluded_items):
	"""
	returns: a str which, when 'eval' is called on it, is a
		a valid arg for 'IT.filterfalse' which is used in
		'filter_by_min_spt' to remove items below min_spt
	pass in: list of excluded items (returned by
		 'get_items_below_min_spt')
	"""
	excluded_items_expr = []
	str_templ = '(q=="{0}")'
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
	excluded_items = get_items_below_min_spt(dataset, item_count,
		min_spt, trans_count)
	if not excluded_items:
		# if all items are above min_spt, ie, there are no items to exclude
		# so just return original args
		return dataset, item_count
	else:
		# there is at least one item to exclude
		# now build the expression required by 'IT.filterfalse' from the
		# list of excluded items
		filter_str = build_min_spt_filter_str(excluded_items)
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


def config_fptree_builder(dataset, trans_count, min_spt=None):
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
	if min_spt:
		dataset, item_count = filter_by_min_spt(dataset, item_count,
								trans_count, min_spt)
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


def build_fptree(dataset, trans_count, min_spt=None, root_node_name="root"):
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
		min_spt)
	for trans in dataset:
		add_nodes(trans, header_table, root)
	# trim the headertable so it includes just the first node_link
		# of each item type which can then be used to find all other
		# nodes of same type
	header_table = {k:v[:2] for k, v in header_table.items()}
	return fptree, header_table


def main(dataset):
	return build_fptree(dataset=dataset, trans_count=TRANS_COUNT,
		min_spt=MIN_SPT, root_node_name='root')



dataset = [
	    ['E', 'B', 'D', 'A'],
		['E', 'A', 'D', 'C', 'B'],
		['C', 'E', 'B', 'A'],
		['A', 'B', 'D'],
		['D'],
		['D', 'B'],
		['D', 'A', 'E'],
		['B', 'C'],
	]

TRANS_COUNT = len(dataset)
MIN_SPT = 0.3
SORT_KEY=get_sort_key(dataset)
c_reorder_items = FT.partial(reorder_items,
	sort_key=get_sort_key(dataset))

fptree, htab = main(dataset)


if __name__=="__main__":
	# import cProfile
	# cProfile.run("main(dataset)")
	TRANS_COUNT = len(dataset)
	MIN_SPT = 0.3
	SORT_KEY=get_sort_key(dataset)
	c_reorder_items = FT.partial(reorder_items,
		sort_key=get_sort_key(dataset))
	fptree, htab = main(dataset)





