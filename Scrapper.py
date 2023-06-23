import requests
import json
import time
import random
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self, config):
        self.config = config
        #here we should read and check all config values
        self.driver = None
        self.init_driver()

    def init_driver(self):
        options = Options()
        options.add_argument('--disable-logging')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f"user-agent={self.config['userAgent']}")
        options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(options=options, service_log_path='selenium.txt' )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.delete_all_cookies()
        self.driver.get(self.config['base_url'])
        time.sleep(1.5)

    def scrap_page(self):
        #this include a parameters varaible to scrapp to more than css ( IT CAN be any )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        page_content = self.driver.find_element(By.CSS_SELECTOR, self.config['css_selector'])  
        page_html = page_content.get_attribute('outerHTML')
        return page_html

    def extract_data(self, raw_data):
                #this include a parameters varaible to scrapp to more than css ( IT CAN be any )

        soup = BeautifulSoup(raw_data, 'html.parser')
        data_divs = soup.find_all(self.config['data_div']['tag'], self.config['data_div']['class'])  
        data_list = []
        for div in data_divs:
            data_dict = {}
            # Extract data from div based on config
            # ...
            data_list.append(data_dict)
        return data_list

    def goto_next_page(self):
        #logic here is to have an actual varaible counting page and replacing number in base url
        self.driver.get(self.config['next_page_url'])
        time.sleep(5)

    def goto_link(self, link):
        self.driver.get(link)
        time.sleep(5)

    def call_api(self, api_url):
        response = requests.get(api_url)
        return response.json()

    def send_data(self, data):
        response = requests.post(self.config['data_endpoint'], data=json.dumps(data))
        return response.status_code
    def scrape_site(self, config):
        # Get the initial state
        state = config['initial_state']
        #here we should have each state mapped to a method in the config so we can run any fsm logic by calling methods with appropriate parameters 
        # While there is a next state, execute the current state and get the next state
        while state is not None:
            # Get the method to execute for the current state
            method = getattr(self, config['states'][state]['method'])

            # Execute the method with the provided parameters
            result = method(*config['states'][state]['parameters'])

            # Get the next state
            state = config['states'][state]['next_state']

            # If the next state is a function, call it with the result to determine the actual next state
            if callable(state):
                state = state(result)