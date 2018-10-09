### Compile and read PUR formatted data 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
import re 
from tqdm import tqdm  # for something in tqdm(something something):

from adding_comtrs_functions import add_comtrs_pre_1990
from adding_comtrs_functions import add_comtrs_1990_2004
from adding_comtrs_functions import add_comtrs_2005_2016
from fix_pur_data_step1 import replace_bad_characters
# from pur_data_compiler_v10 import

# Step 0: Clean up the data since '?' results in errors 
replace_bad_characters()

pdb.set_trace()

# Step 1: Add the comtrs column (already completed for 1974 - 1989)
for year in range(1974,1990): 
    add_comtrs_pre_1990(year)  # preliminary processing of 1974 - 1989 data

pdb.set_trace()


# Step 2: add the comtrs columns to 1990 - 2004 data (already completed for 1990-2002)
for year in tqdm(range(1990,2005)):  # process post-1989 data by adding 'comtrs' row 
    add_comtrs_1990_2004(year)
    print(f'completed adding comtrs for year {year}')


pdb.set_trace()

# Step 3: add the comts from 2005 - 2016 data: 
for year in range(2005,2017):
    add_comtrs_2005_2016(year)



# add_comtrs_2005_2016(year)




