### Create bar chart from crop_loss_calcs ###  

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
import seaborn as sns
import re 
from tqdm import tqdm  # for something in tqdm(something something):
import unittest



def import_data(deficit_irrigation_option):
	if deficit_irrigation_option == 1:
		overall_ID_table = pd.read_csv('deficit_irrigation_option_revenue_loss_estimates.csv', index_col = [0])  # import deficit irrigation data 
	else:
		overall_ID_table =pd.read_csv('overall_irrigation_district_revenue_loss_estimates_to_graph.csv', index_col = [0])  # import data 

	return overall_ID_table 

def plot_dollar_losses(deficit_irrigation_option):

	overall_ID_table = import_data(deficit_irrigation_option)

	n_groups = len(overall_ID_table)

	baseline_curtailment_rev_loss = overall_ID_table.total_revenue_lost_baseline

	rev_loss_25_gw_reduction = overall_ID_table.total_revenue_lost_25 - baseline_curtailment_rev_loss

	rev_loss_50_gw_reduction = overall_ID_table.total_revenue_lost_50 - baseline_curtailment_rev_loss

	rev_loss_75_gw_reduction = overall_ID_table.total_revenue_lost_75 - baseline_curtailment_rev_loss


	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8
 
	rects_25_af = plt.barh(index, (rev_loss_25_gw_reduction / 1000000), bar_width / 1.5,   # /1000000 for millions of dollars
	                 alpha=opacity,
	                 color='b',
	                 label='Revenue loss with 25% reduction of dry year GW use')

	rects_50_af = plt.barh(index + bar_width, (rev_loss_50_gw_reduction / 1000000) , bar_width / 1.5,  # /1000000 for millions of dollars
	                 alpha=opacity,
	                 color='g',
	                 label='Revenue loss with 50% reduction of dry year GW use')

	plt.xlabel('Revenue loss, millions of dollars')

	if deficit_irrigation_option == 1:
		plt.title('Revenue Loss for Irrigation Districts Utilizing Regulated Deficiency Irrigation')
	else:
		plt.title('Economic Analysis of Revenue Loss for Irrigation Districts')
	plt.yticks(index + bar_width, (overall_ID_table.index))

	plt.legend()
	 
	plt.tight_layout()
	plt.show()


def plot_losses_as_percent_total_revenue(deficit_irrigation_option):

	overall_ID_table = import_data(deficit_irrigation_option)

	n_groups = len(overall_ID_table)

	baseline_curtailment_rev_loss = overall_ID_table.total_revenue_lost_baseline
	rev_loss_25_gw_reduction = overall_ID_table.total_revenue_lost_25 - baseline_curtailment_rev_loss
	rev_loss_50_gw_reduction = overall_ID_table.total_revenue_lost_50 - baseline_curtailment_rev_loss
	rev_loss_75_gw_reduction = overall_ID_table.total_revenue_lost_75 - baseline_curtailment_rev_loss

	# percentages 
	percent_rev_loss_at_25 = rev_loss_25_gw_reduction / overall_ID_table.baseline_revenue * 100
	percent_rev_loss_at_50 = rev_loss_50_gw_reduction / overall_ID_table.baseline_revenue * 100
	percent_rev_loss_at_75 = rev_loss_75_gw_reduction / overall_ID_table.baseline_revenue * 100

	pdb.set_trace()
	print('check out rev loss values here')

	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8
 
	rects_25_af = plt.barh(index + bar_width, percent_rev_loss_at_25, bar_width / 1.5,   # percent of total ag revenue
	                 alpha=opacity,
	                 color='orange',
	                 label='Percent revenue loss with 25% reduction in GW use')

	rects_50_af = plt.barh(index + 2* bar_width, percent_rev_loss_at_50 , bar_width / 1.5,  # percent of total ag revenue
	                 alpha=opacity,
	                 color='r',
	                 label='Percent revenue loss with 50% of dry year GW use')

	if deficit_irrigation_option == 1:
		plt.title('Economic Analysis of Revenue Loss for Irrigation Districts Utilizing Deficit Irrigation')
	else:
		plt.title('Economic Analysis of Revenue Loss for Irrigation Districts')


	plt.xlabel('Percent revenue loss')
	plt.xlim(0,100)
	plt.yticks(index + bar_width, (overall_ID_table.index))
	# pdb.set_trace()
	plt.legend()
	 
	# plt.tight_layout()
	plt.show()



deficit_irrigation_option = 0


plot_dollar_losses(deficit_irrigation_option)
plot_losses_as_percent_total_revenue(deficit_irrigation_option)








pdb.set_trace()