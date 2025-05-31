import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('Starting the script...')

from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from utils import *
from transelations import translated_models, make_model_translated, makes, encar_translations
from datetime import date

TODAY = date.today()

def export_json(data: dict, output_json):
    logging.info(f'Exporting JSON to {output_json}')
    with open(output_json, 'w', encoding='utf-8') as j:
        json.dump(data, j, ensure_ascii=False, indent=4)
        logging.info('File exported successfully')


def get_images(images):
    logging.info('Getting images')
    base_url = images.img['src'].split('_')[0]
    suffix = '_'.join(images.img['src'].split('_')[1:])[3:]
    image_numbers = list(range(1, 10)) + list(range(15, 25))
    return [f"{base_url}_{num:03d}{suffix}" for num in image_numbers]


def read_text_file(text_file):
    logging.info(f'Reading text file: {text_file}')
    with open(text_file, encoding='utf-8') as file:
        return file.read()


def get_list_cars(car_list_path):
    logging.info('Extracting car list from HTML')
    list_htmls = read_text_file(car_list_path)
    soup_list_htmls = bs(list_htmls, 'lxml')
    cars = soup_list_htmls.find_all(class_='ItemBigImage_link_item__OiB1H')
    makes = soup_list_htmls.find_all(class_='make')
    car_data = {
        'urls': [car.attrs['href'] for car in cars],
        'car_ids': [car.attrs['data-enlog-dt-param'].replace('"', '').split(':')[1].replace('}', '').strip() for car in cars],
        'make': [car.text for car in makes],
        'model': [car.find(class_='ItemBigImage_car__ovlrq').strong.text.split()[1] for car in cars],
        'mileage': [car.find(class_='ItemBigImage_car__ovlrq').ul.find_all('li')[1].text.strip() for car in cars],
        'fuel': [car.find(class_='ItemBigImage_car__ovlrq').ul.find_all('li')[2].text.strip() for car in cars],
        'price': [car.find(class_='ItemBigImage_num__Fu15_').text.strip() for car in cars]
    }
    logging.info(f'Found {len(cars)} cars')
    return car_data


def df_to_dict(df, col):
    logging.info(f'Converting DataFrame column {col} to dictionary')
    return dict(zip(df['car_ids'], df[col]))


def get_detail_cars(df, cars_detail_path):
    logging.info('Extracting car details from HTML')
    detail_htmls = read_text_file(cars_detail_path)
    soup_htmls = bs(detail_htmls, 'lxml')
    car_details = soup_htmls.find_all('a')
    main_https = 'https://fem.encar.com/cars/detail/'

    # Precompute lookups
    price_dict = df_to_dict(df, 'price')
    make_dict = df_to_dict(df, 'make')
    model_dict = df_to_dict(df, 'model')
    fuel_dict = df_to_dict(df, 'fuel')
    mileage_dict = df_to_dict(df, 'mileage')

    dict_data = []
    for i in car_details:
        if i['href'].startswith(main_https):
            logging.info(f'Processing car ID: {i["href"].split("/")[-1]}')
            modal = [n for n in i.find(class_='BottomSheet-module_bottom_sheet__LeljN').ul.find_all('li')]
            car_id = i['href'].split('/')[-1].split('?')[0]
            car_data = {
                'title': i.h3.text,
                'auction_date': '2025-02-10',
                'category': 'sale',
                'car_ids': car_id,
                'car_identifire': car_id,
                'option': [n.text for n in i.find(class_='DetailOption_list_option__kTYgR').find_all('li') if len(n.attrs['class']) > 0],
                'images': get_images(i.find(class_='DetailCarPhotoPc_img_big__LNVDo')),
                'power': modal[3].span.text,
                'car_type': modal[6].span.text,
                'color': modal[7].span.text,
                'seat': ''.join([i for i in modal[9].span.text if i.isdigit()]),
                'mission': modal[5].span.text,
                'year': f"20{modal[1].span.text[:2]}",
                'price': price_dict.get(car_id, 'N/A'),
                'make': make_dict.get(car_id, 'N/A'),
                'models': model_dict.get(car_id, 'N/A'),
                'fuel': fuel_dict.get(car_id, 'N/A'),
                'mileage': mileage_dict.get(car_id, 'N/A')
            }
            car_data['option'] = [n[1] for n in encar_translations if n[0] in car_data['option']]
            dict_data.append(car_data)

    logging.info(f'Total cars processed: {len(dict_data)}')
    process_model(dict_data)
    process_title(dict_data)
    proccess_data(dict_data)
    return dict_data


car_list_path = f'/Users/amd/PycharmProjects/encar/encar_text{TODAY}.txt'
cars_detail_path = f'/Users/amd/PycharmProjects/encar/encar_{TODAY}.txt'

logging.info('Generating car list')
cars_list = get_list_cars(car_list_path)
df = pd.DataFrame(cars_list)
logging.info('Fetching car details')
cars_details = get_detail_cars(df, cars_detail_path)
export_json(cars_details, f'encar/encar_data/final_json/cars_details{TODAY}.json')
logging.info('Script finished successfully')
