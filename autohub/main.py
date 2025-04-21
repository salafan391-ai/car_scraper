from scrape import Scrape
from scrape_urls import ScrapeUrls
from file_proccessor import FileProccessing
from dotenv import load_dotenv
import os
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
def read_autohub_file(file_path):
    with open(file_path) as j:
        return json.load(j)
class ScrapeAutohub(Scrape):
    def __init__(self, url):
        super().__init__(url)
        self.car_urls = []
        self.ids = []
        self.entries=[]
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
            # select_element_year = Select(self.driver.find_element(By.ID,"i_sCarYearStr"))
            # select_element_year.select_by_value("2010")
            # self.driver.find_element(By.XPATH,'//*[@id="tab2"]/div/div[20]/a[1]').click()
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
                    entry = element.find_elements(By.CSS_SELECTOR,'.i_comm_main_txt2.text_style7')
                    for i, j in zip(text,entry):

                        id = i.find_element(By.TAG_NAME,'a').get_attribute('onclick').split("'")[1]
                        urls = f'https://www.sellcarauction.co.kr/newfront/onlineAuc/on/onlineAuc_on_detail.do?receivecd={id}'
                        print(urls)
                        self.car_urls.append("{}".format(urls))
                        self.ids.append(id)
                        self.entries.append(j.text)
                        data={'auc_date':self.auc_date,'ids':self.ids,'entries':self.entries,'car_urls':self.car_urls}
                        FileProccessing().export_json(data,AUTOHUB_JSON_URLS)
                try:
                    current_page = self.driver.find_element(By.XPATH, "//ul[@class='pagination']/li[contains(@class, 'active')]/a")
                    next_page_number = int(current_page.text) + 1
                    next_button_xpath = f"//ul[@class='pagination']/li/a[text()='{next_page_number}']"
                    arrow_button_xpath = '//*[@id="frm"]/div/div[4]/div/div[103]/ul/li[14]/a'

                    # Try to find the next page button first
                    next_button = self.driver.find_elements(By.XPATH, next_button_xpath)

                    if next_button:
                        # Click on the next page button if found
                        next_button[0].click()
                    else:
                        # If next button is not found, try clicking the arrow button
                        try:
                            arrow_button = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, arrow_button_xpath))
                            )
                            arrow_button.click()
                        except Exception as e:
                            logging.error(f"Pagination arrow button not clickable: {e}")
                            self.driver.quit()
                            return

                    # Wait for the page to load after clicking
                    time.sleep(5)
                    elements = self.driver.find_elements(By.CLASS_NAME, 'product-listing')
                    print(f"Found {len(elements)} product listings on the new page.")

                except Exception as e:
                    logging.error(f"An error occurred while navigating to the next page: {e}")
         
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        
        finally:
            self.driver.quit()
            
ScrapeAutohub('https://www.sellcarauction.co.kr/newfront/login.do').start_logging_in()


# urls =read_autohub_file(AUTOHUB_JSON_URLS)
# ScrapeUrls(urls['car_urls'],f'autohub/autuhub_data/detailed_file/autohub_detail_data_{TODAY}','con_top').scrap_autohub_chunks_async(max_concurrency=5)


