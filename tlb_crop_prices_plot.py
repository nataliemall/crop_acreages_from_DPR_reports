# tlb_crop_prices_plot.py
### Figure 4 #####


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
from matplotlib.patches import Patch
import os 
import pdb
import pandas as pd
from tqdm import tqdm  # for something in tqdm(something something):


from pur_and_county_data_retrieval import county_commissioner_data



def data_comparison_by_orchard_crop(sum_cc_crop_types, crop_types_in_county):

    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    

    irrigation_district_list = ['Tulare_County', 'Kern_County', 'Kings_County', 'Fresno_County']

    list_years = pd.date_range(start = '1/1/1980', end = '1/1/2017', freq = 'Y')
    oranges = pd.DataFrame(index = list_years, columns = ['year', 'acres_Tulare', 'acres_Kern', 'acres_Kings', 'acres_Fresno'])
    # pdb.set_trace()
    total_this_irrig = {}
    average_rev_this_irrig = {}
    for num, irrigation_district in enumerate(irrigation_district_list):
        county_name = irrigation_district.split('_')[0]
        column_name = str('acres_' + county_name )
        df = df_all[df_all.county==county_name]

        common_crop_list = str(['ORANGES NAVEL', 'ORANGES VALENCIA', 'ALMONDS ALL', 'PISTACHIOS', 'GRAPES TABLE', 'GRAPES WINE'])
        # df_common_crops = df[df.crop in common_crop_list  ]
        # pdb.set_trace()
        # oranges: 
        oranges_navel_cc = df[df.crop == 'ORANGES NAVEL']  # CC label  
        oranges_rev_per_acre = oranges_navel_cc['yield'] * oranges_navel_cc['ppu']
        df_oranges_nav_rev = pd.DataFrame(oranges_rev_per_acre)

        # pdb.set_trace()
        df_oranges = pd.DataFrame(oranges_navel_cc, columns = {"acres"})


        orange_valencia_cc = df[df.crop == 'ORANGES VALENCIA']  # CC label ORANGES VALENCIA
        df_oranges2 = pd.DataFrame(orange_valencia_cc, columns = {"acres"})
        oranges_val_rev_per_acre = orange_valencia_cc['yield'] * orange_valencia_cc['ppu']
        df_oranges_val_rev = pd.DataFrame(oranges_val_rev_per_acre)


        oranges_navel_cc_vals = oranges_navel_cc.acres
        oranges_valencia_cc_vals = orange_valencia_cc.acres


        almonds_cc = df[df.crop == 'ALMONDS ALL']  # CC label  
        df_almonds = pd.DataFrame(almonds_cc, columns = {"acres"})
        almonds_val_rev_per_acre = almonds_cc['yield'] * almonds_cc['ppu']
        df_almonds_rev = pd.DataFrame(almonds_val_rev_per_acre)


        y_array_almonds = almonds_cc.acres


        pist_cc = df[df.crop == 'PISTACHIOS']  # CC label  
        df_pist = pd.DataFrame(pist_cc, columns = {"acres"})
        pist_rev_per_acre = pist_cc['yield'] * pist_cc['ppu']
        df_pist_rev = pd.DataFrame(pist_rev_per_acre)

        y_array_pist = pist_cc.acres

        grapes_table_cc = df[df.crop == 'GRAPES TABLE']  # CC label  
        df_grapes_table = pd.DataFrame(grapes_table_cc, columns = {"acres"})
        grapes_table_rev_per_acre = grapes_table_cc['yield'] * grapes_table_cc['ppu']
        df_grapes_table_rev = pd.DataFrame(grapes_table_rev_per_acre)


        y_array_grapes_table = grapes_table_cc.acres

        grapes_wine_cc = df[df.crop == 'GRAPES WINE']  # CC label  
        df_grapes_wine = pd.DataFrame(grapes_wine_cc, columns = {"acres"})
        grapes_wine_rev_per_acre = grapes_wine_cc['yield'] * grapes_wine_cc['ppu']
        df_grapes_wine_rev = pd.DataFrame(grapes_wine_rev_per_acre)


        y_array_grapes_wine = grapes_wine_cc.acres

        ### Create df for perennial acreage ###
        df_orange_orange = pd.merge(df_oranges, df_oranges2,  how = 'outer' , left_index = True, right_index = True)
        df_alm_pist = pd.merge(df_almonds, df_pist, how = 'outer' , left_index = True, right_index = True)
        df_grapes_grapes = pd.merge(df_grapes_table, df_grapes_wine,  how = 'outer' , left_index = True, right_index = True)

        df_orange_alm_pist = pd.merge(df_orange_orange, df_alm_pist ,  how = 'outer' , left_index = True, right_index = True)
        df_orange_alm_pist_grapes = pd.merge(df_orange_alm_pist, df_grapes_grapes ,  how = 'outer' , left_index = True, right_index = True)

        sum_all_perennials = df_orange_alm_pist_grapes.sum(axis = 1)


        ### create df for perennial prices ###
        # df_rev_orange_orange = pd.merge(df_oranges_val_rev, df_oranges_nav_rev,  how = 'outer' , left_index = True, right_index = True)
        df_rev_alm_pist = pd.merge(df_almonds_rev, df_pist_rev, how = 'outer' , left_index = True, right_index = True)
        df_rev_grapes_grapes = pd.merge(df_grapes_table_rev, df_grapes_wine_rev,  how = 'outer' , left_index = True, right_index = True)

        df_rev_orange_alm_pist = pd.merge(df_oranges_nav_rev, df_rev_alm_pist ,  how = 'outer' , left_index = True, right_index = True)
        df_rev_orange_alm_pist_grapes = pd.merge(df_rev_orange_alm_pist, df_rev_grapes_grapes ,  how = 'outer' , left_index = True, right_index = True)

        average_price_perennials = df_rev_orange_alm_pist_grapes.mean(axis = 1)



        # pdb.set_trace()
        # print('test perennial rev df')


        # df_test = pd.DataFrame(oranges_valencia_cc_vals) 
        # df_oranges_2 = pd.DataFrame(oranges_navel_cc_vals )
        # df_almonds = pd.DataFrame(y_array_almonds)
        # df_pist = pd.DataFrame(y_array_pist)
        # df_grapes_table = pd.DataFrame(y_array_grapes_table )
        # df_grapes_wine = pd.DataFrame( y_array_grapes_wine)

        # oranges_navel_cc = 

        # if orange_valencia_cc.empty:
        #     test3 = almonds_cc.acres + pist_cc.acres + grapes_table_cc.acres + grapes_wine_cc.acres
        # else:
        #     test3 = oranges_navel_cc.acres + orange_valencia_cc.acres + almonds_cc.acres + pist_cc.acres + grapes_table_cc.acres + grapes_wine_cc.acres
        

        total_this_irrig[num] = sum_all_perennials 
        average_rev_this_irrig[num] = average_price_perennials

    tulare = total_this_irrig[0]
    df_tulare = pd.DataFrame(tulare)
    df_tulare= df_tulare.rename(columns= {"acres":"acres_tulare"})

    kern = total_this_irrig[1]
    df_kern = pd.DataFrame(kern)
    df_kern = df_kern.rename(columns= {"acres":"acres_kern"})

    kings = total_this_irrig[2]
    df_kings = pd.DataFrame(kings)
    df_kings = df_kings.rename(columns= {"acres":"acres_kings"})

    fresno = total_this_irrig[3]
    df_fresno = pd.DataFrame(fresno)
    df_fresno = df_fresno.rename(columns= {"acres":"acres_fresno"})




    tulare_rev = average_rev_this_irrig[0]
    df_tulare_rev = pd.DataFrame(tulare_rev)
    # df_tulare= df_tulare.rename(columns= {"acres":"acres_tulare"})

    kern_rev = average_rev_this_irrig[1]
    df_kern_rev = pd.DataFrame(kern_rev)
    # df_kern = df_kern.rename(columns= {"acres":"acres_kern"})

    kings_rev = average_rev_this_irrig[2]
    df_kings_rev = pd.DataFrame(kings_rev)
    # df_kings = df_kings.rename(columns= {"acres":"acres_kings"})

    fresno_rev = average_rev_this_irrig[3]
    df_fresno_rev = pd.DataFrame(fresno_rev)
    # df_fresno = df_fresno.rename(columns= {"acres":"acres_fresno"})






    # pdb.set_trace()

    fresno_kings = pd.merge(df_kings, df_fresno, left_index = True, right_index = True)
    kern_tulare = pd.merge(df_kern, df_tulare, left_index = True, right_index = True)
    perennials_by_county = pd.merge(fresno_kings, kern_tulare, left_index = True, right_index = True)
    print('merge totals for each county here')

    perennials_tlb = np.sum(perennials_by_county, axis = 1)




    fresno_kings_rev = pd.merge(df_kings_rev, df_fresno_rev, left_index = True, right_index = True)
    kern_tulare_rev = pd.merge(df_kern_rev, df_tulare_rev, left_index = True, right_index = True)
    perennial_rev_by_county = pd.merge(fresno_kings_rev, kern_tulare_rev, left_index = True, right_index = True)
    print('merge totals for each county here')

    perennial_rev_tlb = np.mean(perennial_rev_by_county, axis = 1)
    # pdb.set_trace()
    # print('check out here')

        
    x_array_oranges = pd.to_datetime(oranges_navel_cc_vals.index.values)
    oranges_cc_total = oranges_navel_cc_vals.values + oranges_valencia_cc_vals.values
    # pdb.set_trace()
    # oranges[str(column_name)] =  oranges_cc_total 
    # pdb.set_trace() 

    # crops of greatest acreage
    # print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(30))
    # print(df[df.index=='1990'].sort_values(by='acres', ascending=False).head(30))

    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(20)
    # pdb.set_trace()


    # make a graph of the most common commodities 


    # almonds: 

    almonds_cc = df[df.crop == 'ALMONDS ALL']  # CC label  
    y_array_almonds = almonds_cc.acres
    x_array_cc_almonds = pd.to_datetime(y_array_almonds.index.values)

    pist_cc = df[df.crop == 'PISTACHIOS']  # CC label  
    y_array_pist = pist_cc.acres
    x_array_cc_pist = pd.to_datetime(pist_cc.index.values)

    grapes_table_cc = df[df.crop == 'GRAPES TABLE']  # CC label  
    y_array_grapes_table = grapes_table_cc.acres
    x_array_cc_grapes_table = pd.to_datetime(y_array_grapes_table.index.values)


    grapes_wine_cc = df[df.crop == 'GRAPES WINE']  # CC label  
    y_array_grapes_wine = grapes_wine_cc.acres
    x_array_cc_grapes_wine = pd.to_datetime(grapes_wine_cc.index.values)


    return x_array_cc_grapes_wine, y_array_grapes_wine, x_array_cc_grapes_table, y_array_grapes_table, x_array_cc_pist, y_array_pist, x_array_cc_almonds, y_array_almonds, x_array_oranges, oranges_cc_total, county_name, perennials_tlb, perennial_rev_tlb


def data_comparison_by_field_crop(sum_cc_crop_types, crop_types_in_county):

    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    

    irrigation_district_list = ['Tulare_County', 'Kern_County', 'Kings_County', 'Fresno_County']

    list_years = pd.date_range(start = '1/1/1980', end = '1/1/2017', freq = 'Y')
    oranges = pd.DataFrame(index = list_years, columns = ['year', 'acres_Tulare', 'acres_Kern', 'acres_Kings', 'acres_Fresno'])
    
    # print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10))
    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    # pdb.set_trace()
    total_this_irrig = {}
    average_rev_annuals_this_irrig = {}
    for num, irrigation_district in enumerate(irrigation_district_list):
        county_name = irrigation_district.split('_')[0]
        column_name = str('acres_' + county_name )
        df = df_all[df_all.county==county_name]
        print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10))
        highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(20)
        # pdb.set_trace()

        silage_cc = df[df.crop == 'SILAGE']  # CC label  
        df_silage = pd.DataFrame(silage_cc, columns = {"acres"})
        df_silage = df_silage.rename(columns= {"acres":"acres_silage"})
        silage_rev_per_acre = silage_cc['yield'] * silage_cc['ppu']
        df_silage_rev = pd.DataFrame(silage_rev_per_acre)

        # silage_corn = df[df.crop == 'CORN SILAGE']  # CC label  
        # df_silage2 = pd.DataFrame(silage_corn, columns = {"acres"})
        # df_silage2 = df_silage2.rename(columns= {"acres":"acres_silage"})


        alfalfa_cc = df[df.crop == 'HAY ALFALFA']  # CC label  
        df_alfalfa = pd.DataFrame(alfalfa_cc, columns = {"acres"})
        df_alfalfa= df_alfalfa.rename(columns= {"acres":"acres_alfalfa"})
        alfalfa_rev_per_acre = alfalfa_cc['yield'] * alfalfa_cc['ppu']
        df_alfalfa_rev = pd.DataFrame(alfalfa_rev_per_acre)
        # y_array_almonds = almonds_cc.acres

        cotton_cc = df[df.crop == 'COTTON LINT PIMA']  # CC label  
        df_cotton = pd.DataFrame(cotton_cc, columns = {"acres"})
        df_cotton= df_cotton.rename(columns= {"acres":"acres_cotton1"})
        cotton_rev_per_acre = cotton_cc['yield'] * cotton_cc['ppu']
        df_cotton_rev = pd.DataFrame(cotton_rev_per_acre)

        cotton_cc2 = df[df.crop == 'COTTON LINT UNSPECIFIED']
        df_cotton2 = pd.DataFrame(cotton_cc2, columns = {"acres"})
        df_cotton2= df_cotton2.rename(columns= {"acres":"acres_cotton2"})
        cotton2_rev_per_acre = cotton_cc2['yield'] * cotton_cc2['ppu']
        df_cotton2_rev = pd.DataFrame(cotton2_rev_per_acre)


        # cotton1 = pd.DataFrame(cotton_cc, columns = {'acres'})
        # cotton2 = pd.DataFrame(cotton_cc2, columns = {'acres'})
        # cotton2_renames = cotton2.rename(columns = {"acres": "acres_cotton2"})
        # cotton_all = pd.merge(cotton1, cotton2_renames, left_on, right_index = True)
        # y_array_pist = pist_cc.acres

        wheat_cc = df[df.crop == 'WHEAT ALL']  # CC label  
        df_wheat = pd.DataFrame(wheat_cc, columns = {"acres"})
        df_wheat= df_wheat.rename(columns= {"acres":"acres_wheat"})
        wheat_rev_per_acre = wheat_cc['yield'] * wheat_cc['ppu']
        df_wheat_rev = pd.DataFrame(wheat_rev_per_acre)
        # y_array_grapes_table = grapes_table_cc.acres

        tomatoes_cc = df[df.crop == 'TOMATOES PROCESSING']  # CC label  
        df_tomatoes = pd.DataFrame(tomatoes_cc, columns = {"acres"})
        df_tomatoes= df_tomatoes.rename(columns= {"acres":"acres_tomatoes"})
        tomato_rev_per_acre = tomatoes_cc['yield'] * tomatoes_cc['ppu']
        df_tomatoe_rev = pd.DataFrame(tomato_rev_per_acre)
        # y_array_grapes_wine = grapes_wine_cc.acres

        # df_test = pd.DataFrame(oranges_valencia_cc_vals) 
        # df_oranges_2 = pd.DataFrame(oranges_navel_cc_vals )
        # df_almonds = pd.DataFrame(y_array_almonds)
        # df_pist = pd.DataFrame(y_array_pist)
        # df_grapes_table = pd.DataFrame(y_array_grapes_table )
        # df_grapes_wine = pd.DataFrame( y_array_grapes_wine)

        # df_wheat = pd.DataFrame(wheat_cc)

        # if orange_valencia_cc.empty:
        #     test3 = almonds_cc.acres + pist_cc.acres + grapes_table_cc.acres + grapes_wine_cc.acres
        # else:
        # test3 = np.sum(silage_cc.acres + alfalfa_cc.acres + cotton_cc2.acres + wheat_cc.acres + tomatoes_cc.acres, axis = 0)
        df_wheat_tom = pd.merge(df_wheat, df_tomatoes,  how = 'outer' , left_index = True, right_index = True)
        df_cotton_cotton = pd.merge(df_cotton2, df_cotton, how = 'outer' , left_index = True, right_index = True)
        # df_silage_silage = pd.merge(df_silage, df_silage2, how = 'outer' , left_index = True, right_index = True )
        df_silage_alfalfa = pd.merge(df_alfalfa, df_silage,  how = 'outer' , left_index = True, right_index = True)

        df_sil_alf_cotton = pd.merge(df_cotton_cotton, df_silage_alfalfa ,  how = 'outer' , left_index = True, right_index = True)
        df_sil_alf_cotton_wheat_tom = pd.merge(df_sil_alf_cotton, df_wheat_tom ,  how = 'outer' , left_index = True, right_index = True)


        sum_all_annuals = df_sil_alf_cotton_wheat_tom.sum(axis = 1)
        total_this_irrig[num] = sum_all_annuals 

        df_rev_wheat_tom = pd.merge(df_wheat_rev, df_tomatoe_rev,  how = 'outer' , left_index = True, right_index = True)
        df_rev_cotton_cotton = pd.merge(df_cotton2_rev, df_cotton_rev, how = 'outer' , left_index = True, right_index = True)
        # df_silage_silage = pd.merge(df_silage, df_silage2, how = 'outer' , left_index = True, right_index = True )
        df_rev_silage_alfalfa = pd.merge(df_alfalfa_rev, df_silage_rev,  how = 'outer' , left_index = True, right_index = True)

        df_rev_sil_alf_cotton = pd.merge(df_rev_cotton_cotton, df_rev_silage_alfalfa ,  how = 'outer' , left_index = True, right_index = True)
        df_rev_sil_alf_cotton_wheat_tom = pd.merge(df_rev_sil_alf_cotton, df_rev_wheat_tom ,  how = 'outer' , left_index = True, right_index = True)

        # pdb.set_trace()
        average_revenues_annual = df_rev_sil_alf_cotton_wheat_tom.mean(axis = 1)
        average_rev_annuals_this_irrig[num] = average_revenues_annual

        # ave_2016 = (1658.9244      +  1208.900 +  468.4108  + 549.3400  ) / 4



    # pdb.set_trace()
    tulare = total_this_irrig[0]
    df_tulare = pd.DataFrame(tulare)
    df_tulare= df_tulare.rename(columns= {"acres":"acres_tulare"})

    kern = total_this_irrig[1]
    df_kern = pd.DataFrame(kern)
    df_kern = df_kern.rename(columns= {"acres":"acres_kern"})

    kings = total_this_irrig[2]
    df_kings = pd.DataFrame(kings)
    df_kings = df_kings.rename(columns= {"acres":"acres_kings"})

    fresno = total_this_irrig[3]
    df_fresno = pd.DataFrame(fresno)
    df_fresno = df_fresno.rename(columns= {"acres":"acres_fresno"})
    # pdb.set_trace()

    fresno_kings = pd.merge(df_kings, df_fresno, left_index = True, right_index = True)
    kern_tulare = pd.merge(df_kern, df_tulare, left_index = True, right_index = True)

    annuals_by_county = pd.merge(fresno_kings, kern_tulare, left_index = True, right_index = True)
    annuals_tlb = np.sum(annuals_by_county, axis = 1)




    tulare_rev = average_rev_annuals_this_irrig[0]
    df_tulare_rev = pd.DataFrame(tulare_rev)
    # df_tulare= df_tulare.rename(columns= {"acres":"acres_tulare"})

    kern_rev = average_rev_annuals_this_irrig[1]
    df_kern_rev = pd.DataFrame(kern_rev)
    # df_kern = df_kern.rename(columns= {"acres":"acres_kern"})

    kings_rev = average_rev_annuals_this_irrig[2]
    df_kings_rev = pd.DataFrame(kings_rev)
    # df_kings = df_kings.rename(columns= {"acres":"acres_kings"})

    fresno_rev = average_rev_annuals_this_irrig[3]
    df_fresno_rev = pd.DataFrame(fresno_rev)
    # df_fresno = df_fresno.rename(columns= {"acres":"acres_fresno"})


    # annual_rev_tlb
    fresno_kings_rev = pd.merge(df_kings_rev, df_fresno_rev, left_index = True, right_index = True)
    kern_tulare_rev = pd.merge(df_kern_rev, df_tulare_rev, left_index = True, right_index = True)
    annual_rev_by_county = pd.merge(fresno_kings_rev, kern_tulare_rev, left_index = True, right_index = True)
    print('merge totals for each county here')

    annual_rev_tlb = np.mean(annual_rev_by_county, axis = 1)
        
    # x_array_oranges = pd.to_datetime(oranges_navel_cc_vals.index.values)
    # oranges_cc_total = oranges_navel_cc_vals.values + oranges_valencia_cc_vals.values
    # pdb.set_trace()
    # oranges[str(column_name)] =  oranges_cc_total 
    # pdb.set_trace() 

    # crops of greatest acreage
    # print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(30))
    # print(df[df.index=='1990'].sort_values(by='acres', ascending=False).head(30))

    # highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(20)
    # pdb.set_trace()


    # make a graph of the most common commodities 


    # pdb.set_trace()
    # print('test out dataframe here')
    # # almonds: 

    # almonds_cc = df[df.crop == 'ALMONDS ALL']  # CC label  
    # y_array_almonds = almonds_cc.acres
    # x_array_cc_almonds = pd.to_datetime(y_array_almonds.index.values)

    # pist_cc = df[df.crop == 'PISTACHIOS']  # CC label  
    # y_array_pist = pist_cc.acres
    # x_array_cc_pist = pd.to_datetime(pist_cc.index.values)

    # grapes_table_cc = df[df.crop == 'GRAPES TABLE']  # CC label  
    # y_array_grapes_table = grapes_table_cc.acres
    # x_array_cc_grapes_table = pd.to_datetime(y_array_grapes_table.index.values)


    # grapes_wine_cc = df[df.crop == 'GRAPES WINE']  # CC label  
    # y_array_grapes_wine = grapes_wine_cc.acres
    # x_array_cc_grapes_wine = pd.to_datetime(grapes_wine_cc.index.values)


    return x_array_cc_grapes_wine, y_array_grapes_wine, x_array_cc_grapes_table, y_array_grapes_table, x_array_cc_pist, y_array_pist, x_array_cc_almonds, y_array_almonds, x_array_oranges, oranges_cc_total, county_name, annuals_tlb, annual_rev_tlb




def plot_crop_acreages(x_array_cc_grapes_wine, y_array_grapes_wine,
        x_array_cc_grapes_table, y_array_grapes_table,
        x_array_cc_pist, y_array_pist,
        x_array_cc_almonds, y_array_almonds,
        x_array_oranges, oranges_cc_total, county_name):




    plt.plot(x_array_cc_grapes_wine, y_array_grapes_wine, label = 'grapes wine CC', linestyle = '--', color = 'k')
    plt.plot(x_array_cc_grapes_table, y_array_grapes_table, label = 'grapes table CC', linestyle = '--', color = 'b')
    plt.plot(x_array_cc_pist, y_array_pist, label = 'Pistachios CC', linestyle = '--', color = 'y')
    plt.plot(x_array_cc_almonds, y_array_almonds, label = 'Almonds CC', linestyle = '--', color = 'r')
    plt.plot(x_array_oranges, oranges_cc_total, label = 'Oranges CC', linestyle = '--', color = 'g')

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



def plot_totals(perennials_tlb, perennial_rev_tlb, annuals_tlb, annual_rev_tlb):

    # pdb.set_trace()
    x_array = pd.to_datetime(perennials_tlb.index.values)

    # fig, ax1 = plt.subplots()
    fig, ax = plt.subplots(3,2, sharex = True)
    # x_array = x_array[x_array> '1983']
    # test = perennials_tlb[perennials_tlb.index > 1983]
    # test = perennials_tlb.values[4:10]
    # pdb.set_trace()
    ax[0,0].plot(x_array, perennials_tlb.values / 1000000, label = 'perennials', color = 'g')
    ax[0,0].plot(x_array, annuals_tlb.values / 1000000, label = 'annuals', color = 'y')
    ax[0,0].legend()
    ax[0,0].set_ylabel('Crop acreage in basin (millions)')
    ax[0,0].set_title('Histrical Crop Acreage and Prices in Tulare Lake Basin')
    ax[0,0].set_ylim(0)
    ax[0,0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

    # ax2 = ax1.twinx()
    ax[1,0].plot(x_array, perennial_rev_tlb.values, label = 'Nominal revenue perennials', color = 'g')
    ax[1,0].plot(x_array, annual_rev_tlb.values, label = 'Nominal revenue annuals', color = 'y')
    ax[1,0].set_ylabel('Revenue per acre (dollars)')
    ax[1,0].set_ylim(0, 10000)
    ax[1,0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    # ax[1,0].legend()

    test = pd.read_csv('cpi_multipliers.csv')
    df_cpi = pd.DataFrame(test, columns = {"year", "cpi"})
    df_cpi = df_cpi.set_index( "year")
    # pdb.set_trace()

    # test = pd.merge(df_cpi,perennials_tlb , left_index = True, right_index = True)

    adjusted_perennial_vals = perennial_rev_tlb.values * 240  /  df_cpi[ df_cpi.index > '1979'].cpi   # convert to 2016 dollars
    adjusted_annual_vals = annual_rev_tlb.values * 240  /  df_cpi[ df_cpi.index > '1979'].cpi 

    # pdb.set_trace()
    ax[2,0].plot(x_array, adjusted_perennial_vals.values, label = 'adjusted revenue perennials', color = 'g')
    ax[2,0].plot(x_array, adjusted_annual_vals.values, label = 'adjusted revenue annuals', color = 'y')
    ax[2,0].set_ylabel('Inflation-adjusted revenue \n per acre (2016 dollars)') 
    ax[2,0].set_ylim(0)
    ax[2,0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.show()

def plot_cc_overall_data_function(irrigation_district):

    county_list = [ 'Fresno_County', 'Tulare_County', 'Kings_County', 'Kern_County']
    sum_cc_crop_types = {}  # Creates dictionary for CC data
    for num, irrigation_district in enumerate(county_list) : 
        sum_cc_crop_types[irrigation_district] = county_commissioner_data(irrigation_district)

    county_tree_total = sum_cc_crop_types['Fresno_County'].all_tree_crops + sum_cc_crop_types['Tulare_County'].all_tree_crops \
        + sum_cc_crop_types['Kings_County'].all_tree_crops + sum_cc_crop_types['Kern_County'].all_tree_crops

    county_annual_crops_total = sum_cc_crop_types['Fresno_County'].all_annual_crops + sum_cc_crop_types['Tulare_County'].all_annual_crops \
        + sum_cc_crop_types['Kings_County'].all_annual_crops + sum_cc_crop_types['Kern_County'].all_annual_crops

    year_array = np.int64(sum_cc_crop_types['Fresno_County'].year).flatten()

    fig, ax = plt.subplots(2,2, sharex = True)

    ax[0,0].plot(year_array, (county_tree_total.values / 1000000), color = 'g' , label = 'Perennial crops' )
    ax[0,0].plot(year_array, (county_annual_crops_total.values / 1000000) , color = 'y', label = 'Annual crops')

    ax[0,0].legend()

    ax[0,0].set_title('Crop Acreage in Tulare Lake Basin')
    ax[0,0].set_xlabel('Year', fontsize = 14)
    ax[0,0].set_ylabel('Total area of crops grown \n (millions of acres)' )
    ax[0,0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

    test = pd.read_csv('cpi_multipliers.csv')
    df_cpi = pd.DataFrame(test, columns = {"year", "cpi"})
    df_cpi = df_cpi.set_index( "year")

    adjusted_perennial_vals = perennial_rev_tlb.values * 240  /  df_cpi[ df_cpi.index > '1979'].cpi   # convert to 2016 dollars
    adjusted_annual_vals = annual_rev_tlb.values * 240  /  df_cpi[ df_cpi.index > '1979'].cpi 

    # pdb.set_trace()
    ax[1,0].plot(year_array, adjusted_perennial_vals.values, label = 'adjusted revenue perennials', color = 'g')
    ax[1,0].plot(year_array, adjusted_annual_vals.values, label = 'adjusted revenue annuals', color = 'y')
    ax[1,0].set_ylabel('Inflation-adjusted revenue \n per acre (2016 dollars)') 
    ax[1,0].set_ylim(0)
    ax[1,0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)


        # pdb.set_trace()
    add_droughts = 1
    if add_droughts == 1 :

        year_list_array = np.arange(1980, 2017)
        logic_rule = ( (year_list_array > 2011) & (year_list_array < 2017)) # or (year_list_array > 1991 & year_list_array < 1995))  
        collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule), facecolor='orange', alpha=0.3)
        collection1 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule), facecolor='orange', alpha=0.3)
        ax[0, 0].add_collection(collection)
        ax[1, 0].add_collection(collection1)

        logic_rule2 =  ( (year_list_array < 1993) & (year_list_array > 1986)  )   
        collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule2), facecolor='orange', alpha=0.3)
        collection3 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule2), facecolor='orange', alpha=0.3)
        
        ax[0, 0].add_collection(collection2)
        ax[1, 0].add_collection(collection3)

        legend_elements = [Patch(facecolor = 'orange', alpha=0.3, label = 'drought year')]
        ax[1,0].legend(handles = legend_elements, loc= 'lower right')  # custom legend 



    plt.show()


    if not os.path.isdir('figure_drafts'):
        os.mkdir('figure_drafts')
    plt.savefig('figure_drafts/cc_crop_acreage_change_tlb2', dpi = 300)
    pdb.set_trace()





plot_indivual_acreages = 0
plot_cc_overall_data = 1 


irrigation_district = 'Tulare_County'
# irrigation_district = 'Kern_County'
# irrigation_district = 'Kings_County'
# irrigation_district = 'Fresno_County'
sum_cc_crop_types = county_commissioner_data(irrigation_district) 
# crop_types_in_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '_mod_Oct24.csv')), index_col = 'crop_ID') 
crop_types_in_county = pd.read_csv(os.path.join(irrigation_district, str('calPUR_by_crop_type_' + str(irrigation_district) + '.csv')), index_col = 'crop_ID') 

x_array_cc_grapes_wine, y_array_grapes_wine, x_array_cc_grapes_table, y_array_grapes_table, x_array_cc_pist, y_array_pist, x_array_cc_almonds, y_array_almonds, x_array_oranges, oranges_cc_total, county_name, perennials_tlb, perennial_rev_tlb = data_comparison_by_orchard_crop(sum_cc_crop_types, crop_types_in_county)

x_array_cc_grapes_wine, y_array_grapes_wine, x_array_cc_grapes_table, y_array_grapes_table, x_array_cc_pist, y_array_pist, x_array_cc_almonds, y_array_almonds, x_array_oranges, oranges_cc_total, county_name, annuals_tlb, annual_rev_tlb = data_comparison_by_field_crop(sum_cc_crop_types, crop_types_in_county)


if plot_indivual_acreages == 1: 
    plot_totals(perennials_tlb, perennial_rev_tlb, annuals_tlb, annual_rev_tlb)
    pdb.set_trace()
    plot_crop_acreages(x_array_cc_grapes_wine, y_array_grapes_wine,
            x_array_cc_grapes_table, y_array_grapes_table,
            x_array_cc_pist, y_array_pist,
            x_array_cc_almonds, y_array_almonds,
            x_array_oranges, oranges_cc_total, county_name)


if plot_cc_overall_data == 1: 
    plot_cc_overall_data_function(irrigation_district)








