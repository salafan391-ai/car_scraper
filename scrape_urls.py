import aiohttp
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
import async_timeout
from tqdm import tqdm
from datetime import date
TODAY=date.today()
class ScrapeUrls:
    def __init__(self,input_file,output_file,target_class):
        self.urls = input_file
        self.output_text_file = output_file
        self.target_class=target_class
        asyncio.run(self.scrap_autohub_chunks_async(max_concurrency=5))
    async def fetch_car_detail(self,session, url, semaphore, progress_bar,retries=3, delay=1):
        """Fetch car detail with retry and concurrency limit."""
        async with semaphore:
            for attempt in range(retries):
                try:
                    # Set a timeout for the request
                    async with async_timeout.timeout(30):  # Timeout after 10 seconds
                        async with session.get(url, ssl=False) as response:
                            html = await response.text()
                            # Parse the HTML to extract the car detail
                            soup = bs(html, 'html.parser')
                            car = soup.find(class_=self.target_class)
                            if car:
                                return str(car)  # Return the car detail as string
                            return "No car detail found"  # Fallback for missing details
                except aiohttp.ClientError as e:
                    # Retry on client errors (e.g., server disconnects)
                    print(f"Attempt {attempt + 1} failed for {url}: {e}")
                    if attempt + 1 == retries:
                        return f"Failed to fetch {url} after {retries} attempts"
                    await asyncio.sleep(delay)  # Delay before retrying
                finally:
                    progress_bar.update(1)  # Update the progress bar for each completed task

    async def scrap_autohub_chunks_async(self, max_concurrency=5):
        # Limit concurrency with a semaphore
        semaphore = asyncio.Semaphore(max_concurrency)

        async with aiohttp.ClientSession() as session:
            # Create a progress bar
            with tqdm(total=len(self.urls), desc="Fetching car details", unit="car") as pbar:
                tasks = []
                for url in self.urls:
                    task = self.fetch_car_detail(session, url, semaphore, pbar)  # Pass progress bar to the function
                    tasks.append(task)

                # Run all tasks concurrently
                results = await asyncio.gather(*tasks)

            # Write the results to the file
            with open(f"{self.output_text_file}.txt", 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(str(result) + '\n')
