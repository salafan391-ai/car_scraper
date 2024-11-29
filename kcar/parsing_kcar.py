from datetime import date, datetime
import pathlib
from translate import Translate
from parser import Parser
from transelations import *
from utils import *
import concurrent.futures
from junks import junks

BASE_DIR = pathlib.Path().resolve()

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

    def parse_car_data(self, i, j):
        try:
            car_data = {
                'auction_name': 'kcar',
                'car_ids': j,
                'auction_date': self.parse_datetime(i.find("p", {"id": "weekly_title"}).span.text),
                'title': i.find(class_='contents').find_all('tr')[2].find('td', {'colspan': "3"}).text,
                'price': float(i.find("strong", {"id": "auc_strt_prc"}).text.replace(",", ""))*10000*0.0027,
                'year': int(i.find(class_="carinfo").find_all("p")[1].span.text),
                'mileage': i.find(class_="carinfo").find_all("p")[2].span.text,
                'feul': i.find(class_="carinfo").find_all("p")[3].span.text,
                'entry': int(i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[1]),
                'power': i.find(class_='cardetailinfo').find('table').find_all('tr')[4].find_all('td')[1].p.text,
                'color': i.find(class_='cardetailinfo').find('table').find_all('tr')[2].find_all('td')[3].text.split('/')[1].strip(),
                'mission': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].find_all("span")[2].text,
                'score': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].find_all("span")[-1].text.split()[1],
                'images': [f"https://www.kcarauction.com{n['src']}" for n in i.find(class_="optionscreen").find_all("img")],
                'inspection_image': str(i.find(class_='car_blueprint')).replace('/IMG/ex', 'https://www.kcarauction.com/IMG/ex')
            }
            return car_data
        except AttributeError as e:
            print(f"Error parsing car data: {e}")
            return None

    def parsing_details(self) -> None:
        file_path = f'kcar/kcar_data/detailed_file/kcar_detail_data_{TODAY}.txt'
        kcar_class = self.getting_class(file_path, 'detail_carbox')
        json_urls = self.read_json_file(f'/Users/amd/my_scrapping/kcar/kcar_data/kcar_urls/kcar_{TODAY}.json')

        dict_list = []
        dict_list.append({'icon': 'https://www.kcarauction.com/images/ko/common/logo.jpg'})
        dict_list.append({'auction_name': "kcar"})
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use a thread pool to parallelize car data parsing
            futures = {executor.submit(self.parse_car_data, i, j): (i, j) for i, j in zip(kcar_class, set(json_urls['ids']))}
            for future in concurrent.futures.as_completed(futures):
                car_data = future.result()
                if car_data:
                    dict_list.append(car_data)
        # Filter cars by year and make
        filtered_cars = filter_cars_by_year(dict_list)
        for car in filtered_cars:
            car['make'] = car['title'].split()[0]

       
        translate_words('make',filtered_cars, makes)
        
        # Create a set of translated model names for faster lookups
   
        process_model(filtered_cars)
        for model in filtered_cars:
            for word in translated_models:
                if model['models'] == word[0]:
                    model['models'] = word[1]
        
        print(len(filtered_cars))
        process_title(filtered_cars)
        proccess_data(filtered_cars)
        # Export filtered data to a JSON file
    
        self.export_json(filtered_cars, f'kcar/kcar_data/final_json/detail_json_{TODAY}B.json')
        
