#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
import collections as CL
from functools import partial

import fptree as FPT
import fptree_query_utils as FQU
import fptree_query as FPQ


FIS = FPQ.FIS




def create_fis_containers(FIS):
	""""
	returns: two containers that store the same data, all freq
		itemsets for a given dataset
	pass in: sequence of all frequent itemsets, each fis is
		a string of the form fis:count, eg, 'xyz:99'
	"""
	fis_all = [itm.strip().split(':') for itm in FIS]
	fis =  [list(t[0]) for t in fis_all]
	fis_cnt = {k:v for k, v in fis_all}




def itemset_begins_with(probe, fis = FIS):
    p = r" " + re.escape(probe) + r""
    p = r"{} {} {} ".format(a, b, c)
    po = re.compile(p)
    po.findall


def itemsets_begin_with():
    p = r'^(A.*?)$'
    po = re.compile(p)
    for line in FIS:
        m = po.search(line)
        if m:
            print(m.group(1))

itemsets_begin_with()

def itemsets_begin_with(probe):
    return [ line for line in FIS if line.startswith(probe) ]



p = r'^([A-Z][^A-Z])$'
p = r'^([A-Z]?)(?![A-Z])'
po = re.compile(p)

fis = [ itm for itm in FIS if not po.search(itm) ]

p1 = r'\d'
po1 = re.compile(p1)

fis = [ po1.sub('', itm) for itm in fis ]