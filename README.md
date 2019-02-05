## Special user-friendly version for the wonderful lab group 

### We'll skip the messy part of processing the raw data, and instead download the handy compressed file of nice clean data (originally from the Pesticide Information Portal). 

Step 1: Download and unzip the file into the folder dedicated to all things dedicated to the February 13th Code Review 

```pur_data_with_comtrs.zip```

 This was sent to you via email since it's a large file. 

 Step 2: Download the rest of the moving parts: 

```adding_comtrs_functions.py```

```fix_pur_data_step1.py```

```clean_calPIP_data.py```

```compile_normalize_data_by_comtrs.py```

```calPUR_county_comparison.py```

```pur_and_county_data_retrieval.py```

```plotting_functions.py```

```acreage_calc_plots_single_irrigation_district.py```

Step 3: Run the part of the code this is all about. 

``` compile_normalize_data_by_comtrs.py```

Step 4: Graph it!

``` acreage_calc_plots_single_irrigation_district.py ```






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


