#!/usr/bin/env python3
# encoding: utf-8

import os
import sys

import pytest

import fptree_config as FPC

import fptree_build as FPT
import fptree_mine as FPM
import fptree_query as FPQ

#----------------------- parameters --------------------------#

MIN_FREQ_ITEMSET_LENGTH = [3, 4]



#----------------------- fixtures --------------------------#

@pytest.fixture(scope='function', params=[3, 4], autouse=False)
def fpg_config_6(request):
	return FPC.get_configs('config-t6.json')


@pytest.fixture(scope="module")
def myFixture1():
	return 5

@pytest.fixture(scope="module")
def myFixture2():
	return 2


@pytest.fixture(scope='function', params=['p1', 'p2'], ids=None)
def fpg_config_6a(request):
	if request.param == 'p1':
		return request.getfuncargvalue("myFixture1")
	elif request.param == 'p2':
		return request.getfuncargvalue("myFixture2")



#----------------------- predicates --------------------------#

def ex1(x):
	return x**2



#----------------------- assertions --------------------------#


def test_ex2(fpg_config_6a):
	pass



def test_io_1(fpg_config_6):
	"""
	the fn argument corresponds to a particular fixture object
	"""
	configs = fpg_config_6
	assert configs['min_support'] == 0.2


def test_io_1(fpg_config_6):
	configs = fpg_config_6
	configs['min_freq_itemset_length'] = MIN_FREQ_ITEMSET_LENGTH[0]
	assert configs['min_freq_itemset_length'] == 3


def test_fptree_mine_1(fpg_config_6):
	configs = fpg_config_6
	assert configs['target'] == {"ABDF": 5}


@pytest.mark.parametrize("input,expected", [
	( ex1(3), (9) ),
	( ex1(5), (25)),
	])
def test_ex1(input, expected):
	assert input == expected

