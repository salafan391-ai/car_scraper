from bs4 import BeautifulSoup as bs
from transelations import translated_models,tiple,make_model_translated
from utils import *
import json
import pathlib
from datetime import date
from parser import Parser
import re
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
import pandas as pd
translator = GoogleTranslator(source='auto', target='en')
# Sample string
auction_date_str = "18/11/2024 1:00 PM"

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
        file_path = f'/Users/amd/test_cookie/detailed_23_11_20241.txt'
        html = self.read_text_file(file_path)
        soup = self.get_soup(html)
        lotte_class= soup.find_all(class_='exhibited-vehicle')
        print(len(lotte_class))
        dict_list = []
        for i in lotte_class:
            car_data = {
                'auction_name':"lotte",
                'auction_date': auction_date_str,
                'image':i.find(class_='img_vr').a.img['src'],
                'car_ids':i.find(class_='img_vr').a.img['src'].split('/')[-1].split('.')[0],
                'entry':i.find(class_='entry-num').strong.text.strip(),
                'images':[n.img['src'] for n in i.find_all('li',class_='swiper-slide')],
                'inspection_image':str(i.find(class_='car-status-map').img),
                'year':int(i.find(class_='vehicle-detail_bar').find_all('table')[1].find('td').text.strip()),
                'mileage':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[1].text.strip(),
                'mission':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[3].text.strip(),
                'color':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[5].text.strip(),
                'feul':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[7].text.strip(),
                'power':i.find(class_='vehicle-detail_bar').find_all('table')[1].find_all('td')[9].text.strip(),
                'model':i.find(class_='vehicle-detail_bar').find_all('table')[0].find_all('td')[5].text.strip(),
                'title':i.find('h2',class_='tit').text.strip(),
                'price':int(i.find(class_='starting-price').find('strong').text.strip().split()[0].replace(',',''))*10000*0.0027
            }
            dict_list.append(car_data)

        filtered_cars = filter_cars_by_year(dict_list)
        print(len(filtered_cars))
        process_model(filtered_cars)
        for model in filtered_cars:
            for word in translated_models:
                if model['models'] == word[0]:
                    model['models'] = word[1]
        
         
        for i in filtered_cars:
            for n in make_model_translated:
                if i['models'] == n[1]:
                    i['make'] = n[2]


        
        process_title(filtered_cars)
        proccess_data(filtered_cars)
        self.export_json(filtered_cars, f'lotte/lotte_final_json/detail_json_{TODAY}.json')
                    



