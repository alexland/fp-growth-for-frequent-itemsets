# encoding: utf-8

import pytest


#------------------ content of test_strings.py ---------------#
def test_compute(param1): 
	assert param1 < 4
	
	
#---------------- content of conftest.py ----------------#

def pytest_addoption(parser): 
	parser.addoption("--stringinput", action="append", default=[], help="list of str inputs for test fns")
	
	
def pytest_generate_tests(metafunc):
	if 'stringinput' in metafunc.fixturenames:
		metafunc.paramaterize("stringinput", metafunc.config.option.stringinput)
		