# encoding: utf-8

"""

"""

# TODO: refactor, where appropriate, comprehensions as generator expressions
# FIXME: min_spt doesn't make sense for my use cases
# TODO: add min support

# TODO: make build_tree a partial so 'htab' doesn't have to passed in
# TODO: above: add_nodes_ = partial(add_nodes, header_table=header_table)
# TODO: create variable to avoid repeated lookups for 'parent_node.children[itm]'
# TODO: use CL.deque() where appropriate (in lieu of lists for htab.values() ?)
# TODO: write viz module comprised of python obj --> JSON translator + pygraphviz render
# TODO: create a new table (like header table) that stores the terminus node for each route


import collections as CL
from operator import itemgetter
from functools import partial
import itertools as IT



# min_spt = 50000
# dfile = "/Users/dougybarbo/Projects/data-pipeline-II/kosarak.dat"
# with open(dfile, "r", encoding="utf-8") as fh:
# 	pdata = [ line.strip().split() for line in fh.readlines() ]


data = [
	['C', 'A', 'T', 'S'],
	['C', 'A', 'T', 'S', 'U', 'P'],
	['C', 'A', 'T'],
	['C', 'A', 'T', 'C', 'H'],
	['C', 'A', 'T', 'A', 'N'],
	['C', 'A', 'T', 'N', 'I', 'P'],
	['C', 'A', 'T', 'E', 'G', 'O', 'R', 'Y'],
	['C', 'A', 'T', 'I', 'O', 'N'],
	['C', 'A', 'T', 'A', 'P', 'U', 'L', 'T'],
	['C', 'A', 'T', 'C', 'H', 'Y'],
	['C', 'A', 'T', 'A', 'L', 'O', 'G'],
	['C', 'A', 'T', 'E', 'R'],
	['C', 'A', 'T', 'S'],
	['C', 'A', 'T', 'A', 'R', 'A', 'C', 'T'],
	['C', 'A', 'T', 'T', 'L', 'E'],
	['A', 'T', 'O', 'M'],
	['E', 'R', 'R', 'O', 'R'],
	['A', 'T', 'M'],
	['L', 'E', 'A', 'R', 'N'],
	['T', 'E', 'R', 'M'],
	['A', 'T', 'T', 'A', 'C', 'H']
]


#---------------------- building the fp-tree -----------------------#

def filter_by_min_spt(dataset, item_counter, min_spt):
		"""
		returns: 
			(i) filterd dataset (remove items w/ freq < min_spt);
			(ii) filtered item counter
		pass in:
			(i) dataset (the raw dataset);
			(ii) dict w/ items for keys, values are frequency;
			(iii) min_spt (float, eg, 0.03 means each item must appear in 
			at least 3% of the dataset); 
		removes any item from every transaction if that item's total freq
		is below 'min_spt' 
		"""
		# identify the (unique) items that fallow below min_spt
		total = sum([len(row) for row in dataset])
		ic0 = {k:v for k, v in item_counter.items() if (v/total) < min_spt}
		if not ic0:
			# if all items are above min_spt, ie, there are no items to exclude
			# so just return original args
			return dataset, item_counter
		else:
			# there is at least one item to exclude
			# build the expression
			excluded_items = list(ic0.keys())
			excluded_items_expr = []
			str_templ = '(q=="{0}")'
			for itm in excluded_items:
			    excluded_items_expr.append(str_templ.format(itm))
			filter_str = " | ".join(excluded_items_expr)
			# remove those below threshold items from the dataset
			tx = [IT.filterfalse(lambda q: eval(filter_str), trans) 
					for trans in dataset]
			ic = {k:v for k, v in item_counter.items() if (v/total) >= min_spt}
			return list(map(list, tx)), ic



def config_fptree_builder(dataset, min_spt=None):
	"""
	returns: header table & dataset for input to build_tree;
	pass in: 
		raw data (nested list of dataset);
		min_spt (float) fraction of total dataset in which an item
			must appear to be included in the fptree
	"""
	dataset = [ set(trans) for trans in dataset ]
	# flatten the data (from list of sets to list of items)
	trans_flat = [itm for trans in dataset for itm in trans]
	# get frequency of each item
	item_counter = CL.defaultdict(int)
	for itm in trans_flat:
		item_counter[itm] += 1
	if min_spt:
		dataset, item_counter = filter_by_min_spt(dataset, item_counter, min_spt)
	# to sort by decr frequency, then secondary (alpha) sort by key (incr),
	# sort first by secondary key, then again by primary key
	ic = sorted(((k, v) for k, v in item_counter.items()), 
		key=itemgetter(0))
	ic = sorted(ic, key=itemgetter(1), reverse=True)
	sort_key = {t[0]: i for i, t in enumerate(ic)}
	fnx = lambda q: sorted(q, key=sort_key.__getitem__)
	dataset = map(fnx, dataset)
	# build header table from freq_items w/ empty placeholders for node pointer
	htable = CL.defaultdict(list)
	for k in item_counter.keys():
	    htable[k].append(item_counter[k])
	return htable, dataset
 
 
class TreeNode:

	def __init__(self, node_name, parent_node):
		self.name = node_name
		self.node_link = None
		self.count = 1
		self.parent = parent_node
		self.children = {} 

	def incr(self, freq=1):
		self.count += freq 
 
			
def add_nodes(trans, header_table, parent_node):
	"""
	pass in: 
		a transaction (list), 
		header table (dict)
		parent_node (instance of class TreeNode);
	returns: nothing, converts a single transaction to
		nodes in an fp-tree (or increments counts if exists)
		and updates the companion header table 
	"""
	while len(trans) > 0:
		itm = trans.pop(0)
		# does this item appear in the same route?
		# if so it will have to be upsteam & adjacent given how the items
		# are sorted prior to tree building & given that the fp-tree is
		# built from the top down
		if itm in parent_node.children.keys():
			parent_node.children[itm].incr()
		else:
			# create the node & add it to the tree
			parent_node.children[itm] = TreeNode(itm, parent_node)
			this_node = parent_node.children[itm]
			try:
				# is there at least one node pointer for this itm 
				# in the header table?
				# ie, does this item appear in another route, or
				header_table[itm][1]
				# if so:
				header_table[itm][-1].node_link = this_node
				header_table[itm].append(this_node)
			except IndexError:
				# this is the 1st time this itm is seen by this fn
				# ie, no node pointer for this item in h/t, so add it
				header_table[itm].append(this_node)
		this_node = parent_node.children[itm]
		add_nodes(trans, header_table, this_node)


def build_fptree(dataset, min_spt):
	"""
	pass in: 
		raw data (list of dataset; one transcation per list)
	returns: fptree;
	the 'main' fn in this module; instantiates fptree and builds it
	by calling 'add_node'; when called, bind result to 2 variables:
	one for thetree; the second for for the header table;
	"""
	fptree = TreeNode('root', None)
	root = fptree
	header_table, dataset = config_fptree_builder(dataset, min_spt)
	for trans in dataset:
		add_nodes(trans, header_table, root)
	header_table = {k:v[:2] for k, v in header_table.items()}
	return fptree, header_table


def main(dataset, min_spt):
	build_fptree(dataset, min_spt)


def fpt(tn):
	"""
	returns: None;
	pass in: an fptree node;
	convenience funciton for informal, node-by-node introspection
	of the fptree object; call unbound to variable
	"""
	print("count: {0}".format(tn.count))
	print("name: {0}".format(tn.name))
	print("children: {0}".format(list(tn.children.keys())))
	print("parent: {0}".format(tn.parent.name))


if __name__ == '__main__':
	
	data = [
		['E', 'B', 'D', 'A'],
		['E', 'A', 'D', 'C', 'B'],
		['C', 'E', 'B', 'A'],
		['A', 'B', 'D'],
		['D'],
		['D', 'B'],
		['D', 'A', 'E'],
		['B', 'C'],
	 ]
	 # returns complete fp-tree & header table
	fptree, htab = main(data, 0.1)



#---------------------- querying the fp-tree -----------------------#

# TODO: if 2 items have same freq, sort by alpha/numeric order
# TODO: eliminate the "sort header table" from mineTree
# TODO: to exemplary queries below, add frequency (refactor mineTree)
# TODO: refactor variable names: distinguish: 'itm' to itmset and 'itm to itm
# TODO: add frequency to 'frequent_items' so i can sort the results
# TODO: get rid of 'min_spt' in place of something more appropriate

#---------- to traverse a given route, upward toward root ------------#

def ascend_route(node):
	"""
	returns: all nodes in a given route from the node passed in to the root
	pass in: a single node in an fp-tree
	"""
	node_route = []
	while node != None:
	    node_route.append(node.name)
	    node = node.parent
	return node_route




#---------- to traverse all instances of a given item ------------#

def like_item_traversal(itm):
	"""
	returns:
	pass in:
	this is the counterpart fn to 'ascend_route' which traverses 
	fptree upward; this fn does transverse traversal across
	nodes of dthe same type
	"""
	linked_nodes = []
	node = htab[itm][-1]
	while node != None:
		linked_nodes.append(node)
		node = node.node_link
	linked_nodes.append(itm)
	return linked_nodes

# eg, all of the 'A' nodes
# (i) get the route origin from header_table; this is pointer to
	# node representing 1st instance of 'A'
# A1 = header_table['A'][-1]
# (ii) now bind this node's 'node_link' attribute to a variable
	# that represents the 2nd instance of A, first testing for 
	# node_link attribute (if none then only one instance of that itm)
# if A1.node_link != None:
	
	# A2 = A1.node_link

# (iii) repeat step 2 until, eg,
	# A3 = A2.node_link


# frequent_items = [] 
# mineTree(fptree, htab, min_spt, set([]), frequent_items)

# step 1: # list comprised of just freq items inv sorted by their frequencies
# hx = { k:v[0] for k, v in htable.items() }
# fi = [itm[0] for itm in sorted(hx.items(), key=itemgetter(1))]

# sort and coerce to intergers (vs str)
# frequent_items = sorted([ list(map(int, sorted(x))) for x in frequent_items ])

#----- exemplary query I: what are the most frequent pairs: ----#
# frequent_pairs = [ x for x in frequent_items if len(x) == 2 ]
	 
	
#----- exemplary query II: given an item, recommend another item

# eg, given "11", or [6, 4], recommend other items:

# predicate
# pd = 11

# predicate
# pd = 'cat'
# express as set:
# pd = {ch for ch in 'cat'}


# if the predicate is a multi-item sequence (list)
# res = filter(lambda q: pd < q, frequent_items)
# OR
# fi0 = [ itm for itm in frequent_items if pd < itm ]


# now remove the predicate from res:

# remove_predicate = lambda q: q ^ pd

# res = map(remove_predicate, fi0)

# nested set to a flat list
# res = [itm for t in res for itm in t ]


# if predicate is single item (int)
# res = filter(lambda q: pd in q, frequent_items)

# now remove the predicate from the patterns returned
# for lx in res:
#     lx.remove(11)
# res = [ lx for lx in res if not len(lx) == 0 ]
# res = {itm for lx in res for itm in lx}



#--------------- traversal downward from root to find terminal nodes -----------#

# terminal nodes have no children


# write this as a recursive function:
# terminal_nodes_in_route = []
# for node in nodes:
# 	while not len(node.children.keys()) == 0:
# 		nodes = node.children
# 	terminal_nodes_in_route.append(node)
		
		
		





