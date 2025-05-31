import pandas as pd
import json
from datetime import date
from utils import *
from datetime import datetime, timedelta
from math import ceil


def get_auction_date():
    today = datetime.now().date() + timedelta(days=1)
    return f"{datetime.strptime(str(today), '%Y-%m-%d').strftime('%d/%m/%Y')} 09:00 AM"


TODAY = date.today()
AUCTION_DATE = get_auction_date()
INPUT_FILE = f'/Volumes/ahmed/car_auction_data/autobell/jsion_data/dtailed_data{TODAY}.json'

def get_inspection_image(image):
    try:
        num=image.split('2F')[4][:-1]
        id1 = image.split('2F')[-1].split('.')[0][:-3]
        id2 = image.split('3F')[-1].split('&')[0]
        id0 = id1[1:5]
        return f'https://auction.autobell.co.kr/FileUpDown/{num}/valimg/{id0}/{id1}.jpg'
    except:
        pass
with open(INPUT_FILE, 'r') as f:
    json_data = json.load(f)

def korcars_export():
    with open(INPUT_FILE, 'r') as f:
        autobell_data = json.load(f)
    autobell_data=[car for car in autobell_data if 'car_ids' in car]
    for car in autobell_data:
        car['category'] = 'auction'
        car['auction_date'] = AUCTION_DATE    
        car['price'] = ceil(int(car['price'].replace(',', ''))*10000/365)
        car['inspection_image'] = f"<img class='inspection_image' src='{get_inspection_image(car['image'])}'><img>"

    autobell_data=filter_cars_by_year(autobell_data,2019)
    autobell_data=[car for car in autobell_data if car['fuel'] !='غاز' and car['fuel'] !='هيدروجين']

    reversed_autobell_data = list(reversed(autobell_data))
    chunk_size = 300
    if len(reversed_autobell_data) > chunk_size:
        for i in range(0, len(reversed_autobell_data), chunk_size):
            chunk_data = reversed_autobell_data[i:i + chunk_size]
            with open(f'/Volumes/ahmed/car_auction_data/autobell/jsion_data/detail_json_{TODAY}abobdr{i//chunk_size + 1}.json', 'w') as f:
                json.dump(chunk_data, f, ensure_ascii=False, indent=4)
    else:
        with open(f'/Volumes/ahmed/car_auction_data/autobell/jsion_data/detail_json_{TODAY}abubdr.json', 'w') as f:
            json.dump(reversed_autobell_data, f, ensure_ascii=False, indent=4)

def mnaf_export(output,year,currency=None):
    with open(INPUT_FILE, 'r') as f:
        autobell_data = json.load(f)
    autobell_data=[car for car in autobell_data if 'car_ids' in car]
        # autobell_df = pd.DataFrame(autobell_data)
    for car in autobell_data:
        car['category'] = 'auction'
        car['auction_date'] = AUCTION_DATE
        car['inspection_image'] = f"<img class='inspection_image' src='{get_inspection_image(car['image'])}'><img>"   
        if currency:
            car['price'] = ceil(int(car['price'].replace(',', ''))*10000/currency)
        else:
            car['price'] = int(car['price'].replace(',', ''))*10000
    autobell_data=filter_cars_by_year(autobell_data,year)
    chunk_size = 300
    if len(autobell_data) > chunk_size:
        for i in range(0, len(autobell_data), chunk_size):
            chunk_data = autobell_data[i:i + chunk_size]
            with open(f'/Volumes/ahmed/car_auction_data/autobell/jsion_data/detail_json_{TODAY}{output}{i//chunk_size + 1}.json', 'w') as f:
                json.dump(chunk_data, f, ensure_ascii=False, indent=4)
    else:
        with open(f'/Volumes/ahmed/car_auction_data/autobell/jsion_data/detail_json_{TODAY}{output}.json', 'w') as f:
            json.dump(autobell_data, f, ensure_ascii=False, indent=4)



korcars_export()
# mnaf_export(output='omarfleet',year=2010)
# mnaf_export(output='mnafcars',year=2010,currency=1373)
# mnaf_export(output='korcars',year=2019,currency=365)
# mnaf_export(output='korea_auto',year=0,currency=365)
# mnaf_export(output='luxemotors',year=2010,currency=365)

# with open('autobell/autobell_data/final_json/detail_json_2025-03-10.json') as j:
#     data = json.load(j)
# print(len([car['entry'] for car in data]))
# print(len(set([car['entry'] for car in data]))) 
# all_data = []
# for i in range(1,4):
   
#     with open(f'/Volumes/ahmed/2025-04-28/detail_json_2025-04-28omarfleet{i}.json') as j:
#         data = json.load(j)
#         all_data.extend(data)
# with open(f'/Volumes/ahmed/2025-04-28/detail_json_2025-04-28omarfleet.json','w') as j:
#     json.dump(all_data,j,ensure_ascii=False,indent=4)
