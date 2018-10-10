### plotting functions #### 

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



def plot_dataset_comparison(irrigation_district, sum_crop_types, sum_cc_crop_types ): 
    year_list_array = np.arange(1990, 2017)
    fig, ax = plt.subplots()
    linestyles = ['-', '--', '-.', ':']
    # add calPIP data 
    # ax.plot(year_list_array[1:27], tree_acreage_summed_for_year[1:27], color = 'g', linestyle = ':', label = 'calPIP tree crop acreage')
    # ax.plot(year_list_array[1:27], annual_acreage_summed_for_year[1:27], color = 'y', linestyle = ':',  label = 'cal PIP annual crop acreage')
    # ax.plot(year_list_array[1:27], forage_acreage_summed_for_year[1:27], label = 'forage crop acreage')
    ax.set_title(str(irrigation_district + ' Crop Type Changes Dataset Comparison '))
    plt.ylabel('Total acres planted')

    add_droughts = 0 
    if add_droughts == 1 :
        logic_rule = ( (year_list_array > 2010) & (year_list_array < 2016)) # or (year_list_array > 1991 & year_list_array < 1995))  
        collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule), facecolor='orange', alpha=0.3)
        ax.add_collection(collection)
        logic_rule2 =  ( (year_list_array < 1995) & (year_list_array > 1990)  )   
        collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule2), facecolor='orange', alpha=0.3)
        ax.add_collection(collection2)

    try:  # works when un-normalized
        # add calPUR data: 
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops.values
        # pdb.set_trace()
        ax.plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage')
    except: # occurs when data is normalized 
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops_normalized.values
        ax.plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage normalized')

    annual_crop_y_vals = sum_crop_types.all_annual_crops.values
    ax.plot(x_vals, annual_crop_y_vals, color = 'y', label = 'calPUR annual crop acreage')

    # add County Commissioner Data:
    x_vals_cc = sum_cc_crop_types.year.values
    y_vals_tree_cc = sum_cc_crop_types.all_tree_crops.values
    y_vals_annual_cc = sum_cc_crop_types.all_annual_crops.values
    ax.plot(x_vals_cc, y_vals_tree_cc, linestyle = '-.', color = 'g', label = 'County Commissioner tree crop acreage')
    ax.plot(x_vals_cc, y_vals_annual_cc, color = 'y', linestyle = '-.', label = 'County Commissioner annual crop acreage')    

    ax.plot()
    plt.legend()
    plt.savefig(os.path.join(str(irrigation_district), str(irrigation_district) + '_cc_comparison'), dpi = 300)
    # plt.show()

############## end of calPIP dataset functions #################


####### Bar chart creation #########
def surface_water_bar_plot(irrigation_district, sum_crop_types_normalized):
    # pdb.set_trace()
    plt.cla()  #clears the axes for each new graph
    sum_crop_types_normalized.year = np.int64(sum_crop_types_normalized.year)
    sum_crop_types_normalized2 = sum_crop_types_normalized.set_index('year')
    data_2016 = sum_crop_types_normalized2.loc[2016]

    # pdb.set_trace()

    y_min_water_demand = data_2016.minimum_water_demand_for_year
    y_normal_water_demand = data_2016.water_demand_with_2010_AW_values
    plt.hlines(y_normal_water_demand, -1, 2, colors = '#6baed6', label = 'estimated annual water demand')
    plt.hlines(y_min_water_demand, -1, 2, colors = '#08519c', label = 'minimum water demand')

    water_portfolios = pd.read_csv('irrigation_district_water_portfolios.csv', index_col = 'irrigation district')  # 2009 is a normal year 
    wet_year_surface_water = water_portfolios.wet_year_surface_water[irrigation_district]
    wet_year_gw = water_portfolios.wet_year_gw[irrigation_district]
    dry_year_surface_water = water_portfolios.dry_year_surface_water[irrigation_district]
    dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]

    x_labels = ['wet year', 'dry year']
    surface_levels = [wet_year_surface_water, dry_year_surface_water]
    gw_levels = [wet_year_gw, dry_year_gw]

    x_pos = [i for i, _ in enumerate(x_labels)]
    # pdb.set_trace()

    plt.bar(x_pos, gw_levels,  width = 0.5, label = 'Estimated groundwater use', color = '#74c476', bottom = surface_levels)
    plt.bar(x_pos, surface_levels, width = 0.5, label = 'Surface water use', color='#1d91c0')
    plt.legend(loc = "upper right")

    plt.xticks(x_pos, x_labels) 
    plt.title(str('Sample Water Portfolio Changes for ' + str(irrigation_district)))
    plt.ylabel('Annual water volume [acre-feet]')
    # plt.show()
    plt.savefig(str('water_portfolio_figures/' + str(irrigation_district) + ' bar graph'), dpi = 300)
    # pdb.set_trace()

def gw_crop_type_comparison_plot(irrigation_district_list):
    # irrigation_district_list = ['Tulare Irrigation District', 'Cawelo Water District',  'North Kern Water Storage District', 'Lost Hills Water District', 'Lower Tule River Irrigation District', 'Westlands Water District', 'Kern Delta Water District', 'Tulare Lake Basin Water Storage District', 'Delano - Earlimart Irrigation District', 'Wheeler Ridge - Maricopa Water Storage District', 'Semitropic Water Service District', 'Arvin - Edison Water Storage District', 'Shafter - Wasco Irrigation District' ]
    # pdb.set_trace()
    zero_fillers = np.zeros((len(irrigation_district_list), 5))

    district_matrix = pd.DataFrame(zero_fillers, columns = [ 'irrigation_district_name', 'irrigation_district_acronym', 'perennial_annual_ratio', 'gw_surface_percent', 'gw_surface_percent_wet'  ] )
    for num, irrigation_district in enumerate(irrigation_district_list):
        water_portfolios = pd.read_csv('irrigation_district_water_portfolios.csv', index_col = 'irrigation district')
        sum_crop_types_normalized = pd.read_csv(str('calPUR_data_normalized' + str(irrigation_district) + '.csv'), index_col = 'year')
        sum_crop_types_normalized.index = sum_crop_types_normalized.index.astype(int) # convert index years to integers

        perennial_annual_ratio = sum_crop_types_normalized.percent_tree_crops
        dry_year_surface_water = water_portfolios.dry_year_surface_water[irrigation_district]
        dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]
        wet_year_surface_water = water_portfolios.wet_year_surface_water[irrigation_district]
        wet_year_gw = water_portfolios.wet_year_gw[irrigation_district]

        gw_surface_percent = dry_year_surface_water / ( dry_year_gw + dry_year_surface_water) * 100 # surface water as a percent of total, dry year
        gw_surface_percent_wet = wet_year_surface_water / (wet_year_gw + wet_year_surface_water) * 100 
        # pdb.set_trace()
        district_matrix.irrigation_district_name[num] = irrigation_district
        district_matrix.irrigation_district_acronym[num] = water_portfolios.irrigation_district_acronym[irrigation_district]
        district_matrix.perennial_annual_ratio[num] = perennial_annual_ratio[2016]
        district_matrix.gw_surface_percent[num] = gw_surface_percent
        district_matrix.gw_surface_percent_wet[num] = gw_surface_percent_wet

        point_size = np.sqrt((water_portfolios.irrigated_acreage.values) )  # square root since marker size is ^2
        # point_size
    # pdb.set_trace()        

    fig, ax = plt.subplots()
    ax.scatter(district_matrix.perennial_annual_ratio, district_matrix.gw_surface_percent, color = 'green', s = point_size, alpha = 0.7 )
    plt.hlines(50, 0, 100, colors = '#6baed6', label = 'test')
    plt.vlines(50, 0, 100, colors = '#08519c', label = 'test vline')
    plt.xlabel('Percentage of perennial crops in irrigation district')
    plt.ylabel('Surface water as a percent of total agricultural water use within the irrigation district')
    # pdb.set_trace()
    nn_old = irrigation_district_list
    nn = water_portfolios.irrigation_district_acronym.tolist()
    nn = district_matrix.irrigation_district_acronym.tolist()
    pdb.set_trace()

    for i, txt in enumerate(nn):
        text_x_coord = district_matrix.perennial_annual_ratio[i] - 3
        text_y_coord = district_matrix.gw_surface_percent[i] + 0.1
        ax.annotate(txt, (district_matrix.perennial_annual_ratio[i], district_matrix.gw_surface_percent[i] ), xycoords='data',
                  xytext=(text_x_coord, text_y_coord), textcoords='data',
                  size=10, va="center", ha="center",
                   ) # bbox=dict(boxstyle="round4", fc="w"),
        # pdb.set_trace()
    ax.scatter(district_matrix.perennial_annual_ratio, district_matrix.gw_surface_percent_wet, color = 'orange' , s = point_size, alpha = 0.7 )

    plt.show()
    pdb.set_trace()


def plot_data_for_irrigation_district(irrigation_district, sum_crop_types, normalized):

    # pdb.set_trace()
    if normalized == 0:
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops.values
    if normalized == 1:
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops_normalized.values

    plt.plot(x_vals, y_vals)
    plt.xlabel('year')
    plt.ylabel('Acres of tree crop')
    plt.title(str(irrigation_district))
    plt.show()

def plot_tree_crop_percentages_for_irrigation_district(irrigation_district, sum_crop_types):
    # pdb.set_trace()
    year_array = np.int64(sum_crop_types.year.values)
    year_array_flattened = year_array.flatten()
    x_vals2 = pd.to_datetime(year_array_flattened, format='%Y')
    y_vals = sum_crop_types.percent_tree_crops.values
    plt.plot(x_vals2, y_vals)
    plt.xlabel('year')
    plt.ylabel('Percentage of calPIP permitted acreage that is tree crop')
    plt.title(str(irrigation_district))
    plt.show()  

def plot_water_demand_graph(sum_crop_types_normalized, irrigation_district):
    plt.figure()
    # pdb.set_trace()
    x_vals = sum_crop_types_normalized.year.values
    y_vals = sum_crop_types_normalized.water_demand_with_2010_AW_values.values

    # y_vals_changing = sum_crop_types_normalized.water_demand_with_changing_AW_values.values
    plt.xlabel('year')
    plt.ylabel('CalPUR estimated water demand [acre-feet]')
    plt.title(str( 'Estimated yearly water demand for ' + str(irrigation_district) ) )
    plt.plot(x_vals, y_vals, color = 'g', label = 'calPUR crop total estimated water demand from 2010 AW value')

    # # pdb.set_trace()
    # x_vals_changing = x_vals[24:37]
    # y_vals_changing = sum_crop_types_normalized.water_demand_with_changing_AW_values.values[24:37]
    # plt.plot(x_vals_changing, y_vals_changing, color = 'b', label = 'calPUR crop total estimated AW from 1998 - 2010 DWR data')
    
    x_vals_min = sum_crop_types_normalized.year.values
    y_vals_min = sum_crop_types_normalized.minimum_water_demand_for_year.values
    plt.plot(x_vals_min, y_vals_min, color = 'r', label = 'minimum required applied water for permanent crop survival')


    y_max = max(y_vals)
    # pdb.set_trace()
    plt.ylim(0 , y_max)
    plt.legend()
    plt.show()

def plot_acreage_and_demand_side_by_side(irrigation_district, sum_crop_types_normalized, normalized):
    '''Creates plot sharing x-axis (years) '''
    # Two subplots, the axes array is 1-d

    ## water demand values
    x_vals = sum_crop_types_normalized.year.values
    y_vals = sum_crop_types_normalized.water_demand_with_2010_AW_values.values

    y_vals_min = sum_crop_types_normalized.minimum_water_demand_for_year.values
    ## Acreage values 
    x_acreage_vals = sum_crop_types_normalized.year.values
    y_acreage_vals = sum_crop_types_normalized.all_tree_crops_normalized.values
    annual_crop_y_vals = sum_crop_types_normalized.all_annual_crops.values

    f, axarr = plt.subplots(2, sharex=True)
    # plt.ylabel('Crop Acreage')
    axarr[0].plot(x_acreage_vals, y_acreage_vals, color = 'g', label = 'cal PUR Tree crop acreage')
    axarr[0].plot(x_acreage_vals, annual_crop_y_vals, color = 'y', label = 'calPUR annual crop acreage')
    plt.legend(handles=[axarr[0]])  ## These labels don't show up 
    axarr[0].set_title(str(irrigation_district))
    # axarr[0].xlabel('year')
    # axarr[0].ylabel('Crop Acreage')
    # plt.ylabel('Estimated water demand')
    # for ax in axarr.flat:
    #     pdb.set_trace()
    #     ax.set(xlabel='x-label', ylabel='y-label')
    axarr.flat[0].set(xlabel='Year', ylabel='Crop Acreage')
    axarr.flat[1].set(xlabel='Year', ylabel='Water Demand (Acre-feet)')
    axarr[1].plot(x_vals, y_vals, color = 'b', label = 'Estimated water demand')
    axarr[1].plot(x_vals, y_vals_min, color = 'r', label = 'Estimated minimum perennial water demand')
    # plt.savefig(irrigation_district_time_series_figures '')
    plt.ylim(ymin = 0 )

    plt.savefig(str('irrigation_district_time_series_figures/' + str(irrigation_district) + ' time_series'), dpi = 300)
    # plt.show()

def plot_all_the_irrigation_district_bar_charts(irrigation_district_list):
    ## run a loop 

    for irrigation_district in irrigation_district_list:
        # sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist = retrieve_data_for_irrigation_district(irrigation_district, normalized)
        sum_crop_types_normalized = pd.read_csv(str('calPUR_data_normalized' + str(irrigation_district) + '.csv'))
        surface_water_bar_plot(irrigation_district, sum_crop_types_normalized)



