from bs4 import BeautifulSoup as bs
import pandas as pd
from utils import *
from transelations import *
from datetime import date
from file_proccessor import FileProccessing
import json
from datetime import datetime
from math import ceil
import os
TODAY = date.today()	
excel_today = TODAY.strftime("%Y%m%d")
image_ranges=['28', '21', '34', '33', '32', '27', '31', '30', '29', '26', '25', '24', '40', '39', '38', '23', '37', '36', '22', '35', '41', '42', '43', '44', '45', '46', '47', '61', '62', '63', '64', '65', '66']


# def get_images(html):
# 	soup = bs(html, 'html.parser')
# 	images_ab = soup.find_all(class_='swiper-wrapper')
# 	ab1 = []
# 	for i in images_ab[0]:
# 		try:
# 			ab1.append(i.find('img').attrs['src'].split('/')[-1].split('.')[0][-2:])
# 		except AttributeError as attr:
# 			pass
# 	print(ab1)
# get_images(html1)
base_excel_path = '/Volumes/ahmed/car_auction_data/lotte/excels/'
excel_path = f"{base_excel_path}{[i for i in os.listdir(base_excel_path) if i.startswith('._') == False][-1]}"
print(excel_path)
df = pd.read_excel('/Users/amd/Downloads/20250531_193419-출품 차량 리스트.xlsx', engine='openpyxl',index_col=0)
print(df)
def get_matching_value(df, value,col):
	matching_row = df.loc[df['출품번호'] == value]
	return matching_row[col].values[0]

with open(f'lotte/lotte_detailed_data/detailed_{TODAY}.txt', 'r', encoding='utf-8') as f:
	data =f.read()

soup = bs(data, 'html.parser')
tbody = soup.find_all('tbody')
trs=[]
for i in range(len(tbody)):
	trs.extend(tbody[i].find_all('tr'))
# date_str = soup.find('p',class_='auction-date').text.strip().split(':')[1].strip()[:-3]

def get_car_ids(tr):
	return tr.a.attrs['onclick'].split(',')[1].replace('"','')
def get_entry(tr):
	print(f"Entry: {tr.find_all('td')[0].text.strip()}")
	return int(tr.find_all('td')[0].text.strip())
	

def parse_date():
	"경매예정일2025년 05월 12일\n오후 1시(2일전)"
	date_str = [i for i in soup.find('p',class_='auction-date').text.strip() if i.isdigit()]
	year = int(''.join(date_str[:4]))
	month = int(''.join(date_str[4:6]))
	day = int(''.join(date_str[6:8]))
	# Convert the date string to a datetime object

	return datetime(year, month, day).strftime('%d/%m/%Y') + ' 08:00 AM'

dict_list=[]
for i in trs:
	car_data = {
		'auction_name':'lotte',
		'auction_date':parse_date(),
		'category':'auction',
		'car_ids':get_car_ids(i),
		'car_identifire':get_car_ids(i),
		'image':f"https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}28.JPG",
		'images':sorted([f"https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}{n}.JPG" for n in image_ranges]),
		'inspection_image':f"<img class='inspection-image' loading='lazy' src='https://imgmk.lotteautoauction.net/AU_INSP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}.JPG'>",
		'title':i.find('a').text.strip(),
		'entry':get_entry(i),
		'year':i.find_all('td')[4].text.strip(),
		'color':i.find_all('td')[6].text.strip(),
		'score':i.find_all('td')[7].text.strip(),
		'mileage':i.find_all('td')[5].text.strip().replace('Km','').replace('km','').replace(',',''),
		'mission':str(get_matching_value(df,get_entry(i),'변속기')),
		'fuel':str(get_matching_value(df,get_entry(i),'연료')),
		'power':str(get_matching_value(df,get_entry(i),'배기량')),
		'model':str(get_matching_value(df,get_entry(i),'차종그룹')),
		'price':int(get_matching_value(df,get_entry(i),'시작가(만원)')*10000),
	}
	dict_list.append(car_data)



process_model_lotte(dict_list)
for model in dict_list:
	model['year'] = int(model['year']) if model['year'].isdigit() else 0
	for word in make_model_translated:
		if model['models'] == word[0]:
			model['models'] = word[1]




for i in dict_list:
	for n in make_model_translated:
		if i['models'] == n[1]:
			i['make'] = n[2]
for i in dict_list:
	if not 'make' in list(i.keys()):
		print(i['models'])

process_title(dict_list)
proccess_data(dict_list)
print(len(dict_list))
dict_list = [i for i in dict_list if i['price'] > 0]
with open(f'lotte/lotte_final_json/detailed_json_{TODAY}.json', 'w', encoding='utf-8') as f:
	json.dump(dict_list, f, ensure_ascii=False, indent=4)
# mnafcars=filter_cars_by_year(dict_list,2011)

# for car in mnafcars:
# 	car['price']=int(get_matching_value(df,car['entry'],'시작가(만원)')*10000*0.00070)
	
# with open(f'lotte/lotte_final_json/detailed_json_{TODAY}mnaf.json', 'w', encoding='utf-8') as f:
# 	json.dump(mnafcars, f, ensure_ascii=False, indent=4)
def korcars_export(dict_list, output,year=None):
    if year:
        korcars = [car for car in dict_list if int(car['year']) > year and car['fuel'] != '가솔린']
    else:
        korcars = dict_list
    for car in korcars:
        car['price'] = int(get_matching_value(df, car['entry'], '시작가(만원)') * 10000/366)
    chunk_size = 300
    total_chunks = ceil(len(korcars) / chunk_size)
    if len(korcars) >= chunk_size:
        for i in range(total_chunks):
            chunk = korcars[i * chunk_size : (i + 1) * chunk_size]
            with open(f'/Volumes/ahmed/car_auction_data/lotte/jsion_data/detailed_json_{TODAY}_{output}_part{i + 1}.json', 'w', encoding='utf-8') as f:
                json.dump(chunk, f, ensure_ascii=False, indent=4)
    else:
        with open(f'/Volumes/ahmed/car_auction_data/lotte/jsion_data/detailed_json_{TODAY}_{output}.json', 'w', encoding='utf-8') as f:
            json.dump(korcars, f, ensure_ascii=False, indent=4)


def mnafcars_export(dict_list, output, currency=None):
    mnafcars = [car for car in dict_list if int(car['year']) >= 2011]
    for car in mnafcars:
        if currency:
            car['price'] = int(get_matching_value(df, car['entry'], '시작가(만원)') * 10000/currency)
        else:
            car['price'] = int(get_matching_value(df, car['entry'], '시작가(만원)') * 10000)
    chunk_size = 300
    total_chunks = ceil(len(mnafcars) / chunk_size)
    if len(mnafcars) > chunk_size:
        for i in range(total_chunks):
            chunk = mnafcars[i * chunk_size : (i + 1) * chunk_size]
            with open(f'/Volumes/ahmed/car_auction_data/lotte/jsion_data/detailed_json_{TODAY}_{output}_part{i + 1}.json', 'w', encoding='utf-8') as f:
                json.dump(chunk, f, ensure_ascii=False, indent=4)
    else:
        with open(f'/Volumes/ahmed/car_auction_data/lotte/jsion_data/detailed_json_{TODAY}_{output}.json', 'w', encoding='utf-8') as f:
            json.dump(mnafcars, f, ensure_ascii=False, indent=4)



# mnafcars_export(dict_list)
korcars_export(dict_list,'korcars',2019)
korcars_export(dict_list, 'yemen')
mnafcars_export(dict_list,'mnaf',1380)
mnafcars_export(dict_list,'omarfleet')
mnafcars_export(dict_list,'luxe-motors',365)
