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
    plt.plot(x_array, y_array, label = 'Alfalfa PUR', color = 'g')

    alfalfa_cc = df[df.crop == 'HAY ALFALFA']  # CC label  
    y_array_cc = alfalfa_cc[alfalfa_cc.index > '1989'].acres
    plt.plot(y_array_cc, label = 'Alfalfa CC', linestyle = '--', color = 'g')

    

    # silage: 
    crop_code = 22000  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'Silage PUR', color = '#fc9272')
    pdb.set_trace()

    silage_cc = df[df.crop == 'SILAGE']  # CC label  
    y_array_cc = silage_cc[silage_cc.index > '1989'].acres
    plt.plot(y_array_cc, label = 'Silage CC', linestyle = '--', color = 'r')

    # Wheat: 
    crop_code = 29139  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'Wheat PUR', color = 'y')

    wheat_cc = df[df.crop == 'WHEAT ALL']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'Wheat CC', linestyle = '--', color = 'y')

    # pdb.set_trace()

    # # Sudan: 
    # crop_code = 22011  # sudangrass PUR code    - very low 
    # y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    # plt.plot(x_array, y_array, label = 'Sudangrass PUR', color = 'm')

    sudan_cc = df[df.crop == 'HAY SUDAN']  # CC label  
    y_array_cc = sudan_cc[sudan_cc.index > '1989'].acres
    plt.plot(sudan_cc.index[10:37], sudan_cc[10:37].acres.values, label = 'Sudan CC', linestyle = '--', color = 'm')

    oats_grain_cc = df[df.crop == 'OATS GRAIN']  # CC label  
    y_array_cc = oats_grain_cc[oats_grain_cc.index > '1989'].acres
    plt.plot(oats_grain_cc.index[10:37], oats_grain_cc[10:37].acres.values, label = 'OATS GRAIN CC', linestyle = '--', color = 'b')

    hay_grain_cc = df[df.crop == 'HAY GRAIN']  # CC label  
    y_array_cc = hay_grain_cc[hay_grain_cc.index > '1989'].acres
    plt.plot(hay_grain_cc.index[10:37], hay_grain_cc[10:37].acres.values, label = 'HAY GRAIN CC', linestyle = '--', color = '#99d8c9')


    pasture_forage_cc = df[df.crop == 'PASTURE FORAGE MISC.']  # CC label  
    y_array_cc = pasture_forage_cc[pasture_forage_cc.index > '1989'].acres
    plt.plot(pasture_forage_cc.index[10:37], pasture_forage_cc[10:37].acres.values, label = 'PASTURE FORAGE MISC CC', linestyle = '--', color = '#fdae6b')



    # hay_cc = df[df.crop == 'HAY forage']  # CC label  
    # y_array_cc = hay_cc[hay_cc.index > '1989'].acres
    # plt.plot(hay_cc.index[10:37], hay_cc[10:37].acres.values, label = 'Sudan CC', linestyle = '--', color = 'm')


    # crop_code = 22000  # forage hay PUR code  -very low 
    # y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    # plt.plot(x_array, y_array, label = 'Forage Hay and Silage PUR', color = 'c')

    # crop_code = 24000  # grain crops PUR code   # this code is not contained in post-1989 PUR dataset
    # y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    # pdb.set_trace()
    # plt.plot(x_array, y_array, label = 'GRAIN CROPS PUR', color = '#c994c7')

    crop_code = 28078  # grain PUR code  # very low 
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'GRAIN PUR', color = 'black')

    pdb.set_trace()
    crop_code = 29131  # SORGHUM/MILO PUR code  # very low 
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'SORGHUM/MILO PUR', color = '#8856a7')

# FORAGE HAY/SILAGE
    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    highest_acres2 = crop_types_in_county['2016'].sort_values(ascending = False).head(30)

    pdb.set_trace()

    # test = crop_types_in_county['1990']
    plt.xlabel('year')
    plt.ylabel('crop acreage')
    plt.legend()
    plt.title(str('Common Grass Crops in ' + str(county_name) + 'county'))
    plt.show()

    pdb.set_trace()


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
    x_array_oranges = pd.to_datetime(oranges_navel_cc_vals.index.values)

    oranges_valencia_cc_vals = orange_valencia_cc[orange_valencia_cc.index > '1989'].acres
    oranges_cc_total = oranges_navel_cc_vals.values + oranges_valencia_cc_vals.values


    plt.plot(x_array_oranges, oranges_cc_total, label = 'Oranges CC', linestyle = '--', color = 'g')
    plt.plot(x_array, y_array, label = 'Oranges PUR', color = 'g')
    pdb.set_trace()
    # almonds: 
    crop_code = 3001  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    silage_cc = df[df.crop == 'ALMONDS ALL']  # CC label  
    y_array_cc = silage_cc[silage_cc.index > '1989'].acres
    pdb.set_trace()
    x_array_cc_silage = pd.to_datetime(y_array_cc.index.values)
    plt.plot(x_array_cc_silage, y_array_cc, label = 'Almonds CC', linestyle = '--', color = 'r')
    plt.plot(x_array, y_array, label = 'Almonds PUR', color = 'r')

    # pistachios: 
    crop_code = 3011  # pistachio PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    pist_cc = df[df.crop == 'PISTACHIOS']  # CC label  
    y_array_cc = pist_cc[pist_cc.index > '1989'].acres
    x_array_cc_pist = pd.to_datetime(y_array_cc.index.values)
    plt.plot(x_array_cc_pist, y_array_cc, label = 'Pistachios CC', linestyle = '--', color = 'y')
    plt.plot(x_array, y_array, label = 'Pistachios PUR', color = 'y')


    # walnuts: 
    crop_code = 3009  # walnut PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()

    wheat_cc = df[df.crop == 'WALNUTS ENGLISH']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    x_array_cc_wheat = pd.to_datetime(y_array_cc.index.values)
    plt.plot(x_array_cc_wheat, y_array_cc, label = 'Walnuts CC', linestyle = '--', color = 'b')
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

    # pdb.set_trace()


def data_comparison_corn_silage_crops(irrigation_district, sum_cc_crop_types, crop_types_in_county):

    county_name = irrigation_district.split('_')[0]
    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df_all[df_all.county==county_name]

    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(20))
    highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)
    df.index = pd.to_datetime(df.index)
    
    x_array = pd.to_datetime(crop_types_in_county.columns.values)
    
    # make a graph of the most common commodities 


    crop_code = 22005  # CORN (FORAGE - FODDER)
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'CORN (FORAGE - FODDER) PUR', color = 'g')

    crop_code = 29119  # CORN, HUMAN CONSUMPTION PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'Silage PUR', color = 'r')

    alfalfa_cc = df[df.crop == 'CORN SWEET ALL']  # CC label  
    y_array_cc = alfalfa_cc[alfalfa_cc.index > '1989'].acres
    plt.plot(y_array_cc, label = 'CORN SWEET ALL CC', linestyle = '--', color = 'g')

    silage_cc = df[df.crop == 'CORN CRAZY']  # CC label  
    y_array_cc = silage_cc[silage_cc.index > '1989'].acres
    plt.plot(y_array_cc, label = 'CORN CRAZY CC', linestyle = '--', color = 'r')


    wheat_cc = df[df.crop == 'CORN GRAIN']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'CORN GRAIN CC', linestyle = '--', color = 'y')


    wheat_cc = df[df.crop == 'CORN SEED']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'CORN SEED CC', linestyle = '--', color = 'black')


    wheat_cc = df[df.crop == 'CORN SILAGE']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'CORN SILAGE CC', linestyle = '--', color = 'm')
    pdb.set_trace()

    wheat_cc = df[df.crop == 'SORGHUM SILAGE']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'SORGHUM SILAGE CC', linestyle = '--', color = 'k')
    pdb.set_trace()

    wheat_cc = df[df.crop == 'SILAGE']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'SILAGE CC', linestyle = '--', color = 'c')
    pdb.set_trace()




    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    # highest_acres2 = crop_types_in_county['2016'].sort_values(ascending = False).head(10)

    # pdb.set_trace()
    # test = crop_types_in_county['1990']
    plt.xlabel('year')
    plt.ylabel('crop acreage')
    plt.legend()
    plt.title(str('Corn Crops in ' + str(county_name) + 'county'))
    plt.show()


def data_comparison_hays(irrigation_district, sum_cc_crop_types, crop_types_in_county): 
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
    plt.plot(x_array, y_array, label = 'Alfalfa PUR', color = 'g')

    alfalfa_cc = df[df.crop == 'HAY ALFALFA']  # CC label  
    y_array_cc = alfalfa_cc[alfalfa_cc.index > '1989'].acres
    plt.plot(y_array_cc, label = 'Alfalfa CC', linestyle = '--', color = 'g')

    

    # OAT (FORAGE - FODDER) 22006: 
    crop_code = 22006  # OAT (FORAGE - FODDER) PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'OAT (FORAGE - FODDER) PUR', color = '#fc9272')
    pdb.set_trace()

    hay_cc = df[df.crop == 'HAY OTHER UNSPECIFIED']  # CC label  
    y_array_cc = hay_cc[hay_cc.index > '1989'].acres
    plt.plot(y_array_cc, label = 'Silage CC', linestyle = '--', color = 'r')

    # WHEAT (FORAGE - FODDER): 
    crop_code = 22007  # alfalfa PUR code
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'Wheat PUR', color = 'y')

    wheat_cc = df[df.crop == 'WHEAT ALL']  # CC label  
    y_array_cc = wheat_cc[wheat_cc.index > '1989'].acres
    plt.plot(wheat_cc.index[10:37], wheat_cc[10:37].acres.values, label = 'Wheat CC', linestyle = '--', color = 'y')

    # pdb.set_trace()

    # # Sudan: 
    # crop_code = 22011  # sudangrass PUR code    - very low 
    # y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    # plt.plot(x_array, y_array, label = 'Sudangrass PUR', color = 'm')

    sudan_cc = df[df.crop == 'HAY SUDAN']  # CC label  
    y_array_cc = sudan_cc[sudan_cc.index > '1989'].acres
    plt.plot(sudan_cc.index[10:37], sudan_cc[10:37].acres.values, label = 'Sudan CC', linestyle = '--', color = 'm')

    oats_grain_cc = df[df.crop == 'OATS GRAIN']  # CC label  
    y_array_cc = oats_grain_cc[oats_grain_cc.index > '1989'].acres
    plt.plot(oats_grain_cc.index[10:37], oats_grain_cc[10:37].acres.values, label = 'OATS GRAIN CC', linestyle = '--', color = 'b')

    hay_grain_cc = df[df.crop == 'HAY GRAIN']  # CC label  
    y_array_cc = hay_grain_cc[hay_grain_cc.index > '1989'].acres
    plt.plot(hay_grain_cc.index[10:37], hay_grain_cc[10:37].acres.values, label = 'HAY GRAIN CC', linestyle = '--', color = '#99d8c9')


    pasture_forage_cc = df[df.crop == 'PASTURE FORAGE MISC.']  # CC label  
    y_array_cc = pasture_forage_cc[pasture_forage_cc.index > '1989'].acres
    plt.plot(pasture_forage_cc.index[10:37], pasture_forage_cc[10:37].acres.values, label = 'PASTURE FORAGE MISC CC', linestyle = '--', color = '#fdae6b')



    # hay_cc = df[df.crop == 'HAY forage']  # CC label  
    # y_array_cc = hay_cc[hay_cc.index > '1989'].acres
    # plt.plot(hay_cc.index[10:37], hay_cc[10:37].acres.values, label = 'Sudan CC', linestyle = '--', color = 'm')


    crop_code = 22008  # BARLEY (FORAGE - FODDER)
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'BARLEY (FORAGE - FODDER) PUR', color = 'c')

    # crop_code = 24000  # grain crops PUR code   # this code is not contained in post-1989 PUR dataset
    # y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    # pdb.set_trace()
    # plt.plot(x_array, y_array, label = 'GRAIN CROPS PUR', color = '#c994c7')

    crop_code = 28078  # grain PUR code  # very low 
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'GRAIN PUR', color = 'black')

    pdb.set_trace()
    crop_code = 29131  # SORGHUM/MILO PUR code  # very low 
    y_array = crop_types_in_county.loc[lambda df: crop_types_in_county.index == crop_code, : ].values.flatten()
    plt.plot(x_array, y_array, label = 'SORGHUM/MILO PUR', color = '#8856a7')

# FORAGE HAY/SILAGE
    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    highest_acres2 = crop_types_in_county['2016'].sort_values(ascending = False).head(30)

    pdb.set_trace()

    # test = crop_types_in_county['1990']
    plt.xlabel('year')
    plt.ylabel('crop acreage')
    plt.legend()
    plt.title(str('Common Grass Crops in ' + str(county_name) + 'county'))
    plt.show()

    pdb.set_trace()

def data_comparison_pasture_silage_crops(irrigation_district, sum_cc_crop_types, crop_types_in_county):
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

    sudan_cc = df[df.crop == 'PASTURE RANGE']  # CC label  
    y_array_cc = sudan_cc[sudan_cc.index > '1989'].acres
    plt.plot(sudan_cc.index[10:37], sudan_cc[10:37].acres.values, label = 'PASTURE RANGE CC', linestyle = '--', color = 'm')

    oats_grain_cc = df[df.crop == 'SILAGE']  # CC label  
    y_array_cc = oats_grain_cc[oats_grain_cc.index > '1989'].acres
    plt.plot(oats_grain_cc.index[10:37], oats_grain_cc[10:37].acres.values, label = 'SILAGE CC', linestyle = '--', color = 'b')

    hay_grain_cc = df[df.crop == 'CORN SILAGE']  # CC label  
    y_array_cc = hay_grain_cc[hay_grain_cc.index > '1989'].acres
    plt.plot(hay_grain_cc.index[10:37], hay_grain_cc[10:37].acres.values, label = 'CORN SILAGE CC', linestyle = '--', color = '#99d8c9')


    pasture_forage_cc = df[df.crop == 'PASTURE FORAGE MISC.']  # CC label  
    y_array_cc = pasture_forage_cc[pasture_forage_cc.index > '1989'].acres
    plt.plot(pasture_forage_cc.index[10:37], pasture_forage_cc[10:37].acres.values, label = 'PASTURE FORAGE MISC CC', linestyle = '--', color = '#fdae6b')

    plt.xlabel('year')
    plt.ylabel('crop acreage')
    plt.legend()
    plt.title(str('Excluded Crops in ' + str(county_name) + 'county'))
    plt.show()

    pdb.set_trace()




retrieve_data = 0
normalized = 1 

# county_list = [ 'Fresno_County', 'Tulare_County', 'Kings_County', 'Kern_County']
irrigation_district = 'Tulare_County'

if retrieve_data == 1: 
    if not os.path.isdir(str(irrigation_district)):  # creates this folder 
        os.mkdir(str(irrigation_district))
    sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district, totals_in_irrig_dist = retrieve_data_for_irrigation_district(irrigation_district, normalized)



# crop_types_in_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '_to_examine.csv')), index_col = 'crop_ID') 
crop_types_in_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '_mod_Oct24.csv')), index_col = 'crop_ID') 


sum_crop_types_each_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_data_normalized' + str(irrigation_district) + '.csv')))
sum_cc_crop_types = county_commissioner_data(irrigation_district) 


# data_comparison_by_field_crop(irrigation_district, sum_cc_crop_types, crop_types_in_county)

# data_comparison_hays(irrigation_district, sum_cc_crop_types, crop_types_in_county)
# plt.figure()
# data_comparison_by_orchard_crop(irrigation_district, sum_cc_crop_types, crop_types_in_county)


# data_comparison_corn_silage_crops(irrigation_district, sum_cc_crop_types, crop_types_in_county)

data_comparison_pasture_silage_crops(irrigation_district, sum_cc_crop_types, crop_types_in_county)

pdb.set_trace()




