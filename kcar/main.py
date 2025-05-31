from scrape import Scrape
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import math
import logging
from dotenv import load_dotenv
import json
from datetime import date
from scrape_urls import ScrapeUrls
# from .parsing_kcar import *
# from autohub.autohub_scraper import scrap_autohub_chunks_async



def read_urls(lane):
    with open(f'/Volumes/ahmed/car_auction_data/kcar/json_urls/kcar_{TODAY}{lane}.json') as j:
        return json.load(j)



LANE = 'B'

# load_dotenv()
USERNAME ='KCAR_USERNAME'
PASSWORD ='KCAR_PASSWORD'
TODAY = date.today()
JSON_URLS = f'/Volumes/ahmed/car_auction_data/kcar/json_urls/kcar_{TODAY}{LANE}.json'
class ScrapKcar(Scrape):
    def __init__(self, url):
        super().__init__(url)
        self.car_urls = []
        self.car_ids = []
        self.entries=[]
    def start_logging_in(self):
        try:
            self.login('tradebull24','Adnan0290$',"user_id","user_pw")
            # Implicitly wait for elements to be present

            # Click the agree button
            agree_button = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[@onclick=\"encar.fnAgreeBid('Y');\"]")))
            agree_button.click()

            # Navigate to the weekly auction page
            
            weekly_auction_link = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[@href='/kcar/auction/weekly_auction/colAuction.do?PAGE_TYPE=wCfm&LANE_TYPE=A']")))
            weekly_auction_link.click()

            total = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "all03")))
            total = total.text
            tot = (math.ceil(int(total)/18))
            print('number of pages',tot)
            for page_number in range(1,tot+1):  # Adjust range if needed
                print('page',page_number,'scraped successfully')
                page_url = f"https://www.kcarauction.com/kcar/auction/weekly_auction/colAuction.do?PAGE_TYPE=wCfm&LANE_TYPE={LANE}#{page_number}"
                self.driver.get(page_url)
                
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )

                # Wait for a specific element to confirm the page is ready
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "listbox"))
                )
                time.sleep(3)

                # Scroll down to load more content if necessary (optional)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for any lazy loaded elements to appear
                time.sleep(3)
                # Scrape car listings
                car_listings = self.driver.find_elements(By.CLASS_NAME, "listbox")
                count=0
                for car in car_listings:
                    try:
                        car_id = car.find_element(By.TAG_NAME, "a")
                        entry = car.find_element(By.TAG_NAME, "table").text
                        self.entries.append(entry.split('\n')[4].split()[1])
                        id1 = car_id.get_attribute('id').replace('CAR_','')
                        id2 = car_id.get_attribute('href').split(',')[1].replace("'",'')
                        self.car_urls.append(f'https://www.kcarauction.com/kcar/auction/weekly_detail/auction_detail_view.do?PAGE_TYPE=wCfm&CAR_ID={id1}&AUC_CD={id2}')
                        self.car_ids.append(car_id.get_attribute('id'))
                        self.write_to_json(ids=self.car_ids,entries=self.entries,car_urls=self.car_urls)
                        count+=1
                        print(count,id1,id2)
                    except Exception as e:
                        logging.error(f"An error occurred while processing car listing: {e}")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        
        finally:
            self.driver.quit()
    def write_to_json(self,*args,**kwargs):
        data=kwargs
        with open(JSON_URLS, 'w', encoding='utf-8') as file:
            d= json.dumps(data,ensure_ascii=False,indent=4)
            file.write(d)
if __name__ == '__main__':
    # pass
    # ScrapKcar('https://www.kcarauction.com/kcar/user/user_login.do').start_logging_in()
    urls = []
    for i in ['A','B']:
        with open(f'/Volumes/ahmed/car_auction_data/kcar/json_urls/kcar_{TODAY}{LANE}.json') as j:
            urls.extend(read_urls(i)['car_urls'])
    # print(len(urls))
    # with open(f'/Volumes/ahmed/car_auction_data/kcar/json_urls/kcar_{TODAY}{LANE}.json') as j:
    #         urls.extend(read_urls(LANE)['car_urls'])
    ScrapeUrls(set(urls),f'/Volumes/ahmed/car_auction_data/kcar/text_data/kcar_detail_data_{TODAY}','detail_carbox')
    # # KcarParsing().parsing_details()
    








    # file_path =f'kcar/kcar_data/kcar_urls/kcar_2025-01-08A.json'
    # with open(file_path) as j:
    #     url = json.load(j)
    # selector = '.sel_option'  # Adjust this selector based on your needs
    # output_file = f'kcar/kcar_data/detailed_file/kcar_data_{TODAY}.txt'  # Specify the output file name
    # print(len(url['car_urls'][:10]))
    # # Run the scraping function

    # scrap_autohub_chunks_async(url['car_urls'][:10], selector, output_file)

