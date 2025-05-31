import json
import aiohttp
import asyncio
from typing import List, Optional, Tuple

from datetime import datetime
TODAY = datetime.now().date().strftime("%Y-%m-%d")


def get_images(id):
    images = []
    id_part1, id_part2, id_part3, id_part4 = id  # Unpack for readability
    
    # Generate URLs for the first set of images (_02_)
    for count in range(2, 33):  # From 1 to 32 inclusive
        padded_count = f"{count:02}"  # Zero-pad the count
        images.append(
            f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
            f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_{padded_count}.jpg%3F{id_part4}01"
            f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
        )
    return images
# def get_onload_images(id,length):
#     images = []
#     id_part1, id_part2, id_part3, id_part4 = id  # Unpack for readability
    
#     # Generate URLs for the first set of images (_02_)
#     for count in range(1, 33):
#         print(length)  # From 1 to 32 inclusive
#         padded_count = f"{count:02}"  # Zero-pad the count
#         images.append(
#             f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
#             f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_{padded_count}.jpg%3F{id_part4}01"
#             f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
#         )
#     return images
async def get_onload_images(session: aiohttp.ClientSession, id: Tuple[str, str, str, str]) -> List[str]:
    images = []
    id_part1, id_part2, id_part3, id_part4 = id  # Unpack for readability
    
    # Generate URLs for the second set of images (_02_99_)
    for count in range(1, 14):  # From 1 to 14 inclusive
        padded_count = f"{count:02}"  # Zero-pad the count
        image_url = (
            f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
            f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_99_{padded_count}.jpg%3F{id_part4}01"
            f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
        )
        if await check_image_validity(session, image_url):
            images.append(image_url)
    return images

def parse_ids(image: str) -> Optional[Tuple[str, str, str, str]]:
    try:
        id = image.split('2F')[4]
        id1 = image.split('2F')[-1].split('.')[0][:-6]
        id2 = image.split('3F')[-1].split('&')[0]
        id0 = id1[1:5]
        return (id, id0, id1, id2)
    except IndexError:
        return None

async def check_image_validity(session: aiohttp.ClientSession, url: str) -> bool:
    try:
        async with session.get(url) as response:
            return response.status == 200
    except:
        return False

async def process_car(session: aiohttp.ClientSession, car: dict) -> dict:
    car_id = car.get('car_ids', 'unknown')
    print(f"\nProcessing car ID: {car_id}")
    
    id = parse_ids(car['image'])
    if not id:
        print(f"❌ Could not parse image URL for car {car_id}")
        car['images'] = []
        return car
        
    id_part1, id_part2, id_part3, id_part4 = id
    
    # Try _02_99_ pattern in sequence
    for count in range(1, 14):  # From 1 to 14 inclusive
        padded_count = f"{count:02}"  # Zero-pad the count
        image_url = (
            f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
            f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_99_{padded_count}.jpg%3F{id_part4}01"
            f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
        )
        
        if await check_image_validity(session, image_url):
            print(f"✅ Found valid image for car {car_id}")
            images = await get_onload_images(session, id)
            checked_images = get_images(parse_ids(car['image']))
            car['images'] = checked_images[:-len(images)]+images
            print(f"📸 Found {len(images)} onload images for car {car_id}")
            return car
        else:
            car['images'] = get_images(parse_ids(car['image']))
            print(f"❌ Image not found for car {car_id} (attempt {count}/13)")
    
    print(f"⚠️ No valid images found for car {car_id} after all attempts")
    car['onload_images'] = []
    return car

async def main():
    with open(f'autobell/autobell_data/final_json/detail_json_{TODAY}.json', 'r') as f:
        data = json.load(f)

    total_cars = len(data)
    print(f"\nStarting to process {total_cars} cars...")

    async with aiohttp.ClientSession() as session:
        tasks = [process_car(session, car) for car in data]
        processed_data = await asyncio.gather(*tasks)

    # Count results
    # cars_with_images = sum(1 for car in processed_data if car['images'])
    # cars_without_images = sum(1 for car in processed_data if not car['images'])
    
    print(f"\nProcessing complete!")
    print(f"Total cars processed: {total_cars}")
    # print(f"Cars with images: {cars_with_images}")
    # print(f"Cars without images: {cars_without_images}")

    with open(f'/Volumes/ahmed/car_auction_data/autobell/jsion_data/dtailed_data{TODAY}.json', 'w') as j:
        json.dump(processed_data, j, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
    
    
