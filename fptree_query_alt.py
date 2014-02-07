#!/usr/bin/env python3
# encoding: utf-8


import itertools as IT
from copy import deepcopy
import collections as CL
ddir = "/Users/dougybarbo/Projects/fp-growth-for-frequent-itemsets"
import os
os.chdir(ddir)

%run fptree
%run fptree_query_utils
%run fptree_query

route = Route('', '', '', 0)

fptree = FPT.fptree
header_table = FPT.htab
dataset = FPT.data0
MIN_SPT = 0.3
trans_count = len(dataset)

k = 'A'
route.prefix_path.appendleft(route.root)
route.root = route.node
route.node = k
route.count = header_table[k][0]


class Route:
	__slots__ = ['node', 'prefix_path', 'root', 'count']
	def __init__(self, node, prefix_path, root, count):
		self.node = node
		self.prefix_path = CL.deque(prefix_path)
		self.root = root
		self.count = count

	def __repr__(self):
		return "node: {0}  prefix_path: {1}  root: {2}  count: {3}".format(
			self.node, self.prefix_path, self.root, self.count)

def persist(route, sort_key=FPT.sort_key):
    fnx = lambda q: sorted(q, key=sort_key.__getitem__)
    freq_itemset = route.node + ''.join(route.prefix_path) + route.root
    freq = route.count
    return {freq_itemset: freq}

def update_route(route, k, f_list=header_table):
	route.prefix_path.appendleft(route.root)
	route.root = route.node
	route.node = k
	count = f_list[k]
	if isinstance(count, list):
		count = count[0]
		route.count = count
	return route

def get_cpbs(route, header_table=FPT.htab, f_list=FPT.htab):
	cpb_all = get_conditional_pattern_bases(route.node, header_table=FPT.htab)
	f_list = p_create_flist(cpb_all)
	cpb_all = filter_cpb_by_flist(cpb_all, f_list)
	cpb_all = sort_cpb_by_freq(cpb_all)
	cpb_all = deepcopy(list(cpb_all))
	if cpb_all == []:
		print(persist(route))
		return None
	else:
		return cpb_all, f_list


#----------------#

#----- top level: iterating over unique transaction items ------#

for k in header_table.keys():

	# initialize the route:
	route = Route('', '', '', 0)

	# update the route:
	update_route(route, k)

	# calculate conditional pattern bases:
	x = get_cpbs(route, cheader_table)
	if not x:
		# persist frequent itemsets & 'continue', ie break out of this loop &
		# go to next key in header_table.keys()
		persist(route, sort_key=FPT.sort_key)
		print("recursion path terminated; frequent itemsets persisted")
		continue
	else:
		cpb_all, f_list = x
		print("continue recursion")

		for k in f_list.keys():

			# build fptree from conditional pattern bases:
			cfptree, cheader_table = build_fptree(cpb_all, len(cpb_all), min_spt, k)
			# update the route:
			update_route(route, k, f_list)
			# get conditional pattern bases of new conditional fptree:
			x = get_cpbs(route, cheader_table)
			if not x:
				persist(route, sort_key=FPT.sort_key)
				print("recursion path terminated AND frequent itemsets persisted")
			else:
				cpb_all, f_list = x
				print("continue recursion")
				# current state of route is correct to continue recursion





# updating the route (using example of 'A'):
	# begin at top level
	# loop initialized for its context (loop)
	r0 = Route('', '', '', 0)
	k = 'A'					#  a unique transaction item
	update_route(route_init, k)

		# next level
		# init set to route's val when exit enclosing loop
		for k in f_list.keys():
			# loops twice once for 'B', once for 'D', but
			# route is initialized each time
			route_init = route
			update_route(route_init, k)
