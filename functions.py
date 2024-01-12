from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from driver import Driver
from driver import ExecutionStatus
import time
import csv

def read_csv(): 
    all_names = []
    with open('test.csv', 'r') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        for linha in leitor_csv:
            name = linha['Name']
            all_names.append(name)
    return all_names

def send_message(driver, name):
    text_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']//footer//div[@role='textbox']")))    
    text_field.send_keys(f"O pai é peri, @{name}")

    sleep(5)

    send_message = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//footer//div//span[@data-icon='send']")))
    send_message.click()     
    sleep(5)

#define a helper function
def click_modal_button(driver, button_text):    
    modal_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[text() = '%s']" % (button_text))))
    modal_button.click()                                            

#define a function that adds contact_to_add to group_name
def add_contact_to_group(driver, group_name, name, time_after_add):
    #find chat with the correct title
    el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()
    sleep(1)
    #wait for it to load by detecting that the header changed with the new title
    # el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))
    # print('Passei aqui')
    # print(el_header_title)
    # el_header_title.click()
    #click on the menu button
    el_menu_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//div//span[@data-icon='menu']")))
    el_menu_button.click()
    sleep(1)
    
    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()    
    sleep(1)
    
    contact_to_add = name
    #click on the Add Participant button
    el_add_participant = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//section//div[string() = 'Add member']")))
    el_add_participant.click()    

        #click on the Search
    el_modal_popup = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
    driver.find_element(By.XPATH, "//div[contains(@title, 'Search input textbox')]").send_keys(contact_to_add)
    sleep(1)
        
    user_exist = verify_if_exists(driver, el_modal_popup)
    if user_exist is True:
        #click on the Contact
        el_contact_to_add = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//span[@title='%s']" % (contact_to_add))))
        el_contact_to_add.click()    
        
        #check whether already added
        if (len(el_modal_popup.find_elements(By.XPATH, "//div[text() = 'Already added to group']")) > 0):
            print(contact_to_add + ' was already an existing participant of ' + group_name)
            if((len(el_modal_popup.find_elements(By.XPATH, "//div[text() = 'Already added to group']")) > 0)):
                el_modal_popup.find_element(By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='x']").click()
        else:    
            #click on the Green Check Mark
            el_green_check = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='checkmark-medium']")))
            el_green_check.click()   
            click_modal_button(driver,'Add member')                
            if(cancel_invite(driver=driver, el_modal_popup=el_modal_popup) is not True):
                #send_message(driver, name)
                print(contact_to_add + ' added to ' + group_name)
    sleep(time_after_add)

def sleep(seconds):
    time.sleep(seconds)

def cancel_invite(driver, el_modal_popup): 
    try:
        sleep(3)
        el_modal_popup = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
        if len(el_modal_popup.find_elements(By.XPATH, "//div[@data-animate-modal-body='true']//div[contains(text(), 'You can invite them privately to join this group.')]")) > 0:
            print("Contato não pode ser adicionado")
            click_modal_button(driver, 'Cancel')
        return True
    except Exception:
        return False

def verify_if_exists(driver, el_modal_popup):
    try:
        el_modal_popup = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
        if len(el_modal_popup.find_elements(By.XPATH, "//div[@data-animate-modal-body='true']//div//span[contains(text(), 'No chats, contacts or messages found')]")) > 0:
            print("Contato não existe.")
            el_modal_popup.find_element(By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='x']").click()
            return False
        else:
            return True
    except Exception:
        return False

def get_names(names, startNumber, finishNumber):
    return names[startNumber:finishNumber]

def script(chat_name, driver): 
    try:
    #wait 60 secs to allow for the user to manually scan the Whatsapp Web QR code to log on
        el_side = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "side")))

        #locate the search box
        el_search = el_side.find_element(By.XPATH, "//div[contains(@title, 'Search')]")
        print("Logged in and located search box:", el_search)

        sleep(1)
        el_search.clear()
        el_search.send_keys(chat_name)
       
    except Exception as exception:
        print("Exception: {}".format(type(exception).__name__))
        print("Exception message: {}".format(exception))
        
def main(number_of_people_to_add, time_to_finish, chat_name, start):
    try:
        people_added = 0
        start_execution = datetime.now()
        all_names = read_csv()
        drivers = [Driver(people=get_names(all_names, startNumber=start, finishNumber=number_of_people_to_add * 1), start=start),
                    Driver(people=get_names(all_names, startNumber=(start+number_of_people_to_add), finishNumber=number_of_people_to_add * 2), start=(start+number_of_people_to_add))]
        execution_status = ExecutionStatus.RUNNING
        while is_running(execution_status):
            for driver in drivers:
                start_crew = datetime.now()
                script(chat_name=chat_name, driver=driver.web_driver)                   
                print('Adicionando usuários ao grupo: ', chat_name)
                for count in range(len(driver.people)):
                    if count < number_of_people_to_add:
                        add_contact_to_group(name=driver.people[count], time_after_add=time_to_finish, group_name=chat_name, driver=driver.web_driver)
                        people_added +=1
                        count +=1
                driver.start += number_of_people_to_add * 2
                if(len(driver.people) == 0):
                    execution_status = ExecutionStatus.FINISHED
                else:
                    driver.people = get_names(all_names, startNumber=driver.start, finishNumber=(driver.start+number_of_people_to_add))
                    end_crew = datetime.now()
                    print('Crew finished, duration: {}'.format(end_crew - start_crew)) 
            
        end_execution = datetime.now()
        print(f"{people_added} people added to group {chat_name}!")
        print('Execution ended, duration: {}'.format(end_execution - start_execution)) 

    except Exception as exception:
        raise exception

def is_running(status):
    return status == ExecutionStatus.RUNNING

def finish_execution(execution_status): 
    execution_status = ExecutionStatus.FINISHED
    return execution_status 