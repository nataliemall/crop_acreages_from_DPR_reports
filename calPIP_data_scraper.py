## Data scraper from: ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/
# if exception: print('Download data manually from ''ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/''  and place files in pur_data_raw folder' )

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
import re 
from tqdm import tqdm  # for something in tqdm(something something):

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import urllib 
import zipfile
import filetype



# specify the URL

web_page_with_zip_files = 'ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/'
# web_page_with_zip_files = 'transfer.cdpr.ca.gov/pub/outgoing/pur_archives/'

# query the website and return the html to the variable ‘page’
# pdb.set_trace()
page = urlopen(web_page_with_zip_files)

# parse the html using beautiful soup and store in variable `soup`
# soup = BeautifulSoup(page, ‘html.parser’)

soup = BeautifulSoup(page, 'html.parser')

name = soup.find('pur1974') 

# pdb.set_trace()

# zipurl = name['']
# href="/pub/outgoing/pur_archives/pur1974.zip"


archive = urllib.request.URLopener()
archive.retrieve("ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/", "pur1974.zip")


path_to_zip_file = '/Users/nataliemall/Box Sync/herman_research_box/crop_acreages_CA_DPR_reports/pur1974.zip'
outFile = zipfile.ZipFile(path_to_zip_file, 'wb')


pdb.set_trace()
# zip -s 0 pur1974.zip --out unsplit-pur1974.zip


pdb.set_trace()
os.rename("pur1974.zip", "pur_data_raw_test/pur1974.zip")

pdb.set_trace()
# pdb.set_trace()
# path_to_zip_file = '/Users/nataliemall/Box Sync/herman_research_box/crop_acreages_CA_DPR_reports/pur1974.zip'
# zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
# zip_ref.extractall(pur_data_raw_test)
# zip_ref.close()

zipfile.is_zipfile('pur1974.zip')
pdb.set_trace()

kind = filetype.guess('pur1974.zip')
if kind is None:
    print('Cannot guess file type!')

pdb.set_trace()
print('File extension: %s' % kind.extension)
print('File MIME type: %s' % kind.mime)



pdb.set_trace()

def fixBadZipfile(zipFile):  
 f = open(zipFile, 'r+b')  
 data = f.read()  
 pos = data.find('\x50\x4b\x05\x06') # End of central directory signature  
 if (pos > 0):  
     self._log("Trancating file at location " + str(pos + 22)+ ".")  
     f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
     f.truncate()  
     f.close()  
 else:  
 	print('expection')
     # raise error, file is truncated  

fixBadZipfile('pur1974.zip')

pdb.set_trace()

with zipfile.ZipFile("pur1974.zip","r") as zip_ref:
    zip_ref.extractall("pur_data_raw_test")

pdb.set_trace()

# down vote
# Here's what I got to work in Python 3:

# import zipfile, urllib.request, shutil

# url = web_page_with_zip_files
# file_name = 'pur1974.zip'

# with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
#     shutil.copyfileobj(response, out_file)
#     with zipfile.ZipFile(file_name) as zf:
#         zf.extractall()

# pdb.set_trace()




# for link in soup.findAll('a', href = True):
#     pdb.set_trace()
#     href = link['href']

#     pdb.set_trace()
#     if any(href.endswith(x) for x in ['.zip']):


#         print("Downloading '{}'".format(href))

#         remote_file = requests.get(web_page_with_zip_files + href)

#         pdb.set_trace()
#         print('test_here')

# pdb.set_trace()

# point to output directory
# outpath ='/Users/nataliemall/Box Sync/herman_research_box/pur_scraped_data'
# url = 'ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/'
# mbyte=1024*1024

# print(f'Reading: ', {url})
# html = requests.get(url).text
# soup = BeautifulSoup(html)

# print(f'Processing: ', {url})
# for name in soup.findAll('a', href=True):
#     zipurl = name['href']
#     if( zipurl.endswith('.zip') ):
#         outfname = outpath + zipurl.split('/')[-1]
#         r = requests.get(zipurl, stream=True)
#         if( r.status_code == requests.codes.ok ) :
#             fsize = int(r.headers['content-length'])
#             print('Downloading %s (%sMb)' % ( outfname, fsize/mbyte ))
#             with open(outfname, 'wb') as fd:
#                 for chunk in r.iter_content(chunk_size=1024): # chuck size can be larger
#                     if chunk: # ignore keep-alive requests
#                         fd.write(chunk)
#                 fd.close()





# <a class="icon file" draggable="true" href="/pub/outgoing/pur_archives/pur1974.zip">pur1974.zip</a>