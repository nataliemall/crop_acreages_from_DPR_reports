## Plot data for a specific irrigation district ## 

import numpy as np 
import os 
import pdb
import pandas as pd


from pur_and_county_data_retrieval import retrieve_data_for_irrigation_district
from pur_and_county_data_retrieval import county_commissioner_data
from plotting_functions import plot_dataset_comparison
from plotting_functions import surface_water_bar_plot
from plotting_functions import gw_crop_type_comparison_plot
from plotting_functions import plot_data_for_irrigation_district
from plotting_functions import plot_water_demand_graph


retrieve_data = 1   # set equal to zero if you've already retrieved the data for the irrigation district.  Otherwise set equal to 1 
counties = 'Kings_County', 'Tulare_County', 'Fresno_County', 'Kern_County'   # list of your available counties 


############ Choose a region for which to plot data ###########

### Counties: ###

# irrigation_district = 'Kings_County'
# irrigation_district = 'Kern_County'
# irrigation_district = 'Fresno_County'
# irrigation_district = 'Tulare_County'

### larger regions ###
# irrigation_district = 'tlb_irrigation_districts_all'
# irrigation_district = 'comtrs_all_sections'

### Irrigation districts:  ###
# irrigation_district = 'Wasco Irrigation District'
irrigation_district = 'Buena Vista Water Storage District'
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

if irrigation_district in counties: # Compares with county commissioner data only if analyzing a county (kings, kern, fresno, or tulare) 
    compare_with_county_data = 1
else:
    compare_with_county_data = 0 


plot_single_irrigation_district = 1 
plot_water_demand = 1  # creates a time series of water demand within the region
create_bar_chart = 0   # keep this one equal to zero because I didn't give you the data 
normalized = 1  # The physical limit of 640 acres for aach 1-square-mile section is enforced. Keep this equal to one 

if not os.path.isdir(str(irrigation_district)):  # creates empty directory for the district if it does not yet exist
    os.mkdir(str(irrigation_district))


### Extract data from the specific region: 
if retrieve_data == 1:  
    sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist = retrieve_data_for_irrigation_district(irrigation_district, normalized)


# Load calPUR dataset 
if normalized == 1 and plot_single_irrigation_district == 1:  # read in data that has been normalized (i.e. each 1-square-mile section constrained to the physical limitation of 640 acres)
    sum_crop_types_normalized = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
elif normalized == 0:  # reads non-normalized data 
    sum_crop_types = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data' + str(irrigation_district) + '.csv')))


if compare_with_county_data == 1:  # Will run only if examining county data

    sum_cc_crop_types = county_commissioner_data(irrigation_district)  # Load County Commissioner dataset 

    # Plot combination of datasets: 
    if normalized == 1:
        plot_dataset_comparison(irrigation_district, sum_crop_types_normalized, sum_cc_crop_types )
    else:    
        plot_dataset_comparison(irrigation_district, sum_crop_types, sum_cc_crop_types )


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



pdb.set_trace() 


