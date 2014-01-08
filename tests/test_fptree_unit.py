# encoding: utf-8

import collections as CL
from operator import itemgetter
from functools import partial
import itertools as IT

import pytest
import fptree as FPT

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

def item_counter(dataset):
	dataset = [set(trans) for trans in dataset]
	# flatten the data (from list of sets to list of items)
	trans_flat = [itm for trans in dataset for itm in trans]
	# get frequency of each item
	ic = CL.defaultdict(int)
	for itm in trans_flat:
		ic[itm] += 1
	return ic


#------------------------- test fns --------------------------------#



#------------------------- assertions --------------------------------#

def test_item_counter():
	ic = FPT.item_counter(data1)
	kx = sorted(list(ic.keys()))
	assert kx == sorted(['B', 'C', 'A', 'D', 'E'])


def test2_item_counter():
	ic = FPT.item_counter(data1)
	vx = sorted(list(ic.values()))
	assert vx == sorted([6, 3, 5, 6, 4])


# def test_get_items_below_min_spt():
# 	item_count = item_counter(data1)
# 	assert FPT.get_items_below_min_spt(data1, item_count, 
# 		min_spt=0.55) == ["C", "E"]


def test_build_min_spt_filter_str():
	assert FPT.build_min_spt_filter_str(["A", "B"]) == '(q=="A") | (q=="B")'


def test2_build_min_spt_filter_str():
	assert FPT.build_min_spt_filter_str(["A"]) == '(q=="A")'


def test3_build_min_spt_filter_str():
	import string
	excl_items = string.ascii_uppercase[:6]
	assert FPT.build_min_spt_filter_str(excl_items) == '(q=="A") | (q=="B") | (q=="C") | (q=="D") | (q=="E") | (q=="F")'




