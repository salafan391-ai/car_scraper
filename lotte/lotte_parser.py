from bs4 import BeautifulSoup as bs
from transelations import translated_models,make_model_translated,wheel_features
from utils import *
import json
import pathlib
from datetime import date
from parser import Parser
import re
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
import pandas as pd

TODAY = date.today()

translator = GoogleTranslator(source='auto', target='en')
# Sample string
auction_date_str = "21/04/2025 08:00 AM"

df = pd.read_csv(f'/Users/amd/Downloads/alfaqih - sheet1 (4).csv')
def matching(value,df):
    row = df.loc[df['رقم الاعلان']==value]
    return [i for i in df.columns if row[i].values[0] == 'نعم'] 
def get_matching_value(df, value,col):
	matching_row = df.loc[df['رقم الاعلان'] == value]
	return matching_row[col].values[0]


print(df['order'])
def parse_data(auction_date_str):
    # Extract date, time, and "days prior" information
    pattern = r"Auction Date:\s(\d{2}/\d{2}/\d{4})\s(\d{1,2}:\d{2}\s[APM]+)\s\(\s(\d+)\sday[s]?\sprior\)"
    match = re.search(pattern, auction_date_str)

    if match:
        date_str = match.group(1)     # "11/11/2024"
        time_str = match.group(2)     # "1:00 PM"
        days_prior = int(match.group(3))  # "2"

        # Parse the date and time
        auction_datetime = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %I:%M %p")

        # Calculate the date the auction info was posted (days prior)
        posted_date = auction_datetime - timedelta(days=days_prior)

        # Output the results
        print("Auction Date and Time:", auction_datetime)
        print("Posted Date:", posted_date)
    else:
        print("The auction date format did not match.")



BASE_DIR = pathlib.Path().resolve()


TODAY = date.today()



class LotteParsing(Parser):
    def __init__(self):
        super().__init__()
    def parsing_detail(self) -> None:
        file_path = f'lotte/lotte_detailed_data/text_data_{TODAY}.txt'
        html = self.read_text_file(file_path)
        soup = self.get_soup(html)
        lotte_class= soup.find_all(class_='exhibited-vehicle')
        print(len(lotte_class))
        dict_list = []
        for i in lotte_class:
            car_data = {
                'auction_name':"lotte",
                'category':'auction',
                'auction_date': auction_date_str,
                'car_ids':i.find(class_='img_vr').a.img['src'].split('/')[-1].split('.')[0],
                'entry':int(i.find(class_='entry-num').strong.text.strip()),
                'images':sorted(list(set([n.img['src'] for n in i.find_all('li',class_='swiper-slide')]))),
                'car_identifire':i.find(class_='vehicle-detail_bar').find_all('table')[0].find_all('td')[10].text.strip(),
                'year':int(i.find(class_='vehicle-detail_bar').find_all('table')[1].find('td').text.strip()),
                'mileage':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[1].text.strip(),
                'mission':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[3].text.strip(),
                'color':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[5].text.strip(),
                'fuel':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[7].text.strip(),
                'power':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[9].text.strip(),
                'title':i.find('h2',class_='tit').text.strip(),
                # 'price':int(''.join([n for n in i.find(class_='starting-price').find('strong').text.strip().split()[0].replace(',','') if n.isdigit()]))*10000*0.0026,
                # 'body':get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'الفحص'),
                # 'interior':get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'لون الداخلية'),
                # 'shipping':int(get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'سعر الشحن')),
                # "option":matching(int(i.find(class_='entry-num').strong.text.strip()),df),
                # 'price':int(get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'سعر السيارة')),
                # 'seat_number':int(get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'عدد الركاب')),
                # "order":int(get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'order')),
                # 'power':int(get_matching_value(df,int(i.find(class_='entry-num').strong.text.strip()),'المحرك')),
            }
            dict_list.append(car_data)

        # filtered_cars = filter_cars_by_year(dict_list)
        print(len(dict_list))
        
        process_model_lotte(dict_list)
        for model in dict_list:
            for word in make_model_translated:
                if model['models'] == word[0]:
                    model['models'] = word[1]
        for i in dict_list:
            for n in make_model_translated:
                if i['models'] == n[1]:
                    i['make'] = n[2]

        for i in dict_list:
            i['images'] = sorted(i["images"])
            try:
                i['body'] = get_matching_value(df,i['entry'],'الفحص')
                i['interior'] = get_matching_value(df,i['entry'],'لون الداخلية')
                i['shipping'] = int(get_matching_value(df,i['entry'],'سعر الشحن'))
                i['option'] = matching(i['entry'],df)
                i['price'] = int(get_matching_value(df,i['entry'],'سعر السيارة'))
                i['seat_number'] = int(get_matching_value(df,i['entry'],'عدد الركاب'))
                i['order'] = int(get_matching_value(df,i['entry'],'order'))
                i['color'] = get_matching_value(df,i['entry'],'لون السيارة')
            except Exception as e:
                print(i['entry'],e)

        
        
        process_title(dict_list)
        proccess_data(dict_list)
        dict_list = sorted(dict_list, key=lambda x: x['order'])
       
#         for i in dict_list:
#             i['description'] = f'''
# الشركة المصنعة: {i['make']}
# رقم الهيكل: {i['car_identifire']}
# اللون الداخلي: {i['interior']}
# فحص السيارة: {i['body']}
# سعر الشحن: 7000 ريال
# العمولة: 2250 ريال
# قم الإعلان : [] اسم السيارة : {i['make']} {i['models']}  {wheel_features[i['wheel']]} موديل : 2020 لون السيارة : {i['color']} لون الداخلية: {i['interior']} نوع الوقود: {i['fuel']} سنة الصنع: {i['year']} العداد: {i['mileage']} رقم الشاصي: SALRA2BK3L2431898 المواصفات : المحرك: {i['power']} سي سي حالة البدي : {i['body']} سعر بداية المزاد غير شامل الشحن والعمولة : {i['price']}ريال سعودي















# '''
        self.export_json(dict_list, f'lotte/lotte_final_json/detail_json_{TODAY}alfaqih.json')
                    


