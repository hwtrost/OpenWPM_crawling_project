###
###
###

import sqlite3
import pandas as pd
from webcrawler import *
from http_requests import *
from cookies import *
from js_calls import *

NUM_SITES = 5
sites_path = 'top-1m.csv'
vanilla_path = './data_vanilla/crawl-data.sqlite'
adblock_path = './data_adblock/crawl-data.sqlite'
results_file = open('results.txt','w')

# The list of sites that we wish to crawl
data = pd.read_csv(sites_path,header=None)
sites = data.iloc[:NUM_SITES,1]

crawl('vanilla',sites,NUM_SITES)
crawl('adblock',sites,NUM_SITES)

# create cursor objects for stored data
vanilla_conn = sqlite3.connect(vanilla_path)
adblock_conn = sqlite3.connect(adblock_path)
vanilla_cur = vanilla_conn.cursor()
adblock_cur = adblock_conn.cursor()


# write third party tables to results file
write_third_party_data(vanilla_cur,NUM_SITES,results_file,
                    'Top 10 Most Popular Third-Party Domains of Websites in Vanilla Mode')
write_third_party_data(adblock_cur,NUM_SITES,results_file,
                    'Top 10 Most Popular Third-Party Domains of Websites in Ad-Blocking Mode')


# get arrays with number of http requests made by sites
vanilla_requests = get_http_request_data(vanilla_cur,NUM_SITES)
adblock_requests = get_http_request_data(adblock_cur,NUM_SITES)


# make bar graph with http request data
make_http_bar_graph(sites,vanilla_requests,adblock_requests,results_file)
