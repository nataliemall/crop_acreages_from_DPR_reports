# plot_district_crop_changes.py 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):
from matplotlib.patches import Patch

from pur_and_county_data_retrieval import retrieve_data_for_irrigation_district


row = 0 
column = 0 

fig, ax = plt.subplots(2,2, sharex = True)

legend_elements = [Patch(facecolor = 'orange', alpha=0.3, label = 'Drought year')]
ax[1,0].legend(handles = legend_elements, loc= 'lower right')  # custom legend 

plt.show()

pdb.set_trace()
