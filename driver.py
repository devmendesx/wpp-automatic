from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from enum import Enum

class Driver():
    def __init__(self, people, start):
        chrome_options = Options()
        self.people = people
        self.start = start
        chrome_options.add_argument("--start-maximized")
        self.web_driver = webdriver.Chrome(options=chrome_options)
        self.web_driver.get('https://web.whatsapp.com/')


class ExecutionStatus(Enum):
    FINISHED = 1
    RUNNING = 2