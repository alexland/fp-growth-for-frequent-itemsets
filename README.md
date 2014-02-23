FP-Growth: compact storage & very fast retrieval of frequent item sets
=======================

[![Build Status](https://travis-ci.org/alexland/fp-growth-for-frequent-itemsets.png?branch=master)](https://travis-ci.org/alexland/fp-growth-for-frequent-itemsets)

-----

to run the tests for this library:

```
python3 runtests.py -v

```

definitions:

*  _**fp-tree**_: a graph that provides a compact encoding of transaction data and enables efficient retrieval of frequent itemsets (frequently recurring sequences of elements that comprise the transaction data)

* _**fp-growth**_: the technique for building an fp-tree and populating it with transaction data, then efficiently extracing frequent itemsets from it

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


2 key (novel) elements of this FP-Growth implementation:

	(i) can be queried in a natural way for user-clickstream analytics, e.g.,
		which page is a user most often likely to visit given an immediate prior path?

	(ii) along with min support, includes a filter for minimum sequence length


some useful references on the subject of fp-trees and fo-growth:

[I'm an inline-style link](https://www.google.com)

[Prof Christian Borgelt's Site](http://www.borgelt.net/fpgrowth.html) inclues implementations of FP-Growth in C and a large number of academic references on this subject

[Frequent Itemset Mining Implementations Repository](http://fimi.ua.ac.be/src/) a large collection of FP-Growth implementations (src) and accompanying papers

[Hareendra Perera's blog](http://hareenlaks.blogspot.com/2011/06/fp-tree-example-how-to-identify.html)

    - a concise but atomic explanation of the FP-Growth algorithm; the focus of this excellent Post is the algorithmic data flow--ie, it omits many details relating to the FP-Tree data structure (eg, it doesn't mention the header table); but it's this meticulous selection of detail that i found so valuable when building the FP-Growth implementation in this repository.