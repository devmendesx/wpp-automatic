from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from functions import add_contact_to_group
import time

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://web.whatsapp.com/')

#wait 60 secs to allow for the user to manually scan the Whatsapp Web QR code to log on
el_side = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "side")))

#locate the search box
el_search = el_side.find_element(By.XPATH, "//div[contains(@title, 'Search')]")
print("Logged in and located search box:", el_search)

list_chat_groups_test = [
'Grupe'
]

start_time = datetime.now()

#loop through a provided list of chat groups to perform an action
#REPLACE list_chat_groups_test with your chosen list name defined in Part 2
for chat_name in list_chat_groups_test:
        
    el_search.clear()
    el_search.send_keys(chat_name)
    
    try:

        ##########################################################
        ## COMMENT OUT the #1, #2, #3 or #4 BLOCKS as necessary ##
        ##########################################################
        
        #1 Add Contact to Group
        print('Attempting to add to', chat_name, ":")
        for name in ['Renê']:
            add_contact_to_group(driver, chat_name, name)

#         #2 Remove Contact from Group
#         print('Attempting to remove from group ', chat_name, ":")
#         remove_contact_from_group(chat_name, 'INSERT USER NAME HERE')      
        
#         #3 Set Contact as Group Admin
#         print('Attempting to make group admin of ', chat_name, ":")
#         make_group_admin(chat_name, 'INSERT USER NAME HERE')

#         #4 Dismiss Contact as Group Admin
#         print('Attempting to dismiss as admin of ', chat_name, ":")
#         dismiss_as_group_admin(chat_name, 'INSERT USER NAME HERE')

        
    except Exception as exception:
        print("Exception: {}".format(type(exception).__name__))
        print("Exception message: {}".format(exception))
    
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))