### tulare_county_debugging.py

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

tulare_data = pd.read_csv('Tulare_County/calPUR_by_crop_type_Tulare_County.csv', index_col = 'crop_ID')

# pdb.set_trace()

for crop_ID in tulare_data.index:
	# pdb.set_trace()
	x_vals = tulare_data.columns.values
	y_vals = tulare_data[tulare_data.index == crop_ID].values.flatten()
	plt.plot(x_vals, y_vals)

plt.show()

tulare_data.headers()
pdb.set_trace()


