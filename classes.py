from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from enum import Enum
from typing import List

# class ExecutionStatus(Enum):
#     FINISHED = 1
#     RUNNING = 2

class WABotGroup():
    def __init__(self, names, device_name):
        chrome_options = webdriver.ChromeOptions();
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f'--user-data-dir=./Devices/User_Data_{device_name}')
        self.names = names
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://web.whatsapp.com/')
        self.functions = Orchestrator()

    def find_chat(self, chat_name): 
        try:
            self.driver.refresh()
            el_side = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.ID, "side")))
            #locate the search box
            el_search = el_side.find_element(By.XPATH, "//div[contains(@title, 'Search')]")
            self.functions.sleep(1)
            el_search.clear()
            el_search.send_keys(chat_name)
        except Exception as exception:
            print("Exception: {}".format(type(exception).__name__))
            print("Exception message: {}".format(exception))

    def select_target_chat(self, chat_name):
        self.functions.sleep(2)
        el_target_chat = WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (chat_name))))
        el_target_chat.click()

    def add_contact_to_group(self, group_name, contact_to_add):
        # find the target chat
        self.select_target_chat(chat_name=group_name)

        # click on the menu button
        self.functions.sleep(2)
        el_menu_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//div//span[@data-icon='menu']")))
        el_menu_button.click()
        
        #click on the group infoß
        self.functions.sleep(2)
        el_group_info = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
        el_group_info.click()    

        self.functions.sleep(1)
        #click on the Add Participant button
        el_add_participant = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//section//div[string() = 'Add member']")))
        el_add_participant.click()    

        #click on the Search
        self.functions.sleep(2)
        el_modal_popup = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
        self.driver.find_element(By.XPATH, "//div[contains(@title, 'Search input textbox')]").send_keys(contact_to_add)
        
        self.functions.sleep(2)
        user_exist = self.verify_if_exists(el_modal_popup)
        if user_exist is True:
            #click on the Contact
            self.functions.sleep(2)
            el_contact_to_add = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//span[@title='%s']" % (contact_to_add))))
            el_contact_to_add.click()    
            
            self.functions.sleep(2)
            #check whether already added
            if (len(el_modal_popup.find_elements(By.XPATH, "//div[text() = 'Already added to group']")) > 0):
                print(contact_to_add + ' was already an existing participant of ' + group_name)
                if((len(el_modal_popup.find_elements(By.XPATH, "//div[text() = 'Already added to group']")) > 0)):
                    el_modal_popup.find_element(By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='x']").click()
            else:
                self.functions.sleep(2)
                #click on the Green Check Mark
                el_green_check = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='checkmark-medium']")))
                el_green_check.click()   
                self.click_modal_button('Add member') 
                self.functions.sleep(4)               
                if(self.cancel_invite(el_modal_popup=el_modal_popup) is not True):
                    #send_message(driver, name)
                    print(contact_to_add + ' added to ' + group_name)

    def cancel_invite(self, el_modal_popup): 
        try:
            el_modal_popup = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
            if len(el_modal_popup.find_elements(By.XPATH, "//div[@data-animate-modal-body='true']//div[contains(text(), 'You can invite them privately to join this group.')]")) > 0:
                print("Contato não pode ser adicionado")
                self.click_modal_button('Cancel')
            return True
        except Exception:
            return False
    #define a helper function
    def click_modal_button(self, button_text):    
        modal_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[text() = '%s']" % (button_text))))
        modal_button.click()     
        
    def verify_if_exists(self, el_modal_popup):
        try:
            el_modal_popup = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
            if len(el_modal_popup.find_elements(By.XPATH, "//div[@data-animate-modal-body='true']//div//span[contains(text(), 'No chats, contacts or messages found')]")) > 0:
                print("Contato não existe.")
                el_modal_popup.find_element(By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-icon='x']").click()
                return False
            else:
                return True
        except Exception:
            return False
        
    def send_message(self, message):
        text_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']//footer//div[@role='textbox']")))   
        text_field.clear() 
        text_field.send_keys(message)

        self.functions.sleep(5)

        send_message = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//footer//div//span[@data-icon='send']")))
        send_message.click()     
        self.functions.sleep(5)


class WABotMessage():

    def __init__(self, messages, device_name):
        chrome_options = webdriver.ChromeOptions();
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f'--user-data-dir=./Devices/User_Data_{device_name}')
        self.messages = messages
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://web.whatsapp.com/')
        self.functions = Orchestrator()


    def find_chat(self, chat_name): 
        try:
            #wait 60 secs to allow for the user to manually scan the Whatsapp Web QR code to log on
            el_side = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.ID, "side")))

            #locate the search box
            el_search = el_side.find_element(By.XPATH, "//div[contains(@title, 'Search')]")
            print("Logged in and located search box:", el_search)

            self.functions.sleep(2)
            el_search.clear()
            el_search.send_keys(chat_name)
        
        except Exception as exception:
            print("Exception: {}".format(type(exception).__name__))
            print("Exception message: {}".format(exception))

    def select_target_chat(self, chat_name):
        self.functions.sleep(2)
        el_target_chat = WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (chat_name))))
        el_target_chat.click()

    def send_message(self, message, chat):
        self.select_target_chat(chat_name=chat)
        text_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']//footer//div[@role='textbox']")))   
        text_field.clear() 
        text_field.send_keys(message)

        self.functions.sleep(5)

        send_message = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//footer//div//span[@data-icon='send']")))
        send_message.click()     
        self.functions.sleep(5)

class Orchestrator():

    def selectOperation(self):
        print("Which operation would you like use today?")
        print("1 - Start adding people to groups.")
        print("2 - Start sending messages to people.")
        operation = int(input("Select option: "))
        devices_number = int(input("How many devices: "))

        if operation == 1:
            self.startAddingGroupContacts(devices_number=devices_number)
        if operation == 2:
            self.startSendingMessages(devices_number=devices_number)

        print("All done or the command you typed does not exist.")

    def startAddingGroupContacts(self, devices_number):
        devices: List[WABotGroup] = []
        all_names = self.read_names()
        all_groups = self.read_groups()
        for device in range(devices_number):
            device_name = input(f"Digite o nome do {device+1} dispositivo: ")
            devices.append(WABotGroup(names=self.store_names(all_contacts=all_names), device_name=device_name))
        users_added = len(all_names)
        while True:
            for chat_name in all_groups:
                for device in devices:
                    device.find_chat(chat_name)
                    for contact in device.names:
                        device.add_contact_to_group(group_name=chat_name, contact_to_add=contact)
                        users_added -=1
                    device.names = self.restore_names(all_contacts=all_names)
            if len(all_names) == 0 and len(all_names) == users_added: 
                break

    def startSendingMessages(self, devices_number):
        devices: List[WABotMessage] = []
        all_names = self.read_names()
        all_messages = self.read_messages()
        for device in range(devices_number):
            device_name = input(f"Digite o nome do {device+1} dispositivo: ")
            devices.append(WABotMessage(messages=all_messages, device_name=device_name))
        while True:
            for name in all_names:
                for device in devices:
                    device.find_chat(name)
                    for message in all_messages:
                        device.send_message(message=message, chat=name)
            break
            
    def remove_names(self, all_contacts, names_to_remove):
        for name_to_remove in names_to_remove:
            for name in all_contacts:
                if name == name_to_remove:
                    all_contacts.remove(name_to_remove)

    def store_names(self, all_contacts):
        names_to_store = all_contacts[:1]
        self.remove_names(all_contacts=all_contacts, names_to_remove=names_to_store)
        return names_to_store
    
    def restore_names(self, all_contacts):
        names_to_store = all_contacts[:1]
        self.remove_names(all_contacts=all_contacts, names_to_remove=names_to_store)
        return names_to_store

    def sleep(self, seconds):
        time.sleep(seconds)

    def read_groups(self): 
        all_groups = []
        with open('groups.csv', 'r') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                group = linha['Group']
                all_groups.append(group)
        return all_groups
    
    def read_names(self): 
        all_names = []
        with open('names.csv', 'r') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                name = linha['Name']
                all_names.append(name)
        return all_names
    
    def read_messages(self): 
        all_messages = []
        with open('messages.csv', 'r') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                message = linha['Message']
                all_messages.append(message)
        return all_messages
