#!/usr/bin/env python3
# encoding: utf-8

import os
import sys

import pytest

import fptree_config as FPC

import fptree_build as FPT
import fptree_mine as FPM
import fptree_query as FPQ



#----------------------- fixtures --------------------------#


# MIN_SPT = configs['min_support']
# MIN_FREQ_ITEMSET_LENGTH = configs['min_freq_itemset_length']
# dataset = load_data(configs['data_file'])
# TRANS_COUNT = len(dataset)
# TARGET = configs['target']


@pytest.fixture(scope="module")
def fpg_config_6():
	return FPC.get_configs('config-t6.json')


#----------------------- assertions --------------------------#

def test_io_1(fpg_config_6):
	"""
	the fn argument corresponds to a particular fixture object
	"""
	configs = fpg_config_6
	assert configs['min_support'] == 0.2
