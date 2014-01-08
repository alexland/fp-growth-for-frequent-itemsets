# encoding: utf-8


import fptree as FPT



def like_item_traversal(htab, itm):
	"""
	returned: list of pointers to node objects having the same 
		'name' attribute
	pass in: 
		(i) header table
		(ii) str/int representation of a given unique transaction item
	"""
	linked_nodes = []
	node = htab[itm][-1]
	while node != None:
		linked_nodes.append(node)
		node = node.node_link
	return linked_nodes
	

# tests:
# (i) assert linked_nodes[0] is htab[itm][-1]
# (ii) can i traverse the nodes via the node links?
# (iii) sum the count for each node in linked_nodes & compare it to
#		count in htab 