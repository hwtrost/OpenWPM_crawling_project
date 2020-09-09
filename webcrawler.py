###
###
### note: had to install webpack, webpack-cli, web-ext globally

from OpenWPM.automation import CommandSequence,TaskManager
import pandas as pd

NUM_BROWSERS = 2
NUM_SITES = 100
vanilla_path = './data_vanilla'
adblock_path = './data_adblock'
sites_path = 'top-1m.csv'

data = pd.read_csv(sites_path,header=None)
sites = data.iloc[:NUM_SITES,1]

def crawl(mode):
    # Loads the default manager preferences and copies of the default browser dictionaries
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)
    adblock = (mode == 'adblock')

    # Update browser configuration (use this for per-browser settings)
    for i in range(NUM_BROWSERS):
        browser_params[i]['http_instrument'] = True #Record http requests and responses, saved to http_requests table
        browser_params[i]['cookie_instrument'] = True #Record cookie data, saved to javascript_cookies table
        browser_params[i]['js_instrument'] = True #Record JS calls, saved to javascript table
        browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
        browser_params[i]['display_mode'] = 'native' #Launch all browsers headless
        browser_params[i]['ublock-origin'] = adblock # True for adblock mode, False for vanilla mode

    # Update TaskManager configuration (use this for crawl-wide settings)
    if adblock:
        manager_params['data_directory'] = adblock_path
        manager_params['log_directory'] = adblock_path
    else:
        manager_params['data_directory'] = vanilla_path
        manager_params['log_directory'] = vanilla_path

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    # Visits the sites with all browsers simultaneously
    for site in sites:
        site = 'http://' + site
        command_sequence = CommandSequence.CommandSequence(site,reset=True)
        command_sequence.get(sleep=10, timeout=60)
        #command_sequence.dump_profile_cookies(120)
        manager.execute_command_sequence(command_sequence) # ** = synchronized browsers

    # Shuts down the browsers and waits for the data to finish logging
    manager.close()
    return

# run crawl in vanilla and ad-blocking modes
crawl('vanilla')
crawl('adblock')
