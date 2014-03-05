#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import re
import csv as CSV
from copy import deepcopy
from operator import itemgetter
import json as JSON

from redis import StrictRedis as Redis



def get_configs(fname, configs_dir=os.path.abspath('tests/configs_test/')):
	config_file = os.path.join(configs_dir, fname)
	with open(config_file, 'r', encoding='utf-8') as fh:
		return JSON.load(fh)


def load_data(dfile=None, max_transactions=250):
	import random as RND
	if dfile and dfile.endswith('.csv'):
		with open(dfile, 'r', encoding='utf-8') as fh:
 			reader = CSV.reader(fh)
 			return [line for line in reader]

	elif dfile and not dfile.endswith('.csv'):
		with open(dfile, "r", encoding="utf-8") as fh:
			data = [ line.strip().split(' ') for line in fh.readlines()
				if not line.startswith('#') ]
			RND.shuffle(data)
			data = data[:max_transactions]
	else:
		import string
		import random as RND
		p = list(string.ascii_uppercase[:20])
		fnx = lambda: RND.randint(2, 10)
		data = [ RND.sample(p, fnx()) for c in range(100000) ]
		RND.shuffle(data)
		if max_transactions & max_transactions < len(data):
			return data[:max_transactions]
		else:
			return data


def db_connect(db_id, port, host):
	return Redis(db=db_id, port=port, host=host)