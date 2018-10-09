# plot_district_crop_changes.py 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):

from pur_and_county_data_retrieval import retrieve_data_for_irrigation_district


def subplots_dataset_comparison(irrigation_district, sum_crop_types, num , fig, ax  ): 
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

    # # Add water demand data
    # x_vals = sum_crop_types.year.values
    # y_vals = sum_crop_types.all_tree_crops_normalized.values
    # ax[row, column].plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage normalized')

    # annual_crop_y_vals = sum_crop_types.all_annual_crops.values
    # # pdb.set_trace()

    # ax[row, column].plot(x_vals, annual_crop_y_vals, color = 'y', label = 'calPUR annual crop acreage')

    # add minimum water demand Data:
    x_vals_min = sum_crop_types.year.values
    y_vals_min = sum_crop_types.minimum_water_demand_for_year.values / 1000 # convert to TAF
    y_vals_estimated = sum_crop_types.water_demand_with_2010_AW_values.values / 1000 # convert to TAF
    ax[row, column].plot(x_vals_min, y_vals_min, color = '#41b6c4', label = 'Minimum water required for perennial crop survival')
    ax[row, column].plot(x_vals_min, y_vals_estimated, color = '#225ea8', label = 'Estimated water demand')    
    ax[row, column].set_ylim(0)
    # ax[row, column].plot()
    if num == 1:
        ax[row, column].legend(loc = 0)  # places legend in best location 





retrieve_data = 0
normalized = 1
high_perennials = 0   # 1 = mostly perennials, 0 = mostly annuals, 2 = switched 

# irrigation_district_list = [
#     'Tulare Irrigation District',
#     'Cawelo Water District',
#     'Lost Hills Water District',
#     'Lower Tule River Irrigation District',
#     'Westlands Water District',
#     'Kern Delta Water District',
#     'Tulare Lake Basin Water Storage District',
#     'Delano - Earlimart Irrigation District',
#     'Wheeler Ridge - Maricopa Water Storage District',
#     'Semitropic Water Service District',
#     'Arvin - Edison Water Storage District',
#     'Shafter - Wasco Irrigation District',
#     'North Kern Water Storage District',
#     'Kern - Tulare Water District',
#     'Buena Vista Water Storage District',
#     'Alta Irrigation District',
#     'Berrenda Mesa Water District',
#     'Consolidated Irrigation District',
#     'Corcoran Irrigation District',
#     'Fresno Irrigation District',
#     'Orange Cove Irrigation District',
#     'Panoche Water District',
#     'Pixley Irrigation District',
#     'Riverdale Irrigation District',
#     'Kings River Water District',
#     'Lindmore Irrigation District',
#     'James Irrigation District',
#     'Firebaugh Canal Company',
#     'Dudley Ridge Water District'] 

if high_perennials == 1:
    irrigation_district_list = [
        'Orange Cove Irrigation District',
        'Cawelo Water District',
        'Cawelo Water District',
        'Fresno Irrigation District'] 

if high_perennials == 0:
    irrigation_district_list = [
        'Tulare Irrigation District',
        'Tulare Lake Basin Water Storage District',
        'Westlands Water District',
        'Panoche Water District']

if high_perennials == 2:
    irrigation_district_list = [
        'Wheeler Ridge - Maricopa Water Storage District',
        'Semitropic Water Service District',
        'Lost Hills Water District',
        'Shafter - Wasco Irrigation District'] 


if retrieve_data == 1: 
    for irrigation_district in irrigation_district_list: 
        if not os.path.isdir(str(irrigation_district)):  # creates this folder 
            os.mkdir(str(irrigation_district))

        sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district(irrigation_district, normalized)

fig, ax = plt.subplots(2,2, sharex = True)
if high_perennials == 1:
    plt.suptitle('Water Demand for Irrigation Districts with Primarily Perennial Crops', fontsize=14)
if high_perennials == 0: 
    plt.suptitle('Water Demand for Irrigation Districts with Primarily Annual Crops', fontsize=14)
if high_perennials == 2:
    plt.suptitle('Water Demand for Irrigation Districts with Shift to Perennial Crops', fontsize=14)

fig.text(0.5, 0.04, 'Year', ha='center')
fig.text(0.04, 0.5, 'Agriculatural water demand within irrigation district (TAF)', va='center', rotation='vertical')

# pdb.set_trace()
sum_crop_types_each_county = {}

for num, irrigation_district in enumerate(irrigation_district_list): 
    sum_crop_types_each_county[irrigation_district] = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
    subplots_dataset_comparison(irrigation_district, sum_crop_types_each_county[irrigation_district], num , fig, ax  )


if not os.path.isdir('figure_drafts'):
    os.mkdir('figure_drafts')

if high_perennials == 1:
    plt.savefig('figure_drafts/water_demand_high_perennial_comparison', dpi = 300)
if high_perennials == 0: 
    plt.savefig('figure_drafts/water_demand_high_annual_comparison', dpi = 300)
if high_perennials == 2:
    plt.savefig('figure_drafts/water_shift_comparison', dpi = 300)
plt.show()

pdb.set_trace()
