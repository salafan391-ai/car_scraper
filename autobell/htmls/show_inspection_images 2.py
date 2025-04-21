import boto3
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs

# R2 Config
R2_ACCESS_KEY = 'f00521a9030766502ffdd53ac571f715'
R2_SECRET_KEY = '7fb9715d627bca69754202ce9d6cd3a63399f75641ab33e1a76e3ffc2aa1ff03'
R2_ACCOUNT_ID = '5f609be3294e42fbcada608b624a1c95'
R2_BUCKET_NAME = 'ahmedcars'
R2_ENDPOINT = f'https://5f609be3294e42fbcada608b624a1c95.r2.cloudflarestorage.com'

# Load JSON
with open('autobell/autobell_data/final_json/detail_json_2025-04-10.json') as f:
    car_data = json.load(f)

# Create S3-compatible client for R2
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    endpoint_url=R2_ENDPOINT,
        region_name="auto",
    
)

for car in car_data:
    image_url = bs(car['inspection_image'],'lxml').find('img').attrs['src']
    try:
        # Download image
        response = requests.get(image_url)
        if response.status_code == 200:
            filename = image_url.split('/')[-1]
            key = f"{R2_BUCKET_NAME}/{filename}"

            # Upload to R2
            s3.put_object(
                Bucket=R2_BUCKET_NAME,
                Key=filename,
                Body=response.content,
                ContentType='image/jpeg'
            )
            print(f"[✓] Uploaded: {filename}")
        else:
            print(f"[✗] Failed to download: {image_url}")
    except Exception as e:
        print(f"[!] Error: {e}")
