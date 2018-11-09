# plot_district_water_portfolios.py 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):

from pur_and_county_data_retrieval import retrieve_data_for_irrigation_district


# def surface_water_bar_plot(irrigation_district, sum_crop_types_normalized):
#     # pdb.set_trace()
#     plt.cla()  #clears the axes for each new graph
#     sum_crop_types_normalized.year = np.int64(sum_crop_types_normalized.year)
#     sum_crop_types_normalized2 = sum_crop_types_normalized.set_index('year')
#     data_2016 = sum_crop_types_normalized2.loc[2016]

#     y_min_water_demand = data_2016.minimum_water_demand_for_year
#     y_normal_water_demand = data_2016.water_demand_with_2010_AW_values
#     plt.hlines(y_normal_water_demand, -1, 2, colors = '#6baed6', label = 'estimated annual water demand')
#     plt.hlines(y_min_water_demand, -1, 2, colors = '#08519c', label = 'minimum water demand')

#     water_portfolios = pd.read_csv('irrigation_district_water_portfolios.csv', index_col = 'irrigation district')  # 2009 is a normal year 
#     wet_year_surface_water = water_portfolios.wet_year_surface_water[irrigation_district]
#     wet_year_gw = water_portfolios.wet_year_gw[irrigation_district]
#     dry_year_surface_water = water_portfolios.dry_year_surface_water[irrigation_district]
#     dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]

#     x_labels = ['wet year', 'dry year']
#     surface_levels = [wet_year_surface_water, dry_year_surface_water]
#     gw_levels = [wet_year_gw, dry_year_gw]

#     x_pos = [i for i, _ in enumerate(x_labels)]
#     # pdb.set_trace()

#     plt.bar(x_pos, gw_levels,  width = 0.5, label = 'Estimated groundwater use', color = '#74c476', bottom = surface_levels)
#     plt.bar(x_pos, surface_levels, width = 0.5, label = 'Surface water use', color='#1d91c0')
#     plt.legend(loc = "upper right")

#     plt.xticks(x_pos, x_labels) 
#     plt.title(str(irrigation_district))
#     plt.ylabel('Annual water volume [acre-feet]')
#     # plt.show()
#     plt.savefig(str('water_portfolio_figures/' + str(irrigation_district) + ' bar graph'), dpi = 300)

def subplots_dataset_comparison(irrigation_district, sum_crop_types, num , fig, ax , high_perennials ): 
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

    sum_crop_types.year = np.int64(sum_crop_types.year)
    sum_crop_types_normalized2 = sum_crop_types.set_index('year')
    data_2016 = sum_crop_types_normalized2.loc[2016]

    y_min_water_demand = data_2016.deficit_irrigation_water_demand_for_year /1000 # converted to TAF
    y_normal_water_demand = data_2016.water_demand_with_2010_AW_values / 1000 # converted to TAF
    y_perennial_demand = data_2016.perennial_irrigation_water_demand_for_year / 1000 

    ax[row, column].hlines(y_normal_water_demand, -1, 2, colors = '#9ecae1', label = 'Estimated total water demand')
    ax[row, column].hlines(y_perennial_demand, -1, 2, colors = '#4292c6', label = 'Water demand with perennial irrigation only')
    ax[row, column].hlines(y_min_water_demand, -1, 2, colors = '#084594', label = 'Water demand with deficit irrigation')

    water_portfolios = pd.read_csv('irrigation_district_water_portfolios.csv', index_col = 'irrigation district' )  # 2009 is a normal year 
    wet_year_surface_water = water_portfolios.wet_year_surface_water[irrigation_district]
    wet_year_gw = water_portfolios.wet_year_gw[irrigation_district]
    dry_year_surface_water = water_portfolios.dry_year_surface_water[irrigation_district]
    dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]

    try:
        dry_year_label = np.int64(water_portfolios.sample_dry_year[irrigation_district])
    except: 
        # pdb.set_trace()
        dry_year_label = str(water_portfolios.sample_dry_year[irrigation_district])

    try:
        wet_year_label = np.int64(water_portfolios.sample_wet_year[irrigation_district])
    except:
        # pdb.set_trace()
        wet_year_label = str(water_portfolios.sample_wet_year[irrigation_district])

    x_labels = [str('wet year ('+ str(wet_year_label) + ')' ),   str( 'dry year (' + str(dry_year_label) + ')' )]
    surface_levels = [ (wet_year_surface_water / 1000) , (dry_year_surface_water/1000 )]  # divide by 1000 to convert to TAF
    gw_levels = [(wet_year_gw/ 1000), (dry_year_gw/ 1000) ]  # divide by 1000 to convert to TAF

    x_pos = [i for i, _ in enumerate(x_labels)]
    # pdb.set_trace()

    ax[row, column].bar(x_pos, gw_levels ,  width = 0.5, label = 'Estimated groundwater use', color = '#74c476', bottom = surface_levels)
    ax[row, column].bar(x_pos, surface_levels, width = 0.5, label = 'Surface water use', color='#1d91c0')
    # plt.legend(loc = "upper right")

    ax[row, column].set_xticks(x_pos, minor = False)
    ax[row, column].set_xticklabels(x_labels) 
    ax[row, column].set_title(str(irrigation_district), fontsize = 14 )
    # ax[row, column].ylabel('Annual water volume [acre-feet]')
    # plt.show()
    # plt.savefig(str('water_portfolio_figures/' + str(irrigation_district) + ' bar graph'), dpi = 300)

    # pdb.set_trace()
    # add_droughts = 0
    # if add_droughts == 1 :
    #     logic_rule = ( (year_list_array > 2010) & (year_list_array < 2016)) # or (year_list_array > 1991 & year_list_array < 1995))  
    #     collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule), facecolor='orange', alpha=0.3)
    #     ax[row, column].add_collection(collection)
    #     logic_rule2 =  ( (year_list_array < 1995) & (year_list_array > 1990)  )   
    #     collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule2), facecolor='orange', alpha=0.3)
    #     ax[row, column].add_collection(collection2)

    # x_vals = sum_crop_types.year.values
    # y_vals = sum_crop_types.all_tree_crops_normalized.values
    # ax[row, column].plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage normalized')

    # annual_crop_y_vals = sum_crop_types.all_annual_crops.values
    # # pdb.set_trace()

    # ax[row, column].plot(x_vals, annual_crop_y_vals, color = 'y', label = 'calPUR annual crop acreage')

    # add County Commissioner Data:
    # x_vals_cc = sum_cc_crop_types.year.values
    # y_vals_tree_cc = sum_cc_crop_types.all_tree_crops.values
    # y_vals_annual_cc = sum_cc_crop_types.all_annual_crops.values
    # ax[row, column].plot(x_vals_cc, y_vals_tree_cc, linestyle = '-.', color = 'g', label = 'County Commissioner tree crop acreage')
    # ax[row, column].plot(x_vals_cc, y_vals_annual_cc, color = 'y', linestyle = '-.', label = 'County Commissioner annual crop acreage')    

    # ax[row, column].plot()
    if num == 1:
        # ax[row, column].legend(loc = 0)  # places legend in best location 
        if high_perennials == 0 | high_perennials == 1:
            ax[row, column].legend(loc = "lower left")
        else:
            ax[row, column].legend(loc = "lower right")




retrieve_data = 0
normalized = 1
high_perennials = 2  # 1 = mostly perennials, 0 = mostly annuals, 2 = switched 

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

if high_perennials == 0:    # mostly annuals 
    irrigation_district_list = [
        'Tulare Lake Basin Water Storage District',
        'Tulare Irrigation District',
        'Westlands Water District',
        'Kern Delta Water District']

if high_perennials == 1:  # mostly perennials
    irrigation_district_list = [
        'Cawelo Water District', 
        'Orange Cove Irrigation District',
        'Lindmore Irrigation District',
        'Fresno Irrigation District'] 


if high_perennials == 2:   # shifted 
    irrigation_district_list = [
        'Wheeler Ridge - Maricopa Water Storage District',
        'Lost Hills Water District',
        'Semitropic Water Service District',
        'Shafter - Wasco Irrigation District'] 

if high_perennials == 3:    # extra
    irrigation_district_list = [
        'James Irrigation District',
        'Firebaugh Canal Company',
        'Lindmore Irrigation District',
        'Arvin - Edison Water Storage District'] 


if high_perennials == 4:    # more extra
    irrigation_district_list = [
        'Pixley Irrigation District',  # mostly annuals
        'Riverdale Irrigation District',   # mostly annuals 
        'Consolidated Irrigation District',   # mostly perennials
        'Buena Vista Water Storage District']   # switches at the end 

if high_perennials == 5:    # even more extra
    irrigation_district_list = [
        'Kern Delta Water District',        
        'Delano - Earlimart Irrigation District',
        'North Kern Water Storage District',
        'Berrenda Mesa Water District']

if high_perennials == 6:    # even more extra
    irrigation_district_list = [
        'Kern - Tulare Water District',       
        'Corcoran Irrigation District',
        'Dudley Ridge Water District',
        'Kings River Water District',]

if high_perennials == 7:    # even more extra
    irrigation_district_list = [
        'Alta Irrigation District',      
        'Lower Tule River Irrigation District',
        'Dudley Ridge Water District',
        'Kings River Water District',]

if retrieve_data == 1: 
    for irrigation_district in irrigation_district_list: 
        if not os.path.isdir(str(irrigation_district)):  # creates this folder 
            os.mkdir(str(irrigation_district))

        sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist = retrieve_data_for_irrigation_district(irrigation_district, normalized)

# pdb.set_trace()

fig, ax = plt.subplots(2,2, sharex = False)
if high_perennials == 1:
    plt.suptitle('Sample Water Portfolios for Irrigation Districts with Primarily Perennial Crops', fontsize=14)
if high_perennials == 0: 
    plt.suptitle('Sample Water Portfolios for Irrigation Districts with Primarily Annual Crops', fontsize=14)
if high_perennials == 2:
    plt.suptitle('Sample Water Portfolios for Irrigation Districts with Shift to Perennial Crops', fontsize=14)

fig.text(0.5, 0.04, 'Year Type', ha='center', fontsize = 16 )
fig.text(0.04, 0.5, 'Annual water volume [TAF]', va='center', rotation='vertical', fontsize=16)

# pdb.set_trace()
sum_crop_types_each_county = {}

for num, irrigation_district in enumerate(irrigation_district_list): 
    sum_crop_types_each_county[irrigation_district] = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
    subplots_dataset_comparison(irrigation_district, sum_crop_types_each_county[irrigation_district], num , fig, ax , high_perennials )

if not os.path.isdir('figure_drafts'):
    os.mkdir('figure_drafts')

if high_perennials == 1:
    plt.savefig('figure_drafts/water_portfolios_high_perennial', dpi = 300)
if high_perennials == 0: 
    plt.savefig('figure_drafts/water_portfolios_high_annual', dpi = 300)
if high_perennials == 2:
    plt.savefig('figure_drafts/water_portfolios_shifted', dpi = 300)


plt.show()

# pdb.set_trace()




