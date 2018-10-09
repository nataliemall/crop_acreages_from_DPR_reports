       
## Explore what's wrong with 2016 data
## I.e. why such a big drop / big gap compared with CC Data 


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):


def retrieve_data_for_irrigation_district_test(irrigation_district, normalized):

    irrigation_district_data = os.path.join('irrigation_districts_with_comtrs', irrigation_district + '.csv')
    try:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_data, usecols = ['co_mtrs'])
    except:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_data, usecols = ['CO_MTRS']) 

    crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1974,2017)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    # crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    crop_list_normalized = [ 'year', 'all_tree_crops_normalized', 'all_annual_crops', 'all_crops', 'percent_tree_crops', 'water_demand_with_2010_AW_values', 'water_demand_with_changing_AW_values', 'minimum_water_demand_for_year']
    df_shape_normalized = (len(range(1974,2017)), len(crop_list_normalized))
    zero_fillers_normalized = np.zeros(df_shape_normalized)
    sum_crop_types_normalized = pd.DataFrame(zero_fillers_normalized, columns = [ crop_list_normalized ] )

    # pdb.set_trace()

    codes_pre_1990 = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['site_code_pre_1990', 'site_name_pre_1990', 'is_orchard_crop_pre_1990', 'is_annual_crop_pre_1990', 'is_forage_pre_1990', 'applied_water_category_pre_1990']) # , index_col = 0)
    codes_1990_2016 = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['site_code_1990_2016', 'site_name_1990_2016', 'is_orchard_crop_1990_2016', 'is_annual_crop_1990_2016', 'is_forage_1990_2016', 'applied_water_category_1990_2016']) #, index_col = 0)
    HR_2010_AW_Data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', 'AW_HR_2010'])
    HR_min_data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', 'AW_HR_2010_min'])
    # # as shown on table 'sites_1990-2016' from PUR downloaded dataset 

    # pdb.set_trace()

    tree_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_orchard_crop_pre_1990 == 1]
    tree_crops_pre_1990 = [str(round(i)) for i in tree_crops_pre_1990]

    tree_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_orchard_crop_1990_2016 == 1]
    tree_crops_1990_2016_list = tree_crops_1990_2016.values.tolist()  # why necessary?  
    tree_crops_1990_2016 = [str(round(i)) for i in tree_crops_1990_2016_list]

    # pdb.set_trace()

    forage_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_forage_pre_1990 == 1]
    forage_crops_pre_1990 = [str(round(i)) for i in forage_crops_pre_1990]

    forage_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_forage_1990_2016 == 1]
    forage_crops_1990_2016_list = forage_crops_1990_2016.values.tolist()
    forage_crops_1990_2016 = [str(round(i)) for i in forage_crops_1990_2016_list]

    # pdb.set_trace()
    # print('check the to-list function here')


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
    # pdb.set_trace()
    # all_crops_pre_1990 = [str(round(i)) for i in test1]

    for df_row, year in enumerate(tqdm(range(2016,2017))):    # editted here to analyze ONLY 2016 
        print(f'Compiling and normalizing the data into different crop types for year {year}')
        year_string = str(year) 
        year_two_digits = year_string[-2:]
        year_date_time = pd.to_datetime(year, format='%Y')
        directory=os.path.join('calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )

        # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/data_with_comtrs/')
        comtrs_compiled_data = pd.read_csv(os.path.join(directory, ('all_data_year' + year_two_digits + '_by_COMTRS' + '.csv' )), sep = '\t')
        # pdb.set_trace()
        # print('find county column here')
        try:
            crop_data_in_irrigation_district = comtrs_compiled_data.loc[(comtrs_compiled_data["level_0"].isin(comtrs_in_irrigation_dist.co_mtrs)) ]
        except:
            crop_data_in_irrigation_district = comtrs_compiled_data.loc[(comtrs_compiled_data["level_0"].isin(comtrs_in_irrigation_dist.CO_MTRS)) ]
        crop_data_in_irrigation_district = crop_data_in_irrigation_district.rename(columns = {"level_0": "comtrs"}) 
        crop_data_in_irrigation_district = crop_data_in_irrigation_district.set_index('comtrs')



        if year < 1990:

            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_pre_1990)]  # Columns that are tree crops 
            annual_crop_columns =  crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_pre_1990)]
            forage_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(forage_crops_pre_1990)]
            print(tree_crop_columns)

            
            all_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(all_crops_pre_1990)] 

            sum_alfalfa = sum(crop_data_in_irrigation_district['3101'])
            sum_nectarine = sum(crop_data_in_irrigation_district['2303'])
        else: # year 1990 - 2016
            # if year == 1990:
                # pdb.set_trace()
                # print('test stuff out here - sept. 12, 2018')
            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_1990_2016)]  # Columns that are tree crops 
            print(tree_crop_columns)
            annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are annual crops 
            forage_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(forage_crops_1990_2016)]  # Columns that are annual crops 
            
            all_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(all_crops_1990_2016)]
            # pdb.set_trace()
            pdb.set_trace()
            sum_alfalfa = sum(crop_data_in_irrigation_district['23001'])
            sum_nectarine = sum(crop_data_in_irrigation_district['5003'])        

        tree_data = crop_data_in_irrigation_district[tree_crop_columns]
        tree_crop_acreage_by_fruit_type = tree_data[tree_crop_columns].sum()
        acreage_of_all_tree_crops = tree_data[tree_crop_columns].sum().sum()
        pdb.set_trace()

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
            print('normalizing the above amounts so that the total acreage across crop types for each comtrs is not above 640 acres')
            acreage_each_comtrs = all_crop_data.sum(axis = 1)
            all_crop_data_normalized = all_crop_data  # start normalized dataframe 

            number_of_skips = 0 

            for num, comtrs in enumerate(tqdm(all_crop_data_normalized.index)):
                # pdb.set_trace()
                if all_crop_data.loc[comtrs].sum() > 640:
                    # pdb.set_trace()
                    all_crop_data_normalized.loc[comtrs] = all_crop_data_normalized.loc[comtrs] * 640 / acreage_each_comtrs.loc[comtrs]
                    # pdb.set_trace()
                    # tree_data_normalized.loc[comtrs] =  tree_data_normalized.loc[comtrs] * 640 / acreage_each_comtrs.loc[comtrs]    
                else: 
                    number_of_skips = number_of_skips + 1 

            tree_data_normalized = all_crop_data_normalized[tree_crop_columns]
            annual_data_normalized = all_crop_data_normalized[annual_crop_columns]
            forage_data_normalized = all_crop_data_normalized[forage_crop_columns]
            # pdb.set_trace()

            acreage_by_crop_type = all_crop_data_normalized.sum()
            if year < 1990:  # calculate water use by multiplying the total acreage of for each crop type by its AW value
                # acreage_by_crop_type.loc[crop_type]
                # test = pd.merge(codes_pre_1990, acreage_by_crop_type)

                # pdb.set_trace()
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
                # pdb.set_trace()

                acreage_by_crop_type4['AW_group2'] = codes_pre_1990_2['applied_water_category_pre_1990'].loc[codes_pre_1990_2.index]

            if year > 1989:  # calculate water use by multiplying the total acreage of for each crop type by its AW value
                # pdb.set_trace()
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
                # pdb.set_trace()

                acreage_by_crop_type4['AW_group2'] = codes_1990_2016_2['applied_water_category_1990_2016'].loc[codes_1990_2016_2.index] 
                # acreage_by_crop_type4['acreage_within_region'] = acreage_by_crop_type4[0]
                # acreage_by_crop_type4 = acreage_by_crop_type4.drop(columns = [0] )  # drop redundant column 
                codes_1990_2016_2[codes_1990_2016_2.index.duplicated()]
                # acreage_by_crop_type4['AW_group2'] = codes_pre_1990_2['applied_water_category_pre_1990'].loc[codes_pre_1990_2.index]
            

            # pdb.set_trace()

            # pdb.set_trace()
                # snip data to only necessary rows:
            HR_2010_AW_Data_snipped = HR_2010_AW_Data.head(23)
            HR_2010_AW_Data_snipped2 = HR_2010_AW_Data_snipped.set_index('crop_name_HR_2010')

            min_data_snipped = HR_min_data.head(23)
            min_data_snipped2 = min_data_snipped.set_index('crop_name_HR_2010')

            # acreage_by_crop_type4['AW_acre_feet'] = HR_2010_AW_Data_snipped2['AW_HR_2010'].loc[HR_2010_AW_Data_snipped2.index]
            acreage_by_crop_type4['acreage_within_region'] = acreage_by_crop_type4[0]
            acreage_by_crop_type4 = acreage_by_crop_type4.drop(columns = [0] )  # drop redundant column 

            acreage_by_crop_type4['applied_water_per_acre'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['applied_water_for_this_crop_type'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['applied_water_per_acre_by_dwr_year'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['applied_water_for_this_crop_type_by_dwr_year'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            acreage_by_crop_type4['minimum_applied_water_per_acre'] = np.zeros(len(acreage_by_crop_type4.acreage_within_region))
            # pdb.set_trace()
            if (year > 1997) & (year < 2011):  # uses changing applied water values 
                # pdb.set_trace()
                column_name = str('AW_HR_' + str(year))
                HR_yearly_AW_Data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', column_name])
                HR_yearly_AW_Data_snipped = HR_yearly_AW_Data.head(23)
                HR_yearly_AW_Data_snipped_2 = HR_yearly_AW_Data_snipped.set_index('crop_name_HR_2010')

                for num, row in enumerate(tqdm(acreage_by_crop_type4.AW_group2)): 
                    # pdb.set_trace()
                    # aw_group_string = acreage_by_crop_type4.AW_group2.iloc[row]
                    try:
                        # pdb.set_trace()
                        applied_water_numerical_value = HR_yearly_AW_Data_snipped_2[column_name].loc[row]
                    except:
                        applied_water_numerical_value = 0 
                    acreage_by_crop_type4['applied_water_per_acre_by_dwr_year'].iloc[num] = applied_water_numerical_value
                # pdb.set_trace()
                acreage_by_crop_type4['applied_water_for_this_crop_type_by_dwr_year'] = acreage_by_crop_type4.acreage_within_region * np.float64(acreage_by_crop_type4.applied_water_per_acre_by_dwr_year)
                total_water_demand_for_year_changing_AW = acreage_by_crop_type4.applied_water_for_this_crop_type_by_dwr_year.sum()
            else:
                total_water_demand_for_year_changing_AW = 0 

            # for each row in the dataset acreage_by_crop_type4, 
            for num, row in enumerate(tqdm(acreage_by_crop_type4.AW_group2)):   # uses 2010 water use data from DWR 
                # pdb.set_trace()
                # aw_group_string = acreage_by_crop_type4.AW_group2.iloc[row]
                test = str(acreage_by_crop_type4.index[num])
                
                if (year < 1990) & (str(acreage_by_crop_type4.index[num]) in tree_crops_pre_1990):
                    try:
                        minumum_water_demand_for_crop = min_data_snipped2.AW_HR_2010_min.loc[row]
                        # pdb.set_trace()
                    except:
                        minumum_water_demand_for_crop = 0 
                        pdb.set_trace()
                elif (year > 1989) & (str(acreage_by_crop_type4.index[num]) in tree_crops_1990_2016):
                    try:
                        minumum_water_demand_for_crop = min_data_snipped2.AW_HR_2010_min.loc[row]
                    except: 
                        pdb.set_trace()
                        minumum_water_demand_for_crop = 0 
                else:
                    # pdb.set_trace()
                    minumum_water_demand_for_crop = 0 


                try:
                    applied_water_numerical_value = HR_2010_AW_Data_snipped2.AW_HR_2010.loc[row]
                except:
                    applied_water_numerical_value = 0 

                acreage_by_crop_type4['applied_water_per_acre'].iloc[num] = applied_water_numerical_value
                acreage_by_crop_type4['minimum_applied_water_per_acre'].iloc[num] = minumum_water_demand_for_crop


            # pdb.set_trace()
            acreage_by_crop_type4['applied_water_for_this_crop_type'] = acreage_by_crop_type4.acreage_within_region * np.float64(acreage_by_crop_type4.applied_water_per_acre)
            acreage_by_crop_type4['minimum_water_for_this_crop_type'] = acreage_by_crop_type4.acreage_within_region * np.float64(acreage_by_crop_type4.minimum_applied_water_per_acre)

            total_water_demand_for_year = acreage_by_crop_type4.applied_water_for_this_crop_type.sum()
            minumum_water_demand_for_year = acreage_by_crop_type4.minimum_water_for_this_crop_type.sum()
            ## include minumum demand for year here
            # minumum_water_demand_for_year = acreage_by_crop_type4

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
            sum_crop_types_normalized.iloc[df_row]['water_demand_with_2010_AW_values'] = total_water_demand_for_year
            sum_crop_types_normalized.iloc[df_row]['water_demand_with_changing_AW_values'] = total_water_demand_for_year_changing_AW
            # Add column for minimum values here 
            sum_crop_types_normalized.iloc[df_row]['minimum_water_demand_for_year'] = minumum_water_demand_for_year
            sum_crop_types_normalized.set_index('year')
            # pdb.set_trace()

            # pdb.set_trace()
            print('check that stuff is added here')

        else:
            sum_crop_types_normalized = 'not normalized'

    if normalized == 1:
        sum_crop_types_normalized.to_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')), index = False) 
    if normalized == 0:
        sum_crop_types.to_csv(os.path.join(irrigation_district, str('calPUR_data' + str(irrigation_district) + '.csv')), index = False) 

    # pdb.set_trace()
    return sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district

def county_commissioner_data_test(irrigation_district):
    county_name = irrigation_district.split('_')[0]

    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df_all[df_all.county==county_name]

    # first: what crops are highest value total (top 10 in 2016)
    print(df[df.index=='2016'].sort_values(by='value', ascending=False).head(10))
    highest_valued = df[df.index=='2016'].sort_values(by='value', ascending=False).head(10)
    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10))
    highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

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
        # pdb.set_trace()
        acreage_of_all_crops = tree_crops_this_year + annual_crops_this_year + forage_crops_this_year

        sum_cc_crop_types.iloc[df_row]['year'] = year_date_time.year 
        sum_cc_crop_types.iloc[df_row]['all_tree_crops'] = str(tree_crops_this_year)
        sum_cc_crop_types.iloc[df_row]['all_annual_crops'] = str(annual_crops_this_year)
        sum_cc_crop_types.iloc[df_row]['all_crops'] = str(acreage_of_all_crops)

        sum_cc_crop_types.iloc[df_row]['percent_tree_crops'] = str(tree_crops_this_year / acreage_of_all_crops * 100)
        sum_cc_crop_types.set_index('year')
        # pdb.set_trace()

    sum_cc_crop_types.to_csv(os.path.join(irrigation_district, str('cc_data' + str(irrigation_district) + '.csv')), index = False) 
        # annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are tree crops 

    return sum_cc_crop_types



