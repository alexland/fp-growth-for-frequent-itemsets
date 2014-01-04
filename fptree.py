# encoding: utf-8

"""
definitions:

fp-tree: the graph that encodes the frequent itemsets information;

fp-growth: the technique for building fp-tree and extracing info from it

header table: a dict whose keys are the unique items comprising the 
transactions (data rows); the value for each key is a list of len 2; the first
item is the item frequency, the second is a pointer which points to the 
first occurrence of that item in the tree; this pointer, along w/
the 'node_link" attribute for each node, allow efficient traversal of all 
instances of an item type (eg, 'A') across the tree branches; this node
(pointed to in the htab) represents the terminus of the path defined
by nodes of the same type within a single fptree.

prefix path: the nodes comparising the path between root node & the 
	 item being queried; prefix paths are used to createa 
	 a conditional fp-tree

conditional pattern base: collection of prefix paths


"""

# TODO: refactor, where appropriate, comprehensions as generator expressions
# FIXME: min_spt doesn't make sense for my use cases

import collections as CL
from operator import itemgetter
from functools import partial



# min_spt = 50000
# dfile = "/Users/dougybarbo/Projects/data-pipeline-II/kosarak.dat"
# with open(dfile, "r", encoding="utf-8") as fh:
# 	pdata = [ line.strip().split() for line in fh.readlines() ]


data = [
	['c', 'a', 't', 's'],
	['c', 'a', 't', 's', 'u', 'p'],
	['c', 'a', 't'],
	['c', 'a', 't', 'c', 'h'],
	['c', 'a', 't', 'n', 'i', 'p'],
	['c', 'a', 't', 'e', 'g', 'o', 'r', 'y'],
	['c', 'a', 't', 'i', 'o', 'n'],
	['c', 'a', 't', 'a', 'p', 'u', 'l', 't'],
	['c', 'a', 't', 'c', 'h', 'y'],
	['c', 'a', 't', 'a', 'l', 'o', 'g'],
	['c', 'a', 't', 'e', 'r'],
	['c', 'a', 't', 's'],
	['c', 'a', 't', 'a', 'r', 'a', 'c', 't'],
	['c', 'a', 't', 't', 'l', 'e'],
	['a', 't', 'o', 'm'],
	['e', 'r', 'r', 'o', 'r'],
	['a', 't', 'm'],
	['l', 'e', 'a', 'r', 'n'],
	['t', 'e', 'r', 'm'],
	['a', 't', 't', 'a', 'c', 'h']
]


#---------------------- building the fp-tree -----------------------#


def config_fptree_builder(data):
	"""
	returns: header table & data for input to build_tree;
	pass in: raw data (nested list of transactions);
	"""
	data = [ set(trans) for trans in data ]
	# flatten the data (from list of sets to list of items)
	trans_flat = [itm for trans in data for itm in trans]
	# get frequency of each item
	item_counter = CL.defaultdict(int)
	for itm in trans_flat:
		item_counter[itm] += 1
	item_counter = sorted([(v, k) for k, v in item_counter.items() ], reverse=True)
	# list of items sorted by decreasing frequency
	fi = [t[1] for t in item_counter]
	# now use 'fi' to reorder the original data so that the 
	# items w/in each transaction are sorted by decreasing frequency:
	item_counter_orddict = CL.OrderedDict([ (t[1], t[0]) for t in item_counter ])
	fnx = lambda q: (item_counter_orddict[q], q)
	# transactions (data rows) sorted in frequency order
	# the contents in this container are used to build the fptree
	# return data w/ correct itm orering w/in transactions 
	transactions = [ sorted([fnx(itm) for itm in data[i]], reverse=True) 
		for i in range(len(data)) ]
	# now remove the sort key from each transaction item
	#'transactions' is the 'normalized' dataset; and
	# is used to build the fptree
	transactions = [ [t[1] for t in transactions[i]] 
		for i in range(len(transactions)) ]
	# build header table from freq_items w/ empty placeholders for node pointer
	htable = CL.defaultdict(list)
	for k in item_counter_orddict.keys():
	    htable[k].append(item_counter_orddict[k])
	return htable, transactions
 
 

class TreeNode:

	def __init__(self, node_name, parent_node):
		self.name = node_name
		self.node_link = None
		self.count = 1
		self.parent = parent_node
		self.children = {} 

	def incr(self, freq=1):
		self.count += freq 
 
# initialize fptree

	# eg, fptree = TreeNode(node_name='root', count=1, parent_node=None)

# now build tree by adding the "normalized" transactions, one at a time;
	# so for each transaction:

	# (i) check whether the first itm in trans is a child node in the 
	# 	parent node; 
		# (a) # IF YES, then INCREMENT THE COUNT of that child node;
		# (b) ELSE, ADD THE TRANSACTION as a child of that parent node
			# by calling TreeNode()
			
"""
to add transaction as a child of a given parent node:
someNode.children['node_name'] = FPG.TreeNode('node_name', 3, None)

"""
			
	# (ii) check whether itm is in header table, IF YES, then INCREMENT THE COUNT;
	# (II) ELSE, ADD THE ITM to the header table; 
	

# TODO: add to 'build_tree' code to update header table
# TODO: add to 'build_tree' conditionals to check if node is already a child
# TODO; consider having 2 header tables, lne for count, one for node pointers
# TODO: make build_tree a partial so 'htab' doesn't have to passed in
# TODO: above: add_nodes_ = partial(add_nodes, header_table=header_table)
# TODO: create variable to avoid repeated lookups for 'parent_node.children[itm]'
# TODO: use CL.deque() where appropriate (in lieu of lists for htab.values() ?)


def add_nodes(trans, header_table, parent_node):
	"""
	pass in: 
		a transaction (list), 
		header table (dict)
		parent_node (instance of class TreeNode);
	returns: nothing, converts a single transaction to
		nodes (or increments counts if exists)
	"""
	while len(trans) > 0:
		itm = trans.pop(0)
		# does this item appear in the same route?
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


def build_fptree(transactions):
	"""
	pass in: 
		raw data (list of transactions; one transcation per list)
	returns: fptree;
	instantiates fptree and builds it by calling 'add_node';
	when called, bind result to eg, 'fptree'
	"""
	fptree = TreeNode('root', None)
	root = fptree
	header_table, transactions = config_fptree_builder(data)
	for trans in transactions:
		add_nodes(trans, header_table, root)
	header_table = {k:v[:2] for k, v in header_table.items()}
	return fptree, header_table

	

# so to build an fptree, call 'config_fptree_builder', passing in the raw data;
# this returns a 'blank' header table and data processed to build the tree,
# next, call 'build_fptree' (unbound, it returns nothing),
# passing in the two params returned from call to 'config_fptree_builder'


#---------------------- querying the fp-tree -----------------------#

# TODO: if 2 items have same freq, sort by alpha/numeric order
# TODO: eliminate the "sort header table" from mineTree
# TODO: to exemplary queries below, add frequency (refactor mineTree)
# TODO: refactor variable names: distinguish: 'itm' to itmset and 'itm to itm
# TODO: add frequency to 'frequent_items' so i can sort the results
# TODO: get rid of 'min_spt' in place of something more appropriate

#---------- to traverse all instances of a given item ------------#

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









