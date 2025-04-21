from bs4 import BeautifulSoup as bs
import pandas as pd
from utils import *
from transelations import *
from datetime import date
from file_proccessor import FileProccessing
import json
from datetime import datetime
from math import ceil

TODAY = date.today()	

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
df = pd.read_excel('/Users/amd/Downloads/20250420_013331-출품 차량 리스트.xlsx', engine='openpyxl',index_col=0)
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
	return int(tr.find_all('td')[1].text.strip())

def parse_date(date_str):
	# Convert the date string to a datetime object
	date_obj = datetime.strptime(date_str, "%B %d , %Y")
	date_str = date_obj.strftime("%d/%m/%Y %H:%M %p")
	return date_str

dict_list=[]
for i in trs:
	car_data = {
		'auction_name':'lotte',
		'auction_date':"21/04/2025 09:00 AM",
		'category':'auction',
		'car_ids':get_car_ids(i),
		'car_identifire':get_car_ids(i),
		'image':f"https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}28.JPG",
		'images':sorted([f"https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}{n}.JPG" for n in image_ranges]),
		'inspection_image':f"<img class='inspection-image' loading='lazy' src='https://imgmk.lotteautoauction.net/AU_INSP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}.JPG'>",
		'title':i.find('a').text.strip(),
		'entry':get_entry(i),
		'year':i.find_all('td')[5].text.strip(),
		'mileage':i.find_all('td')[6].text.strip().replace('km','').replace('Km',''),
		'color':i.find_all('td')[7].text.strip(),
		'score':i.find_all('td')[8].text.strip(),
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
# mnafcars=filter_cars_by_year(dict_list,2011)

# for car in mnafcars:
# 	car['price']=int(get_matching_value(df,car['entry'],'시작가(만원)')*10000*0.00070)
	
# with open(f'lotte/lotte_final_json/detailed_json_{TODAY}mnaf.json', 'w', encoding='utf-8') as f:
# 	json.dump(mnafcars, f, ensure_ascii=False, indent=4)
def korcars_export(dict_list):
    korcars = [car for car in dict_list if int(car['year']) > 2019 and car['fuel'] != 'غاز']
    for car in korcars:
        car['price'] = int(get_matching_value(df, car['entry'], '시작가(만원)') * 10000 * 0.0027)

    print(len(korcars) / 3)

    chunk_size = 300
    total_chunks = ceil(len(korcars) / chunk_size)

    for i in range(total_chunks):
        chunk = korcars[i * chunk_size : (i + 1) * chunk_size]
        with open(f'lotte/lotte_final_json/detailed_json_{TODAY}_korkars_part{i + 1}.json', 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=4)


def mnafcars_export(dict_list):
	mnafcars=[car for car in dict_list if int(car['year']) > 2011]
	for car in mnafcars:
		car['price']=int(get_matching_value(df,car['entry'],'시작가(만원)')*10000*0.00070)
		# car['images'] = [image.split('/')[-1] for image in car['images']]
		# print([f'https://pub-62ea30bab63244a882fdd29aafc7fe26.r2.dev/{car["car_ids"]}/{i}' for i in car['images']])
		# car['images'] = f'https://pub-62ea30bab63244a882fdd29aafc7fe26.r2.dev/{car['car_ids']}/{car['images'][0]}'
	with open(f'lotte/lotte_final_json/detailed_json_{TODAY}mnaf.json', 'w', encoding='utf-8') as f:
		json.dump(mnafcars, f, ensure_ascii=False, indent=4)


# mnafcars_export(dict_list)
korcars_export(dict_list)
mnafcars_export(dict_list)