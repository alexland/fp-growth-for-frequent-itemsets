
to run the tests for this library:

```
python runtests.py

```

definitions:

*  _**fp-tree**_: the graph that encodes the frequent itemsets information;

* _**fp-growth**_: the technique for building fp-tree and extracing info from it

* _**header table**_: a dict whose keys are the unique items comprising the 
transactions (data rows); the value for each key is a list of len 2; the first
item is the item frequency, the second is a pointer which points to the 
first occurrence of that item in the tree; this pointer, along w/
the 'node_link" attribute for each node, allow efficient traversal of all 
instances of an item type (eg, 'A') across the tree branches; this node
(pointed to in the htab) represents the terminus of the path defined
by nodes of the same type within a single fptree.

* _**prefix path**_: the nodes comparising the path between root node & the 
	 item being queried; prefix paths are used to createa 
	 a conditional fp-tree

* _**conditional pattern base**_: collection of prefix paths
