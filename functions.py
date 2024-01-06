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
import time
import csv
import os


def read_csv(): 
    all_names = []
    with open('test.csv', 'r') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        for linha in leitor_csv:
            name = linha['Name']
            all_names.append(name)
    return all_names

#define a helper function
def click_modal_button(driver, button_text):    
    modal_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[text() = '%s']" % (button_text))))
    modal_button.click()                                                      

#define a function that adds contact_to_add to group_name
def add_contact_to_group(driver, group_name, names):
    #find chat with the correct title
    el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()
        
    #wait for it to load by detecting that the header changed with the new title
    # el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))
    # print('Passei aqui')
    # print(el_header_title)
    # el_header_title.click()
    #click on the menu button
    el_menu_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//div//span[@data-icon='menu']")))
    el_menu_button.click()
    
    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()    
    
    for name in names:
        contact_to_add = name
        #click on the Add Participant button
        el_add_participant = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//section//div[string() = 'Add member']")))
        el_add_participant.click()    
        
        #click on the Search
        el_modal_popup = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
        el_modal_popup.find_element(By.XPATH, "//div[contains(@title, 'Search input textbox')]").send_keys(contact_to_add)
        
        #click on the Contact
        el_contact_to_add = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//span[@title='%s']" % (contact_to_add))))
        el_contact_to_add.click()    
        
        #check whether already added
        if len(el_modal_popup.find_elements(By.XPATH, "//div[text() = 'Already added to group']")) > 0:
            print(contact_to_add + ' was already an existing participant of ' + group_name)
            el_modal_popup.find_element(By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='x']").click()
        else:    
            #click on the Green Check Mark
            el_green_check = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='checkmark-medium']")))
            el_green_check.click()        

            #click on the Add Participant
            click_modal_button(driver,'Add member')
            print(contact_to_add + ' added to ' + group_name)
        time.sleep(10)

def remove_contact_from_group(driver,group_name, contact_to_remove):
    #find chat with the correct title
    el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()    
        
    #wait for it to load by detecting header changed
    el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))
        
    #click on the menu button
    el_menu_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//div[@data-testid='conversation-menu-button']")))
    el_menu_button.click()
    
    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()
    
    #wait until target user can be found
    try:
        el_target_contact = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[@role='gridcell']//span[@title='%s']" % (contact_to_remove))))
        
        #Need to Hover over Contact
        #Ref: https://www.roelpeters.be/mouseover-in-selenium-hover/            
        ActionChains(driver).move_to_element(el_target_contact).perform() #hover over

        #Wait for dropdown arrow to appear, then click it.
        #Ref: https://stackoverflow.com/questions/27934945/selenium-move-to-element-does-not-always-mouse-hover
        el_dropdown_arrow = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[@role='gridcell']//button[@aria-label='Open the chat context menu']")))
        el_dropdown_arrow.click()

        #click on the Make group admin button
        el_remove_from_group = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Remove']")))
        el_remove_from_group.click()

        #click on the green button
        click_modal_button('Remove')
        print(contact_to_remove + ' removed from ' + group_name)
    except:
        print("Error occured while finding user in chat")
        
        
def make_group_admin(driver, group_name, contact_to_add):
    #find chat with the correct title
    el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()    
        
    #wait for it to load by detecting header changed
    el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))
        
    #click on the menu button
    el_menu_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//div[@data-testid='conversation-menu-button']")))
    el_menu_button.click()
    
    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()
    
    #wait until target user can be found
    el_target_contact = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[@role='gridcell']//span[@title='%s']" % (contact_to_add))))
    
    #check whether user is already admin by looking for the Group admin label
    has_group_admin_label = len(el_target_contact.find_elements(By.XPATH, "../../..//div[text() = 'Group admin']"))    
    if has_group_admin_label > 0:    
        print(contact_to_add + (' were' if contact_to_add == 'You' else ' was') + ' already an existing admin of ' + group_name)
    else:
        #Need to Hover over Contact
        #Ref: https://www.roelpeters.be/mouseover-in-selenium-hover/            
        ActionChains(driver).move_to_element(el_target_contact).perform() #hover over

        #Wait for dropdown arrow to appear, then click it.
        #Ref: https://stackoverflow.com/questions/27934945/selenium-move-to-element-does-not-always-mouse-hover
        el_dropdown_arrow = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[@role='gridcell']//button[@aria-label='Open the chat context menu']")))
        el_dropdown_arrow.click()
    
        #click on the Make group admin button
        el_make_group_admin = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Make group admin']")))
        el_make_group_admin.click()
    
        #click on the green button
        click_modal_button('Make group admin')
        print(contact_to_add + ' added as admin of ' + group_name)

def dismiss_as_group_admin(driver, group_name, contact_to_remove):
    #find chat with the correct title
    el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()    
        
    #wait for it to load by detecting header changed
    el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))
        
    #click on the menu button
    el_menu_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//div[@data-testid='conversation-menu-button']")))
    el_menu_button.click()
    
    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()
    
    #wait until target user can be found
    el_target_contact = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[@role='gridcell']//span[@title='%s']" % (contact_to_remove))))
    
    #Check whether user is already admin by looking for the Group admin label
    has_group_admin_label = len(el_target_contact.find_elements(By.XPATH, "../../..//div[text() = 'Group admin']"))    
    if has_group_admin_label < 1:    
        print(contact_to_remove + (' were' if contact_to_remove == 'You' else ' was') + ' not an existing admin of ' + group_name)
    else:
        #Need to Hover over Contact
        #Ref: https://www.roelpeters.be/mouseover-in-selenium-hover/            
        ActionChains(driver).move_to_element(el_target_contact).perform() #hover over

        #Wait for dropdown arrow to appear, then click it.
        #Ref: https://stackoverflow.com/questions/27934945/selenium-move-to-element-does-not-always-mouse-hover
        el_dropdown_arrow = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[@role='gridcell']//button[@aria-label='Open the chat context menu']")))
        el_dropdown_arrow.click()
    
        #click on the Make group admin button
        el_make_group_admin = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Dismiss as admin']")))
        el_make_group_admin.click()
            
        print(contact_to_remove + ' removed as admin of ' + group_name) 