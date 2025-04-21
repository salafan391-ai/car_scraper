from playwright.sync_api import sync_playwright
import json
from datetime import date
from random import choice,choices
import pandas as pd
from datetime import datetime, date

TODAY = date.today()


# df = pd.read_csv('/Users/amd/Downloads/alfaqih_auction - sheet1 (3).csv')
# entries = [int(i) for i in df['رقم الاعلان'].to_list()]
def parse_cookie_string(cookie_string):
    """Convert a cookie string into a list of dictionaries."""
    cookies = []
    for item in cookie_string.split('; '):
        name, value = item.split('=', 1)
        cookies.append({
            'name': name,
            'value': value,
            'domain': '.autobell.co.kr',  # Replace with the actual domain
            'path': '/',  # Use the appropriate path if needed
        })
    return cookies

def scrape_pages(page_urls, cookie_string):
    """Scrape multiple pages efficiently."""
    cookies = parse_cookie_string(cookie_string)

    with sync_playwright() as p:
        # Launch the browser in headless mode for efficiency
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Add cookies to the browser context
        context.add_cookies(cookies)

        # Open a new page
        page = context.new_page()

        for url in page_urls:
            print(f"Scraping {url}...")
            page.goto(url, wait_until='domcontentloaded')

            # Wait for specific content to load if necessary (e.g., a table or unique element)
            page.wait_for_selector(".exhibit-detail")  # Adjust selector to match your target content

            # Extract the page content or specific data
            content = page.content()  # Example: Get the entire page content
            with open(f'autobell/autobell_data/detailed_file/text_data{date.today()}.txt','a') as f:
                f.write(content)  # Print the first 500 characters for preview (optional)

        # Close the browser after all pages are scraped
        browser.close()

# Define your list of page URLs
# with open('autobell/autobell_data/final_json/detail_json_2025-01-13.json') as j:
#     urls = json.load(j)
# for i in urls:
#     print(i['entry'],i['url'])
# urls = [i['url'] for i in urls if int(i['entry']) in entries]
 # Example IDs; adjust based on your logic
df = pd.read_csv('/Users/amd/Downloads/alfaqih_auction - sheet1 (15).csv')
with open(f'autobell/autobell_data/final_json/detail_json_{TODAY}.json') as j:
    urls = json.load(j)
entries = df['رقم الاعلان'].astype(int).to_list()
urls=[i['url'] for i in urls if int(i['entry']) in entries]
urls = set(urls)
print(len(urls))
cookie_string = "SCOUTER=x31m2n6hli4im5; _ga=GA1.1.1629691538.1743128576; JSESSIONID=BxPs8BxaMQhmyPtavsOuUz2HizVRPMfZ1Jem2Sr3wSgco4CulZpsrKYFQNQYiANd.QXV0b0F1Y3Rpb24vQXV0b0F1Y3Rpb24x; _ga_H9G80S9QWN=GS1.1.1744889653.4.1.1744889664.0.0.0"
# Start scraping
scrape_pages(urls, cookie_string)
