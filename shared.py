###
###
###

import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

NUM_TOP_THIRD_PARTY_DOMAINS = 10

def is_third_party(domain, site):
    return domain == site


def write_third_party_data(third_party_domains_dict,data_type,results_file):
# get dict of third party domains and corresponding number of <data_type>
# write domains with highest numbers of <data_type> to results_file
    if data_type == 'HTTP Request Data':
        type = 'requests'
    elif data_type == 'Cookie Data':
        type = 'cookies'
    else:
        type = 'JS API calls'
    sorted_domains_dict = sorted(third_party_domains_dict.items(),key=lambda x: x[1],reverse=True)
    results_file.write(data_type+' : Top 10 Most Popular Third-Party Domains of Websites in '+mode+'\n')
    for i in range(NUM_TOP_THIRD_PARTY_DOMAINS):
        results_file.write(sorted_domains_dict[i][0]+': '+sorted_domains_dict[i][1]+' '+type+'\n')

    results_file.write('\n')
    return


def third_party_data(cur,num_sites,results_file,data_type,mode,query):
# for each third party requested, count number of times it was requested
# write top 10 third parties and number of requests to file
    third_party_domains_dict = {}
    site_data = [0] * num_sites

    for row in cur.execute(query):
        visit_id = row[0]
        print(visit_id)
        third_party_domain = tldextract.extract(row[1]).registered_domain
        if is_third_party(third_party_domain,sites[visit_id]):
            site_data[visit_id] += 1
            if third_party_domain in third_party_domains_dict:
                third_party_domains_dict[third_party_domain] += 1
            else:
                third_party_domains_dict[third_party_domain] = 1

    write_third_party_data(third_party_domains_dict,data_type,results_file)
    return site_data


def make_bar_graph(sites,vanilla_data,adblock_data,graph_title,y_axis_label,results_file):
# make bar graph with number of http requests per site in vanilla and adblock modes
# save to file
    x = np.arange(len(sites))
    width = 0.35

    fig, ax = plt.subplots()
    rects_vanilla = ax.bar(x - width/2, vanilla_data, width, label='Vanilla Mode')
    rects_adblock = ax.bar(x + width/2, adblock_data, width, label='Ad-Blocking Mode')

    ax.set_ylabel(y_axis_label)
    ax.set_title(graph_title)
    ax.set_xticks(x)
    ax.set_xticklabels(sites)
    ax.legend()
    fig.tight_layout()
    plt.savefig(results_file)
    return
