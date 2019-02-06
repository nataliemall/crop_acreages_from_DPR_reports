## This repository takes data from the California Pesticide Use Reporting system and calculates crop acreage to at the 1-square-mile resolution.  This data is then aggregated to larger regions, either county or irrigation district. 

![test](https://github.com/nataliemall/crop_acreages_from_DPR_reports/blob/master/readme_schematic.png?raw=true")



## Order of Operations 
### Downloading, processing, and plotting the California pesticide data to understand historical crop acreage 

Part 1: Will be converted to a simple datascraper to do all this nonsense for you. Stay tuned. 
For now: Download data at ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/
1. Unzip each folder from 1974-2016 (e.g. pur1978.zip)
2. save each folder as pur_data_raw/pur<year>   ( e.g.```pur_data_raw/pur1975```) 

Part 2: Download .py files from crop_acreages_CA_DPR_reports and place in same folder (which should also contain the pur_data_raw folder)

Part 3: Clean the data -  Cleans up bad data and compiles data columns to create a comtrs value for each permit

```clean_calPIP_data.py ```

Part 4: Compile and normalize the data by 1-mile section

``` compile_normalize_data_by_comtrs.py```

Part 5: Create graphs comparing County Commissioner data with calPUR dataset

```calPUR_county_comparison.py```

Part 6, option a: Create several graphs for a chosen irrigation district or county within Tulare Lake Basin

``` acreage_calc_plots_single_irrigation_district.py ```

Part 6, option b: Create a specific graph for all irrigation districts within the Tulare Lake Basin


