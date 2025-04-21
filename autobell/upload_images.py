import boto3
import requests
from botocore.client import Config
from io import BytesIO
from urllib.parse import urlparse, unquote
import os
from concurrent.futures import ThreadPoolExecutor
import json

# Cloudflare R2 credentials
R2_ENDPOINT = "https://5f609be3294e42fbcada608b624a1c95.r2.cloudflarestorage.com"
R2_ACCESS_KEY_ID = "f00521a9030766502ffdd53ac571f715"
R2_SECRET_ACCESS_KEY = "7fb9715d627bca69754202ce9d6cd3a63399f75641ab33e1a76e3ffc2aa1ff03"
R2_BUCKET_NAME = "ahmedcars"

s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto",
)

def sanitize_filename(image_url, num):
    """Generate unique filename with position prefix"""
    parsed_url = urlparse(image_url)
    filename = unquote(os.path.basename(parsed_url.path))
    clean_filename = "".join(c if c.isalnum() or c in "._- " else "_" for c in filename)
    return f"{num:03d}_{clean_filename}" if "." in clean_filename else f"{num:03d}_{clean_filename}.jpg"

def download_and_upload(car_num, image_num, image_url):
    """Download and upload image to car-specific folder"""
    try:
        print(f"Downloading: {image_url}")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        filename = sanitize_filename(image_url, image_num)
        folder = f"car_{car_num}"
        s3_key = f"{folder}/{filename}"

        s3.upload_fileobj(BytesIO(response.content), R2_BUCKET_NAME, s3_key)
        file_url = f"https://pub-62ea30bab63244a882fdd29aafc7fe26.r2.dev/{s3_key}"
        print(f"✅ Uploaded to {file_url}")
        return file_url
    except Exception as e:
        print(f"❌ Error processing {image_url}: {str(e)}")
        return None

def batch_upload(all_images, max_workers=20):
    """Process all images in parallel with enhanced threading"""
    uploaded_urls = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                download_and_upload,
                car_num,
                image_num,
                url
            ) for car_num, image_num, url in all_images
        ]
        
        for future in futures:
            if (result := future.result()):
                uploaded_urls.append(result)

    return uploaded_urls

# Process data with folder organization and parallel uploads
with open('/Users/amd/my_scrapping/autobell/autobell_data/final_json/detail_json_2025-02-27mnaf.json') as j:
    data = json.load(j)

# Generate list of all images with car context
all_images = []
for car_num, car in enumerate(data):
    for image_num, url in enumerate(car.get('images', [])):
        all_images.append((car_num, image_num, url))

# Upload all images in parallel with folder structure
uploaded_urls = batch_upload(all_images, max_workers=20)
print(f"Total uploaded: {len(uploaded_urls)} images")

# Optional: Add URLs back to data structure
url_index = 0
for car in data:
    car_images = []
    for _ in car.get('images', []):
        if url_index < len(uploaded_urls):
            car_images.append(uploaded_urls[url_index])
            url_index += 1
    car['uploaded_images'] = car_images
