import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
import unittest

# make empty results table
def set_up_overall_table(irrigation_district_list, gw_reduction):
  prefix = ['curtailment_af_', 'total_revenue_lost_', 'annual_acres_fallowed_',
            'perennial_acres_fallowed_', 'total_acres_fallowed_', 'total_orchards_pulled_']
  columns = ['baseline'] + [str(i) for i in gw_reduction]
  overall_ID_columns = ['baseline_revenue', 'baseline_acreage']

  for c in columns:
    for p in prefix:
      overall_ID_columns += [p+c]
  print(overall_ID_columns)
  return pd.DataFrame(index=irrigation_district_list, columns=overall_ID_columns)


def generate_district_crop_table(irrigation_district, year):

  codes_with_price_per_acre = pd.read_csv('codes_with_price_per_acre.csv', index_col = 'site_code_1990_2016') 
  crops_in_irrigation_district = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '.csv')), index_col = 'crop_ID', usecols = ['crop_ID', year]) 
  crops_in_irrigation_district = crops_in_irrigation_district.rename(columns = {year: 'acreage'})
  crops_sorted = crops_in_irrigation_district.sort_values('acreage', ascending = False)
  crops_above_10_acres = crops_sorted[crops_sorted['acreage'] > 10 ]  # filter out negligible crops 
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

    crops_above_10_acres.crop_type[crop_ID] = codes_with_price_per_acre.site_name_1990_2016[crop_ID] # add crop type column 
    crops_above_10_acres.is_orchard[crop_ID] = codes_with_price_per_acre.is_orchard_crop_1990_2016[crop_ID] # add orchard column 
    crops_above_10_acres.is_annual[crop_ID] = codes_with_price_per_acre.is_annual_crop_1990_2016[crop_ID] # add field crop column 
    crops_above_10_acres.af_applied_water_per_acre[crop_ID] = codes_with_price_per_acre.af_applied_water[crop_ID] # add AW column 
    crops_above_10_acres.revenue_per_af_water[crop_ID] = codes_with_price_per_acre.revenue_per_af_water[crop_ID]  # add $/AF-water column

    crops_above_10_acres.cost_pulling_replanting_orchard_per_acre[crop_ID] = codes_with_price_per_acre.tree_loss_price_per_acre[crop_ID]  # cost per acre of pulling and fallowing
    crops_above_10_acres.cost_pulling_replanting_orchard_per_acre_year5[crop_ID] = codes_with_price_per_acre.tree_loss_price_per_acre_year5[crop_ID]  # cost per acre of pulling and fallowing of 5-year-old tree
    crops_above_10_acres.total_revenue_from_crop[crop_ID] = codes_with_price_per_acre.dollars_per_acre[crop_ID] * crops_above_10_acres.acreage.values[num] # calculate revenue 

  # pdb.set_trace()
  column_name = str(irrigation_district) + '_crop_codes'
  # crops_above_10_acres = crops_above_10_acres.rename(columns = {'acreage' : column_name})

  crops_above_10_acres.index = crops_above_10_acres.index.rename(column_name)
  # pdb.set_trace()

  crops_above_10_acres['af_demanded'] = crops_above_10_acres.af_applied_water_per_acre * crops_above_10_acres['acreage']
  district_crops_sorted_by_water_value = crops_above_10_acres.sort_values('revenue_per_af_water')

  district_crops_sorted_by_water_value.to_csv(os.path.join(irrigation_district, 'table_major_crops_in_district_%s.csv' % year), index = True) 
  return district_crops_sorted_by_water_value


def calculate_baseline_revenue(irrigation_district, year):
  district_crops_sorted_by_water_value = pd.read_csv(os.path.join(irrigation_district, 'table_major_crops_in_district_%s.csv' % year), index_col = [0])

  baseline_revenue = district_crops_sorted_by_water_value.total_revenue_from_crop.sum()
  # pdb.set_trace()
  return baseline_revenue


def calculate_water_curtailment(irrigation_district, curtailment_level, RDI, year):

  district_crops_sorted_by_water_value = pd.read_csv(os.path.join(irrigation_district, 'table_major_crops_in_district_%s.csv' % year), index_col = [0])

  district_crops_sorted_by_water_value.revenue_per_af_water = district_crops_sorted_by_water_value.revenue_per_af_water.fillna(value = 0)  # convert nans to zeros 
  baseline_acreage = district_crops_sorted_by_water_value.acreage.values.sum()

  water_portfolios = pd.read_csv('irrigation_district_water_portfolios.csv', index_col = 'irrigation district' )  # 2009 is a normal year 
  wet_year_surface_water = water_portfolios.wet_year_surface_water[irrigation_district]
  wet_year_gw = water_portfolios.wet_year_gw[irrigation_district]
  dry_year_surface_water = water_portfolios.dry_year_surface_water[irrigation_district]

  # pdb.set_trace()
  if curtailment_level == 'baseline':
    dry_year_gw = water_portfolios.dry_year_gw[irrigation_district]
  else:
    dry_year_gw = water_portfolios.dry_year_gw[irrigation_district] * (1 - float(curtailment_level)/100)

  district_annual_crops = district_crops_sorted_by_water_value[district_crops_sorted_by_water_value.is_annual == 1 ]
  annual_crops_af_demanded = district_annual_crops.af_demanded.sum()

  district_perennial_crops = district_crops_sorted_by_water_value[district_crops_sorted_by_water_value.is_orchard == 1 ]
  perennial_crops_af_demanded = district_perennial_crops.af_demanded.sum()

  # set initial values 
  total_revenue_lost = 0
  acres_fallowed = 0 
  acres_fallowed_annuals = 0
  acres_fallowed_perennials = 0 
  acres_pulled = 0

  revenue_lost_pulling_orchards = np.zeros(50)
  revenue_lost_rdi = np.zeros(50)

  if dry_year_surface_water > district_crops_sorted_by_water_value.af_demanded.sum():   # if SW enough to supply ag water during dry year
    print(f'Sufficient SW for {irrigation_district} during dry year')
    curtailment_af = 0 
    total_revenue_lost = 0
    acres_fallowed = 0 
    acres_fallowed_annuals = 0
    acres_fallowed_perennials = 0 

  elif (dry_year_surface_water + dry_year_gw) > district_crops_sorted_by_water_value.af_demanded.sum():
    # pdb.set_trace()
    print(f'No economic loss for {curtailment_level} scenario for {irrigation_district}')
    curtailment_af = 0 
    total_revenue_lost = 0 
    acres_fallowed = 0 
    acres_fallowed_annuals = 0
    acres_fallowed_perennials = 0 

  else:
    print('Curtailments necessary')
    curtailment_af = district_crops_sorted_by_water_value.af_demanded.sum() -  (dry_year_surface_water + dry_year_gw)
    
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
      for num, crop_af_demanded in enumerate(district_annual_crops.af_demanded.tolist()):

        # acre_feet_curtailed_this_crop = district_annual_crops.af_demanded[num]
        acre_feet_curtailed = crop_af_demanded + acre_feet_curtailed

        if curtailment_remaining > crop_af_demanded:  # if current crop neeeds to be pulled completely: 
          if end_revenue_loss_calcs == 0:
            curtailment_remaining = curtailment_af - acre_feet_curtailed
            revenue_lost_this_crop = district_annual_crops.revenue_per_af_water.values[num] * crop_af_demanded
            revenue_lost = revenue_lost_this_crop + revenue_lost
            acres_fallowed = acres_fallowed + district_annual_crops.acreage.values[num]

        elif curtailment_remaining <= crop_af_demanded:   # if curtailment remaining is less than af demanded in current crop
          if end_revenue_loss_calcs == 0:

            last_crop_revenue_loss = curtailment_remaining * district_annual_crops.revenue_per_af_water.values[num]

            total_revenue_lost = revenue_lost + last_crop_revenue_loss

            last_crop_acres_fallowed = curtailment_remaining /  crop_af_demanded *  district_annual_crops.acreage.values[num]   # ratio of last crops fallowed
            acres_fallowed = acres_fallowed + last_crop_acres_fallowed
            acres_fallowed_annuals = acres_fallowed

          end_revenue_loss_calcs = 1 


    if (dry_year_surface_water + dry_year_gw) < perennial_crops_af_demanded:

      #Step 1: Fallow all annual crops and calculate revenue loss: 
      revenue_lost_from_annuals = (district_annual_crops.af_demanded * district_annual_crops.revenue_per_af_water).sum()
      revenue_lost = revenue_lost_from_annuals
      end_revenue_loss_calcs = 0 

      acre_feet_curtailed = district_annual_crops.af_demanded.sum()  # acre-feet already curtailed from annuals
      curtailment_remaining = curtailment_af - acre_feet_curtailed
      acres_fallowed_annuals = district_annual_crops.acreage.sum()
      acres_pulled = 0 
      af_from_perennials = district_perennial_crops.af_demanded.sum()

      district_perennial_crops_sorted = district_perennial_crops.sort_values('cost_pulling_replanting_orchard_per_acre_year5')
      district_perennial_crops = district_perennial_crops_sorted  # for crop pulling, sort crops by cheapest to pull and replant 
      district_perennial_crops['orchard_crop_pulled'] = np.zeros(len(district_perennial_crops))

      for num, crop_af_demanded in enumerate(district_perennial_crops.af_demanded.tolist()):

        if district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num] * district_perennial_crops.acreage.values[num]  < district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded:  # cheaper to pull than to fallow
          district_perennial_crops.orchard_crop_pulled.values[num] = 1 # this crop is pulled because it's cheaper to do so
          # pdb.set_trace()
          # print('this crop is more expensive to fallow than to pull')
          use_rdi = 0 # if it's cheaper to pull the crop, do not use rdi 
        else:
          use_rdi = 1 

        # acre_feet_curtailed_this_crop = district_annual_crops.af_demanded[num]
        if use_rdi == 0:
          acre_feet_curtailed = crop_af_demanded + acre_feet_curtailed     # entire crop was pulled, so full volume of would-have-been-used water (crop_af_demanded) is added to the running total of acre_feet_curtailed- NKM 7/11/19
          acre_feet_this_crop_can_giveup = crop_af_demanded   
        if use_rdi == 1:
          acre_feet_curtailed = ( (1 - RDI) * crop_af_demanded ) + acre_feet_curtailed  # RDI% of water supplied to crop   - since we're using RDI, only a fraction of the water demanded has to be curtailed
          acre_feet_this_crop_can_giveup = (1 - RDI) * crop_af_demanded      # correction: represents amount of water being given up at this point in the code (just the amount curtailed using RDI- full curtailment will occur later in need-be)  - NKM 7/13/19
          # ^^Higher RDI value means crop is using a higher portion of it's original (e.g. RDI = 0.9 means an orchard is using 90% of original water supply) -NKM
          #   water allotment - NKM 7/11/19
          #   acre_feet_this_crop_can_giveup is the portion of water stress-irrigated crops give up.  This water is tallied in the accounting, should the land need to be fallowed completely  - NKM 9/13/19

        ratio_final_fallowed_crop = (curtailment_remaining /  acre_feet_this_crop_can_giveup)


        if curtailment_remaining > acre_feet_this_crop_can_giveup:  # continue on, as this entire crop needs to be curtailed 
          # pdb.set_trace()
          print('curtailment remaining should be higher than water demanded for this crop')  

          if end_revenue_loss_calcs == 0:
            curtailment_remaining = curtailment_af - acre_feet_curtailed

            # new revenue loss calculation
            revenue_lost_this_crop = district_perennial_crops.acreage.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]

            if use_rdi == 1:
              revenue_lost_this_crop = district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded
              acres_fallowed_perennials = acres_fallowed_perennials + district_perennial_crops.acreage.values[num]
              # curtailment_remaining = curtailment_af -  acre_feet_curtailed  # acre_feet_curtailed = 50% of water supplied to crop
            if use_rdi == 0: 
              acres_pulled = acres_pulled + district_perennial_crops.acreage.values[num]
            revenue_lost = revenue_lost_this_crop + revenue_lost
      
        elif curtailment_remaining <= acre_feet_this_crop_can_giveup:   # if curtailment remaining is less than af demanded in current crop

          if end_revenue_loss_calcs == 0:

            last_crop_revenue_loss = ratio_final_fallowed_crop *  district_perennial_crops.acreage.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]

            if use_rdi == 1:
              last_crop_revenue_loss = ratio_final_fallowed_crop * ( district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded  )
              acres_fallowed_perennials = acres_fallowed_perennials + ratio_final_fallowed_crop * district_perennial_crops.acreage.values[num]

            total_revenue_lost = revenue_lost + last_crop_revenue_loss
            revenue_lost = total_revenue_lost

            if use_rdi == 0: 
              acres_pulled = acres_pulled + (ratio_final_fallowed_crop *  district_perennial_crops.acreage.values[num])
            curtailment_remaining = 0 

          end_revenue_loss_calcs = 1 

        # pdb.set_trace()
        revenue_lost_rdi[num] = revenue_lost


      ####### Special Case: Stress irrigation not enough to meet curtailments and trees are pulled ############
      if end_revenue_loss_calcs == 0:  # Stress irrigation was not enough to meet curtailment levels 
        # check that acre_feet_curtailed == water demand from annuals + RDI% water demand from perennials:
        water_cut_so_far = district_annual_crops.af_demanded.sum()  + (1- RDI) * district_perennial_crops.af_demanded.sum()   # A higher RDI here means less water was cut - NKM 7/11/19
        class MyTest(unittest.TestCase):
          def test(self):
            self.assertEqual(water_cut_so_far, acre_feet_curtailed)
        # unittest water_cut_so_far == acre_feet_curtailed

        district_perennial_crops_sorted = district_perennial_crops.sort_values('cost_pulling_replanting_orchard_per_acre_year5')
        district_perennial_crops = district_perennial_crops_sorted  # sort in order of cheapest to pull -> most expensive 
        district_perennial_crops = district_perennial_crops[district_perennial_crops.orchard_crop_pulled != 1 ]  # only option are the perennial crops that have not already been pulled

        for num, crop_af_demanded in enumerate(district_perennial_crops.af_demanded.tolist()):
          
          acre_feet_this_crop_can_giveup = RDI * crop_af_demanded  # This represents the amount of water the crop still used after deficit irrigation - NKM 7/11/19
          ratio_final_fallowed_crop = (curtailment_remaining /  acre_feet_this_crop_can_giveup)

          acre_feet_curtailed = ( RDI * crop_af_demanded ) + acre_feet_curtailed   # curtail the rest of the orchards water-demanded, requiring pulling and replanting of the tree crop the next season. - NKM 7/11/19
          
          print(district_perennial_crops.index[num])
          if curtailment_remaining > acre_feet_this_crop_can_giveup:  # continue on, as this entire crop needs to be curtailed 

            if end_revenue_loss_calcs == 0:
              curtailment_remaining = curtailment_af - acre_feet_curtailed

              revenue_lost_this_crop = district_perennial_crops.acreage.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]
              revenue_lost_this_crop = revenue_lost_this_crop - district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded  # subtract lost revenue since this is already counted

              revenue_lost = revenue_lost_this_crop + revenue_lost
              acres_pulled = acres_pulled + district_perennial_crops.acreage.values[num]
              acres_fallowed_perennials = acres_fallowed_perennials - district_perennial_crops.acreage.values[num]  # these acres are now pulled and not fallowed

          elif curtailment_remaining <= acre_feet_this_crop_can_giveup:   # if curtailment remaining is less than af demanded in current crop
            # Final scenario iteration 
            if end_revenue_loss_calcs == 0:
              curtailment_remaining = curtailment_remaining - ratio_final_fallowed_crop * acre_feet_curtailed

              last_crop_revenue_loss_pre = ratio_final_fallowed_crop *  district_perennial_crops.acreage.values[num]  * district_perennial_crops.cost_pulling_replanting_orchard_per_acre_year5.values[num]
              last_crop_revenue_loss = last_crop_revenue_loss_pre - ratio_final_fallowed_crop * (district_perennial_crops.revenue_per_af_water.values[num] * crop_af_demanded )  # subtract lost revenue since already counted

              total_revenue_lost = revenue_lost + last_crop_revenue_loss
              last_crop_acres_pulled = ratio_final_fallowed_crop *  district_perennial_crops.acreage.values[num]   # ratio of last crops fallowed
              acres_pulled = acres_pulled + ratio_final_fallowed_crop * district_perennial_crops.acreage.values[num]
              acres_fallowed_perennials = acres_fallowed_perennials - ratio_final_fallowed_crop * district_perennial_crops.acreage.values[num]  # these acres are now pulled and not fallowed

            end_revenue_loss_calcs = 1 



      if (end_revenue_loss_calcs == 0 ): 
        print('something is still wrong bacause fallowing all land should mean zero water demand ')

  return total_revenue_lost, curtailment_af, acres_fallowed_annuals, acres_fallowed_perennials, acres_pulled, baseline_acreage, revenue_lost_rdi, revenue_lost_pulling_orchards


######## Start of analysis script ############

irrigation_district_list = [
  'Wheeler Ridge - Maricopa Water Storage District',
  'Westlands Water District',
  'Riverdale Irrigation District',
  'Tulare Lake Basin Water Storage District',
  'Shafter - Wasco Irrigation District',
  'Semitropic Water Service District',
  'Pixley Irrigation District',
  'Orange Cove Irrigation District',
  'Lindmore Irrigation District',
  'Kern - Tulare Water District',
  'Kern Delta Water District',
  'James Irrigation District',
  'Delano - Earlimart Irrigation District',
  'Consolidated Irrigation District',
  'Cawelo Water District',
  'Buena Vista Water Storage District']

# # year = '2016'
# for year in ['1996', '2016']: # generate crop tables (only do this once)
#   for irrigation_district in irrigation_district_list:
#     print('Crop table: Year %s, %s' % (year, irrigation_district))
#     district_crops_sorted_by_water_value = generate_district_crop_table(irrigation_district, year)

for year in ['1996', '2016']:
  gw_reduction = [10, 20, 30, 40, 50]
  overall_ID_table = set_up_overall_table(irrigation_district_list, gw_reduction)
  for irrigation_district in irrigation_district_list:
    overall_ID_table.baseline_revenue[irrigation_district] = calculate_baseline_revenue(irrigation_district, year)

  curtailment_level_list = ['baseline'] + [str(g) for g in gw_reduction]

# Curtailment calcs for irrigation district 
  for curtailment_level in curtailment_level_list:
    for irrigation_district in irrigation_district_list:

      RDI = .4 # value between 0 and 1 (fraction of demand needed to keep trees alive at zero yield)  - NKM 7/13/19

      total_revenue_lost, curtailment_af, acres_fallowed_annuals, acres_fallowed_perennials, acres_pulled, baseline_acreage, revenue_lost_rdi, revenue_lost_pulling_orchards = calculate_water_curtailment(irrigation_district, curtailment_level, RDI, year)

      overall_ID_table['curtailment_af_%s' % curtailment_level][irrigation_district] = curtailment_af
      overall_ID_table['total_revenue_lost_%s' % curtailment_level][irrigation_district] = total_revenue_lost
      overall_ID_table['annual_acres_fallowed_%s' % curtailment_level][irrigation_district] = acres_fallowed_annuals
      overall_ID_table['perennial_acres_fallowed_%s' % curtailment_level][irrigation_district] = acres_fallowed_perennials
      overall_ID_table['total_orchards_pulled_%s' % curtailment_level][irrigation_district] = acres_pulled
      overall_ID_table['baseline_acreage'][irrigation_district] = baseline_acreage

  overall_ID_table.to_csv('revenue_loss_year_%s_rdi_%s.csv' % (year, RDI), index = True)
