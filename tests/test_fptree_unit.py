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
	dataset = [ set(trans) for trans in dataset ]
	# flatten the data (from list of sets to list of items)
	trans_flat = [itm for trans in dataset for itm in trans]
	# get frequency of each item
	item_counter = CL.defaultdict(int)
	for itm in trans_flat:
		item_counter[itm] += 1
	return item_counter


#------------------------- test fns --------------------------------#



#------------------------- assertions --------------------------------#


def test_fpt_get_items_below_min_spt:
	assert FPT.get_items_below_min_spt(dataset, item_counter, min_spt) == ["C", "E"]









