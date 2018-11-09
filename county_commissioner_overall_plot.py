# county_commissioner_overall_plot.py
### Figure 3 #####


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):


from pur_and_county_data_retrieval import county_commissioner_data

normalized = 1 

county_list = [ 'Fresno_County', 'Tulare_County', 'Kings_County', 'Kern_County']


sum_cc_crop_types = {}  # Creates dictionary for CC data
for num, irrigation_district in enumerate(county_list) : 
	sum_cc_crop_types[irrigation_district] = county_commissioner_data(irrigation_district)

# pdb.set_trace()	
# test = sum_cc_crop_types['Fresno_County'].set_index('year')

county_tree_total = sum_cc_crop_types['Fresno_County'].all_tree_crops + sum_cc_crop_types['Tulare_County'].all_tree_crops \
	+ sum_cc_crop_types['Kings_County'].all_tree_crops + sum_cc_crop_types['Kern_County'].all_tree_crops

county_annual_crops_total = sum_cc_crop_types['Fresno_County'].all_annual_crops + sum_cc_crop_types['Tulare_County'].all_annual_crops \
	+ sum_cc_crop_types['Kings_County'].all_annual_crops + sum_cc_crop_types['Kern_County'].all_annual_crops

# pdb.set_trace()
year_array = np.int64(sum_cc_crop_types['Fresno_County'].year).flatten()

plt.plot(year_array, (county_tree_total.values / 1000000), color = 'g' , label = 'Perennial crops' )
plt.plot(year_array, (county_annual_crops_total.values / 1000000) , color = 'y', label = 'Annual crops')
plt.legend()
plt.title('Crop Acreage Change in Tulare Lake Basin')
plt.xlabel('Year', fontsize = 14)
plt.ylabel('Total area of crops grown (millions of acres)', fontsize = 14 )
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

if not os.path.isdir('figure_drafts'):
    os.mkdir('figure_drafts')
plt.savefig('figure_drafts/cc_crop_acreage_change_tlb', dpi = 300)
pdb.set_trace()
