import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):



from data_retrieval_test import retrieve_data_for_irrigation_district_test
from data_retrieval_test import county_commissioner_data_test


irrigation_district = 'Orange Cove Irrigation District'
normalized = 1 

sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district_test(irrigation_district, normalized)
# 2016 annual crops: 134 acres


# CC Data
county = 'Tulare_County'
sum_cc_crop_types = county_commissioner_data_test(county)
# results: 2016 annual crops; 723034.0 acres 


pdb.set_trace()




