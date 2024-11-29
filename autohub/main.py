from scrape import Scrape
from scrape_urls import ScrapeUrls
from file_proccessor import FileProccessing
from dotenv import load_dotenv
import os
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import json
from pathlib import Path
from datetime import date
import logging
import math
# from .autohub_parser import *
from file_proccessor import FileProccessing
# from .autohub_scraper import scrap_autohub_chunks_async,selector,output_file


TODAY= date.today()
AUTOHUB_JSON_URLS =f"autohub/autuhub_data/autohub_urls/autohub_urls_{TODAY}.json"


load_dotenv()

class ScrapeAutohub(Scrape):
    def __init__(self, url):
        super().__init__(url)
        self.car_urls = []
        self.ids = []
    def start_logging_in(self):
        try:
            self.login('AUTOHUB_USERNAME','AUTOHUB_PASSWORD','i_sUserId','i_sPswd')
            time.sleep(5)
            target_url = 'https://www.sellcarauction.co.kr/newfront/receive/rc/receive_rc_list.do'
            self.driver.get(target_url)
            time.sleep(5)
            dropdown = Select(self.driver.find_element(By.ID, "i_iPageSize"))
            # Select "100" items per page
            dropdown.select_by_value("100")
            detailed_tap = self.driver.find_element(By.XPATH,'//*[@id="aTabActive2"]')
            detailed_tap.click()
            select_element_year = Select(self.driver.find_element(By.ID,"i_sCarYearStr"))
            select_element_year.select_by_value("2019")
            self.driver.find_element(By.XPATH,'//*[@id="tab2"]/div/div[20]/a[1]').click()
            time.sleep(5)
            elements = self.driver.find_elements(By.CLASS_NAME, 'product-listing')
            self.auc_date = self.driver.find_element(By.CLASS_NAME,'timeline-heading').text
            count_row = self.driver.find_element(By.CLASS_NAME,'row')
            num_pages = count_row.find_elements(By.TAG_NAME,'div')[-1].find_element(By.XPATH,'//*[@id="frm"]/div/div[3]/div[5]/strong/span').text
            page = math.ceil(int(num_pages)/100)
            
            count=1
            while count<page:
                count+1
                # Extract elements on the current page
                print(page)
                for element in elements:
                    # Extract text
                    text = element.find_elements(By.CLASS_NAME,'car-title')
                    for i in text:
                        id = i.find_element(By.TAG_NAME,'a').get_attribute('onclick').split("'")[1]
                        urls = f'https://www.sellcarauction.co.kr/newfront/onlineAuc/on/onlineAuc_on_detail.do?receivecd={id}'
                        print(urls)
                        self.car_urls.append("{}".format(urls))
                        self.ids.append(id)
                        data={'auc_date':self.auc_date,'ids':self.ids,'car_urls':self.car_urls}
                        FileProccessing().export_json(data,AUTOHUB_JSON_URLS)
                current_page = self.driver.find_element(By.XPATH, "//ul[@class='pagination']/li[contains(@class, 'active')]/a")
                # Find the next page button
                next_page_number = int(current_page.text) + 1
                next_button_xpath = f"//ul[@class='pagination']/li/a[text()='{next_page_number}']"
                arrow_button_xpath = '//*[@id="frm"]/div/div[4]/div/div[103]/ul/li[14]/a'
                arrow_button=self.driver.find_element(By.XPATH,arrow_button_xpath)
                next_button = self.driver.find_elements(By.XPATH, next_button_xpath)
                print(arrow_button)
                if not arrow_button:
                    self.driver.quit()
                else:
                    
                    if not next_button:
                        # If the next page button is not found using the next page number, click on the arrow button
                        arrow_button_xpath = '//*[@id="frm"]/div/div[4]/div/div[103]/ul/li[14]/a'
                        arrow_button = self.driver.find_element(By.XPATH, arrow_button_xpath)
                        arrow_button.click()
                    else:
                        # If the next page button is found, click on it
                        next_button[0].click()
                    time.sleep(5)  # Add a delay to ensure the page fully loads
                    elements = self.driver.find_elements(By.CLASS_NAME, 'product-listing')
         
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        
        finally:
            self.driver.quit()

    
ScrapeAutohub('https://www.sellcarauction.co.kr/newfront/login.do').start_logging_in()

# urls = AutohubParsing().read_json_file(AUTOHUB_JSON_URLS)
# scrap_autohub_chunks_async(urls['car_urls'], selector, output_file)
# AutohubParsing().parsing_detail()