# from bs4 import BeautifulSoup as bs
# import os
from datetime import datetime, date
from parser import Parser
from random import choice
# from utils import *
# from transelations import makes,translated_models,auto_hub_options
import json
import pandas as pd
TODAY = date.today()



# with open('autohub/autuhub_data/final_json/detail_json_2025-01-211.json') as f:
#     data = json.load(f)
# for i in data:
#     if i['seats']>0:
#         print(i['seats'])


# BASE_DIR = '/Users/amd/Downloads/autohub_2024_12_10'

# def get_price(price):
#     if ',' in price:
#         price = int(price.replace(',',''))*10000 
#     elif '.' in price:
#         price = int(price.replace('.',''))*100000
#     else:
#         price = int(price)*1000000
#     return price*0.0027
# def generate_htmls_files(folder_path):
#     htmls=[]
#     files =[]
#     for i in os.listdir(folder_path):
#         if i.endswith('html'):
#             print(i)
#             htmls.append(f"{folder_path}/{i}")
#         elif i.endswith('files'):
#             files.append(f"{folder_path}/{i}")
#     return (htmls,files)
# def parse_htmls(htmls):
#     dict_list=[]
#     for i in htmls:
#         with open(i) as f:
#             d=f.read()
#         car = bs(d,'lxml')
#         try:
#             car_data = {
#                 'category':'auction',
#                 'title' : car.find('h2').text.split('\t')[-1].strip(),
#                 'price':get_price(car.find(class_='start_pay').find_all('strong')[1].text.split()[0]),
#                 'year':int(car.find(class_='car-details-sidebar').find_all('li')[4].text.split()[1]),
#                 'mileage':car.find(class_='car-details-sidebar').find_all('li')[7].strong.text.split('(')[0].strip(),
#                 'fuel':car.find(class_='car-details-sidebar').find_all('li')[6].strong.text,
#                 'car_identifire': car.find(class_='car-details-sidebar').find_all('li')[3].strong.text,
#                 'entry':int(car.find(class_='car-details-sidebar').find_all('li')[0].strong.text),
#                 'power':car.find(class_='car-details-sidebar').find_all('li')[8].strong.text,
#                 'color':car.find(class_='car-details-sidebar').find_all('li')[11].strong.text.split()[0].replace('(',''),
#                 'mission':car.find(class_='car-details-sidebar').find_all('li')[10].strong.text,
#                 'score':''.join(car.find_all(class_='tabl_3_tb_th')[0].td.text.strip().replace(':','').split()[1::2]),
#                 'storage_items':[i.attrs['title'] for i in car.find(class_='tabl_3_tb_th').find_all('input') if 'checked' in i.attrs],
#                 'option':[i.attrs['title'] for i in car.find_all(class_='tabl_3_tb_th')[1].find_all('input') if 'checked' in i.attrs],
#                 'images': [f"{BASE_DIR}{i.attrs['src'][1:].replace('_L','')}" for i in car.find(class_='slick-track')],
#                 'car_ids':car.find(class_='img-fluid').attrs['src'].split('/')[-1].split('.')[0][:-2]        
#             }
#             dict_list.append(car_data)
#         except Exception as e:
#             print(e)
#     return dict_list
# htmls,files=generate_htmls_files(BASE_DIR)
# data=parse_htmls(htmls)

# for i in data:
#     i['option'] = [n[2] for n in auto_hub_options if n[1] in i['option']]+ [n[2] for n in auto_hub_options if n[0] in i['option']]
#     i['make'] =i['title'].split()[1]



# translate_words('make',data,makes)
# process_model(data)
# for i in data:
#     for n in translated_models:
#         if i['models'] == n[0]:
#             i['models'] = n[1]

# proccess_data(data)
# process_title(data)
# Parser().export_json(data,f'autohub/autuhub_data/final_json/autohub_{TODAY}_alfaqih.json')
# all_data = Parser().read_json_file('autohub/autuhub_data/final_json/autohub_2025-01-21_alfaqih.json')
# print(len(all_data))
with open(f'/Volumes/ahmed/car_auction_data/autohub/jsion_data/detail_json_2025-05-27.json') as f:
    all_data = json.load(f)

all_data=[i for i in all_data if i['entry'] != '']
print(len(all_data))
# for i in all_data:
#     try:
#         i['entry'] = float(i['entry'])
#     except Exception as e:
#         print(e)
#         continue
df = pd.read_csv('/Users/amd/Downloads/alfaqih_auction - sheet1 (1).csv')
df=df[df['رقم الاعلان'].notnull()]
def get_matching_values(df,value,col):
    return df.loc[df['رقم الاعلان'] == value][col].values[0]
entries = df['رقم الاعلان'].astype(int).tolist()
filtered_cars = [i for i in all_data if int(i['entry']) in entries]
print(len(filtered_cars))
for i in filtered_cars:
    try:
        i['body'] = get_matching_values(df,i['entry'],'الفحص')
        i['interior'] = get_matching_values(df,i['entry'],'لون الداخلية')
        i['shipping'] = int(get_matching_values(df,i['entry'],'سعر الشحن'))
        i['price'] = int(get_matching_values(df,i['entry'],'سعر السيارة '))
        i['seats'] = int(get_matching_values(df,i['entry'],'عدد الركاب'))
        i['power'] = int(get_matching_values(df,i['entry'],'المحرك'))
        i['color'] = get_matching_values(df,i['entry'],'لون السيارة')
        i['order'] = int(get_matching_values(df,i['entry'],'order'))
        i['images'] = [[i['images'][0],i['images'][2],i['images'][5],i['images'][4]]+i['images'][9:-5]][0]
    except Exception as e:
        print(i['entry'],e)
        continue
# sorted_cars = sorted(filtered_cars, key=lambda x: x['order'])
# filtered_cars = sorted_cars
Parser().export_json(filtered_cars,f'/Volumes/ahmed/car_auction_data/autohub/jsion_data/autohub_{TODAY}_alfaqih.json')
# for i in filtered_cars:
#     print(i['price'])
# f_cars=[]
# for i in all_data:
#     if i['entry'] in entries:
#         f_cars.append(i)
#     else:
#         print([(n,n/100) for n in entries if n not in [i['entry'] for i in all_data]])
        
# print(len(f_cars))

