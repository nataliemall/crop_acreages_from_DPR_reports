### compare crop types within a county



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


def data_comparison_by_field_crop(irrigation_district, sum_cc_crop_types, crop_types_in_county):

    county_name = irrigation_district.split('_')[0]
    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df_all[df_all.county==county_name]

    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(20))
    highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)
    df.index = pd.to_datetime(df.index)

    # x_array = crop_types_in_county.columns.values
    
    x_array = pd.to_datetime(crop_types_in_county.columns.values)
    
    # make a graph of the most common commodities 

    # alfalfa: 
    crop_code = 23001  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    alfalfa_cc = df[df.crop == 'HAY ALFALFA']  # CC label  
    y_array_cc = alfalfa_cc[alfalfa_cc.index > '1989'].acres

    plt.plot(y_array_cc, label = 'Alfalfa CC', linestyle = '--', color = 'g')
    plt.plot(x_array, y_array, label = 'Alfalfa PUR', color = 'g')
    
    # silage: 
    crop_code = 22000  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    silage_cc = df[df.crop == 'SILAGE']  # CC label  
    y_array_cc = silage_cc[silage_cc.index > '1989'].acres

    plt.plot(y_array_cc, label = 'Silage CC', linestyle = '--', color = 'r')
    plt.plot(x_array, y_array, label = 'Silage PUR', color = 'r')

    # Wheat: 
    crop_code = 29139  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    wheat_cc = df[df.crop == 'WHEAT ALL']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres

    pdb.set_trace()
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'Wheat CC', linestyle = '--', color = 'y')
    plt.plot(x_array, y_array, label = 'Wheet PUR', color = 'y')



    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    # highest_acres2 = crop_types_in_county['2016'].sort_values(ascending = False).head(10)

    # pdb.set_trace()
    # test = crop_types_in_county['1990']
    plt.xlabel('year')
    plt.ylabel('crop acreage')
    plt.legend()
    plt.title(str('Primary Field Crops in' + str(county_name) + 'county'))
    plt.show()



def data_comparison_by_orchard_crop(irrigation_district, sum_cc_crop_types, crop_types_in_county):

    county_name = irrigation_district.split('_')[0]
    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df_all[df_all.county==county_name]

    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(30))
    print(df[df.index=='1990'].sort_values(by='acres', ascending=False).head(30))

    highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    
    x_array = pd.to_datetime(crop_types_in_county.columns.values)

    # make a graph of the most common commodities 

    # oranges: 
    crop_code = 2006  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    oranges_navel_cc = df[df.crop == 'ORANGES NAVEL']  # CC label  
    orange_valencia_cc = df[df.crop == 'ORANGES VALENCIA']  # CC label ORANGES VALENCIA

    oranges_navel_cc_vals = oranges_navel_cc[oranges_navel_cc.index > '1989'].acres
    oranges_valencia_cc_vals = orange_valencia_cc[orange_valencia_cc.index > '1989'].acres
    oranges_cc_total = oranges_navel_cc_vals + oranges_valencia_cc_vals


    plt.plot(oranges_cc_total, label = 'Oranges CC', linestyle = '--', color = 'g')
    plt.plot(x_array, y_array, label = 'Oranges PUR', color = 'g')
    
    # almonds: 
    crop_code = 3001  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    silage_cc = df[df.crop == 'ALMONDS ALL']  # CC label  
    y_array_cc = silage_cc[silage_cc.index > '1989'].acres

    plt.plot(y_array_cc, label = 'Almonds CC', linestyle = '--', color = 'r')
    plt.plot(x_array, y_array, label = 'Almonds PUR', color = 'r')

    # pistachios: 
    crop_code = 3011  # pistachio PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    wheat_cc = df[df.crop == 'PISTACHIOS']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres

    plt.plot(y_array_cc, label = 'Pistachios CC', linestyle = '--', color = 'y')
    plt.plot(x_array, y_array, label = 'Pistachios PUR', color = 'y')


    # walnuts: 
    crop_code = 3009  # walnut PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    wheat_cc = df[df.crop == 'WALNUTS ENGLISH']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres

    plt.plot(y_array_cc, label = 'Walnuts CC', linestyle = '--', color = 'b')
    plt.plot(x_array, y_array, label = 'Walnuts PUR', color = 'b')


    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    # highest_acres2 = crop_types_in_county['2016'].sort_values(ascending = False).head(10)

    # pdb.set_trace()
    # test = crop_types_in_county['1990']
    plt.xlabel('year')
    plt.ylabel('crop acreage')
    plt.legend()
    plt.title(str('Primary Orchard Crops in ' + str(county_name) + ' County'))

    plt.show()
    print('test')

    pdb.set_trace()






retrieve_data = 0
normalized = 1 

# county_list = [ 'Fresno_County', 'Tulare_County', 'Kings_County', 'Kern_County']

if retrieve_data == 1: 
    for irrigation_district in county_list: 
        if not os.path.isdir(str(irrigation_district)):  # creates this folder 
            os.mkdir(str(irrigation_district))

        sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district(irrigation_district, normalized)


irrigation_district = 'Tulare_County'

crop_types_in_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '_to_examine.csv')), index_col = 'crop_ID') 


sum_crop_types_each_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
sum_cc_crop_types = county_commissioner_data(irrigation_district) 


data_comparison_by_field_crop(irrigation_district, sum_cc_crop_types, crop_types_in_county)

data_comparison_by_orchard_crop(irrigation_district, sum_cc_crop_types, crop_types_in_county)



pdb.set_trace()




