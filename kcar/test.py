import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import json
import pandas as pd



def read_kcar_urls(lane):
    with open(f'/Volumes/ahmed/car_auction_data/kcar/json_urls/kcar_{TODAY}{lane}.json') as j:
        data=json.load(j)
    return data

def successful_scrapes(urls):
    with open(f'kcar/kcar_data/detailed_file/kcar_successful_scrapes{TODAY}.json', 'w', encoding='utf-8') as f:
        json.dump(urls,f,ensure_ascii=False,indent=4)
def unsuccessful_scrapes(urls):
    with open(f'kcar/kcar_data/detailed_file/kcar_unsuccessful_scrapes{TODAY}.json', 'w', encoding='utf-8') as f:
        json.dump(urls,f,ensure_ascii=False,indent=4)
df = pd.read_csv('/Users/amd/Downloads/alfaqih_auction - sheet1 (13).csv')
df = df[df['رقم الاعلان'].notna()]
# df = df[df['رقم الاعلان'].notna() & df['المزاد '] == 'k car']
df['رقم الاعلان'] = df['رقم الاعلان'].astype(int)

TODAY = date.today()
successful_scrape = []
unsuccessful_scrape = []
# Function to handle a single URL
def scrape_url(url):
    
    try:
        # Initialize WebDriver (use options for faster scraping)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Optional: Headless mode for speed
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        # Wait for the alert (if it appears) and accept it
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"Handling alert on {url}: {alert.text}")
            alert.accept()
        except Exception as e:
            print(f"No alert on {url}: {e}")

        # Wait for a specific element to ensure the page has loaded
        try:
            # Replace 'element_locator' with the actual identifier for the target element
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sel_option"))  # Adjust locator as needed
            )
            print(f"Page fully loaded for {url}.")
            successful_scrape.append(url)
        except Exception as e:
            print(f"Page might not have fully loaded for {url}: {e}")
            unsuccessful_scrape.append(url)

        # Alternatively, use a short sleep to ensure the page finishes loading
        time.sleep(5)

        # Scrape the content
        page_content = driver.page_source
        print(f"Scraped {url} successfully.")

        # Clean up
        driver.quit()
        return f"URL: {url}\n{page_content}\n{'-'*80}\n"  # Format content
    except Exception as e:
        unsuccessful_scrape.append(url)
        print(f"Error scraping {url}: {e}")
        
        return f"URL: {url}\nERROR: {e}\n{'-'*80}\n"

    finally:
        successful_scrapes(successful_scrape)
        unsuccessful_scrapes(unsuccessful_scrape)

a,b = read_kcar_urls('A'),read_kcar_urls('B')
df_a,df_b = pd.DataFrame(a),pd.DataFrame(b)
combined_df = pd.concat([df_a,df_b],ignore_index=True)
urls = combined_df['car_urls'].to_list()
combined_df['entries']=combined_df['entries'].str.split('(').str[0]
combined_df['entries']=combined_df['entries'].str.strip()
urls = combined_df[combined_df['entries'].isin(df['رقم الاعلان'].astype(str))]['car_urls'].to_list()
print(f"Total URLs to scrape: {len(urls)}")

# Use ThreadPoolExecutor for concurrent scraping
def scrape_urls(urls):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust workers for your system
        results = list(executor.map(scrape_url, urls))

    end_time = time.time()
    print(f"Scraped {len(urls)} URLs in {end_time - start_time:.2f} seconds.")

    # Write all results to a single text file
    with open(f"/Volumes/ahmed/car_auction_data/kcar/text_data/alfaqih_data{TODAY}.txt", "a", encoding="utf-8") as f:
        f.writelines(results)

    print(f"Data saved to /Volumes/ahmed/car_auction_data/kcar/text_data/alfaqih_data{TODAY}.txt")
# scrape_urls(urls)
with open(f'kcar/kcar_data/detailed_file/kcar_unsuccessful_scrapes{TODAY}.json') as j:
    unsuccessfull_urls = json.load(j)

print(len(unsuccessfull_urls))
# # with open(f'/Users/amd/Desktop/my_scrapping/kcar/kcar_data/detailed_file/kcar_successful_scrapes{TODAY}.json') as j:
# #     successful_urls = json.load(j)

# # print(len(unsuccessfull_urls))

# # while len(unsuccessfull_urls) > 0:
scrape_urls(unsuccessfull_urls)