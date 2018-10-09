## Plot a specific irrigation district ## 

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
from pur_and_county_data_retrieval import load_calPIP_data_all_years
from plotting_functions import plot_dataset_comparison
from plotting_functions import surface_water_bar_plot
from plotting_functions import gw_crop_type_comparison_plot
from plotting_functions import plot_data_for_irrigation_district
from plotting_functions import plot_tree_crop_percentages_for_irrigation_district
from plotting_functions import plot_water_demand_graph
from plotting_functions import plot_acreage_and_demand_side_by_side
from plotting_functions import plot_all_the_irrigation_district_bar_charts
# from plotting_functions import
# from pur_and_county_data_retrieval import 

normalized = 1
retrieve_data = 1
plot_single_irrigation_district = 1 
compare_with_county_data = 1
plot_water_demand = 1
create_bar_chart = 1

# Counties 
# irrigation_district = 'tlb_irrigation_districts_all'

# irrigation_district = 'Kings_County'
# irrigation_district = 'Kern_County'
# irrigation_district = 'Fresno_County'
irrigation_district = 'Tulare_County'

# irrigation_district = 'North_Kern_Water_Storage_District'
# irrigation_district = 'Cawelo_Water_District'
# irrigation_district = 'Wasco_Irrigation_District'
# irrigation_district = 'Buena_Vista_Water_Storage_District'

## List of automatically produced regions  ###

# irrigation_district = 'Tulare Irrigation District'
# irrigation_district = 'Cawelo Water District'
# irrigation_district = 'North Kern Water Storage District'

# irrigation_district = 'Lost Hills Water District'
# irrigation_district = 'Lower Tule River Irrigation District'
# irrigation_district = 'Westlands Water District'
# irrigation_district = 'Kern Delta Water District'
# irrigation_district = 'Tulare Lake Basin Water Storage District'   # this one must have some bugs 
# irrigation_district = 'Delano - Earlimart Irrigation District'
# irrigation_district = 'Wheeler Ridge - Maricopa Water Storage District'
# irrigation_district = 'Semitropic Water Service District'
# irrigation_district = 'Arvin - Edison Water Storage District'
# irrigation_district = 'Shafter - Wasco Irrigation District'
# irrigation_district = 'Southern San Joaquin Municipal Utility District'  # not in TLB 
# pdb.set_trace()

if os.path.isdir(str(irrigation_district)):
    irrig_file = 'exists'
else:
    os.mkdir(str(irrigation_district))


### Run this to re-extract data from this specific region: 
if retrieve_data == 1:  
    sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist = retrieve_data_for_irrigation_district(irrigation_district, normalized)

pdb.set_trace() 
print( 'check out totals_in_irrig_dist')

# Load calPUR dataset 
if normalized == 1 and plot_single_irrigation_district == 1:
    sum_crop_types_normalized = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
elif normalized == 0:
    sum_crop_types = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data' + str(irrigation_district) + '.csv')))


if compare_with_county_data == 1:  # county data only 
    # Load County Commissioner dataset 
    sum_cc_crop_types = county_commissioner_data(irrigation_district)

    # # Load calPIP dataset - not going to use in thesis 
    # (all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, 
    #     percent_tree_acreage_summed_for_year) = load_calPIP_data_all_years(irrigation_district)

    # Plot combination of datasets: 
    if normalized == 1:
        plot_dataset_comparison(irrigation_district, sum_crop_types_normalized, sum_cc_crop_types )
    else:    
        plot_dataset_comparison(irrigation_district, sum_crop_types, sum_cc_crop_types )

# pdb.set_trace()

if plot_water_demand == 1:
    plot_water_demand_graph(sum_crop_types_normalized, irrigation_district)


if compare_with_county_data == 0: 
    # pdb.set_trace()
    if normalized == 1:
        plot_data_for_irrigation_district(irrigation_district, sum_crop_types_normalized, normalized)
    if normalized == 0:
        plot_data_for_irrigation_district(irrigation_district, sum_crop_types, normalized)

if (create_bar_chart == 1) & (compare_with_county_data == 0):
    surface_water_bar_plot(irrigation_district, sum_crop_types_normalized)






