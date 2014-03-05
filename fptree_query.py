#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import re
import collections as CL
from functools import partial

import fptree_build as FPT
import fptree_mine as FPM


FIS = FPM.FIS


def create_fis_containers(freq_item_sets=FIS):
	""""
	returns: two containers that store the same data, all freq
		itemsets for a given dataset, nested list of freq itemsets
		is returned then a dict where each key is a fis, value is
		count
	pass in: sequence of all frequent itemsets, each fis is
		a string of the form fis:count, eg, 'xyz:99'
	recommend when calling this function, bind the result to
	two variables, like so: fis, fis_cnt = create_fis_containers()
	"""
	fis_all = [itm.strip().split(':') for itm in freq_item_sets]
	fis =  [list(t[0]) for t in fis_all]
	fis_cnt = {k:int(v) for k, v in fis_all}
	return fis, fis_cnt


def all_itemsets_that_begin_with(query, fis):
	query_str = r'{}'.format(query)
	return [ line for line in fis if line.startswith(query_str) ]


def itemset_begins_with(probe, fis):
    p = r" " + re.escape(probe) + r""
    p = r"{} {} {} ".format(a, b, c)
    po = re.compile(p)
    po.findall




p = r'^([A-Z][^A-Z])$'
p = r'^([A-Z]?)(?![A-Z])'
po = re.compile(p)

# fis = [ itm for itm in FIS if not po.search(itm) ]

p1 = r'\d'
po1 = re.compile(p1)

# fis = [ po1.sub('', itm) for itm in fis ]



fis, fis_cnt = create_fis_containers()

# the primary container that supports most frequent itemset queries
fis1 = sorted(fis_cnt.keys())

