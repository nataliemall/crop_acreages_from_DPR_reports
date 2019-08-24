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



def import_data(year, deficit_irrigation_option):
	overall_ID_table = pd.read_csv('revenue_loss_year_%s_rdi_%s.csv' % (year, deficit_irrigation_option), index_col=0)
	return overall_ID_table 

def plot_dollar_losses(deficit_irrigation_option):

	overall_ID_table = import_data(deficit_irrigation_option)

	n_groups = len(overall_ID_table)

	baseline = overall_ID_table.total_revenue_lost_baseline

	rev_loss_10 = overall_ID_table.total_revenue_lost_10 - baseline

	rev_loss_50 = overall_ID_table.total_revenue_lost_50 - baseline

	rev_loss_75 = overall_ID_table.total_revenue_lost_75 - baseline


	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8
 
	rects_10_af = plt.barh(index, (rev_loss_10 / 1000000), bar_width / 1.5,   # /1000000 for millions of dollars
	                 alpha=opacity,
	                 color='b',
	                 label='Revenue loss with 25% reduction of dry year GW use')

	rects_50_af = plt.barh(index + bar_width, (rev_loss_50 / 1000000) , bar_width / 1.5,  # /1000000 for millions of dollars
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


def plot_losses_as_percent_total_revenue(RDI):

	df1996 = import_data('1996', RDI)
	df2016 = import_data('2016', RDI)

	fig, ax = plt.subplots(figsize=(8.5,6.5))
	index = np.arange(len(df1996))
	bar_width = 0.5

	grays = ['#f7f7f7', '#d9d9d9', '#bdbdbd', '#969696', '#636363', '#252525']
	blues = ['#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#3182bd', '#08519c']
	oranges = ['#feedde', '#fdd0a2', '#fdae6b', '#fd8d3c', '#e6550d', '#a63603']

	for gw in [50, 40, 30, 20, 10]:
		pct_rev_loss = (df1996['total_revenue_lost_%s'%gw] - df1996.total_revenue_lost_baseline) / df1996.baseline_revenue * 100
		plt.barh(index+bar_width+0.2, pct_rev_loss, bar_width/1.5, color=grays[int(gw/10)], label='%s%% Curtailment' % gw)
		plt.barh(index+bar_width+0.2, pct_rev_loss, bar_width/1.5, color=blues[int(gw/10)], label=None)

		pct_rev_loss = (df2016['total_revenue_lost_%s'%gw] - df2016.total_revenue_lost_baseline) / df2016.baseline_revenue * 100
		plt.barh(index+bar_width-0.2, pct_rev_loss, bar_width/1.5, color=oranges[int(gw/10)], label=None)

	# labeling etc
	plt.title('Estimated Revenue Loss from Groundwater Curtailments', fontsize = 17)
	plt.xlabel('Percent revenue loss', fontsize = 14)
	plt.xticks(fontsize = 14)
	plt.xlim(0,100)
	ylabels = df2016.index
	ylabels_test = []

	ylabels_string = list(ylabels)
	for num, district in enumerate(ylabels_string):
		# pdb.set_trace()
		ylabels_string[num] = str(ylabels_string[num].replace("District", "D"))
		ylabels_string[num] = str(ylabels_string[num].replace("Irrigation", "I"))
		ylabels_string[num] = str(ylabels_string[num].replace("Water", "W"))
		ylabels_string[num] = str(ylabels_string[num].replace("Storage", "S"))
		ylabels_string[num] = str(ylabels_string[num].replace("Service", "S"))
		ylabels_string[num] = str(ylabels_string[num].replace("I D", "ID"))
		ylabels_string[num] = str(ylabels_string[num].replace("W D", "WD"))
		ylabels_string[num] = str(ylabels_string[num].replace("W S D", "WSD"))
		ylabels_string[num] = str(ylabels_string[num].replace("e - M", "e\n - M"))  #splits up long name of Wheeler Ridge - Maricopa district 


	plt.yticks(index + bar_width, (ylabels_string), fontsize = 14)
	plt.legend(fontsize = 14)
	 



plot_losses_as_percent_total_revenue(RDI=.4)


plt.tight_layout()
# plt.savefig('figure_drafts/JHbarchart.svg')
plt.show()


