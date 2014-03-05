#!/usr/bin/env python3
# encoding: utf-8

import pytest

import fptree_build as FPT
import fptree_query as FPQ

dataset = [
	    ['E', 'B', 'D', 'A'],
		['E', 'A', 'D', 'C', 'B'],
		['C', 'E', 'B', 'A'],
		['A', 'B', 'D'],
		['D'],
		['D', 'B'],
		['D', 'A', 'E'],
		['B', 'C'],
	]


def fn(x):
	return x**2

def test_2():
	assert fn(4) == 16