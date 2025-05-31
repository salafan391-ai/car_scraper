import json
import asyncio
import aiohttp
from pathlib import Path
from tqdm import tqdm  # Import tqdm for progress bars
from datetime import date

TODAY = date.today()


def get_onload_images(id):
    images = []
    id_part1, id_part2, id_part3, id_part4 = id  # Unpack for readability
    
    # Generate URLs for the first set of images (_02_)
    for count in range(1, 33):  # From 1 to 32 inclusive
        padded_count = f"{count:02}"  # Zero-pad the count
        images.append(
            f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
            f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_{padded_count}.jpg%3F{id_part4}01"
            f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
        )
    
    # Generate URLs for the second set of images (_02_99_)
    for count in range(1, 14):  # From 1 to 14 inclusive
        padded_count = f"{count:02}"  # Zero-pad the count
        images.append(
            f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
            f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_99_{padded_count}.jpg%3F{id_part4}01"
            f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
        )
    return images


def parse_ids(image):
    try:
        id = image.split('2F')[4]
        id1 = image.split('2F')[-1].split('.')[0][:-6]
        id2 = image.split('3F')[-1].split('&')[0]
        id0 = id1[1:5]
        return (id, id0, id1, id2)
    except IndexError:
        return None


async def check_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return url
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return None


async def main(images, progress_bar):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for image in images:
            tasks.append(check_url(session, image))
            progress_bar.update(1)  # Update progress bar for each URL queued
        results = await asyncio.gather(*tasks)
        return [url for url in results if url]


def run_checker(images):
    with tqdm(total=len(images), desc="Checking URLs", unit="url") as progress_bar:
        return asyncio.run(main(images, progress_bar))


# Paths
input_path = Path(f'autobell/autobell_data/final_json/detail_json_{TODAY}.json')
output_path = Path(f'autobell/autobell_data/final_json/detail_json_{TODAY}mnaf.json')

# Load data
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data = [car for car in data if car['year'] >= 2010]
data = [car for car in data if car['price'] != '1']

car_ids = set([car['car_ids'] for car in data if 'car_ids' in car])
data = [car for car in data if 'car_ids' in car]
data = [car for car in data if car['car_ids'] in list(car_ids)]
for count,car in enumerate(data):
    try:
        print(count)
        print(car['car_ids'])
    except Exception as e:
        print(e)
        continue


# Process data with progress bar
with tqdm(total=len(data), desc="Processing Items", unit="item") as overall_progress:
    for i in data:
        ids = parse_ids(i['image'])
        if ids:
            images = get_onload_images(ids)
            i['images'] = run_checker(images)
        overall_progress.update(1)  # Update overall progress bar for each item

# Save updated data
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
