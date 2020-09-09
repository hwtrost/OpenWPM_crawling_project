###
###
###

import pandas as pd
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tldextract

NUM_SITES = 100
NUM_TOP_THIRD_PARTY_DOMAINS = 10

# path,file variables
sites_path = 'top-1m.csv'
vanilla_path = './data_vanilla/crawl-data.sqlite'
adblock_path = './data_adblock/crawl-data.sqlite'
results_file = open('results.txt','w')

# The list of sites to crawl
data = pd.read_csv(sites_path,header=None)
sites = data.iloc[:NUM_SITES,1]

print(sites)


# analysis string variables
vanilla_mode = 'Vanilla Mode'
adblock_mode = 'Ad-Blocking Mode'

http_query = 'SELECT visit_id,url FROM http_requests'#['url','http_requests']
cookie_query = 'SELECT visit_id,host FROM javascript_cookies'#['host','javascript_cookies']
js_query = 'SELECT visit_id,script_url FROM javascript'#['script_url','javascript']

http_title = 'HTTP Request Data'
cookie_title = 'Cookie Data'
js_title = 'JavaScript API Call Data'

http_y_label = 'Number of HTTP Requests'
cookie_y_label = 'Number of Cookies Stored'
js_y_label = 'Number of JS API Calls Made'

http_graph_file = 'http_requests.png'
cookie_graph_file = 'cookies.png'
js_graph_file = 'js_calls.png'


def is_third_party(domain, site):
    #print(domain)
    #print(site)
    #is_third = (domain != site)
    #print(is_third)
    return domain != site


def write_third_party_data(third_party_domains_dict,data_type,mode):
# get dict of third party domains and corresponding number of <data_type>
# write domains with highest numbers of <data_type> to results_file
    if data_type == 'HTTP Request Data':
        type = 'requests'
    elif data_type == 'Cookie Data':
        type = 'cookies'
    else:
        type = 'JS API calls'
    sorted_domains_dict = sorted(third_party_domains_dict.items(),key=lambda x: x[1],reverse=True)
    results_file.write(data_type+': Top 10 Most Popular Third-Party Domains of Websites in '+mode+'\n')
    for i in range(NUM_TOP_THIRD_PARTY_DOMAINS):
        #print(sorted_domains_dict[i][0])
        #print(str(sorted_domains_dict[i][1]))
        line = str(i+1)+'. '+sorted_domains_dict[i][0]+': '+str(sorted_domains_dict[i][1])+' '+type+'\n'
        results_file.write(line)
    results_file.write('\n')
    return


def third_party_data(cur,data_type,mode,query):
# for each third party requested, count number of times it was requested
# write top 10 third parties and number of requests to file
    third_party_domains_dict = {}
    site_data = [0] * NUM_SITES
    #query_1 = 'SELECT MIN(visit_id) FROM '+query[1]
    #query_2 = 'SELECT visit_id,'+query[0]+' FROM '+query[1]

    #id_subtract = cur.execute(query_1)
    #id_subtract = id_subtract.fetchone()[0]
    #if query == 'SELECT visit_id,host FROM javascript_cookies':
        #for row in cur.execute('SELECT * FROM javascript_cookies'):
            #print(row)

    for row in cur.execute(query):
        if query=='SELECT visit_id,host FROM javascript_cookies':
            print(row)
        visit_id = row[0]-1

        #print(visit_id)
        third_party_domain = tldextract.extract(row[1]).registered_domain
        if is_third_party(third_party_domain,sites[visit_id]):
            site_data[visit_id] += 1
            if third_party_domain in third_party_domains_dict:
                third_party_domains_dict[third_party_domain] += 1
            else:
                third_party_domains_dict[third_party_domain] = 1

    #print(third_party_domains_dict)

    write_third_party_data(third_party_domains_dict,data_type,mode)
    return site_data


def make_bar_graph(vanilla_data,adblock_data,graph_title,y_axis_label,graph_file):
# make bar graph with number of http requests per site in vanilla and adblock modes
# save to file
    x = np.arange(len(sites))
    width = 0.4

    fig, ax = plt.subplots(figsize=(20,10))
    rects_vanilla = ax.bar(x - width/2, vanilla_data, width, label='Vanilla Mode')
    rects_adblock = ax.bar(x + width/2, adblock_data, width, label='Ad-Blocking Mode')

    ax.set_ylabel(y_axis_label)
    ax.set_xlabel('Top 100 Websites')
    ax.set_title(graph_title)
    ax.set_xticks(x)
    ax.set_xticklabels(sites,rotation='vertical')
    ax.legend()
    plt.subplots_adjust(bottom=0.25)
    #fig.tight_layout()
    plt.savefig(graph_file)
    return


# create cursor objects for stored data
vanilla_conn = sqlite3.connect(vanilla_path)
adblock_conn = sqlite3.connect(adblock_path)
vanilla_cur = vanilla_conn.cursor()
adblock_cur = adblock_conn.cursor()


# get arrays with number of http requests to third party domains made by sites
vanilla_requests = third_party_data(vanilla_cur,http_title,vanilla_mode,http_query)
adblock_requests = third_party_data(adblock_cur,http_title,adblock_mode,http_query)
# make bar graph with http request data
make_bar_graph(vanilla_requests,adblock_requests,http_title,http_y_label,http_graph_file)

# get arrays with number of cookies stored by third party domains on sites
vanilla_cookies = third_party_data(vanilla_cur,cookie_title,vanilla_mode,cookie_query)
adblock_cookies = third_party_data(adblock_cur,cookie_title,adblock_mode,cookie_query)
# make bar graph with cookie data
make_bar_graph(vanilla_cookies,adblock_cookies,cookie_title,cookie_y_label,cookie_graph_file)

# get arrays with number of JS API calls made by third party domains on sites
vanilla_js_calls = third_party_data(vanilla_cur,js_title,vanilla_mode,js_query)
adblock_js_calls = third_party_data(adblock_cur,js_title,adblock_mode,js_query)
# make bar graph with JS call data
make_bar_graph(vanilla_js_calls,adblock_js_calls,js_title,js_y_label,js_graph_file)
