###
###
###

import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def write_third_party_data(cur,num_sites,results_file,table_title):
# for each third party requested, count number of times it was requested
# write top 10 third parties and number of requests to file
    third_party_domains_dict = {}

    for row in cur.execute('SELECT url FROM http_requests'):
        third_party_domain = tldextract.extract(row[0]).registered_domain
        # check if is a third party domain ??
        if third_party_domain in third_party_domains_dict:
            third_party_domains_dict[third_party_domain] += 1
        else:
            third_party_domains_dict[third_party_domain] = 1

    # get most-requested domains from dictonary, write to file
    sorted_domains_dict = sorted(third_party_domains_dict.items(),key=lambda x: x[1],reverse=True)
    results_file.write(table_title+'\n')
    for i in range(10):
        results_file.write(sorted_domains_dict[i][0]+': '+sorted_domains_dict[i][1]+' requests\n')

    results_file.write('\n')

    return



def get_http_request_data(cur,num_sites):
# for each website, count number of http requests made
# return number of requests made by each site
    num_requests = [0] * num_sites
    third_parties_dict = {}

    #for i in range(num_sites):





    return num_requests



def make_http_bar_graph(sites,vanilla_requests,adblock_requests):
# make bar graph with number of http requests per site in vanilla and adblock modes
# save to file
    x = np.arange(len(sites))
    width = 0.35

    fig, ax = plt.subplots()
    rects_vanilla = ax.bar(x - width/2, vanilla_requests, width, label='Vanilla Mode')
    rects_adblock = ax.bar(x + width/2, adblock_requests, width, label='Ad-Blocking Mode')

    ax.set_ylabel('Number of HTTP Requests')
    ax.set_title('HTTP Requests')
    ax.set_xticks(x)
    ax.set_xticklabels(sites)
    ax.legend()

    fig.tight_layout()
    plt.savefig('http_requests.png')

    return
