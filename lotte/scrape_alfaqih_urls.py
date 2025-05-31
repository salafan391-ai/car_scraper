import asyncio
from playwright.async_api import async_playwright
import json
from datetime import date

TODAY = date.today()

# Load URLs from the JSON file
with open(f'lotte/alfaqih_urls/lotte_urls{TODAY}.json') as j:
    URLS = json.load(j)
print(f"Total URLs to scrape: {len(URLS)}")

# Convert cookie string into a list of cookie dictionaries
cookie_string = "_xm_webid_1_=-763447611; _gid=GA1.2.1890055873.1742654067; _fbp=fb.1.1742654066756.458465544999261234; JSESSIONID=m5Bu4k0iTM6aHdi2i9gQyQYA1airSQB5VON1Fbgok5m8nc71vBxtN26yOYP1dI7M.UlBBQV9kb21haW4vUlBBQV9IUEdfTjEx; _ga_BG67GSX5WV=GS1.1.1742666714.3.1.1742669114.4.0.0; _ga=GA1.1.1717660428.1742654067"
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
        browser = await p.chromium.launch(headless=False)  # Set to True for headless mode
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
