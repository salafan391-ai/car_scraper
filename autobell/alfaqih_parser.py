from bs4 import BeautifulSoup as bs
import re
from utils import *
from datetime import datetime,date
from transelations import *
from file_proccessor import FileProccessing
import pandas as pd
# from .alfaqih_scraper import entries
TODAY = date.today()
auction_date_str = "30/05/2025 08:00 AM"
def get_matching_value(df, value,col):
    try:
        matching_row = df.loc[df['رقم الاعلان'] == value]
        return matching_row[col].values[0]
    except Exception as e:
        print(value)
        return 
df = pd.read_csv('/Users/amd/Downloads/alfaqih_auction - sheet1 (2).csv')
# df['order'] =list(range(1,len(df)+1))
url_pattern = r"https?://[^\s']+"

def extract_mums(num):
    return ''.join([i for i in num if i.isdigit()])


def get_price(price):
    if ',' in price:
        price = extract_mums(price.replace(',', ''))
    elif '.' in price:
        price = extract_mums(price.replace('.', ''))
    else:
        price = extract_mums(price)
    return (float(price) * 10000) *0.0026


with open(f'autobell/autobell_data/detailed_file/text_data{TODAY}.txt', 'r', encoding='utf-8') as f:
    htmls = f.read()

soup = bs(htmls, 'html.parser')
cars = soup.find_all(class_='exhibit-detail')
images = soup.find_all('script')

dict_data = []

for idx, car in enumerate(cars):


    d = {
        'car_ids': car.find(class_='info-box').find_all('dd')[10].text.split()[0],
        'category': 'auction',
        'title': car.find(class_='spec-desc').find('li').strong.text,
        'auction_date': auction_date_str,
        # 'price': int(''.join([n for n in car.find(class_='price-box').text.strip() if n.isdigit()]))*10000*0.0026,
        'year': extract_mums(car.find(class_='info-box').find_all('dd')[-7].text),
        'mileage': car.find(class_='info-box').find_all('dd')[-5].text,
        'fuel': car.find(class_='info-box').find('dl').find_all('dd')[1].text,
        'car_identifire': car.find(class_='info-box').find_all('dd')[10].text.split()[0],
        'entry': int(car.find(class_='car-info').find_all('li')[1].text.split()[-1]),
        'power': car.find(class_='info-box').find_all('dd')[2].text,
        'color': car.find(class_='info-box').find_all('dd')[-4].text.split(')')[-1],
        'mission': car.find(class_='info-box').find_all('dd')[-3].text,
        'seat_num': car.find(class_='info-box').find_all('dd')[3].text[0],
        'score': car.find(class_='rating-info').text,
        'images': sorted(list(set([i.img['src'] for i in car.find_all(class_='swiper-slide')]))),
        'option': [i.text.strip() for i in car.find(class_='block-box').find_all(class_='on')],
        # 'body': get_matching_value(df,int(car.find(class_='car-info').find_all('li')[1].text.split()[-1]),'الفحص'),
        # 'shipping': str(get_matching_value(df,int(car.find(class_='car-info').find_all('li')[1].text.split()[-1]),'سعر الشحن')),
        # 'interior': get_matching_value(df,int(car.find(class_='car-info').find_all('li')[1].text.split()[-1]),'لون الداخلية'),
        # 'price':int(get_matching_value(df,int(car.find(class_='car-info').find_all('li')[1].text.split()[-1]),'سعر السيارة ')),
    }
    dict_data.append(d)
for i in dict_data:
    try:
        i['price'] = int(get_matching_value(df,int(i['entry']),'سعر السيارة '))
        

        i['interior'] = get_matching_value(df,int(i['entry']),'لون الداخلية')
        i['body']= get_matching_value(df,int(i['entry']),'الفحص')
        i['shipping'] = str(get_matching_value(df,int(i['entry']),'سعر الشحن'))
        i['order'] = int(get_matching_value(df,int(i['entry']),'order'))
        i['seats'] = int(get_matching_value(df,int(i['entry']),'عدد الركاب'))
        i['power'] = int(get_matching_value(df,int(i['entry']),'المحرك'))
        i['color'] = get_matching_value(df,int(i['entry']),'لون السيارة')
        print(i['entry'],i['price'],i['seats'])
    except Exception as e:
        print(f"Error parsing car data: {e} {i['entry'] }")
        continue
try:
    dict_data = sorted(dict_data, key=lambda x: x['order'])
except Exception as e:
    print(f"Error parsing car data: {e}")


count=0
for i in dict_data:
    count+=1
    print(f"{count} of {len(dict_data)}")
    try:
        i['make'] = i['title'].split()[0].replace('[','').replace(']','')
        i['option'] = [n[1] for n in autobell_features if n[0] in i['option']]
        i['images'] = [[i["images"][0],i["images"][3],  
                      
                    i["images"][1],
                    i["images"][8],
                    i["images"][9],
                    i["images"][10]] + i["images"][17:]][0]

    except Exception as e:
        print(f"Error parsing car data: {e}")
        continue
# self.export_json(dict_list,f'autobell/autobell_data/final_json/detail_json_{TODAY}.json')
translate_words('make',dict_data,makes)
process_model(dict_data)
for i in dict_data:
    for n in translated_models:
        if i['models'] == n[0]:
            i['models']= n[1]
process_title(dict_data)
proccess_data(dict_data)
dict_data = [i for i in dict_data if 'order' in i]
dict_data = sorted(dict_data, key=lambda x: x['order'])
    
FileProccessing().export_json(dict_data,f'autobell/autobell_data/final_json/detail_json_{TODAY}alfaqih.json')
# for i in dict_data:
#     print(type(i['entry']))
# for i in df['رقم الاعلان']:
#     print(get_matching_value(df,i,'الفحص'))
