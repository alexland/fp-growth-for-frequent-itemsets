# encoding: utf-8

"""
steps to query fp-tree:

	for a given item (any atomic element comprising the transactions):
		
		(i) 	get conditional pattern bases;
		(ii) 	get F-list
		(iii) 	build conditional fp-tree 

"""

# TODO: if 2 items have same freq, sort by alpha/numeric order
# TODO: eliminate the "sort header table" from mineTree
# TODO: to exemplary queries below, add frequency (refactor mineTree)
# TODO: refactor variable names: distinguish: 'item' to itemset and 'item to item
# TODO: add frequency to 'frequent_items' so i can sort the results
# TODO: get rid of 'min_spt' in place of something more appropriate



import itertools as IT

import fptree as FPT



def like_item_traversal(item, header_table=FPT.htab):
	"""
	returned: dict of pointers to node objects having the same 
		'name' attribute, keyed to the node's name attribute w/
		incremented integer appended so keys are unique;
	pass in: 
		(i) str/int representation of a given unique transaction item;
		(ii) header table
		
	"""
	linked_nodes = {}
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(item, next(c))
	node = header_table[item][-1]
	while node != None:
		linked_nodes[fnx(item)] = node
		node = node.node_link
	return linked_nodes
	

# tests:
# (i) assert linked_nodes[0] is htab[item][-1]
# (ii) can i traverse the nodes via the node links?
# (iii) sum the count for each node in linked_nodes & compare it to
#		count in htab 


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
	
	
# tests for a/r:
# (i) the last item in the returned list must be 'root'


def get_conditional_pattern_bases(item, header_table=FPT.htab, string_repr=False):
	"""
	returns:a nested list comprised of all node_routes for a given item,
		one route per list;
	pass in:  
		(i) str/int representation of a given unique transaction item
		(ii) header table;
	this fn transforms a raw 'route' from 'ascend_tree' into a cpb in 2
	steps: (i) remove start & terminus (ii) reverse;
	"""
	cpb_all = []
	linked_nodes = like_item_traversal(item, header_table)
	for node in linked_nodes.values():
		# if the nodes are ponters rather than strings
		route = ascend_route(node, string_repr=string_repr)
		if not string_repr:
			cnt = route[0].count
			# remove the node start & terminus ('root') & reverse
			cpb = route[1:-1][::-1]
			cpb_all.append((cpb, cnt))
		else:
			cpb = route[1:-1][::-1]
			cpb_all.append(cpb)
	return cpb_all
	

def f_list(item, header_table, min_spt, trans_count):
	"""
	returns: 
		(i) a dict whose keys are unique items and whose 
			values are the count in the cpbs for this item;
		(ii) filtered conditional pattern bases by min_spt
	pass in: 
		(i) one unique item in transactions (str)
		(ii) header table;
		(iii) min_spt (float);
		(iv) transaction count (number of transactions)
	this fn first calculates cond ptn bases for the item passed in via
	'get_conditional_pattern_bases', then calculates f-list'
	"""
	cond_ptn_bases = get_conditional_pattern_bases(item, header_table, 
						string_repr=True)
	item_count = FPT.item_counter(cond_ptn_bases)
	cpb_all_filtered, _ = FPT.filter_by_min_spt(cond_ptn_bases, item_count, min_spt, 
		trans_count)
	return cpb_all_filtered, FPT.item_counter(cpb_all_filtered)


def build_conditional_fptree(item, min_spt, trans_count, header_table=FPT.htab):
	"""
	returns: conditional fptree (for a given unique transaction item)
	pass in: 
		(i) one unique item in transactions (str)
		(ii) minimum support (float)
		(iii) count of transactions in initial dataset;
	this fn is a thin wrapper over 'build_fptree'
	"""
	cpb_all_filtered, _ = f_list(item, min_spt, trans_count, header_table) 
	cond_fptree, _ = FPT.build_fptree(dataset=cpb_all_filtered, 
						root_node_name=item)
	return cond_fptree
	
	






	