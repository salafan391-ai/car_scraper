import pandas as pd
import json
from datetime import date
from utils import *

TODAY = date.today()
AUCTION_DATE = "18/04/2025 09:00 AM"
INPUT_FILE = f'autobell/autobell_data/final_json/detail_json_{TODAY}mnaf.json'

def get_inspection_image(image):
    num=image.split('2F')[4][:-1]
    id1 = image.split('2F')[-1].split('.')[0][:-3]
    id2 = image.split('3F')[-1].split('&')[0]
    id0 = id1[1:5]
    return f'https://auction.autobell.co.kr/FileUpDown/{num}/valimg/{id0}/{id1}.jpg'
with open(INPUT_FILE, 'r') as f:
    json_data = json.load(f)

def korcars_export():
    with open(INPUT_FILE, 'r') as f:
        autobell_data = json.load(f)
        # autobell_df = pd.DataFrame(autobell_data)


    for car in autobell_data:
        car['car_identifire'] = car['car_ids']
        car['category'] = 'auction'
        car['auction_date'] = AUCTION_DATE    
        car['price'] = round(int(car['price'].replace(',', ''))*10000*0.0027)
        car['inspection_image'] = f"<img class='inspection_image' src='{get_inspection_image(car['image'])}'><img>"

    autobell_data=filter_cars_by_year(autobell_data,2019)
    autobell_data=[car for car in autobell_data if car['fuel'] !='غاز' and car['fuel'] !='هيدروجين']
    autobell_data=[car for car in autobell_data if car['price']!=27]

    reversed_autobell_data = list(reversed(autobell_data))
    with open(f'autobell/autobell_data/final_json/detail_json_{TODAY}korcars_last.json', 'w') as f:
        json.dump(reversed_autobell_data, f, ensure_ascii=False, indent=4)

def mnaf_export():
    with open(INPUT_FILE, 'r') as f:
        autobell_data = json.load(f)
        # autobell_df = pd.DataFrame(autobell_data)
    for car in autobell_data:
        car['car_identifire'] = car['car_ids']
        car['category'] = 'auction'
        car['auction_date'] = AUCTION_DATE    
        car['price'] = round(int(car['price'].replace(',', ''))*10000*0.00070)

    autobell_data=filter_cars_by_year(autobell_data,2010)
    # autobell_data=[car for car in autobell_data if car['price']!=27]


    with open(f'autobell/autobell_data/final_json/detail_json_{TODAY}mnaf_last.json', 'w') as f:
        json.dump(autobell_data, f, ensure_ascii=False, indent=4)



korcars_export()
mnaf_export()

# with open('autobell/autobell_data/final_json/detail_json_2025-03-10.json') as j:
#     data = json.load(j)
# print(len([car['entry'] for car in data]))
# print(len(set([car['entry'] for car in data])))
