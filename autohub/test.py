from utils import *
import json
from datetime import date
import random
import pandas as pd
from pathlib import Path


TODAY = date.today()

from bs4 import BeautifulSoup as bs
import json


with open('/Volumes/ahmed/car_auction_data/autohub/jsion_data/autohub_urls_2025-05-27-12.json') as j:
    data_urls = json.load(j)
df = pd.DataFrame(data_urls)
df = df.loc[df['entries'] != '']
print(df['entries'])
def get_matching_values(df,value,col):
    try:
        return df.loc[df['entries'] == value][col].values[0]
    except Exception as e:
        return str(e)
print(df.columns)
print(get_matching_values(df,'3596','ids'))
def get_data(output_path,year,currency=None):
    with open('/Volumes/ahmed/car_auction_data/autohub/jsion_data/detail_json_2025-05-27.json') as j:
        mnaf_data = json.load(j)
    data = [car for car in mnaf_data if car['price']!='0' and car['entry'] != '']

    data = [car for car in data if car['year'] != '-']
    for car in data:
        car['year'] = int(car['year'])
        car['inspection_image'] = f"<img src='https://pub-2d440f2e32a84b8f9c0e75225098e530.r2.dev/{get_matching_values(df,car['entry'],'ids')}.png' alt='{car['title']}'>"
        print(car['entry'])
    # mnaf_data = filter_cars_by_year(data,2010)
    data = filter_cars_by_year(data,year)

    # data = [car for car in data if car['fuel'] !='غاز' and car['fuel'] !='هيدروجين']

    for i in data:
        i['price'] = round(int(i['price'].replace(',',''))*10000)
        if currency:
            i['price'] = round(i['price']*currency)
        

    chunk_size = 300
    output_dir = Path('/Volumes/ahmed/car_auction_data/autohub/jsion_data')
    # # output_dir.mkdir(parents=True, exist_ok=True)

    if len(data) > chunk_size:
        for i in range(0, len(data), chunk_size):
            chunk_data = data[i:i + chunk_size]
            chunk_file = output_dir / f'detail_json_{TODAY}_{output_path}_part{i//chunk_size + 1}.json'
            with open(chunk_file, 'w', encoding='utf-8') as j:
                json.dump(chunk_data, j, ensure_ascii=False, indent=4)
    else:
        single_file = output_dir / f'detail_json_{TODAY}_{output_path}.json'
        with open(single_file, 'w', encoding='utf-8') as j:
            json.dump(data, j, ensure_ascii=False, indent=4)

get_data('mnaf',2010,0.00070)
get_data('ommar',2010)
get_data(output_path='korcars',year=2019,currency=0.0027)
get_data(output_path='luxe',year=2010,currency=0.0027)
get_data(output_path='korea_auto',year=0,currency=0.0027)

