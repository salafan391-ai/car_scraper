import aiohttp
import asyncio
import json
import os
from io import BytesIO
from urllib.parse import urlparse, unquote
from aiobotocore.session import get_session
from datetime import date
from asyncio import Semaphore
from tqdm.asyncio import tqdm
import aiofiles  # For async file operations

TODAY = date.today()

# Cloudflare R2 credentials
R2_ENDPOINT = "https://5f609be3294e42fbcada608b624a1c95.r2.cloudflarestorage.com"
R2_ACCESS_KEY_ID = "f00521a9030766502ffdd53ac571f715"
R2_SECRET_ACCESS_KEY = "7fb9715d627bca69754202ce9d6cd3a63399f75641ab33e1a76e3ffc2aa1ff03"
R2_BUCKET_NAME = "ahmedcars2"

PUBLIC_R2_URL = "https://pub-62ea30bab63244a882fdd29aafc7fe26.r2.dev"

# **Lower concurrency to avoid overloading the server**
MAX_CONCURRENT_UPLOADS = 50  
semaphore = Semaphore(MAX_CONCURRENT_UPLOADS)

session = get_session()

def sanitize_filename(image_url):
    """Sanitize and create filename"""
    parsed_url = urlparse(image_url)
    filename = unquote(os.path.basename(parsed_url.path))
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in filename) + ("" if "." in filename else ".jpg")

async def upload_to_r2(client, image_data, folder, filename):
    """Uploads image to Cloudflare R2 with retries"""
    s3_key = f"{folder}/{filename}"
    max_retries = 3

    for attempt in range(max_retries):
        try:
            async with semaphore:
                await client.put_object(Bucket=R2_BUCKET_NAME, Key=s3_key, Body=image_data)
            return f"{PUBLIC_R2_URL}/{s3_key}"
        except Exception as e:
            print(f"⚠️ Retry {attempt+1}: Upload error {filename}: {e}")
            await asyncio.sleep(2 ** attempt)  # **Exponential backoff**

    print(f"❌ Failed to upload {filename}")
    return None

async def fetch_and_upload_image(client, session, car_id, image_url, progress_bar, failed_urls):
    """Downloads and uploads image asynchronously with smart retries"""
    filename = sanitize_filename(image_url)
    max_retries = 3
    timeout = aiohttp.ClientTimeout(total=20)  # **Increased timeout**

    try:
        async with session.get(image_url, timeout=timeout) as response:
            if response.status == 200:
                image_data = await response.read()
                url = await upload_to_r2(client, image_data, car_id, filename)
                if url:
                    progress_bar.update(1)
                return url
            elif response.status == 404:
                print(f"❌ 404 Not Found: {image_url}")
                failed_urls.append(image_url)  # Log failed URL
            else:
                print(f"❌ Failed {image_url}: HTTP {response.status}")
    except asyncio.TimeoutError:
        print(f"⚠️ Timeout: {image_url} (retrying)")
        await asyncio.sleep(2 ** max_retries)
    except asyncio.CancelledError:
        print(f"⚠️ Task cancelled: {image_url}")
        return None
    except Exception as e:
        print(f"⚠️ Error fetching {image_url}: {e}")
        failed_urls.append(image_url)  # Log failed URL

    return None

async def save_failed_images(failed_images):
    """Save failed images asynchronously"""
    async with aiofiles.open(f"failed_uploads_{TODAY}.json", "w") as f:
        await f.write(json.dumps(failed_images, indent=2))

async def process_images(file_path):
    """Process all images asynchronously"""
    with open(file_path) as j:
        data = json.load(j)

    all_images = [(car['car_ids'], url) for car in data for url in car.get('images', [])]
    total_images = len(all_images)

    async with session.create_client(
        "s3",
        region_name="auto",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY
    ) as client, aiohttp.ClientSession() as http_session:  

        failed_images = []
        with tqdm(total=total_images, desc="Uploading Images", unit="img") as progress_bar:
            tasks = [fetch_and_upload_image(client, http_session, car_id, url, progress_bar, failed_images) for car_id, url in all_images]
            uploaded_urls = await asyncio.gather(*tasks, return_exceptions=True)

        uploaded_urls = [url for url in uploaded_urls if url]
        if failed_images:
            print(f"🔁 Retrying {len(failed_images)} failed images...")
            await save_failed_images(failed_images)

    print(f"🚀 Total uploaded: {len(uploaded_urls)} images (out of {total_images})")
    if failed_images:
        print(f"❌ Failed images saved in failed_uploads_{TODAY}.json")

asyncio.run(process_images(f'lotte/lotte_final_json/detailed_json_{TODAY}mnaf.json'))
