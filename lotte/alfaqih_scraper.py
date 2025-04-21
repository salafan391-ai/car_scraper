import asyncio
from playwright.async_api import async_playwright
import json
from datetime import date

TODAY = date.today()

# Load URLs from the JSON file
with open('lotte/alfaqih_urls/lotte_urls2025-04-19.json') as j:
    URLS = json.load(j)
print(f"Total URLs to scrape: {len(URLS)}")

# Convert cookie string into a list of cookie dictionaries
cookie_string = "_xm_webid_1_=2118497742; JSESSIONID=4v15LXzbQ4KyeM1Keohcr6XBUrZNGgq8EL0c5ptIraSPxwcTlDxYC3zv27qdWK0x.UlBBQV9kb21haW4vUlBBQV9IUEdfTjIx; _gid=GA1.2.1965936448.1745080102; _fbp=fb.1.1745080102606.642262274743026894; _gat_gtag_UA_118654321_1=1; _ga_BG67GSX5WV=GS1.1.1745080102.1.1.1745081323.60.0.0; _ga=GA1.1.1059866457.1745080102"
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
        filename = f"/Users/amd/Desktop/my_scrapping/lotte/lotte_detailed_data/text_data_{TODAY}.txt"
        with open(filename, "a", encoding="utf-8") as f:
            for index, url, outer_html in sorted(results):
                f.write(f"URL: {url}\n{outer_html}\n\n")

        await browser.close()

asyncio.run(scrape())