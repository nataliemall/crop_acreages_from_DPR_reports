### Economic analysis for a specific region ###  

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



def connect_site_codes_to_applied_water_per_acre():
    '''connects applied water data to overall table'''

    codes_1990_2016 = pd.read_csv('site_codes_with_crop_types.csv', 
        usecols = ['site_code_1990_2016', 'site_name_1990_2016', 'is_orchard_crop_1990_2016', 'is_annual_crop_1990_2016', 'is_forage_1990_2016', 
        'applied_water_category_1990_2016', 'cc_crop_category_2016', 'tree_loss_price_per_acre', 'tree_loss_price_per_acre_year5']) #, index_col = 0)
    HR_2010_AW_Data = pd.read_csv('site_codes_with_crop_types.csv', usecols = ['crop_name_HR_2010', 'AW_HR_2010'])
   
    HR_2010_AW_Data_snipped = HR_2010_AW_Data.head(23)
    test1 = HR_2010_AW_Data_snipped.rename(columns = {'crop_name_HR_2010': 'applied_water_category_pre_1990'})
    HR_2010_AW_Data_snipped2 = HR_2010_AW_Data_snipped.set_index('crop_name_HR_2010')

    codes_1990_2016_with_af = codes_1990_2016
    codes_1990_2016_with_af['af_applied_water'] = np.zeros(len(codes_1990_2016_with_af))

    for num, site_code in enumerate(codes_1990_2016.applied_water_category_1990_2016):
        try: 
            codes_1990_2016_with_af.af_applied_water[num] = HR_2010_AW_Data_snipped.loc[HR_2010_AW_Data_snipped.crop_name_HR_2010 == site_code].AW_HR_2010  # acre feet of applied water for crop type 
        except:
            print('exception crop type')

    return(codes_1990_2016_with_af)


def county_commissioner_data(codes_1990_2016_with_af):
    '''connects economic data to generate overall codes_with_price_per_acre.csv table'''

    county_list = ('Tulare', 'Kern', 'Kings', 'Fresno')
    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df_tlb = df_all[df_all.county.isin(county_list)]

    df_tlb_year_2016 = df_tlb[df_tlb.index == '2016']

    df_tlb_year_2016['dollars_per_acre'] = np.zeros(len(df_tlb_year_2016)) 
    df_tlb_year_2016['dollars_per_acre'] = df_tlb_year_2016['yield'] * df_tlb_year_2016.ppu 
    
    # pdb.set_trace()
    # print('stopped here')
    codes_with_price_per_acre = codes_1990_2016_with_af
    codes_with_price_per_acre['dollars_per_acre'] = np.nan   # (len(codes_1990_2016_with_af))
    # pdb.set_trace()
    codes_with_price_per_acre['revenue_per_af_water'] = np.nan   #(len(codes_1990_2016_with_af))
    # codes_with_price_per_acre['tree_loss_price_per_acre'] = np.nan   
    # pdb.set_trace()
    # print('start here')

    for num, site_code in enumerate(codes_with_price_per_acre.site_name_1990_2016):
        
        cc_crop_type = codes_with_price_per_acre.cc_crop_category_2016[num]

        dollar_per_acre_value = df_tlb_year_2016.loc[df_tlb_year_2016.crop == cc_crop_type].dollars_per_acre

        if len(dollar_per_acre_value) > 1:     # if more than 1 county has crop type, take the weighted average of $/acre price
            data_this_crop = df_tlb_year_2016.loc[df_tlb_year_2016.crop == cc_crop_type]

            average_dollars_per_acre = sum(data_this_crop.acres * data_this_crop.dollars_per_acre) / sum(data_this_crop.acres)
            codes_with_price_per_acre.dollars_per_acre[num] = average_dollars_per_acre  # price per acre of crop type 
            
            result = data_this_crop.dollars_per_acre.values
            bad_data = 9801   # checks for bad data 

            if bad_data in result:
                print(f'bad_data for this crop type {site_code}')
                pdb.set_trace()

        if len(dollar_per_acre_value) == 1:   
            if bad_data in result:
                print(f'bad_data for this crop type {site_code}')
                pdb.set_trace()

            codes_with_price_per_acre.dollars_per_acre[num] = dollar_per_acre_value   # price per acre of crop type 

    codes_with_price_per_acre.revenue_per_af_water = codes_with_price_per_acre.dollars_per_acre  / codes_with_price_per_acre.af_applied_water  # calculate dollars per AF applied water
    codes_with_price_per_acre.to_csv('codes_with_price_per_acre.csv', index = False) 

    return(df_tlb_year_2016, codes_with_price_per_acre)


def set_up_overall_table(irrigation_district_list):
    overall_ID_table = pd.DataFrame(index =irrigation_district_list)

    overall_ID_columns = [     # Create columns for overall dataframe
        'baseline_revenue',
        'baseline_acreage',

        'curtailment_af_baseline',
        'total_revenue_lost_baseline',
        'annual_acres_fallowed_baseline',
        'perennial_acres_fallowed_baseline',
        'total_acres_fallowed_baseline',
        'total_orchards_pulled_baseline',

        'curtailment_af_25',
        'total_revenue_lost_25',
        'annual_acres_fallowed_25',
        'perennial_acres_fallowed_25',
        'total_acres_fallowed_25',
        'total_orchards_pulled_25',

        'curtailment_af_50',
        'total_revenue_lost_50',
        'annual_acres_fallowed_50',
        'perennial_acres_fallowed_50',
        'total_acres_fallowed_50',
        'total_orchards_pulled_50',

        'curtailment_af_75',
        'total_revenue_lost_75',
        'annual_acres_fallowed_75',
        'perennial_acres_fallowed_75',
        'total_acres_fallowed_75',
        'total_orchards_pulled_75', ]


    overall_ID_table = pd.concat([overall_ID_table,pd.DataFrame(columns=overall_ID_columns)])  # add columns to table 

    return overall_ID_table 


def generate_district_crop_table(irrigation_district):

    codes_with_price_per_acre = pd.read_csv('codes_with_price_per_acre.csv', index_col = 'site_code_1990_2016') 
    # pdb.set_trace()
    crops_in_irrigation_district_2016 = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '.csv')), index_col = 'crop_ID', usecols = ['crop_ID', '2016']) 
    crops_in_irrigation_district_2016 = crops_in_irrigation_district_2016.rename(columns = {'2016': "acreage_2016"})

    crops_sorted = crops_in_irrigation_district_2016.sort_values('acreage_2016', ascending = False)

    crops_above_10_acres = crops_sorted[crops_sorted['acreage_2016'] > 10 ]  # filter out negligible crops 

    codes_with_price_per_acre = codes_with_price_per_acre[~codes_with_price_per_acre.index.isnull()]  # remove null indices 
    codes_with_price_per_acre.index = codes_with_price_per_acre.index.astype(int)  # convert indices to integers 

    crops_above_10_acres['revenue_per_af_water'] = np.nan
    crops_above_10_acres['crop_type'] = np.nan
    crops_above_10_acres['is_orchard'] = np.nan
    crops_above_10_acres['is_annual'] = np.nan
    crops_above_10_acres['af_applied_water_per_acre'] = np.nan
    crops_above_10_acres['total_revenue_from_crop'] = np.nan
    crops_above_10_acres['cost_pulling_replanting_orchard_per_acre'] = np.nan
    crops_above_10_acres['cost_pulling_replanting_orchard_per_acre_year5'] = np.nan


    for num, crop_ID in enumerate(crops_above_10_acres.index):  # creates dataframe of crops in irrigation district, revenue generated, and water used by each crop

        # pdb.set_trace()
        crops_above_10_acres.crop_type[crop_ID] = codes_with_price_per_acre.site_name_1990_2016[crop_ID] # add crop type column 
        crops_above_10_acres.is_orchard[crop_ID] = codes_with_price_per_acre.is_orchard_crop_1990_2016[crop_ID] # add orchard column 
        crops_above_10_acres.is_annual[crop_ID] = codes_with_price_per_acre.is_annual_crop_1990_2016[crop_ID] # add field crop column 
        crops_above_10_acres.af_applied_water_per_acre[crop_ID] = codes_with_price_per_acre.af_applied_water[crop_ID] # add AW column 
        crops_above_10_acres.revenue_per_af_water[crop_ID] = codes_with_price_per_acre.revenue_per_af_water[crop_ID]  # add $/AF-water column

        crops_above_10_acres.cost_pulling_replanting_orchard_per_acre[crop_ID] = codes_with_price_per_acre.tree_loss_price_per_acre[crop_ID]    # cost per acre of pulling and fallowing
        crops_above_10_acres.cost_pulling_replanting_orchard_per_acre_year5[crop_ID] = codes_with_price_per_acre.tree_loss_price_per_acre_year5[crop_ID]    # cost per acre of pulling and fallowing of 5-year-old tree
        crops_above_10_acres.total_revenue_from_crop[crop_ID] = codes_with_price_per_acre.dollars_per_acre[crop_ID] * crops_above_10_acres.acreage_2016.values[num] # calculate revenue 

    # pdb.set_trace()
    column_name = str(irrigation_district) + '_crop_codes'
    # crops_above_10_acres = crops_above_10_acres.rename(columns = {'acreage_2016' : column_name})

    crops_above_10_acres.index = crops_above_10_acres.index.rename(column_name)
    # pdb.set_trace()

    crops_above_10_acres['af_demanded_2016'] = crops_above_10_acres.af_applied_water_per_acre * crops_above_10_acres['acreage_2016']
    district_crops_sorted_by_water_value = crops_above_10_acres.sort_values('revenue_per_af_water')

    district_crops_sorted_by_water_value.to_csv(os.path.join(irrigation_district, 'table_major_crops_in_district.csv'), index = True) 
    return district_crops_sorted_by_water_value


def calculate_baseline_revenue(irrigation_district):
    district_crops_sorted_by_water_value = pd.read_csv(os.path.join(irrigation_district, 'table_major_crops_in_district.csv'), index_col = [0])

    baseline_revenue = district_crops_sorted_by_water_value.total_revenue_from_crop.sum()
    # pdb.set_trace()
    return baseline_revenue


def calculate_water_curtailment(irrigation_district, curtailment_level, deficit_irrigation_option):

    district_crops_sorted_by_water_value = pd.read_csv(os.path.join(irrigation_district, 'table_major_crops_in_district.csv'), index_col = [0])

    district_crops_sorted_by_water_value.revenue_per_af_water = district_crops_sorted_by_water_value.revenue_per_af_water.fillna(value = 0)  # convert nans to zeros 
    baseline_acreage = district_crops_sorted_by_water_value.acreage_2016.values.sum()

    water_portfolios = pd.read_csv('irrigation_district_water_portfolios.csv', index_col = 'irrigation district' )  # 2009 is a normal year 
    wet_year_surface_water = water_portfolios.wet_year_surface_water[irrigation_district]
    wet_year_gw = water_portfolios.wet_year_gw[irrigation_district]
    dry_year_surface_water = water_portfolios.dry_year_surface_water[irrigation_district]

    # pdb.set_trace()
    if curtailment_level == 'baseline':
        dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]

    if curtailment_level == 'gw_reduction_25_percent':
        dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]  * 0.75

    if curtailment_level == 'gw_reduction_50_percent':
        dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]  * 0.5

    if curtailment_level == 'gw_reduction_75_percent':
        dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]  * 0.25  


    district_annual_crops = district_crops_sorted_by_water_value[district_crops_sorted_by_water_value.is_annual == 1 ]
    # district_annual_crops
    annual_crops_af_demanded = district_annual_crops.af_demanded_2016.sum()

    district_perennial_crops = district_crops_sorted_by_water_value[district_crops_sorted_by_water_value.is_orchard == 1 ]
    perennial_crops_af_demanded = district_perennial_crops.af_demanded_2016.sum()

    # set initial values 
    total_revenue_lost = 0
    acres_fallowed = 0 
    acres_fallowed_annuals = 0
    acres_fallowed_perennials = 0 
    acres_pulled = 0

    # pdb.set_trace()
    if dry_year_surface_water > district_crops_sorted_by_water_value.af_demanded_2016.sum():   # if SW enough to supply ag water during dry year
        print(f'Sufficient SW for {irrigation_district} during dry year')
        curtailment_af = 0 
        total_revenue_lost = 0
        acres_fallowed = 0 
        acres_fallowed_annuals = 0
        acres_fallowed_perennials = 0 
        # pdb.set_trace()
        # print('examine here')

    elif (dry_year_surface_water + dry_year_gw) > district_crops_sorted_by_water_value.af_demanded_2016.sum():
        # pdb.set_trace()
        print(f'No economic loss for {curtailment_level} scenario for {irrigation_district}')
        curtailment_af = 0 
        total_revenue_lost = 0 
        acres_fallowed = 0 
        acres_fallowed_annuals = 0
        acres_fallowed_perennials = 0 

    else:
        print('Curtailments necessary')
        # pdb.set_trace()
        curtailment_af = district_crops_sorted_by_water_value.af_demanded_2016.sum() -  (dry_year_surface_water + dry_year_gw)
        
        #set initial conditions
        revenue_lost = 0 
        acre_feet_curtailed = 0 
        end_revenue_loss_calcs = 0 
        curtailment_remaining = curtailment_af
        acres_fallowed = 0 
        
        if (dry_year_surface_water + dry_year_gw) > perennial_crops_af_demanded:
            print(f'No perennial fallowing for {curtailment_level} scenario for {irrigation_district}')
            acres_fallowed_perennials = 0 

            
            # Calculate revenue loss from the required fallowing of annual crops: 
            for num, crop_af_demanded in enumerate(district_annual_crops.af_demanded_2016.tolist()):

                # acre_feet_curtailed_this_crop = district_annual_crops.af_demanded_2016[num]
                acre_feet_curtailed = crop_af_demanded + acre_feet_curtailed

                if curtailment_remaining <= crop_af_demanded:   # if curtailment remaining is less than af demanded in current crop
                    if end_revenue_loss_calcs == 0:
                        # pdb.set_trace()

                        last_crop_revenue_loss = curtailment_remaining * district_annual_crops.revenue_per_af_water.values[num]

                        total_revenue_lost = revenue_lost + last_crop_revenue_loss

                        last_crop_acres_fallowed = curtailment_remaining /  crop_af_demanded *  district_annual_crops.acreage_2016.values[num]   # ratio of last crops fallowed
                        acres_fallowed = acres_fallowed + last_crop_acres_fallowed
                        acres_fallowed_annuals = acres_fallowed
                        # pdb.set_trace()
                        # print('test final amount here')

                    end_revenue_loss_calcs = 1 

                else:
                    if end_revenue_loss_calcs == 0:
                        curtailment_remaining = curtailment_af - acre_feet_curtailed
                        revenue_lost_this_crop = district_annual_crops.revenue_per_af_water.values[num] * crop_af_demanded
                        revenue_lost = revenue_lost_this_crop + revenue_lost
                        acres_fallowed = acres_fallowed + district_annual_crops.acreage_2016.values[num]


        if (dry_year_surface_water + dry_year_gw) < perennial_crops_af_demanded:
            # pdb.set_trace()
            print(f'Perennial fallowing necessary for {curtailment_level} scenario for {irrigation_district}')

            #Step 1: Fallow all annual crops and calculate revenue loss: 
            revenue_lost_from_annuals = (district_annual_crops.af_demanded_2016 * district_annual_crops.revenue_per_af_water).sum()
            revenue_lost = revenue_lost_from_annuals
            end_revenue_loss_calcs = 0 

            acre_feet_curtailed = district_annual_crops.af_demanded_2016.sum()  # acre-feet already curtailed from annuals
            curtailment_remaining = curtailment_af - acre_feet_curtailed
            acres_fallowed_annuals = district_annual_crops.acreage_2016.sum()
            acres_fallowed = acres_fallowed_annuals
            
            # pdb.set_trace()
            # print('test acres fallowed calcs here')


            # assert there is enough water necessary to meet curtailment level 
            af_from_perennials = district_perennial_crops.af_demanded_2016.sum()

            class MyTest(unittest.TestCase):
                def test(self):
                    self.assertEqual(af_from_perennials, curtailment_remaining)

            # pdb.set_trace()              
            #Step 2: Calculate revenue loss from the required fallowing of perennial crops: 

            # if deficit_irrigation_option == 0: # usually only sorts this way when deficit irrigation not an option 
                # pdb.set_trace()
                # print('sort by highest replacement cost here')

            district_perennial_crops_sorted = district_perennial_crops.sort_values('cost_pulling_replanting_orchard_per_acre_year5')
            district_perennial_crops = district_perennial_crops_sorted  # for crop pulling, sort crops by cheapest to pull and replant 

            for num, crop_af_demanded in enumerate(district_perennial_crops.af_demanded_2016.tolist()):

                if deficit_irrigation_option == 1: 
                    if district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num] * district_perennial_crops.acreage_2016.values[num]  < district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded:  # cheaper to pull than to fallow
                        # pdb.set_trace()
                        # print('this crop is more expensive to fallow than to pull')
                        use_rdi = 0 # if it's cheaper to pull the crop, do not use rdi 
                    else:
                        use_rdi = 1 
                else:
                    use_rdi = 0 
                # switch from deficit to pulling if pulling is cheaper 

                # acre_feet_curtailed_this_crop = district_annual_crops.af_demanded_2016[num]
                if use_rdi == 0:
                    acre_feet_curtailed = crop_af_demanded + acre_feet_curtailed
                    acre_feet_this_crop_can_giveup = crop_af_demanded
                if use_rdi == 1:
                    acre_feet_curtailed = ( 0.5 * crop_af_demanded ) + acre_feet_curtailed  # 50% of water supplied to crop
                    acre_feet_this_crop_can_giveup = 0.5 * crop_af_demanded

                ratio_final_fallowed_crop = (curtailment_remaining /  acre_feet_this_crop_can_giveup)


                if curtailment_remaining > acre_feet_this_crop_can_giveup:  # continue on, as this entire crop needs to be curtailed 
                    # pdb.set_trace()
                    # print('curtailment remaining should be higher than water demanded for this crop')  

                    if end_revenue_loss_calcs == 0:
                        curtailment_remaining = curtailment_af - acre_feet_curtailed

                        # new revenue loss calculation
                        revenue_lost_this_crop = district_perennial_crops.acreage_2016.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]

                        if use_rdi == 1:
                            revenue_lost_this_crop = district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded
                            # curtailment_remaining = curtailment_af -  acre_feet_curtailed  # acre_feet_curtailed = 50% of water supplied to crop
                        
                        revenue_lost = revenue_lost_this_crop + revenue_lost
                        acres_fallowed = acres_fallowed + district_perennial_crops.acreage_2016.values[num]
            
                elif curtailment_remaining <= acre_feet_this_crop_can_giveup:   # if curtailment remaining is less than af demanded in current crop
                    # pdb.set_trace()
                    # print('curtailment remaining dipped below the water demanded for this crop')
                    if end_revenue_loss_calcs == 0:
                        # pdb.set_trace()

                        last_crop_revenue_loss = ratio_final_fallowed_crop *  district_perennial_crops.acreage_2016.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]
                        # curtailment_remaining * district_perennial_crops.revenue_per_af_water.values[num]
                        if use_rdi == 1:
                            last_crop_revenue_loss = ratio_final_fallowed_crop * ( district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded  )

                        total_revenue_lost = revenue_lost + last_crop_revenue_loss
                        # pdb.set_trace()
                        # print('test orange cove here')                        

                        last_crop_acres_fallowed = ratio_final_fallowed_crop *  district_perennial_crops.acreage_2016.values[num]   # ratio of last crops fallowed
                        # pdb.set_trace()
                        # print('fix last crop acres fallowed here')
                        acres_fallowed = acres_fallowed + last_crop_acres_fallowed
                        acres_fallowed_perennials = acres_fallowed - acres_fallowed_annuals
                        if deficit_irrigation_option == 0:
                            acres_pulled = acres_fallowed_perennials
                        # pdb.set_trace()

                    end_revenue_loss_calcs = 1 



            ####### Special Case: Stress irrigation not enough to meet curtailments and trees are pulled ############
            if (end_revenue_loss_calcs == 0 ) and (deficit_irrigation_option == 1):  # Stress irrigation was not enough to meet curtailment levels 
                # check that acre_feet_curtailed == water demand from annuals + 50% water demand from perennials:
                water_cut_so_far = district_annual_crops.af_demanded_2016.sum()  + 0.5 * district_perennial_crops.af_demanded_2016.sum()
                class MyTest(unittest.TestCase):
                    def test(self):
                        self.assertEqual(water_cut_so_far, acre_feet_curtailed)
                # unittest water_cut_so_far == acre_feet_curtailed

                # pdb.set_trace()
                # print('some crops have to be pulled')
                # print('check curtailment_remaining == curtailment_af - water_cut_so_far ')
                district_perennial_crops_sorted = district_perennial_crops.sort_values('cost_pulling_replanting_orchard_per_acre_year5')
                district_perennial_crops = district_perennial_crops_sorted  # sort in order of cheapest to pull -> most expensive 
                for num, crop_af_demanded in enumerate(district_perennial_crops.af_demanded_2016.tolist()):
                    
                    acre_feet_this_crop_can_giveup = 0.5 * crop_af_demanded
                    ratio_final_fallowed_crop = (curtailment_remaining /  acre_feet_this_crop_can_giveup)

                    acre_feet_curtailed = ( 0.5 * crop_af_demanded ) + acre_feet_curtailed   # reduce applied water by another 50% of original demand, requiring pulling and replanting of the tree crop the next season
                  
                    # pdb.set_trace()
                    print(district_perennial_crops.index[num])
                    if curtailment_remaining > acre_feet_this_crop_can_giveup:  # continue on, as this entire crop needs to be curtailed 
                        # pdb.set_trace()
                        # print('curtailment remaining should be higher than water demanded for this crop')  

                        if end_revenue_loss_calcs == 0:
                            curtailment_remaining = curtailment_af - acre_feet_curtailed

                            # new revenue loss calculation
                            revenue_lost_this_crop = district_perennial_crops.acreage_2016.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]
                            revenue_lost_this_crop = revenue_lost_this_crop - district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded  # subtract lost revenue since this is already counted
                            # if deficit_irrigation_option == 1:
                            #     revenue_lost_this_crop = district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded
                            #     # curtailment_remaining = curtailment_af -  acre_feet_curtailed  # acre_feet_curtailed = 50% of water supplied to crop
                            

                            revenue_lost = revenue_lost_this_crop + revenue_lost
                            # acres_fallowed = acres_fallowed + district_perennial_crops.acreage_2016.values[num]
                            # pdb.set_trace()
                            # print('test out pulled acreage calcs')
                            acres_pulled = acres_pulled + district_perennial_crops.acreage_2016.values[num]


                    elif curtailment_remaining <= acre_feet_this_crop_can_giveup:   # if curtailment remaining is less than af demanded in current crop
                        # Final scenario iteration 
                        # print('curtailment remaining dipped below the water demanded for this crop')
                        if end_revenue_loss_calcs == 0:
                            # pdb.set_trace()

                            last_crop_revenue_loss_pre = ratio_final_fallowed_crop *  district_perennial_crops.acreage_2016.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]
                            last_crop_revenue_loss = last_crop_revenue_loss_pre - ratio_final_fallowed_crop * (district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded )  # subtract lost revenue since already counted

                            # curtailment_remaining * district_perennial_crops.revenue_per_af_water.values[num]
                            # if deficit_irrigation_option == 1:
                                # last_crop_revenue_loss = ( curtailment_remaining /  crop_af_demanded ) * ( district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded  )

                            total_revenue_lost = revenue_lost + last_crop_revenue_loss
                            # pdb.set_trace()
                            # print('test very end here')

                            last_crop_acres_fallowed = ratio_final_fallowed_crop *  district_perennial_crops.acreage_2016.values[num]   # ratio of last crops fallowed
                            # pdb.set_trace()
                            # print('fix last crop acres fallowed here')
                            # acres_fallowed = acres_fallowed + last_crop_acres_fallowed
                            # acres_fallowed_perennials = acres_fallowed - acres_fallowed_annuals

                            # pdb.set_trace()
                            # print('this is what should happen at crop 3008')
                            acres_pulled = acres_pulled + ratio_final_fallowed_crop * district_perennial_crops.acreage_2016.values[num]
                        # pdb.set_trace()
                        end_revenue_loss_calcs = 1 



            if (end_revenue_loss_calcs == 0 ) and (deficit_irrigation_option == 1): 
                pdb.set_trace()
                print('something is still wrong bacause fallowing all land should mean zero water demand ')


    total_acres_fallowed = acres_fallowed

    # pdb.set_trace()
    return total_revenue_lost, curtailment_af, total_acres_fallowed, acres_fallowed_annuals, acres_fallowed_perennials, acres_pulled, baseline_acreage

    # pdb.set_trace()

# calculate water shortage (from AWMPs)  
# calculate which crops will be fallowed (starting with field crops)
# calculate revenue loss associated with fallowed fields (dollars per acre, for orchard crops: number of trees pulled and lost opportunity cost )
# pdb.set_trace()

irrigation_district_list_graphed = [
    'Westlands Water District',

    'Cawelo Water District',

    'Kern Delta Water District',
    'Tulare Lake Basin Water Storage District',
    'Delano - Earlimart Irrigation District',
    'Wheeler Ridge - Maricopa Water Storage District',
    'Semitropic Water Service District',

    'Shafter - Wasco Irrigation District',
    'Kern - Tulare Water District',
    'Buena Vista Water Storage District',

    'Consolidated Irrigation District',

    'Orange Cove Irrigation District',
    'Panoche Water District',
    'Pixley Irrigation District',
    'Riverdale Irrigation District',

    'Lindmore Irrigation District',
    'James Irrigation District']




irrigation_district_list_all = [
    'Wheeler Ridge - Maricopa Water Storage District',
    'Westlands Water District',
    'Tulare Irrigation District',
    'Cawelo Water District',
    'Lost Hills Water District',
    # 'Lower Tule River Irrigation District',   # no GW estimates 
    'Kern Delta Water District',
    'Tulare Lake Basin Water Storage District',
    'Delano - Earlimart Irrigation District',
    'Semitropic Water Service District',
    # 'Arvin - Edison Water Storage District',    # no GW estimates 
    'Shafter - Wasco Irrigation District',
    'North Kern Water Storage District',
    'Kern - Tulare Water District',
    'Buena Vista Water Storage District',
    # 'Alta Irrigation District',    # no GW estimates 
    # 'Berrenda Mesa Water District',     # no GW estimates 
    'Consolidated Irrigation District',
    # 'Corcoran Irrigation District',    # no GW estimates 
    'Fresno Irrigation District',
    'Orange Cove Irrigation District',
    'Panoche Water District',
    'Pixley Irrigation District',
    'Riverdale Irrigation District',
    # 'Kings River Water District',     # no GW estimates 
    'Lindmore Irrigation District',
    'James Irrigation District',
    # 'Firebaugh Canal Company',    # no GW estimates 
    'Dudley Ridge Water District'] 

# irrigation_district_list = [
#     # 'Tulare Irrigation District',
#     # 'Cawelo Water District',
#     # 'Lost Hills Water District' ] #,
#     'Lower Tule River Irrigation District']


# # individual irrigation test ##
# deficit_irrigation_option = 0
# irrigation_district = 'Consolidated Irrigation District'
# curtailment_level = 'gw_reduction_50_percent'
# # curtailment_level = 'baseline'
# total_revenue_lost, curtailment_af, total_acres_fallowed, acres_fallowed_annuals, acres_fallowed_perennials, acres_pulled_rdi = calculate_water_curtailment(irrigation_district, curtailment_level, deficit_irrigation_option)
# pdb.set_trace()
# print('Stop here- individual calculations complete')



######## Start of analysis script ############
irrigation_district_list = irrigation_district_list_graphed    # Select irrigation districts analyzed 

run_dollars_per_acre_foot_cals = 0 # optional - only run if updated data in 'site_codes_with_crop_types.csv' 
if run_dollars_per_acre_foot_cals == 1:    # (generated codes_with_price_per_acre datafile, used for all irrigation districts)
    # Step 1: connect site codes to applied water per acre 
    codes_1990_2016_with_af = connect_site_codes_to_applied_water_per_acre()
    # Step 2: Connect CC economic data to crop dataframe 
    df_tlb_year_2016, codes_with_price_per_acre = county_commissioner_data(codes_1990_2016_with_af)


overall_ID_table = set_up_overall_table(irrigation_district_list)


# Baseline Calcs for irrigation district: 
for irrigation_district in irrigation_district_list:

    district_crops_sorted_by_water_value = generate_district_crop_table(irrigation_district)
    baseline_revenue = calculate_baseline_revenue(irrigation_district)
    overall_ID_table.baseline_revenue[irrigation_district] = baseline_revenue


curtailment_level_list = [
    'baseline',
    'gw_reduction_25_percent',
    'gw_reduction_50_percent',
    'gw_reduction_75_percent']

for curtailment_level in curtailment_level_list:

    # Curtailment calcs for irrigation district 
    for irrigation_district in irrigation_district_list:

        deficit_irrigation_option = 0  # if deficit_irrigation_option = 1 , orchard crop revenue loss is calculated by reducing irrigation 50% and eliminating crop yield for season 
    
        # retrieve data to calculate AF water shortage (base year)
        if curtailment_level == 'baseline':
            deficit_irrigation_option = 1 

        total_revenue_lost, curtailment_af, total_acres_fallowed, acres_fallowed_annuals, acres_fallowed_perennials, acres_pulled, baseline_acreage = calculate_water_curtailment(irrigation_district, curtailment_level, deficit_irrigation_option)

        if curtailment_level == 'baseline':
            overall_ID_table.curtailment_af_baseline[irrigation_district] = curtailment_af
            overall_ID_table.total_revenue_lost_baseline[irrigation_district] = total_revenue_lost
            overall_ID_table.annual_acres_fallowed_baseline[irrigation_district] = acres_fallowed_annuals
            overall_ID_table.perennial_acres_fallowed_baseline[irrigation_district] = acres_fallowed_perennials
            overall_ID_table.total_acres_fallowed_baseline[irrigation_district] = total_acres_fallowed
            overall_ID_table.total_orchards_pulled_baseline[irrigation_district] = acres_pulled
            overall_ID_table.baseline_acreage[irrigation_district] = baseline_acreage
        if curtailment_level == 'gw_reduction_25_percent':
            overall_ID_table.curtailment_af_25[irrigation_district] = curtailment_af
            overall_ID_table.total_revenue_lost_25[irrigation_district] = total_revenue_lost
            overall_ID_table.annual_acres_fallowed_25[irrigation_district] = acres_fallowed_annuals
            overall_ID_table.perennial_acres_fallowed_25[irrigation_district] = acres_fallowed_perennials
            overall_ID_table.total_acres_fallowed_25[irrigation_district] = total_acres_fallowed
            overall_ID_table.total_orchards_pulled_25[irrigation_district] = acres_pulled
        if curtailment_level == 'gw_reduction_50_percent':
            overall_ID_table.curtailment_af_50[irrigation_district] = curtailment_af
            overall_ID_table.total_revenue_lost_50[irrigation_district] = total_revenue_lost
            overall_ID_table.annual_acres_fallowed_50[irrigation_district] = acres_fallowed_annuals
            overall_ID_table.perennial_acres_fallowed_50[irrigation_district] = acres_fallowed_perennials
            overall_ID_table.total_acres_fallowed_50[irrigation_district] = total_acres_fallowed
            overall_ID_table.total_orchards_pulled_50[irrigation_district] = acres_pulled
        if curtailment_level == 'gw_reduction_75_percent':
            overall_ID_table.curtailment_af_75[irrigation_district] = curtailment_af
            overall_ID_table.total_revenue_lost_75[irrigation_district] = total_revenue_lost
            overall_ID_table.annual_acres_fallowed_75[irrigation_district] = acres_fallowed_annuals
            overall_ID_table.perennial_acres_fallowed_75[irrigation_district] = acres_fallowed_perennials
            overall_ID_table.total_acres_fallowed_75[irrigation_district] = total_acres_fallowed
            overall_ID_table.total_orchards_pulled_75[irrigation_district] = acres_pulled


# pdb.set_trace()

if deficit_irrigation_option == 1: 
    overall_ID_table.to_csv('deficit_irrigation_option_revenue_loss_estimates.csv', index = True)


elif irrigation_district_list == irrigation_district_list_graphed:
    overall_ID_table.to_csv('overall_irrigation_district_revenue_loss_estimates_to_graph.csv', index = True)
elif irrigation_district_list == overall_irrigation_district_revenue_loss_estimates_all:
    overall_ID_table.to_csv('overall_irrigation_district_revenue_loss_estimates.csv', index = True)

pdb.set_trace()



































