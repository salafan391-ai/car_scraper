from scrape import Scrape
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from .lotte_parser import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

load_dotenv()
TODAY=date.today()

class ScrapeLotte(Scrape):
    def __init__(self, url):
        super().__init__(url)
        self.count=0
        # Set up the WebDriver path and download folder
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": "/Users/amd/my_scrapping/lotte/lotte_detailed_data",  # Change to your desired download path
            "download.prompt_for_download": False,
            "directory_upgrade": True
        })
        self.driver = webdriver.Chrome(service=Service(),options=chrome_options)

    def start_logging_in(self):
        self.login('LOTTE_USERNAME','LOTTE_PASSWORD',"userId","userPwd")

        # Wait for login to complete
        self.driver.implicitly_wait(10)

        # Navigate to the target page
        self.driver.get("https://www.lotteautoauction.net/hp/cmm/actionMenuLinkPage.do?baseMenuNo=1010000&link=forward%3A%2Fhp%2Fauct%2Fmyp%2Fentry%2FselectMypEntryList.do&redirectMode=&popHeight=&popWidth=&subMenuNo=1010200&subSubMenuNo=")

        # Wait for the page to load
        self.driver.implicitly_wait(10)
        self.__main_loop()

        # Scrape the car descriptions
    def __scrape_flex_wrap_elements(self):
        length = self.driver.find_element(By.CLASS_NAME,'total-carnum')
        print(length.text.split())
       
        car_elements = self.driver.find_elements(By.CLASS_NAME, "tbl-t02")
        for car_element in car_elements:
            try:
                with open(f'lotte/lotte_detailed_data/detailed_{TODAY}.txt','a',encoding='utf-8') as file:
                    features = car_element.get_attribute('outerHTML')
                    file.write(features)
                    file.write("-" * 80+'\n')  # Separator between elements
            except Exception as e:
                print("Error while scraping:", e)
        

        # Function to navigate through numbered pages
    def __navigate_through_page_numbers(self):
        page_numbers=[]
                # Select "View 100 at a time" from the dropdown
        select_element = self.driver.find_element(By.ID, "recordCount")
        select = Select(select_element)
        select.select_by_value("100")  # Select the option with value "100"
        time.sleep(2)  # Give some time for the page to update

        while True:
            self.__scrape_flex_wrap_elements()

            try:
                # Find the current page element (active page with 'on' class)
                current_page = self.driver.find_element(By.CSS_SELECTOR, "a.on")
                current_page_number = int(current_page.text)

                # Find all page number links within the pagination span
                page_links = self.driver.find_elements(By.CSS_SELECTOR, "div.pagination span a")

                # Initialize the next_page variable
                next_page = None

                # Loop through the page links to find the next page
                for page_link in page_links:
                    if int(page_link.text) > current_page_number:
                        next_page = page_link
                        page_numbers.append(int(next_page.text))
                        break

                # If a next page is found, click on it
                if next_page:
                    next_page.click()
                    time.sleep(2)  # Adjust sleep time as needed
                else:
                    # Check if the next page button exists and is enabled
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "a.btn-next")
                    print(next_button.text)
                    if "disabled" not in next_button.get_attribute("class"):
                        next_button.click()
                        time.sleep(2)  # Adjust sleep time as needed
                    else:
                        break  # No more pages, exit the loop

            except Exception as e:
                print("No more page links or error encountered:", e)
                break
    def __main_loop(self):

        # Main loop to handle both page numbers and the "Next" button
        while True:
            self.__navigate_through_page_numbers()

            try:
                # Find and click the "Next" button if it exists
                next_button = self.driver.find_element(By.CLASS_NAME, "btn_next")
                if next_button.is_enabled():
                    next_button.click()
                    time.sleep(2)  # Wait for the next set of pages to load
                else:
                    break  # Exit the loop if the "Next" button is not enabled
            except Exception as e:
                print("No more pages to scrape or error encountered:", e)
                break
        # Close the browser
        self.driver.quit()

# ScrapeLotte("https://www.lotteautoauction.net/hp/auct/cmm/viewLoginUsr.do?loginMode=redirect").start_logging_in()
LotteParsing().parsing_detail()
