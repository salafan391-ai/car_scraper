from datetime import date, datetime
from parser import Parser
from utils import *
from transelations import translated_models,makes,make_model_translated
from junks import junks
from tqdm import tqdm  # Import tqdm for the progress bar
from bs4 import BeautifulSoup as bs


TODAY = date.today()
# json_file_urls = Parser().read_json_file(f'autohub/autuhub_data/autohub_urls/autohub_urls_{TODAY}.json')
# aution_date =str(datetime.strptime(json_file_urls['auc_date'].split()[1],'%Y/%m/%d'))
with open(f'autohub/autuhub_data/detailed_file/merged_text_data.txt') as f:
    data = f.read().split('HTML')
print(len(data))
def parese_data(data,date=date.today()):
    lst = []
    for n,i in enumerate(data):
        try:
            print(n)
            soup =bs(i, 'lxml')
            ids = soup.find('img')['src'].split('/')[-1].split('.')[0]
            car = soup.find(class_='con_top')
            car_data = {
                'car_ids':ids,
                'auction_name' : 'autohub',
                'title' : car.find('h2').text.split('\t')[-1].strip(),
                # 'auction_date':aution_date,
                'inspection_image':str(car.find(class_='car_blueprintnew').prettify()).replace('/images/front', 'https://www.sellcarauction.co.kr/images/front'),
                'price':float(car.find(class_='i_comm_main_txt2').text.replace(',', ''))*10000*0.0027,
                'year':int(car.find_all('strong')[6].text.split()[0]),
                'mileage':car.find_all('strong')[9].text.split()[0],
                'feul':car.find_all('strong')[8].text,
                'entry':int(car.find(class_='text_style7').text),
                'power':car.find_all('strong')[10].text,
                'color':car.find_all('strong')[13].text.split()[0],
                'mission':car.find_all('strong')[12].text,
                'score':''.join(car.find(class_='tabl_3_tb_th').find('td').text.split()[2::3]),
                'images':[n['src'] for n in car.find(class_='slider-slick').find_all('img') if not n['src'].endswith('S.jpg')],
            }
            

            lst.append(car_data)
        except Exception as e:
            print(e)
            continue
    set_makes = set()
    for i in lst:
        i['image'] = i['images'][0]
        i['make'] =i['title'].split()[0]
        i['model'] = i['title'].split()[1:]
        if i['make'] not in [n[0] for n in makes]:
            set_makes.add(i['make'])
    print('makes',set_makes)
    translate_words('make',lst,makes)
    process_model(lst)
    for i in lst:
        for n in translated_models:
            if i['models'] == n[0]:
                i['models'] = n[1]

    process_title(lst)
    proccess_data(lst)
    Parser().export_json(lst, f'autohub/autuhub_data/final_json/detail_json_{TODAY}2.json')

parese_data(data)