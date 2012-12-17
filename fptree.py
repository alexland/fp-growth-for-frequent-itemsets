#!/usr/local/bin/python2.7
# encoding: utf-8

# TODO: remove inferequent items

import os
import sys
import collections as CL
import numpy as NP

t1 = ['e', 'a', 'd', 'b']
t2 = ['d', 'a', 'c', 'e', 'b']
t3 = ['c', 'a', 'b', 'e']
t4 = ['b', 'a', 'd']
t5 = ['d']
t6 = ['d', 'b']
t7 =['b', 'c']
t8 = ['a', 'd', 'e']

t_all = [t1, t2, t3, t4, t5, t6, t7, t8]


def priority_order(trow, cn):
	"""
		returns: the original transaction row now ordered
			by item frequency;
		pass in: trow, single transaction as python list,
			cn, Counter object;
		items in a transaction sorted according
		to frequency of occurrence
	"""
	idx = []
	for itm in trow:
		idx.append(cn[itm])
	NP.argsort(idx)[::-1]
	idx = NP.argsort(idx)[::-1]
	trow = NP.array(trow)
	x = trow[idx]
	return x.tolist()


def priority_table(data, support):
	"""
		returns: data w/ each transaction resorted in frequency order;
		pass in: data, a python nested list, and support,
			as an integer percentage;
	"""
	from collections import Counter
	t_all = [itm for row in data for itm in row]
	cn = Counter(t_all)
	pt = [priority_order(trow, cn) for trow in data]
	s = (len(data) * support) / 100.
	cn = { k:v for k, v in cn.iteritems() if v > s }
	items_over_support = cn.keys()
	return [[itm for itm in row if itm in items_over_support]
		for row in pt]

