import json
import requests
import aiohttp
import asyncio
import json

with open('autobell/autobell_data/final_json/detail_json_2025-04-10.json') as j:
    car_data = json.load(j)

images = [car['inspection_image'] for car in car_data]


# with open('/Users/amd/my_scrapping/autobell/autobell_data/final_json/detail_json_2025-03-06korcars_last.json') as j:
#     data=json.load(j)
# images=[car['inspection_image'] for car in data]
async def fetch_status(session, url):
    async with session.get(url) as response:
        print(response.status)

async def main():
    
    urls = [image.split("'")[3] for image in images]  # Extract URLs

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, url) for url in urls]
        await asyncio.gather(*tasks)

asyncio.run(main())
