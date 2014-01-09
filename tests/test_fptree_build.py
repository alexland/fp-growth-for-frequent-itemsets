# encoding: utf-8

import collections as CL
from operator import itemgetter
from functools import partial
import itertools as IT

import pytest
import fptree as FPT


# TODO: setup each dataset as a 'fixture'
# TODO: research caching of module under test


#-------------------------- test set-up & tear-down -----------------#

data1 = [
	['B', 'D', 'A', 'E'],
	['B', 'D', 'A', 'E', 'C'],
	['B', 'A', 'E', 'C'],
	['B', 'D', 'A'],
	['D'],
	['B', 'D'],
	['D', 'A', 'E'],
	['B', 'C']
]

data2 = [
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


#------------------------- fixtures --------------------------------#


@pytest.fixture(scope="module")
def myFixture1():
	return 5

@pytest.fixture(scope="module")
def myFixture2():
	return 2

@pytest.fixture(scope="module", params=["param1", "param2"])
def myFixture(request):
	if request.param == "param1":
		return request.getfuncargvalue("myFixture1")
	elif request.param == "param2":
		return request.getfuncargvalue("myFixture2")




#------------------------- test fns --------------------------------#

def items_frequency(data):
	"""
	returns frequency of each item across all transactions;
	"""
	from collections import defaultdict
	data = [set(trans) for trans in data]
	trans_flat = [itm for trans in data for itm in trans]
	item_counter = CL.defaultdict(int)
	for itm in trans_flat:
		item_counter[itm] += 1
	return item_counter
	

def build_fptree(data):
	fptree = FPT.TreeNode('root', None)
	root = fptree
	htab, transactions = FPT.config_fptree_builder(data, len(data))
	for trans in transactions:
		FPT.add_nodes(trans, htab, root)
	htab = {k:v[:2] for k, v in htab.items()}
	return htab, fptree


def fnx1():
	"""
	compares itm frequency dict w/ cumulative totals per item from fptree
	"""
	import collections as CL
	data = [ set(trans) for trans in data ]
	items_all = [itm for trans in data for itm in trans]
	

def unique_items():
	"""
	
	"""
	return {itm for trans in data for itm in trans}


def like_item_traversal1(data, itm):
	"""
	pass in: dataset & single transaction item (str), which
		can be any key in the header_table;
	returns: linked_nodes (list) comprised of all node names
		linked in one continuous route;
	checks that the 'node_link' attribute for any node points 
	to another having the same 'name' attribute (ie, all nodes
	linked via their 'node_link' attribute have the same name);
	this is done by gathering 'name' attribute of all nodes in route
	calling 'set' on the list and checking that length is 1;
	"""
	htab, fptree = build_fptree(data)
	linked_nodes = []
	node = htab[itm][-1]
	while node != None:
		linked_nodes.append(node.name)
		node = node.node_link
	return len(set(linked_nodes))
	

def like_item_traversal2(data, itm):
	"""
	pass in: dataset & single transaction item (str), which
		can be any key in the header_table;
	returns: a linked_nodes (list) comprised of all node names
		linked in one continuous route;
	checks that the 'node_link' attribute for any node points 
	to another having the same 'name' attribute (ie, all nodes
	linked via their 'node_link' attribute have the same name);
	this is done by gathering 'name' attribute of all 'linked' nodes
	(eg, all nodes w/ name attribute 'A')
	and checking that they are all the same and equal to 'itm' passed in
	"""
	htab, fptree = build_fptree(data)
	linked_nodes = []
	node = htab[itm][-1]
	while node != None:
		linked_nodes.append(node.name)
		node = node.node_link
	linked_nodes.append(itm)
	return linked_nodes


def item_freq1(itm):
	"""
	compares item frequencies from 2 difference sources:
	(i) header_table; and (ii) cumulative sum by node traversal
		using node_links; these two values should be identical;
	"""
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(itm, next(c))
	htab, fptree = build_fptree(data1)
	node = htab[itm][-1]
	cnt = 0
	while node != None:
		cnt += node.count
		node = node.node_link
	return htab[itm][0], cnt


def item_freq1a(itm):
	"""
	for the dataset, 'data2',
	compares item frequencies from 2 difference sources:
	(i) header_table; and (ii) cumulative sum by node traversal
		using node_links; these two values should be identical;
	"""
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(itm, next(c))
	htab, fptree = build_fptree(data1)
	node = htab[itm][-1]
	cnt = 0
	while node != None:
		cnt += node.count
		node = node.node_link
	return htab[itm][0], cnt


def item_freq2(data):
	"""
	identifies all instances of a given item
	from across entire fptree
	should return int(3)
	"""
	itm = 'A'
	unique_item_instances = []
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(itm, next(c))
	htab, fptree = build_fptree(data)
	node = htab[itm][-1]
	while node != None:
		unique_item_instances.append(node)
		node = node.node_link
	return len(unique_item_instances)


def item_freq3(data):
	"""
	identifies all instances of a given item
	from across entire fptree
	should return int(2)
	"""
	itm = 'E'
	unique_item_instances = []
	c = IT.count()
	fnx = lambda a: "{0}{1}".format(itm, next(c))
	htab, fptree = build_fptree(data)
	node = htab[itm][-1]
	while node != None:
		unique_item_instances.append(node)
		node = node.node_link
	return len(unique_item_instances)


#------------------------- assertions --------------------------------#

def test_1(myFixture1):
	assert myFixture1 == 5


def test_2(myFixture2):
	assert myFixture2 == 2


def test_all(myFixture):
	assert myFixture in (2, 5)


@pytest.mark.parametrize("input,expected", [
	("3+5", 8),
	("2+4", 6),
	("6*9", 54),
	])
def test_eval(input, expected):
	assert eval(input) == expected


@pytest.mark.parametrize("input,expected", [
	(item_freq1("A"), (5, 5)),
	(item_freq1("D"), (6, 6)),
	(item_freq1("B"), (6, 6)),
	(item_freq1("E"), (4, 4)),
	(item_freq1("C"), (3, 3)),
	])
def test1_item_freq1(input, expected):
	assert input == expected


@pytest.mark.parametrize("input,expected", [
	(item_freq1("A")[0]==item_freq1("A")[1], True),
	(item_freq1("D")[0]==item_freq1("D")[1], True),
	(item_freq1("B")[0]==item_freq1("B")[1], True),
	(item_freq1("E")[0]==item_freq1("E")[1], True),
	(item_freq1("C")[0]==item_freq1("C")[1], True),
	])
def test2_item_freq2(input, expected):
	assert input == expected

# htab, _ = FPT.config_fptree_builder(data1)
# @pytest.mark.paramaterize("input,expected",
# 	[ eval("(item_freq1({0})[0]==item_freq1({0})[1], True)".format(k)) 
# 		for k in htab.keys() ]
# )
# def test_item_freq2(input, expected):
# 	assert (input) == expected

@pytest.mark.parametrize("input,expected", [
	(like_item_traversal1(data1, "A"), 1),
	(like_item_traversal1(data1, "B"), 1),
	(like_item_traversal1(data1, "C"), 1),
	(like_item_traversal1(data1, "D"), 1),
	(like_item_traversal1(data1, "E"), 1),
	])
def test2_like_item_traversal1(input, expected):
	assert input == expected


fnx = lambda nr: all(nr[0] == itm for itm in nr)
@pytest.mark.parametrize("input,expected", [
	(fnx(like_item_traversal2(data1, "A")), True),
	(fnx(like_item_traversal2(data1, "B")), True),
	(fnx(like_item_traversal2(data1, "C")), True),
	(fnx(like_item_traversal2(data1, "D")), True),
	(fnx(like_item_traversal2(data1, "E")), True),
	])
def test1_like_item_traversal2(input, expected):
	assert input == expected


# @pytest.mark.paramaterize("input,expected", [
# 	(like_item_traversal2(data1, "A"), 1),
# 	(like_item_traversal2(data1, "B"), 1),
# 	(like_item_traversal2(data1, "C"), 1),
# 	(like_item_traversal2(data1, "D"), 1),
# 	(like_item_traversal2(data1, "E"), 1),
# 	])
# def test1_like_item_traversal2(input, expected):
# 	assert input == expected



def test1_like_item_traversal1():
	assert like_item_traversal1(data1, 'A') == 1




def test_item_freq():
	header_table_item_freq, cumulative_freq = item_freq1('A')
	assert header_table_item_freq == cumulative_freq
	 

def test_item_freq2a():
	assert item_freq2(data1) == 3


def test_item_freq3():
	assert item_freq3(data1) == 3


def test_headertable1():
	""" 
	verifies that the values in the header table are all
	lists of length 2
	"""
	htab, _ = build_fptree(data1)
	assert all( (len(v)==2) & (isinstance(v, list)) for v in htab.values() )


def test_headertable2():
	""" 
	verifies that the header table has a complete set of keys
	"""
	# ui = unique_items()
	# ht = build_header_table(data)
	# diff = ui.difference(ht)
	# assert len(diff)==0
	pass


def test_fnx2():
	import py
	py.test.raises(ValueError, int, 'foo')



		