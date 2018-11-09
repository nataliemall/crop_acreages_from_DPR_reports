### Data compilation and plotting for a specific region ###  

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


def read_and_sort_site_codes():

    # irrigation_district_comtrs_list = os.path.join('irrigation_districts_with_comtrs', irrigation_district + '.csv')
    # try:
    #     comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_comtrs_list, usecols = ['co_mtrs'])
    # except:
    #     comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_comtrs_list, usecols = ['CO_MTRS']) 

    crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1974,2017)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    # crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    crop_list_normalized = [ 'year', 'all_tree_crops_normalized', 'all_annual_crops', 'all_crops', 'percent_tree_crops', 'water_demand_with_2010_AW_values', 'deficit_irrigation_water_demand_for_year', 'perennial_irrigation_water_demand_for_year']
    df_shape_normalized = (len(range(1974,2017)), len(crop_list_normalized))
    zero_fillers_normalized = np.zeros(df_shape_normalized)
    sum_crop_types_normalized = pd.DataFrame(zero_fillers_normalized, columns = [ crop_list_normalized ] )

    # pdb.set_trace()

    codes_pre_1990 = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['site_code_pre_1990', 'site_name_pre_1990', 'is_orchard_crop_pre_1990', 'is_annual_crop_pre_1990', 'is_forage_pre_1990', 'applied_water_category_pre_1990']) # , index_col = 0)
    codes_1990_2016 = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['site_code_1990_2016', 'site_name_1990_2016', 'is_orchard_crop_1990_2016', 'is_annual_crop_1990_2016', 'is_forage_1990_2016', 'applied_water_category_1990_2016']) #, index_col = 0)
    HR_2010_AW_Data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', 'AW_HR_2010'])
    HR_min_data = pd.read_csv('site_codes_with_crop_types.csv', names = ['crop_name_HR_2010', 'AW_HR_2010_min'])
    # # as shown on table 'sites_1990-2016' from PUR downloaded dataset 

    tree_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_orchard_crop_pre_1990 == 1]

    # name lists 
    tree_crops_names_pre_1990 = codes_pre_1990.site_name_pre_1990.loc[codes_pre_1990.is_orchard_crop_pre_1990 == 1]
    annual_crops_names_pre_1990 = codes_pre_1990.site_name_pre_1990.loc[codes_pre_1990.is_annual_crop_pre_1990 == 1]
    tree_crops_names_1990_2016 = codes_1990_2016.site_name_1990_2016.loc[codes_1990_2016.is_orchard_crop_1990_2016 == 1]
    annual_crops_names_1990_2016 = codes_1990_2016.site_name_1990_2016.loc[codes_1990_2016.is_annual_crop_1990_2016 == 1]

    tree_crops_names_pre_1990.to_csv('tree_crops_pre_1990_list.csv', index = False)
    annual_crops_names_pre_1990.to_csv('field_crops_pre_1990_list.csv', index = False)
    tree_crops_names_1990_2016.to_csv('tree_crops_post_1990_list.csv', index = False)
    annual_crops_names_1990_2016.to_csv('field_crops_post_1990_list.csv', index = False)


    pdb.set_trace()

    # tree_crops_pre_1990 = [str(round(i)) for i in tree_crops_pre_1990]

    # tree_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_orchard_crop_1990_2016 == 1]
    # tree_crops_1990_2016_list = tree_crops_1990_2016.values.tolist()  # why necessary?  
    # tree_crops_1990_2016 = [str(round(i)) for i in tree_crops_1990_2016_list]

    # # pdb.set_trace()

    # forage_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_forage_pre_1990 == 1]
    # forage_crops_pre_1990 = [str(round(i)) for i in forage_crops_pre_1990]

    # forage_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_forage_1990_2016 == 1]
    # forage_crops_1990_2016_list = forage_crops_1990_2016.values.tolist()
    # forage_crops_1990_2016 = [str(round(i)) for i in forage_crops_1990_2016_list]

    # annual_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_annual_crop_pre_1990 == 1]
    # annual_crops_pre_1990 = [str(round(i)) for i in annual_crops_pre_1990]

    # annual_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_annual_crop_1990_2016 == 1]
    # annual_crops_1990_2016_list = annual_crops_1990_2016.values.tolist()
    # annual_crops_1990_2016 = [str(round(i)) for i in annual_crops_1990_2016_list]

    # concatted_1990_2016 = [tree_crops_1990_2016_list + annual_crops_1990_2016_list + forage_crops_1990_2016_list]
    # concatted_1990_2016_formatted = concatted_1990_2016[0]
    # all_crops_1990_2016 = [str(round(i)) for i in concatted_1990_2016_formatted]


    # concatted_pre_1990 = [tree_crops_pre_1990 + annual_crops_pre_1990 + forage_crops_pre_1990]
    # all_crops_pre_1990 = concatted_pre_1990[0]
    # # pdb.set_trace()
    # # all_crops_pre_1990 = [str(round(i)) for i in test1]

    # totals_in_irrig_dist = {}   # creates dictionary for totals c
    # totals_in_irrig_dist2 = pd.DataFrame({"crop_id" : [0,0,0,0,0], "agreage_year2019" : [0,0,0,0,0]})
    pdb.set_trace()

read_and_sort_site_codes()




