from datetime import date, datetime
import pathlib
from translate import Translate
from parser import Parser
from transelations import *
from utils import *
import concurrent.futures
from junks import junks
import math
from .parse_features import loop_data,combined_df
from math import ceil
import json

BASE_DIR = pathlib.Path().resolve()

def get_matching_value(df, value,col):
    try:
        matching_row = df.loc[df[1] == value]
        return matching_row[col].values[0]
    except Exception as e:
        print(value)
        return 
             

auction_date = '29/05/2025 08:00 AM'

TODAY = date.today()
class KcarParsing(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_datetime(self, input_date_str):
        try:
            input_date_str = input_date_str.replace(".", "-")
            datetime.strptime(input_date_str, "%Y-%m-%d %H:%M")
            return input_date_str
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None

    def parse_car_data(self, i):
        try:
            car_data = {
                'auction_name': 'kcar',
                'category':'auction',
                'car_ids': 'CAR_'+str(i.find_all('a')[0].attrs['href'].split(',')[1].replace("'", '').strip()),
                'car_identifire': i.find(class_="contents").find('table').find_all('tr')[5].text.split('\n')[2],
                'price': int(i.find("strong", {"id": "auc_strt_prc"}).text.strip().split()[0].replace(',','')),
                'auction_date': auction_date,
                'title': i.find(class_='contents').find_all('tr')[2].find('td', {'colspan': "3"}).text,
                'year': int(i.find(class_="carinfo").find_all("p")[1].span.text),
                'mileage': i.find(class_="carinfo").find_all("p")[2].span.text,
                'fuel': i.find(class_="carinfo").find_all("p")[3].span.text,
                'entry': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[1],
                'power': i.find(class_='cardetailinfo').find('table').find_all('tr')[4].find_all('td')[1].p.text,
                'color': i.find(class_='cardetailinfo').find('table').find_all('tr')[2].find_all('td')[3].text.split('/')[1].strip(),
                'mission': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].find_all("span")[2].text,
                'score': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].find_all("span")[-1].text.split()[1],
                'images': [f"https://www.kcarauction.com{n['src']}" for n in i.find(class_="optionscreen").find_all("img")],
                'inspection_image': str(i.find(class_='car_blueprint')).replace('/IMG/ex', 'https://www.kcarauction.com/IMG/ex').replace('car_blueprint','car_blue_print'),
                'options':[[n.text for n in i.find_all('li')] for i in i.find(class_='optioninfo').find(class_='sel_option').find_all('ul') if 'checked' in i.li.input.attrs]

            }
            return car_data
        except AttributeError as e:
            print(f"Error parsing car data: {e}")
            return None

    def parsing_details(self,year,output,currency=None) -> None:
        file_path = f'/Volumes/ahmed/car_auction_data/kcar/text_data/kcar_detail_data_{TODAY}.txt'
        kcar_class = self.getting_class(file_path, 'detail_carbox')
        json_urls =loop_data('A')

        dict_list = []
        dict_list.append({'icon': 'https://www.kcarauction.com/images/ko/common/logo.jpg'})
        dict_list.append({'auction_name': "kcar"})
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use a thread pool to parallelize car data parsing
            futures = {executor.submit(self.parse_car_data, i): (i) for i in kcar_class}
            for future in concurrent.futures.as_completed(futures):
                car_data = future.result()
                if car_data:
                    dict_list.append(car_data)

        dict_list = dict_list[2:]
        # Filter cars by year and make
        for car in dict_list:
            car['make'] = car['title'].split()[0]
            car['inspection_image'] = f"<img src='https://pub-2d440f2e32a84b8f9c0e75225098e530.r2.dev/{car['car_ids']}.png'>"
            if currency:
                car['price'] = car['price'] * 10000 * currency
            else:
                car['price'] = car['price'] * 10000


        translate_words('make',dict_list, makes)
       
        
        # Create a set of translated model names for faster lookups
        process_model(dict_list)
        for model in dict_list:
            for word in translated_models:
                if model['models'] == word[0]:
                    model['models'] = word[1]
        
        
        process_title(dict_list)
        proccess_data(dict_list)
        with open(f'/Volumes/ahmed/car_auction_data/kcar/json_data/kcar_{TODAY}.json', 'w', encoding='utf-8') as f:
            json.dump(dict_list, f, ensure_ascii=False, indent=4)
        # Export filtered data to a JSON file
        # dict_list = [car for car in dict_list if car['price']!=700.0]
        dict_list = filter_cars_by_year(dict_list,year)
        dict_list = [car for car in dict_list if car['price']!=0.0]
        if output == 'korcars':
            dict_list = [car for car in dict_list if car['fuel'] != 'غاز' and car['fuel'] != 'هيدروجين']
        print(len(dict_list))
        
        # Save the data in chunks of 300
        chunk_size=300
        if len(dict_list) > 300:
            total_chunks = ceil(len(dict_list) / chunk_size)
            for i in range(total_chunks):
                chunk = dict_list[i * chunk_size : (i + 1) * chunk_size]
                with open(f'/Volumes/ahmed/car_auction_data/kcar/json_data/detail_json_{TODAY}{output}_part{i + 1}.json', 'w', encoding='utf-8') as f:
                    json.dump(chunk, f, ensure_ascii=False, indent=4)
        else:
            with open(f'/Volumes/ahmed/car_auction_data/kcar/json_data/detail_json_{TODAY}{output}.json', 'w', encoding='utf-8') as f:
                json.dump(dict_list, f, ensure_ascii=False, indent=4)




KcarParsing().parsing_details(year=2019,currency=0.0027,output='korcars')
KcarParsing().parsing_details(year=2010,output='omarcars')
KcarParsing().parsing_details(year=2010,currency=0.00070,output='mnafcars')
KcarParsing().parsing_details(year=0,currency=0.0027,output='korea_auto')
KcarParsing().parsing_details(year=2010,currency=0.0027,output='luxe_motors')

        
