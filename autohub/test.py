from utils import *
import json
from datetime import date
import random
import pandas as pd

TODAY = date.today()

from bs4 import BeautifulSoup as bs
import json


with open('autohub/autuhub_data/final_json/detail_json_mnaf_2025-04-15.json') as j:
    mnaf_data = json.load(j)

data = [car for car in mnaf_data if car['price']!='0']

data = [car for car in data if car['year'] != '-']
for car in data:
    car['year'] = int(car['year'])
# mnaf_data = filter_cars_by_year(data,2010)
data = filter_cars_by_year(data,2010)

# data = [car for car in data if car['fuel'] !='غاز' and car['fuel'] !='هيدروجين']



for i in data:
    i['price'] = round(int(i['price'].replace(',',''))*10000*0.00070)


# print('korkars',len(korkars_data))
for i in data:
    print(i['make'])
print('korcars',len(data))
with open(f'autohub/autuhub_data/final_json/detail_json_{TODAY}_mnaf.json','w') as j:
    json.dump(data,j,ensure_ascii=False,indent=4)

# with open(f'autohub/autuhub_data/final_json/detail_json_{TODAY}korcars1.json','w') as j:
#     json.dump(data[:300],j,ensure_ascii=False,indent=4)

# with open(f'autohub/autuhub_data/final_json/detail_json_{TODAY}korcars2.json','w') as j:
#     json.dump(data[300:600],j,ensure_ascii=False,indent=4)

# with open(f'autohub/autuhub_data/final_json/detail_json_{TODAY}korcars3.json','w') as j:
#     json.dump(data[600:],j,ensure_ascii=False,indent=4)