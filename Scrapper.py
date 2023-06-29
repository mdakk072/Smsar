import requests
import json
import time
import yaml
import random
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Scraper:

    def __init__(self, configFile):
        self.configFileName = configFile
        print("> Scraper Initialized")
        print("-------------------")
        print(f"Configuration File: {configFile}")
        with open(configFile, 'r') as f:
            config = yaml.safe_load(f)
        self.config = config
        self.driver = None
        print("\nSteps and Parameters:")
        print('######################')
        states = self.config.get('states', {})
        for state, step in states.items():
            print(f">State: {state}")
            print(f"    Method: {step.get('method')}")
            print(f"    Next state: {step.get('next_state')}")
            parameters = step.get('parameters', {})
            if parameters:
                print(" Parameters:")
                for key, value in parameters.items():
                    print(f"        {key}: {value}")
            print("----------------------")
        
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
        
        time.sleep(1.5)

    def scrap_page(self, by, value):
        try:
            by_method = getattr(By, by)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            page_content = self.driver.find_element(by_method, value)
            page_html = page_content.get_attribute('outerHTML')
            return page_html
        except TimeoutException:
            print("TimeoutException: Timed out waiting for element to be present.")
            return None
        except NoSuchElementException:
            print(f"No such element found with {by} '{value}'.")
            return None
        except Exception as e:
            print(f"An error occurred during scraping: {str(e)}")
            return None

    def extract_data(self, raw_data, selectors):
        extracted_data = {}
        try:
            with open('raw_data.html', 'wb') as f:
                f.write(raw_data.encode('utf-8'))
            soup = BeautifulSoup(raw_data, 'html.parser')
            for ida, selector in enumerate(selectors):
                print(f"Extracting data with selector: {selector}")
                data_divs = soup.find_all(**selector)
                print(f"Found {len(data_divs)} elements with selector: {selector}")
                data_list = []
                for div in data_divs:
                    div_dict = {
                        'tag': div.name,
                        'attributes': self.extract_attributes(div),
                        'text': div.text.strip(),
                        'raw': str(div)
                    }
                    data_list.append(div_dict)
                extracted_data[ida] = data_list
        except TimeoutException:
            print("TimeoutException: Timed out waiting for element to be present.")
            return None
        except NoSuchElementException:
            print(f"No such element found with selector: {selector}.")
            return None
        except Exception as e:
            print(f"An error occurred during data extraction: {str(e)}")
            return None
        return extracted_data

    def extract_attributes(self, element):
        attributes = dict(element.attrs)
        for child in element.children:
            if child.name is not None:
                child_attributes = self.extract_attributes(child)
                attributes[child.name] = child_attributes
        return attributes

    def goto_next_page(self, base_url, next_page):
        next_page_url = base_url.format(i=next_page)
        next_page += 1

        # Save the updated value of next_page back to the YAML configuration file
        self.config['states']['goto_next_page']['parameters']['next_page'] = next_page
        with open(self.configFileName, 'w') as f:
            yaml.safe_dump(self.config, f)

        self.driver.get(next_page_url)
        time.sleep(5)

    def goto_link(self, link):
        self.driver.get(link)
        time.sleep(5)

    def call_api(self, api_url):
        response = requests.get(api_url)
        return response.json()

    def send_data(self, data, address):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(address, data=json.dumps(data), headers=headers)

        print(response.status_code)
        print(response.text)

        return response.status_code
    
    def scrape_site(self, config=None):
        config = self.config if not config else config
        # Get the initial state
        state = config['initial_state']
        while state is not None:
            step = config['states'][state]
            print("******************************")
            print(">Step:", state)
            print("     Method:", step['method'])
            parameters = step.get('parameters', {})
            if parameters:
                print(">Parameters:")
                for key, value in parameters.items():
                    if isinstance(value, str) and value == "{previous_result}":
                        value = previous_result
                        print(f'>previous_result : {type(previous_result)} {len(previous_result)}')
            method_name = step['method']
            parameters = {}
            # Replace placeholders in parameters with previous result, if applicable
            for key, value in step.get('parameters', {}).items():
                if isinstance(value, str) and value == "{previous_result}":
                    parameters[key] = previous_result
                    print(f'>previous_result : {type(previous_result)} {len(previous_result)}')
                else:
                    parameters[key] = value
            # Execute the method with the provided parameters
            method = getattr(self, method_name)
            result = method(**parameters)
            # Get the next state
            state = step['next_state']
            # If the next state is a function, call it with the result to determine the actual next state
            if callable(state):
                state = state(result)
            # Update the previous result for next iteration
            previous_result = result

scraper = Scraper('configWololo.yaml')
#scraper = Scraper('configAvito.yaml')
scraper.scrape_site()
