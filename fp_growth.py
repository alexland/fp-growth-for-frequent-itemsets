# !/usr/bin/env python3
# encoding: utf-8


import fptree_build as FPT
import fptree_mine as FPM
import fptree_query as FPQ




if __name__=="__main__":

	configs_filename = "~/Projects/fp-growth-for-frequent-itemsets/config.json"
	configs = FPT.get_configs(configs_filename)
	MIN_SPT = configs['MIN_SPT']
	dataset = FPT.load_data()
	# dataset = load_data(configs['data_file'])
	TRANS_COUNT = len(dataset)
	SORT_KEY=FPT.get_sort_key(dataset)
	fptree, htab = FPT.build_fptree(ataset=dataset, trans_count=TRANS_COUNT,
		min_spt=MIN_SPT, root_node_name='root')


