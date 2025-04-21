import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime,date
import pandas as pd
from .comparison import *

TODAY=date.today()


def capture_element_html(url, selector, file):
    options = Options()
    options.add_argument("--headless")  # Run headless Chrome
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("disable-infobars")  # Disable infobars
    options.add_argument("--disable-extensions")  # Disable extensions

    service = Service()  # Specify the path to your chromedriver if needed

    try:
        # Create a new instance of the Chrome driver
        with webdriver.Chrome(service=service, options=options) as driver:
            driver.implicitly_wait(10)  # Set an implicit wait
            driver.get(url)
            element = driver.find_element(By.CSS_SELECTOR, selector)
            html_content = element.get_attribute('outerHTML')
            



            # Write the HTML content to the file
            file.write(f"HTML content for {url}:\n{html_content}\n\n")

    except NoSuchElementException:
        file.write(f"Element not found for selector: {selector} in {url}\n")
    except TimeoutException:
        file.write(f"Timeout while fetching {url}\n")
    except Exception as e:
        file.write(f"Error fetching {url}: {e}\n")

def scrap_autohub_chunks_async(urls, selector, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:  # Open the output file
        with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your needs
            futures = {executor.submit(capture_element_html, url, selector, file): url for url in urls}
            for i,future in enumerate(futures):
                url = futures[future]
                try:
                    future.result()  # Wait for the result (if needed)
                    print(f"{i} of {len(urls)}: Successfully processed {url}")
                except Exception as e:
                    file.write(f"Error processing {url}: {e}\n")
file_path=f'autohub/autuhub_data/autohub_urls/autohub_urls_2025-04-15.json'
with open(file_path) as j:
    urls = json.load(j)['car_urls']
# with open(f'autohub/autuhub_data/final_json/detail_json_mnaf_2025-04-08.json') as j:
#     data = json.load(j)
#     print(len(data))
# df_urls = pd.DataFrame(urls)
# df_urls = df_urls[df_urls['entries']!='']
# df_data = pd.DataFrame(data)
# scrapped = df_urls[df_urls['entries'].isin(df_data['entry'])]['car_urls'].tolist()
# print(len(scrapped))
# def check_urls(*file_path):

#     for i in file_path:
#         with open(i) as j:
#             urls = json.load(j)['car_urls']
#             print(len(urls)) 

# check_urls(file_path,'autohub/autuhub_data/autohub_urls/autohub_urls_2024-12-04.json')
# data_path = f'autohub/autuhub_data/autohub_urls/autohub_urls_2024-12-10.json'
# with open(data_path) as j:
#     lst = json.load(j)
# with open(file_path) as j:
#     ids = json.load(j)

# urls =[]    
# for i in ids:
#     for n in lst:
#         if i['ids'] not in n['car_ids']:
#             print(i['car_urls'])

# unscraped = []
# for i,u in zip(ids['ids'],ids['car_urls']):
#     if i not in [n['car_ids'] for n in lst]:
#         unscraped.append(u)
# print(len(unscraped))

            
# from .test import unscraped_urls
# df = pd.read_csv(file_path)
# urls = df['urls'].tolist()[63:]
# file_path=f'autohub/autuhub_data/autohub_urls/autohub_urls_2025-01-14.json'
# with open(file_path) as j:
#     url = json.load(j)
# urls=[i for i in url['car_urls']]
# print(len(urls[794:]))
selector = '.con_top'  # Adjust this selector based on your needs
output_file = f'autohub/autuhub_data/detailed_file/autohub_data_{TODAY}korcars.txt'  # Specify the output file name

# # # # Run the scraping function
# urls = get_unscrapped()
scrap_autohub_chunks_async(urls, selector, output_file)


