## Order of Operations 
### Working as of October 2018

Part 1: Will be converted to a simple datascraper to do all this nonsense for you. Stay tuned. 
For now: Download data at ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/
1. Unzip each folder from 1974-2016 (e.g. pur1978.zip)
2. save each folder as pur_data_raw/pur<year>   ( e.g. pur_data_raw/pur1975) 

Part 2: Download .py files from crop_acreages_CA_DPR_reports and place in same folder (which should also contain the pur_data_raw folder)

Part 3: Clean the data -  Cleans up bad data and compiles data columns to create a comtrs value for each permit
1. Run the clean_calPIP_data.py script

Part 3: Compile and normalize the data by 1-mile section
1. Run the compile_normalize_data_by_comtrs.py script

Part 4: Create graphs comparing County Commissioner data with calPUR dataset
1. Run calPUR_county_comparison.py

Part 5, option a: Create several graphs for a chosen irrigation district or county within Tulare Lake Basin
1. Run acreage_calc_plots_single_irrigation_district.py 

Part 5, option b: Create a specific graph for all irrigation districts within the Tulare Lake Basin


