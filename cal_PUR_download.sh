#! /bin/bash

## Shell script to download zip files 

# wget -r "ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/"

# wget -r ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/

# for i in 1 2 3 4 5
# do
#   echo "Looping ... number $i"
# done


echo $year 

wget -r ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/pur1975.zip # download file
mv "transfer.cdpr.ca.gov" pur_data_raw_test # move download to pur_data_raw_test
mkdir pur_data_raw_test/pur1975  # make directory for year files 
unzip pur_data_raw_test/transfer.cdpr.ca.gov/pub/outgoing/pur_archives/pur1975.zip -d pur_data_raw_test/pur1975 #unzip these files into the new directiory 






# mv pur75.txt pur_data_raw_test/pur1975  # place these unzipped files into the yearly folder 
# mv pre_1990_sites.xls pur_data_raw_test/pur1975
# mv "Data Dictionary 1974-1989.doc" pur_data_raw_test/pur1975
# pur_data_raw_test/pur1975

# mv transfer.cdpr.ca.gov/pub/outgoing/pur_archives/pur75.txt pur_data_raw_test/pur1975


# cd pur_data_raw_test/transfer.cdpr.ca.gov/pub/outgoing/pur_archives 

