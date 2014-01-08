# encoding: utf-8

"""
steps to query fp-tree:

	for a given item (any atomic element comprising the transactions):
		
		(i) get conditional pattern bases;
		(ii) get F-list

"""


import itertools as IT

import fptree as FPT



def like_item_traversal(htab, itm):
	"""
	returned: dict of pointers to node objects having the same 
		'name' attribute, keyed to the node's name attribute w/
		incremented integer appended so keys are unique;
	pass in: 
		(i) header table
		(ii) str/int representation of a given unique transaction item
	"""
	linked_nodes = {}
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(itm, next(c))
	node = htab[itm][-1]
	while node != None:
		linked_nodes[fnx(itm)] = node
		node = node.node_link
	return linked_nodes
	

# tests:
# (i) assert linked_nodes[0] is htab[itm][-1]
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
	
	
# tests:
# (i) the last item in the returned list must be 'root'


def get_conditional_pattern_bases(htab, itm, string_repr=False):
	"""
	returns:a nested list comprised of all node_routes for a given item,
		one route per list;
	pass in: 
		(i) header table
		(ii) str/int representation of a given unique transaction item
	this fn transforms a raw 'route' from 'ascend_tree' into a cpb in 2
	steps: (i) remove start & terminus (ii) reverse;
	"""
	cpb_all = []
	linked_nodes = like_item_traversal(htab, itm)
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
	
	

def f_list(itm, min_spt, trans_count):
	"""
	returns: a dict whose keys are unique items and whose values are
		the count in the cpbs for this item
	pass in: 
		(i) one unique item in transactions (str)
		(ii) min_spt (float);
		(iii) transaction count (number of transactions)
	this fn first calculates cond ptn bases for the item passed in via
	'get_conditional_pattern_bases', then calculates f-list'
	"""
	cond_ptn_bases = get_conditional_pattern_bases(htab, itm, string_repr=True)
	item_count = FPT.item_counter(cond_ptn_bases)
	x, _ = FPT.filter_by_min_spt(cond_ptn_bases, item_count, min_spt, trans_count)
	return FPT.item_counter(x)


	