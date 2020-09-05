###
###
###

from openwpm.automation import TaskManager, CommandSequence
import pdb

NUM_BROWSERS = 2
vanilla_path = './data_vanilla'
adblock_path = './data_adblock'

def crawl(site_mode,sites,num_sites):
    # Loads the default manager preferences and 3 copies of the default browser dictionaries
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)
    set_ublock_origin = (site_mode == 'adblock')
    # Update browser configuration (use this for per-browser settings)
    for i in range(NUM_BROWSERS):
        browser_params[i]['http_instrument'] = True #Record http requests and responses, saved to http_requests table
        browser_params[i]['cookie_instrument'] = True #Record cookie data, saved to javascript_cookies table
        browser_params[i]['js_instrument'] = True #Record JS calls, saved to javascript table
        browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
        browser_params[i]['display_mode'] = 'headless' #Launch all browsers headless
        browser_params[i]['ublock-origin'] = set_ublock_origin

    # Update TaskManager configuration (use this for crawl-wide settings)
    if set_ublock_origin:
        manager_params['data_directory'] = adblock_path
        manager_params['log_directory'] = adblock_path
    else:
        manager_params['data_directory'] = vanilla_path
        manager_params['log_directory'] = vanilla_path

    #pdb.set_trace()

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    # Visits the sites with all browsers simultaneously
    for site in sites:
        site = 'http://' + site
        command_sequence = CommandSequence.CommandSequence(site)
        command_sequence.get(sleep=0, timeout=60)
        #command_sequence.dump_profile_cookies(120)
        manager.execute_command_sequence(command_sequence) # ** = synchronized browsers

    # Shuts down the browsers and waits for the data to finish logging
    manager.close()
