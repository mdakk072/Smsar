"""
Web Scraper

This file contains a web scraper class, `Scraper`, 
that is used to scrape websites based on a provided configuration.
The scraper is implemented using Selenium, BeautifulSoup, and Requests libraries.

Author: mdakk072

Date: 26/06/2023

Usage:
    - Instantiate the `Scraper` class with the path to the configuration file.
    - Call the `scrape_site` method to initiate the scraping process.

Example:
    scraper = Scraper('config.yaml')
    scraper.scrape_site()

"""
import json
import time
import yaml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from lxml import html
from  lxml.etree import tostring


class PageInteractor:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, by_method, value):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_method, value)))
            element.click()
        except TimeoutException:
            print("TimeoutException: Timed out waiting for element to be clickable.")
        except NoSuchElementException:
            print(f"No such element found with {by_method} '{value}'.")
        except Exception as error:
            print(f"An error occurred during clicking on the element: {str(error)}")

    def enter_text(self, by_method, value, text):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_method, value)))
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            print("TimeoutException: Timed out waiting for element to be present.")
        except NoSuchElementException:
            print(f"No such element found with {by_method} '{value}'.")
        except Exception as error:
            print(f"An error occurred during entering text: {str(error)}")

    def scroll_to_element(self, by_method, value):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_method, value)))
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except TimeoutException:
            print("TimeoutException: Timed out waiting for element to be present.")
        except NoSuchElementException:
            print(f"No such element found with {by_method} '{value}'.")
        except Exception as error:
            print(f"An error occurred during scrolling: {str(error)}")



class Scraper:
    """A web scraper class."""

    def __init__(self, config_file):
        """
        Initialize the scraper.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_filename = config_file
        print("> Scraper Initialized")
        print("-------------------")
        print(f"Configuration File: {config_file}")
        with open(config_file, 'r',encoding='utf-8') as file:
            config = yaml.safe_load(file)
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
        self.step_results = {}  # Store results of each step

        #self.init_driver()

    def init_driver(self):
        """
        Initialize the web driver for Selenium.
        """
        options = Options()
        options.add_argument('--disable-logging')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f"user-agent={self.config['userAgent']}")
        options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(options=options, service_log_path='selenium.txt')
        script = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        self.driver.execute_script(script)
        self.driver.delete_all_cookies()
        self.driver.get(url='https://www.google.com/')
        time.sleep(1.5)
    
    def get_nested_data(self, data, navigation_params):
        """Recursively navigate through nested data using provided navigation parameters.

        Parameters:
        data (any): The data to navigate (can be a dict, a list, or an object).
        navigation_params (list): The navigation parameters (type and name/index/key).

        Returns:
        The extracted data.
        """

        navigation_operations = {
            'key': lambda data, key: data.get(key),
            'index': lambda data, key: data[int(key)],
            'attr': lambda data, key: getattr(data, key, None)
        }

        if navigation_params:
       
            navigation_type, navigation_key = navigation_params.pop(0)
            data = navigation_operations[navigation_type](data, navigation_key)
            if data is None:
                raise ValueError(f'Navigation failed. Could not find {navigation_key} in data.')
            return self.get_nested_data(data, navigation_params)

        return data

    def get_data(self, **kwargs):
        """Get data from a specific source using navigation parameters.

        Parameters:
        kwargs (dict): The parameters with the source and the navigation parameters.

        Returns:
        The extracted data.
        """
        # Get source
        source = getattr(self, kwargs['source'], None)
        if source is None:
            raise ValueError(f"Invalid source: {kwargs['source']}")

        # Get navigation parameters
        navigation_params = kwargs['get']

        # Return the desired data
        print(source)
        print(navigation_params)
        print(source)
        input()
        return self.get_nested_data(source, navigation_params)

    def scrap_page(self, by_method, value):
        """
        Scrape the page using the given method and value.

        Args:
            by (str): The method to locate the element (e.g., 'ID', 'CSS_SELECTOR').
            value (str): The value to search for.

        Returns:
            str: The HTML content of the page, or None if an error occurred.
        """
        try:
            by_method = getattr(By, by_method)
            body_locator = (By.TAG_NAME, 'body')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(body_locator))
            page_content = self.driver.find_element(by_method, value)
            page_html = page_content.get_attribute('outerHTML')
            return page_html
        except TimeoutException:
            print("TimeoutException: Timed out waiting for element to be present.")
            return None
        except NoSuchElementException:
            print(f"No such element found with {by_method} '{value}'.")
            return None
        except AttributeError:
            print(f"AttributeError: The attribute {by_method} does not exist.")
            return None
        except Exception as error:
            print(f"An error occurred during scraping: {str(error)}")
            return None

    def extract_data(self, raw_data, selectors):
        """
        Extract data from the raw HTML using the provided selectors.

        Args:
            raw_data (str): The raw HTML content.
            selectors (list): A list of dictionaries containing selectors.

        Returns:
            dict: Extracted data, or None if an error occurred.
        """
        extracted_data = {}
        try:
            with open('raw_data.html', 'wb') as file:
                file.write(raw_data.encode('utf-8'))
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
        except Exception as error:
            print(f"An error occurred during data extraction: {str(error)}")
            return None
        return extracted_data

    def extract_infos(self, extracted_data, data_to_find):
        """
        Extract the information of interest from the extracted_data 
        using the keys specified in data_to_find.

        Args:
            extracted_data (dict): 
            data_to_find (dict): 

        Returns:
            dict: The data of interest, or None if an error occurred.
        """
        output_data={}
        for data_samples in extracted_data:
            output_data[data_samples]=[]
            for sample in extracted_data[data_samples]:
                infos={}
                for key, value in data_to_find.items():
                    if value['type'] == 'html':
                        # Add HTML extraction logic here
                        pass
                    elif value['type'] == 'xpath':
                        tree = html.fromstring(sample['raw'])
                        elements = tree.xpath(value['attribute'])
                        info=None
                        if not elements:
                            print(f"No elements found with XPath: {value['attribute']}")
                            infos[key]= info
                            continue
                        element = elements[0]
                        if value.get('extract') == 'text':
                            info = element.text_content()
                        elif value.get('extract') == 'attribute':
                            attribute_name = value.get('attribute_name')
                            if not attribute_name:
                                print("No attribute name specified for XPath attribute extraction.")
                                infos[key]= info
                                continue
                            info = element.get(attribute_name)
                        elif value.get('extract') == 'element':
                            print(value['extract'])
                            info = tostring(element)
                        else:
                            print(f"Invalid extract type: {value.get('extract')}")
                            infos[key]= info
                            continue
                        infos[key]= info

                    elif value['type'] == 'text':
                        # Add regex extraction logic here
                        pass
                    elif value['type'] == 'attribute':
                        # Add attribute extraction logic here
                        pass
                output_data[data_samples].append(infos)
        return output_data

    def extract_attributes(self, element):
        """
        Extract attributes from the given HTML element.

        Args:
            element (Tag): The HTML element.

        Returns:
            dict: Extracted attributes.
        """
        attributes = dict(element.attrs)
        for child in element.children:
            if child.name is not None:
                child_attributes = self.extract_attributes(child)
                attributes[child.name] = child_attributes
        return attributes

    def goto_next_page(self, base_url, next_page):
        """
        Go to the next page using the base URL and next page number.

        Args:
            base_url (str): The base URL with a placeholder for the page number.
            next_page (int): The next page number.

        Note:
            This method also updates the configuration file with the new next_page value.
        """
        next_page_url = base_url.format(i=next_page)
        next_page += 1

        # Save the updated value of next_page back to the YAML configuration file
        self.config['states']['goto_next_page']['parameters']['next_page'] = next_page
        with open(self.config_filename, 'w',encoding='utf-8') as file:
            yaml.safe_dump(self.config, file)

        self.driver.get(next_page_url)
        time.sleep(5)

    def goto_link(self, link):
        """
        Go to the specified link.

        Args:
            link (str): The URL to navigate to.
        """
        self.driver.get(link)
        time.sleep(5)

    def call_api(self, api_url, **kwargs):
        """
        Make a GET request to the specified API URL.

        Args:
            api_url (str): The URL of the API.
            **kwargs: Optional parameters for the GET request.

        Returns:
            dict: The JSON response.
        """
        params = kwargs.get('params', None)
        headers = kwargs.get('headers', None)
        timeout = kwargs.get('timeout', 15)

        try:
            response = requests.get(api_url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"An error occurred during API request: {str(error)}")
            return None

    def send_data(self, data, address):
        """
        Send data to the specified address using a POST request.

        Args:
            data (dict): The data to send.
            address (str): The address to send the data to.

        Returns:
            int: The status code of the response.
        """
        headers = {'Content-Type': 'application/json'}
        response = requests.post(address, data=json.dumps(data), headers=headers, timeout=5)

        print(response.status_code)
        print(response.text)

        return response.status_code

    def scrape_site(self, config=None):
        """
        Scrape the website using the provided configuration.

        Args:
            config (dict): The configuration to use (optional).

        Note:
            If no configuration is provided, the default configuration will be used.
        """
        config = self.config if not config else config
        # Get the initial state
        state = config['initial_state']
        previous_result = None
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
            print(type(previous_result))
            
            for key, value in step.get('parameters', {}).items():
                if isinstance(value, str) and value == "{previous_result}":
                    parameters[key] = previous_result
                    print(f'>previous_result : {type(previous_result)} {len(previous_result)}')
                else:
                    parameters[key] = value
            # Execute the method with the provided parameters
            method = getattr(self, method_name)
            result = method(**parameters)
            self.step_results[state] = result
            print(result)
            input(f">End of step {state}")            # Get the next state
            state = step['next_state']
            if callable(state):
                state = state(result)
            # Update the previous result for next iteration
            previous_result = result

#scraper = Scraper('configWololo.yaml')
#scraper = Scraper('configAvito.yaml')
scraper = Scraper('configAvito2.yaml')
scraper.scrape_site()
