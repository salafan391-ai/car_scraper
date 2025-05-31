import asyncio
from playwright.async_api import async_playwright
import json
from datetime import date

TODAY = date.today()

# Load URLs from the JSON file
with open('lotte/alfaqih_urls/lotte_urls2025-05-31.json') as j:
    URLS = json.load(j)
print(f"Total URLs to scrape: {len(URLS)}")

# Convert cookie string into a list of cookie dictionaries
cookie_string = "_xm_webid_1_=-1443678628; _fbp=fb.1.1748082597577.778086543926488001; _gid=GA1.2.1164039495.1748686964; JSESSIONID=crNCVKeokIOEkxj6vRS5CUAXqTI3LiKifYidWH1YCxMsfi99lra7WBvu22TZIiY2.UlBBQV9kb21haW4vUlBBQV9IUEdfTjEx; _gat_gtag_UA_118654321_1=1; _ga_BG67GSX5WV=GS2.1.s1748686964$o5$g1$t1748690964$j33$l0$h0; _ga=GA1.1.2045754007.1748082597"
cookies = [
    {
        "name": item.split("=")[0].strip(),
        "value": item.split("=")[1].strip(),
        "domain": "www.lotteautoauction.net",
        "path": "/"
    }
    for item in cookie_string.split(";")
]

# Limit the number of concurrent requests
CONCURRENCY_LIMIT = 5

async def scrape_page(context, url, index):
    try:
        page = await context.new_page()
        print(f"Scraping URL {index+1}/{len(URLS)}: {url}")

        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_selector(".exhibited-vehicle", timeout=30000)

        # Extract outer HTML of the `.exhibited-vehicle` element
        outer_html = await page.locator(".exhibited-vehicle").evaluate("el => el.outerHTML")
        print(f"Scraped {url}: {outer_html[:100]}...")  # Print first 100 chars

        await page.close()
        return (index, url, outer_html)

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return (index, url, f"Error: {e}")

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set to True for headless mode
        context = await browser.new_context()

        # Add cookies to the context
        await context.add_cookies(cookies)

        # Use a semaphore to control concurrency
        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

        async def limited_scrape(url, index):
            async with semaphore:
                return await scrape_page(context, url, index)

        # Launch all tasks and preserve order
        tasks = [limited_scrape(url, index) for index, url in enumerate(URLS)]
        results = await asyncio.gather(*tasks)

        # Save the results to a TXT file in the original order
        filename = f"lotte/lotte_detailed_data/text_data_{TODAY}.txt"
        with open(filename, "a", encoding="utf-8") as f:
            for index, url, outer_html in sorted(results):
                f.write(f"URL: {url}\n{outer_html}\n\n")

        await browser.close()

asyncio.run(scrape())