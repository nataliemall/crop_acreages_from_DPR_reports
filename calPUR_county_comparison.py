# calPUR_county_comparison.py

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):


from pur_and_county_data_retrieval import retrieve_data_for_irrigation_district
from pur_and_county_data_retrieval import county_commissioner_data
from plotting_functions import plot_dataset_comparison


def subplots_dataset_comparison(irrigation_district, sum_crop_types, sum_cc_crop_types, num , fig, ax  ): 
    year_list_array = np.arange(1990, 2017)
    linestyles = ['-', '--', '-.', ':']
    # pdb.set_trace()
    row = 1
    column = 1 
    if (num == 0) | (num == 1) :
        row = 0 
    if (num  == 0) | (num == 2):
        column = 0 

    irrigation_district_title = irrigation_district.replace("_", " ")
    ax[row, column].set_title(irrigation_district_title)

    # pdb.set_trace()
    add_droughts = 0
    if add_droughts == 1 :
        logic_rule = ( (year_list_array > 2010) & (year_list_array < 2016)) # or (year_list_array > 1991 & year_list_array < 1995))  
        collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule), facecolor='orange', alpha=0.3)
        ax[row, column].add_collection(collection)
        logic_rule2 =  ( (year_list_array < 1995) & (year_list_array > 1990)  )   
        collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule2), facecolor='orange', alpha=0.3)
        ax[row, column].add_collection(collection2)

    x_vals = sum_crop_types.year.values
    y_vals = sum_crop_types.all_tree_crops_normalized.values
    ax[row, column].plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage normalized')

    annual_crop_y_vals = sum_crop_types.all_annual_crops.values
    # pdb.set_trace()

    ax[row, column].plot(x_vals, annual_crop_y_vals, color = 'y', label = 'calPUR annual crop acreage')

    # add County Commissioner Data:
    x_vals_cc = sum_cc_crop_types.year.values
    y_vals_tree_cc = sum_cc_crop_types.all_tree_crops.values
    y_vals_annual_cc = sum_cc_crop_types.all_annual_crops.values
    ax[row, column].plot(x_vals_cc, y_vals_tree_cc, linestyle = '-.', color = 'g', label = 'County Commissioner tree crop acreage')
    ax[row, column].plot(x_vals_cc, y_vals_annual_cc, color = 'y', linestyle = '-.', label = 'County Commissioner annual crop acreage')    

    # ax[row, column].plot()
    if num == 1:
        ax[row, column].legend(loc = 0)  # places legend in best location 




retrieve_data = 1
normalized = 1 

county_list = [ 'Fresno_County', 'Tulare_County', 'Kings_County', 'Kern_County']

if retrieve_data == 1: 
    for irrigation_district in county_list: 
        if not os.path.isdir(str(irrigation_district)):  # creates this folder 
            os.mkdir(str(irrigation_district))

        sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist = retrieve_data_for_irrigation_district(irrigation_district, normalized)

fig, ax = plt.subplots(2,2, sharex = True)
plt.suptitle('Comparison of calPUR and County Commissioner Datasets', fontsize=14)
fig.text(0.5, 0.04, 'Year', ha='center')
fig.text(0.04, 0.5, 'Crop acreage within county [acres]', va='center', rotation='vertical')

sum_crop_types_each_county = {}
sum_cc_crop_types = {}
for num, irrigation_district in enumerate(county_list) : 
    sum_crop_types_each_county[irrigation_district] = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
    sum_cc_crop_types[irrigation_district] = county_commissioner_data(irrigation_district)        
    subplots_dataset_comparison(irrigation_district, sum_crop_types_each_county[irrigation_district], sum_cc_crop_types[irrigation_district] , num, fig, ax )
    # pdb.set_trace()


# pdb.set_trace()
if not os.path.isdir('figure_drafts'):
    os.mkdir('figure_drafts')
plt.savefig('figure_drafts/calPUR_CC_comparison', dpi = 300)
plt.show()

pdb.set_trace()




