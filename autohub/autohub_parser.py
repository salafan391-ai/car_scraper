from datetime import date, datetime
from parser import Parser
from utils import *
from transelations import translated_models,makes,make_model_translated,auto_hub_options
from junks import junks
from tqdm import tqdm  # Import tqdm for the progress bar
from bs4 import BeautifulSoup as bs
import pandas as pd
TODAY = date.today()
AUCTION_DATE='16/04/2025 08:00 AM'
# with open(f'autohub/autuhub_data/detailed_file/autohub_data_2024-12-022.txt') as f:
#     data = f.read().split('HTML')
# print(len(data))


# df = pd.read_csv('/Users/amd/Downloads/alfaqih - Sheet1.csv')
def parese_data(data,date=date.today(),df=False,df_path=None,output_path=None):
    soup =bs(data, 'lxml')
    cars = soup.find_all(class_='con_top')
    lst = []
    count=0
    for car in cars:
        try:
            count+=1
            print(count)
            
            # ids = soup.find('img')['src'].split('/')[-1].split('.')[0]
            
            car_data = {
                'car_ids':car.find(class_='car-details-sidebar').find_all('li')[3].strong.text,
                'category':'auction',
                'auction_name' : 'autohub',
                'title' : car.find('h2').text.split('\t')[-1].strip(),
                'price':car.find(class_='i_comm_main_txt2').text,
                'auction_date':AUCTION_DATE,
                'inspection_image':str(car.find(class_='car_blueprintnew').prettify()).replace('/images/front', 'https://www.sellcarauction.co.kr/images/front'),
                'price':car.find(class_='i_comm_main_txt2').text,
                'year':car.find_all('strong')[6].text.split()[0],
                'mileage':car.find_all('strong')[9].text.split()[0].replace('Km',''),
                'fuel':car.find_all('strong')[8].text,
                'entry':car.find(class_='text_style7').text,
                'power':car.find_all('strong')[10].text,
                'color':car.find_all('strong')[13].text.split()[0],
                'mission':car.find_all('strong')[12].text,
                'score':''.join(car.find(class_='tabl_3_tb_th').find('td').text.split()[2::3]),
                'option':[i.attrs['title'] for i in car.find_all(class_='tabl_3_tb_th')[1].find_all('input') if 'checked' in i.attrs],
                'storage_items':[i.attrs['title'] for i in car.find(class_='tabl_3_tb_th').find_all('input') if 'checked' in i.attrs],
                'images':[n['src'].replace('_L','') for n in car.find(class_='slider-slick').find_all('img') if not n['src'].endswith('S.jpg')],
                'car_identifire': car.find(class_='car-details-sidebar').find_all('li')[3].strong.text,
            }
            

            lst.append(car_data)
        except Exception as e:
            print(e)
            continue
    set_makes = set()
    # lst = [car for car in lst if car['price'] != '0']
    for i in lst:
        i['make'] =i['title'].split()[0]
        i['model'] = i['title'].split()[1:]
        if i['make'] not in [n[0] for n in makes]:
            set_makes.add(i['make'])
        i['option'] = [n[2] for n in auto_hub_options if n[1] in i['option']]+ [n[2] for n in auto_hub_options if n[0] in i['option']]
    print('makes',set_makes)
    translate_words('make',lst,makes)
    process_model(lst)
    for i in lst:
        for n in translated_models:
            if i['models'] == n[0]:
                i['models'] = n[1]
    # if df is True:
    #     df_path = df_path
    #     df = pd.read_excel(df_path,
    #                    engine='xlrd')
    #     for i in lst:
    #         print(i['price'])
    #         i['price'] = float(df[df['Unnamed: 4'] == str(i['entry'])]['Unnamed: 16'].values[0].replace(',',''))*10000*0.00069
    #         print(i['price'])
    process_title(lst)
    proccess_data(lst)
    print(len(lst))
    
    # lst_filtered = [car for car in lst if car['price'] != '0']
    # for car in lst_filtered:
    #     i['price'] = round(int(i['price'])*10000*0.00070)
    Parser().export_json(lst, output_path)

with open('autohub/autuhub_data/detailed_file/autohub_data_2025-04-15korcars.txt') as f:
    data = f.read()
    parese_data(data=data,date=date.today(),df=False,df_path='',output_path=f'autohub/autuhub_data/final_json/detail_json_mnaf_{TODAY}.json')

    # Parser().export_json(lst_filtered, f'autohub/autuhub_data/final_json/detail_json_mnaf_{TODAY}.json')
# def korcars_export(korcars_path,output_path):    

#     with open(korcars_path) as f:
#         data = f.read()
#     parese_data(data=data,output_path=output_path)
# korcars_input_path = f'autohub/autuhub_data/detailed_file/autohub_detail_data_2025-04-08.txt'
# korcars_outut_path = f'autohub/autuhub_data/final_json/detail_json_{TODAY}_korcars.json'

# korcars_export(korcars_input_path,korcars_outut_path)


# with open(file_path1,encoding='utf-8') as f:
#     data = f.read().split('HTML')
# parese_data(data,df=False,df_path='/Users/amd/Downloads/제1311회차(2025-02-12)출품리스트_20250211.xls')