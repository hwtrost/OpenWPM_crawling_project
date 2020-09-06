###
###
###

import sqlite3
import pandas as pd
from webcrawler import *
from shared import *

NUM_SITES = 10
sites_path = 'top-1m.csv'
vanilla_path = './data_vanilla/crawl-data.sqlite'
adblock_path = './data_adblock/crawl-data.sqlite'
results_file = open('results.txt','w')

# The list of sites to crawl
data = pd.read_csv(sites_path,header=None)
sites = data.iloc[:NUM_SITES,1]

crawl('vanilla',sites,NUM_SITES)
crawl('adblock',sites,NUM_SITES)

# create cursor objects for stored data
vanilla_conn = sqlite3.connect(vanilla_path)
adblock_conn = sqlite3.connect(adblock_path)
vanilla_cur = vanilla_conn.cursor()
adblock_cur = adblock_conn.cursor()

# analysis string variables
vanilla_mode = 'Vanilla Mode'
adblock_mode = 'Ad-Blocking Mode'

http_query = 'SELECT visit_id, url FROM http_requests'
cookie_query = 'SELECT visit_id, ?? FROM javascript_cookies'
js_query = 'SELECT visit_id, ?? FROM javascript'

http_title = 'HTTP Request Data'
cookie_title = 'Cookie Data'
js_title = 'JavaScript API Call Data'

http_y_label = 'Number of HTTP Requests'
cookie_y_label = 'Number of Cookies Stored'
js_y_label = 'Number of JS API Calls Made'

http_graph_file = 'http_requests.png'
cookie_graph_file = 'cookies.png'
js_graph_file = 'js_calls.png'

# get arrays with number of http requests to third party domains made by sites
vanilla_requests = third_party_data(vanilla_cur,NUM_SITES,results_file,http_title,van_mode,http_query)
adblock_requests = third_party_data(adblock_cur,NUM_SITES,results_file,http_title,ab_mode,http_query)
# make bar graph with http request data
make_bar_graph(sites,vanilla_requests,adblock_requests,http_title,http_y_label,http_graph_file)

# get arrays with number of cookies stored by third party domains on sites
vanilla_cookies = third_party_data(vanilla_cur,NUM_SITES,results_file,cookie_title,vanilla_mode,cookie_query)
adblock_cookies = third_party_data(adblock_cur,NUM_SITES,results_file,cookie_title,adblock_mode,cookie_query)
# make bar graph with cookie data
make_bar_graph(sites,vanilla_cookies,adblock_cookies,cookie_title,cookie_y_label,cookie_graph_file)

# get arrays with number of JS API calls made by third party domains on sites
vanilla_js_calls = third_party_data(vanilla_cur,NUM_SITES,results_file,js_title,vanilla_mode,js_query)
adblock_js_calls = third_party_data(adblock_cur,NUM_SITES,results_file,js_title,adblock_mode,js_query)
# make bar graph with JS call data
make_bar_graph(sites,vanilla_js_calls,adblock_js_calls,js_title,js_y_label,js_graph_file)
