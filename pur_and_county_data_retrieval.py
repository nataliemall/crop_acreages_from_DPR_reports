### Data compilation and plotting for a specific region ###  

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pandas as pd
import seaborn as sns
import re 
import pdb 
from tqdm import tqdm  # for something in tqdm(something something):


def retrieve_data_for_irrigation_district(irrigation_district, normalized):

    irrigation_district_comtrs_list = os.path.join('irrigation_districts_with_comtrs', irrigation_district + '.csv')
    try:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_comtrs_list, usecols = ['co_mtrs'])
    except:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_comtrs_list, usecols = ['CO_MTRS']) 

    crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1974,2017)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    # crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    crop_list_normalized = [ 'year', 'all_tree_crops_normalized', 'all_annual_crops', 'all_crops', 'percent_tree_crops', 'water_demand_with_2010_AW_values', 'deficit_irrigation_water_demand_for_year', 'perennial_irrigation_water_demand_for_year']
    df_shape_normalized = (len(range(1974,2017)), len(crop_list_normalized))
    zero_fillers_normalized = np.zeros(df_shape_normalized)
    sum_crop_types_normalized = pd.DataFrame(zero_fillers_normalized, columns = [ crop_list_normalized ] )


    codes_pre_1990 = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['site_code_pre_1990', 'site_name_pre_1990', 'is_orchard_crop_pre_1990', 'is_annual_crop_pre_1990', 'is_forage_pre_1990', 'applied_water_category_pre_1990']) # , index_col = 0)
    codes_1990_2016 = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['site_code_1990_2016', 'site_name_1990_2016', 'is_orchard_crop_1990_2016', 'is_annual_crop_1990_2016', 'is_forage_1990_2016', 'applied_water_category_1990_2016']) #, index_col = 0)
    HR_2010_AW_Data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', 'AW_HR_2010'])
    HR_min_data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', 'AW_HR_2010_min'])
    # # as shown on table 'sites_1990-2016' from PUR downloaded dataset 

    # locate crop codes for each of the three crop types ( tree, annual, and forage)
    tree_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_orchard_crop_pre_1990 == 1]
    tree_crops_pre_1990 = [str(round(i)) for i in tree_crops_pre_1990]

    tree_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_orchard_crop_1990_2016 == 1]
    tree_crops_1990_2016_list = tree_crops_1990_2016.values.tolist()  # why necessary?  
    tree_crops_1990_2016 = [str(round(i)) for i in tree_crops_1990_2016_list]

    forage_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_forage_pre_1990 == 1]
    forage_crops_pre_1990 = [str(round(i)) for i in forage_crops_pre_1990]

    forage_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_forage_1990_2016 == 1]
    forage_crops_1990_2016_list = forage_crops_1990_2016.values.tolist()
    forage_crops_1990_2016 = [str(round(i)) for i in forage_crops_1990_2016_list]

    annual_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_annual_crop_pre_1990 == 1]
    annual_crops_pre_1990 = [str(round(i)) for i in annual_crops_pre_1990]

    annual_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_annual_crop_1990_2016 == 1]
    annual_crops_1990_2016_list = annual_crops_1990_2016.values.tolist()
    annual_crops_1990_2016 = [str(round(i)) for i in annual_crops_1990_2016_list]

    concatted_1990_2016 = [tree_crops_1990_2016_list + annual_crops_1990_2016_list + forage_crops_1990_2016_list]
    concatted_1990_2016_formatted = concatted_1990_2016[0]
    all_crops_1990_2016 = [str(round(i)) for i in concatted_1990_2016_formatted]

    concatted_pre_1990 = [tree_crops_pre_1990 + annual_crops_pre_1990 + forage_crops_pre_1990]
    all_crops_pre_1990 = concatted_pre_1990[0]
    
    totals_in_irrig_dist = {}   # creates dictionary for totals c
    # totals_in_irrig_dist2 = pd.DataFrame({"crop_id" : [0,0,0,0,0], "agreage_year2019" : [0,0,0,0,0]})


    for df_row, year in enumerate(tqdm(range(1974,2017))):    # editted here to include up to 2016 
        print(f'Analyzing the data for the given {irrigation_district} for year {year}')
        year_string = str(year) 
        year_two_digits = year_string[-2:]
        year_date_time = pd.to_datetime(year, format='%Y')
        # directory=os.path.join('calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )

        # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/data_with_comtrs/')
        comtrs_compiled_data = pd.read_csv(os.path.join('calPIP_PUR_crop_acreages', (year_two_digits + 'files'), ('all_data_normalized_year' + year_two_digits + '_by_COMTRS' + '.csv' )), sep = '\t')

        try:
            crop_data_in_irrigation_district = comtrs_compiled_data.loc[(comtrs_compiled_data["comtrs"].isin(comtrs_in_irrigation_dist.co_mtrs)) ]
        except:
            crop_data_in_irrigation_district = comtrs_compiled_data.loc[(comtrs_compiled_data["comtrs"].isin(comtrs_in_irrigation_dist.CO_MTRS)) ]
        
        crop_data_in_irrigation_district = crop_data_in_irrigation_district.rename(columns = {"level_0": "comtrs"}) 
        crop_data_in_irrigation_district = crop_data_in_irrigation_district.set_index('comtrs')

        if year < 1990:
            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_pre_1990)]  # Columns that are tree crops 
            annual_crop_columns =  crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_pre_1990)]
            forage_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(forage_crops_pre_1990)]
            all_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(all_crops_pre_1990)] 

            sum_alfalfa = sum(crop_data_in_irrigation_district['3101'])
            sum_nectarine = sum(crop_data_in_irrigation_district['2303'])
        else: # year 1990 - 2016
            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_1990_2016)]  # Columns that are tree crops 
            # print(tree_crop_columns)
            annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are annual crops 
            forage_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(forage_crops_1990_2016)]  # Columns that are annual crops 
            
            all_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(all_crops_1990_2016)]
            sum_alfalfa = sum(crop_data_in_irrigation_district['23001'])
            sum_nectarine = sum(crop_data_in_irrigation_district['5003'])        

        tree_data = crop_data_in_irrigation_district[tree_crop_columns]
        tree_crop_acreage_by_fruit_type = tree_data[tree_crop_columns].sum()
        acreage_of_all_tree_crops = tree_data[tree_crop_columns].sum().sum()
        
        annual_data = crop_data_in_irrigation_district[annual_crop_columns]
        annual_acreage_by_annual_crop_type = annual_data[annual_crop_columns].sum()
        acreage_of_all_annual_crops = annual_data[annual_crop_columns].sum().sum()

        forage_data = crop_data_in_irrigation_district[forage_crop_columns]
        forage_acreage_by_forage_crop_type = forage_data[forage_crop_columns].sum()
        acreage_of_all_forage_crops = forage_data[forage_crop_columns].sum().sum()
        acreage_of_all_crops = acreage_of_all_tree_crops + acreage_of_all_annual_crops + acreage_of_all_forage_crops

        sum_crop_types.iloc[df_row]['year'] = year_date_time.year 
        sum_crop_types.iloc[df_row]['alfalfa'] = str(sum_alfalfa)
        sum_crop_types.iloc[df_row]['all_tree_crops'] = str(acreage_of_all_tree_crops)
        sum_crop_types.iloc[df_row]['all_annual_crops'] = str(acreage_of_all_annual_crops)
        sum_crop_types.iloc[df_row]['all_crops'] = str(acreage_of_all_crops)
        sum_crop_types.iloc[df_row]['percent_tree_crops'] = str(acreage_of_all_tree_crops / acreage_of_all_crops * 100)
        sum_crop_types.set_index('year')

        if normalized == 1:
            # for each comtrs value, find the total number of acres (sum for all crop types)
            # multiply each value in the section by (640 / comtrs total)
            all_crop_data = crop_data_in_irrigation_district[all_crop_columns]
            # print('normalizing the above amounts so that the total acreage across crop types for each comtrs is not above 640 acres')
            acreage_each_comtrs = all_crop_data.sum(axis = 1)
            # all_crop_data_normalized = all_crop_data  # start normalized dataframe 

            # number_of_skips = 0 

            ## section below no longer necessary since data already normalized  
            # for num, comtrs in enumerate(tqdm(all_crop_data_normalized.index)):
            #     
            #     if all_crop_data.loc[comtrs].sum() > 640:
            #         
            #         all_crop_data_normalized.loc[comtrs] = all_crop_data_normalized.loc[comtrs] * 640 / acreage_each_comtrs.loc[comtrs]
            #         
            #         # tree_data_normalized.loc[comtrs] =  tree_data_normalized.loc[comtrs] * 640 / acreage_each_comtrs.loc[comtrs]    
            #     else: 
            #         number_of_skips = number_of_skips + 1 
            
            # if not os.path.isdir('crop_data_by_year'):
            #     os.mkdir('crop_data_by_year')
            # if irrigation_district == 'tlb_irrigation_districts_all':
            #     all_crop_data_normalized.to_csv(str('crop_data_by_year/' + str(year) + 'crops_in_each_comtrs.csv'))  # saves overall dataset for each year 
            totals_in_irrig_dist[year] = all_crop_data.sum(axis = 0)

            ### little block saving df by year for region
            totals_in_current_year = totals_in_irrig_dist[year].to_frame()
            if not 'df_all_years' in locals():  # starts building dataframe
                df_all_years = totals_in_current_year.rename(columns = {0: year})
            else:  # adds to base each year
                df_with_year_to_add = totals_in_current_year.rename(columns = {0: year})
                df_all_years = pd.merge(df_all_years, df_with_year_to_add, how = 'outer', left_index = True, right_index = True)
            ### end of little block saving df by year for region

            if not os.path.isdir(str(irrigation_district)):
                os.mkdir(str(irrigation_district))

            tree_data_normalized = all_crop_data[tree_crop_columns]
            tree_data_by_comtrs = tree_data_normalized.sum(axis = 1)  # for QGIS export 

            if not os.path.isdir('data_for_qgis'):
                os.mkdir('data_for_qgis')
            tree_data_by_comtrs.to_csv(str('data_for_qgis/' + str(irrigation_district) + str(year) + 'tree_data.csv'))
            annual_data_normalized = all_crop_data[annual_crop_columns]
            forage_data_normalized = all_crop_data[forage_crop_columns]

            acreage_by_crop_type = all_crop_data.sum()
            if year < 1990:  # calculate water use by multiplying the total acreage of for each crop type by its AW value
                # acreage_by_crop_type.loc[crop_type]
                # test = pd.merge(codes_pre_1990, acreage_by_crop_type)

                
                print('connect using the loc function here')
                # reformat acreage - croptype data
                acreage_by_crop_type2 = acreage_by_crop_type.reset_index()
                acreage_by_crop_type3 = acreage_by_crop_type2.rename(columns = {"index" : "site_code_pre_1990"})

                # acreage_by_crop_type4 = acreage_by_crop_type3.rename(columns = {"0": "acreage" })
        
                # reformat cropcodes - AW category data
                codes_pre_1990.site_code_pre_1990 = np.int64(codes_pre_1990.site_code_pre_1990)
                codes_pre_1990.site_code_pre_1990 = codes_pre_1990.site_code_pre_1990.astype(object)  # this doesnt actually work? 
                #set indices 

                codes_pre_1990_2 = codes_pre_1990.set_index('site_code_pre_1990')
                acreage_by_crop_type4 = acreage_by_crop_type3.set_index('site_code_pre_1990')
                acreage_by_crop_type4.index = np.int64(acreage_by_crop_type4.index)
                

                acreage_by_crop_type4['AW_group2'] = codes_pre_1990_2['applied_water_category_pre_1990'].loc[codes_pre_1990_2.index]

            if year > 1989:  # calculate water use by multiplying the total acreage of for each crop type by its AW value
                
                test = 'past 1989'
                acreage_by_crop_type2 = acreage_by_crop_type.reset_index()
                acreage_by_crop_type3 = acreage_by_crop_type2.rename(columns = {"index" : "site_code_1990_2016"})

                # reformat cropcodes - AW category data
                codes_1990_2016.site_code_1990_2016 = np.int64(codes_1990_2016.site_code_1990_2016)
                codes_1990_2016.site_code_1990_2016 = codes_1990_2016.site_code_1990_2016.astype(object)  # this doesnt actually work? 
                #set indices 

                codes_1990_2016_2 = codes_1990_2016.set_index('site_code_1990_2016')
                acreage_by_crop_type4 = acreage_by_crop_type3.set_index('site_code_1990_2016')
                acreage_by_crop_type4.index = np.int64(acreage_by_crop_type4.index)
                

                acreage_by_crop_type4['AW_group2'] = codes_1990_2016_2['applied_water_category_1990_2016'].loc[codes_1990_2016_2.index] 
                # acreage_by_crop_type4['acreage_within_region'] = acreage_by_crop_type4[0]
                # acreage_by_crop_type4 = acreage_by_crop_type4.drop(columns = [0] )  # drop redundant column 
                codes_1990_2016_2[codes_1990_2016_2.index.duplicated()]
                # acreage_by_crop_type4['AW_group2'] = codes_pre_1990_2['applied_water_category_pre_1990'].loc[codes_pre_1990_2.index]
            
                # snip data to only necessary rows:
            HR_2010_AW_Data_snipped = HR_2010_AW_Data.head(23)
            HR_2010_AW_Data_snipped2 = HR_2010_AW_Data_snipped.set_index('crop_name_HR_2010')

            min_data_snipped = HR_min_data.head(23)
            min_data_snipped2 = min_data_snipped.set_index('crop_name_HR_2010')
            # perennial_data = H  

            # acreage_by_crop_type4['AW_acre_feet'] = HR_2010_AW_Data_snipped2['AW_HR_2010'].loc[HR_2010_AW_Data_snipped2.index]
            acreage_by_crop_type4['acreage_within_region'] = acreage_by_crop_type4[0]
            
            acreage_by_crop_type4 = acreage_by_crop_type4.drop(labels=[0], axis = 1)  # drop redundant column 

            acreage_by_crop_type4['applied_water_per_acre'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['applied_water_for_this_crop_type'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['applied_water_per_acre_by_dwr_year'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['applied_water_for_this_crop_type_by_dwr_year'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['minimum_applied_water_per_acre'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['perennial_applied_water_per_acre'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))

            # for each row in the dataset acreage_by_crop_type4, 
            for num, row in enumerate(tqdm(acreage_by_crop_type4.AW_group2)):   # uses 2010 water use data from DWR 
                
                # aw_group_string = acreage_by_crop_type4.AW_group2.iloc[row]
                test = str(acreage_by_crop_type4.index[num])
                
                if (year < 1990) & (str(acreage_by_crop_type4.index[num]) in tree_crops_pre_1990):
                    try:
                        deficit_water_demand_for_crop = min_data_snipped2.AW_HR_2010_min.loc[row]  # deficit water demand 
                        perennial_water_demand_for_crop = HR_2010_AW_Data_snipped2.AW_HR_2010.loc[row]    # 100% water for perennials
                    except:
                        deficit_water_demand_for_crop = 0 
                        perennial_water_demand_for_crop = 0 
                elif (year > 1989) & (str(acreage_by_crop_type4.index[num]) in tree_crops_1990_2016):
                    try:
                        deficit_water_demand_for_crop = min_data_snipped2.AW_HR_2010_min.loc[row]  # deficit water demand
                        perennial_water_demand_for_crop = HR_2010_AW_Data_snipped2.AW_HR_2010.loc[row]
                    except: 
                        deficit_water_demand_for_crop = 0 
                        perennial_water_demand_for_crop = 0
                else:                                           # water demands go to zero if not perennial crops 
                    deficit_water_demand_for_crop = 0 
                    perennial_water_demand_for_crop = 0

                try:
                    applied_water_numerical_value = HR_2010_AW_Data_snipped2.AW_HR_2010.loc[row]
                except:
                    applied_water_numerical_value = 0 

                acreage_by_crop_type4['applied_water_per_acre'].iloc[num] = applied_water_numerical_value
                acreage_by_crop_type4['minimum_applied_water_per_acre'].iloc[num] = deficit_water_demand_for_crop
                acreage_by_crop_type4['perennial_applied_water_per_acre'].iloc[num] = perennial_water_demand_for_crop

            acreage_by_crop_type4['applied_water_for_this_crop_type'] = acreage_by_crop_type4.acreage_within_region * np.float64(acreage_by_crop_type4.applied_water_per_acre)
            acreage_by_crop_type4['deficit_irrigation_for_this_crop_type'] = acreage_by_crop_type4.acreage_within_region * np.float64(acreage_by_crop_type4.minimum_applied_water_per_acre)
            acreage_by_crop_type4['perennial_irrigation_for_this_crop_type'] = acreage_by_crop_type4.acreage_within_region * np.float64(acreage_by_crop_type4.perennial_applied_water_per_acre)

            total_water_demand_for_year = acreage_by_crop_type4.applied_water_for_this_crop_type.sum()
            deficit_irrigation_water_demand_for_year = acreage_by_crop_type4.deficit_irrigation_for_this_crop_type.sum()
            perennial_irrigation_water_demand_for_year = acreage_by_crop_type4.perennial_irrigation_for_this_crop_type.sum()

            acreage_of_all_tree_crops_normalized = tree_data_normalized[tree_crop_columns].sum().sum()
            acreage_of_all_annual_crops_normalized = annual_data_normalized[annual_crop_columns].sum().sum()
            acreage_of_all_forage_crops_normalized = forage_data_normalized[forage_crop_columns].sum().sum()
            acreage_of_all_crops_normalized = acreage_of_all_tree_crops_normalized + acreage_of_all_annual_crops_normalized + acreage_of_all_forage_crops_normalized
            ## Create a new column here summing up the total water column in order to find the 2010 water demand 

            sum_crop_types_normalized.iloc[df_row]['year'] = year_date_time.year 
            sum_crop_types_normalized.iloc[df_row]['all_tree_crops_normalized'] = str(acreage_of_all_tree_crops_normalized)
            sum_crop_types_normalized.iloc[df_row]['all_annual_crops'] = str(acreage_of_all_annual_crops_normalized)
            sum_crop_types_normalized.iloc[df_row]['all_crops'] = str(acreage_of_all_crops_normalized)     
            sum_crop_types_normalized.iloc[df_row]['percent_tree_crops'] = str(acreage_of_all_tree_crops_normalized / acreage_of_all_crops_normalized * 100)
            sum_crop_types_normalized.iloc[df_row]['water_demand_with_2010_AW_values'] = total_water_demand_for_year  # uses DWR's applied water demand estimates for 2010 
            # sum_crop_types_normalized.iloc[df_row]['water_demand_with_changing_AW_values'] = total_water_demand_for_year_changing_AW # not needed- uses changing applied water demand estimates from DWR

            sum_crop_types_normalized.iloc[df_row]['deficit_irrigation_water_demand_for_year'] = deficit_irrigation_water_demand_for_year  # minimum water demand for year (50% of water demand of perennial crops)
            sum_crop_types_normalized.iloc[df_row]['perennial_irrigation_water_demand_for_year'] = perennial_irrigation_water_demand_for_year  # water demand for perennial crops at 100% irrigation 
            sum_crop_types_normalized.set_index('year')

        else:
            sum_crop_types_normalized = 'not normalized'
    
    if normalized == 1:
        sum_crop_types_normalized.to_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')), index = False) 
    if normalized == 0:
        sum_crop_types.to_csv(os.path.join(irrigation_district, str('calPUR_data' + str(irrigation_district) + '.csv')), index = False) 

    df_all_years.index.names = ['crop_ID']
    df_all_years.to_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '.csv')), index = True) 

    return sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist

def county_commissioner_data(irrigation_district):
    county_name = irrigation_district.split('_')[0]

    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df_all[df_all.county==county_name]

    df_tulare = df_all[df_all.county=='Tulare']
    df_kern = df_all[df_all.county=='Kern']
    df_kings = df_all[df_all.county=='Kings']
    df_fresno = df_all[df_all.county=='Fresno']

    county_commissioner_codes = pd.read_csv('county_commissioner_crop_types.csv') 
    tree_crops_cc = county_commissioner_codes.site_code_cc.loc[county_commissioner_codes.is_orchard_crop == 1]
    annual_crops_cc = county_commissioner_codes.site_code_cc.loc[county_commissioner_codes.is_annual_crop == 1]
    forage_crops_cc = county_commissioner_codes.site_code_cc.loc[county_commissioner_codes.is_forage_crop == 1]

    crop_list = ['year', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1980,2017)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_cc_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    for df_row, year in tqdm(enumerate(range(1980,2017))):
        year_date_time = pd.to_datetime(year, format='%Y')
        df_this_year = df[df.index == str(year) ]
        df_real_acreages_only = df_this_year[df_this_year.acres > 0 ]

        tree_crops_this_year_this_county = df_real_acreages_only[df_real_acreages_only.crop.isin(tree_crops_cc)]  # Columns that are tree crops 
        annual_crops_this_year_this_county = df_real_acreages_only[df_real_acreages_only.crop.isin(annual_crops_cc)]  # Columns that are tree crops 
        forage_crops_this_year_this_county = df_real_acreages_only[df_real_acreages_only.crop.isin(forage_crops_cc)]

        tree_crops_this_year = tree_crops_this_year_this_county.acres.sum()
        annual_crops_this_year = annual_crops_this_year_this_county.acres.sum()
        forage_crops_this_year = forage_crops_this_year_this_county.acres.sum()
        acreage_of_all_crops = tree_crops_this_year + annual_crops_this_year + forage_crops_this_year
        

        if acreage_of_all_crops == 0: # avoid divide by zero error 
            print('error: do not run county commissioner data parsing - this data is only available on the county scale.  Set compare_with_county_data equal to zero')
            os.system("pause")

        sum_cc_crop_types.iloc[df_row]['year'] = year_date_time.year 
        sum_cc_crop_types.iloc[df_row]['all_tree_crops'] = str(tree_crops_this_year)
        sum_cc_crop_types.iloc[df_row]['all_annual_crops'] = str(annual_crops_this_year)
        sum_cc_crop_types.iloc[df_row]['all_crops'] = str(acreage_of_all_crops)

        sum_cc_crop_types.iloc[df_row]['percent_tree_crops'] = str(tree_crops_this_year / acreage_of_all_crops * 100)
        sum_cc_crop_types.set_index('year')

    sum_cc_crop_types.to_csv(os.path.join(irrigation_district, str('cc_data' + str(irrigation_district) + '.csv')), index = False) 
        # annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are tree crops 

    return sum_cc_crop_types


def load_calPIP_data_all_years(irrigation_district):  # loads the data already calculated rather than recalculate it all 
    all = np.load(str(irrigation_district + 'all_crops_compiled_with_crop_types.npy')).item()
    tree_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'tree_acreage_summed_for_year.csv'))
    annual_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'annual_acreage_summed_for_year.csv'))
    forage_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'forage_acreage_summed_for_year.csv'))
    percent_tree_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'percent_tree_acreage_summed_for_year.csv'))
    
    return all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, percent_tree_acreage_summed_for_year
    # print(read_dictionary['hello']) # displays "world"




