# average crop data for years 1991 - 1996

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):



for year in range (1991,1997):

    # pdb.set_trace()

    data_current_year = pd.read_csv(os.path.join(str('data_for_qgis/' + 'comtrs_all_sections' + str(year) + 'tree_data.csv')), header = None  )
    if not 'data_all_years' in locals():  # starts building dataframe
        data_all_years = data_current_year.rename(columns = {0: "comtrs", 1: str(year)})
        data_all_years2 = data_all_years.set_index("comtrs")
    else:  # adds to base each year
        df_with_year_to_add = data_current_year.rename(columns = {0: "comtrs", 1: str(year)})
        df_with_year_to_add2 = df_with_year_to_add.set_index("comtrs")
        # pdb.set_trace()
        # df_with_year_to_add = data_current_year.rename(columns = {0: comtrs})
        data_all_years2 = pd.merge(data_all_years2, df_with_year_to_add2, how = 'outer', left_index = True, right_index = True)

# pdb.set_trace()


averaged_1991_1996 = data_all_years2.mean(axis = 1)

averaged_1991_1996_2 = pd.DataFrame(averaged_1991_1996)
averaged_1991_1996_3 = averaged_1991_1996_2.rename(columns = {0: 'tree_acreage'})


tree_density_1991_1996 = averaged_1991_1996_3.tree_acreage / 640 * 100 
tree_density_1991_1996_2 = pd.DataFrame(tree_density_1991_1996)

tree_density_1991_1996_3 = tree_density_1991_1996_2.rename(columns = {'tree_acreage' : 'tree_density'})

# pdb.set_trace()
averaged_1991_1996_3.to_csv(str('data_for_qgis/averaged_1991_1996_tree_data.csv'))

tree_density_1991_1996_3.to_csv(str('data_for_qgis/tree_density_91_96.csv'))
# pdb.set_trace()



## create file for 2016 
year = 2016
data_current_year = pd.read_csv(os.path.join(str('data_for_qgis/' + 'comtrs_all_sections' + str(year) + 'tree_data.csv')), header = None  )
data_current_year2 = data_current_year.rename(columns = {0: 'comtrs', 1: 'tree_acreage'})
data_current_year3 = data_current_year2.set_index("comtrs")
tree_density_2016 = data_current_year3.tree_acreage / 640 * 100
tree_density_2016_2 = pd.DataFrame(tree_density_2016)
tree_density_2016_3 = tree_density_2016_2.rename(columns = {'tree_acreage' : 'tree_density'})
tree_density_2016_3.to_csv(str('data_for_qgis/tree_density_16.csv'))

pdb.set_trace()

