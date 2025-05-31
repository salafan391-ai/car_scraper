from bs4 import BeautifulSoup as bs
import os
from parser import Parser
from datetime import date, datetime
from transelations import make_model_translated, translated_models
from utils import *
import json
import pandas as pd

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
df = pd.read_excel('/Users/amd/Downloads/20250322_234708-출품 차량 리스트.xlsx', engine='openpyxl',index_col=0)
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
		'auction_date':"04/03/2024 09:00 AM",
		'car_ids':get_car_ids(i),
		'image':f"https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}28.JPG",
		'images':[f"https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}{n}.JPG" for n in image_ranges],
		'inspection_image':f"<img src='https://imgmk.lotteautoauction.net/AU_INSP/{get_car_ids(i)[2:8]}/{get_car_ids(i)}.JPG'>",
		'title':i.find('a').text.strip(),
		'entry':get_entry(i),
		'year':i.find_all('td')[5].text.strip(),
		'mileage':i.find_all('td')[6].text.strip(),
		'color':i.find_all('td')[7].text.strip(),
		'score':i.find_all('td')[8].text.strip(),
		'price':str(get_matching_value(df,get_entry(i),'시작가(만원)')*10000*0.0027),
		'mission':str(get_matching_value(df,get_entry(i),'변속기')),
		'fuel':str(get_matching_value(df,get_entry(i),'연료')),
		'power':str(get_matching_value(df,get_entry(i),'배기량')),
		'model':str(get_matching_value(df,get_entry(i),'차종그룹')),
	}
	dict_list.append(car_data)

process_model(dict_list)
for model in dict_list:
	for word in translated_models:
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

with open(f'lotte/lotte_final_json/detailed_json_{TODAY}.json', 'w', encoding='utf-8') as f:
	json.dump(dict_list, f, ensure_ascii=False, indent=4)



# def generate_htmls_files(folder_path):
#     htmls=[]
#     files =[]
#     for i in os.listdir(folder_path):
#         if i.endswith('html'):
#             htmls.append(f"{folder_path}{i}")
#         elif i.endswith('files'):
#             files.append(f"{folder_path}{i}")
#     return (htmls,files)


# def parse_htmls(htmls):
#     dict_list=[]
#     for i in htmls:
#         with open(i) as f:
#             d=f.read()
#         soup = bs(d,'lxml')
#         car_data={
#             'category':'auction',
#             'car_ids' :soup.find(class_='img_vr').a.img.attrs['src'].split('/')[-1][:-6],
#             'entry' : soup.find(class_='entry-num').text.strip().split()[-1],
#             'title' : soup.find(class_='tit').text,
#             'price' : float(soup.find(class_='starting-price').em.text.split()[0]),
#             'year' : int(soup.find(class_='tbl-v02').find_all('tr')[4].find_all('td')[1].text),
#             'car_identifier' : soup.find(class_='tbl-v02').find_all('tr')[6].find_all('td')[0].text,
#             'mileage' : soup.find_all(class_='tbl-v02')[1].find_all('td')[1].text,
#             'mission' : soup.find_all(class_='tbl-v02')[1].find_all('td')[3].text,
#             'color': soup.find_all(class_='tbl-v02')[1].find_all('td')[5].text,
#             'fuel': soup.find_all(class_='tbl-v02')[1].find_all('td')[7].text,
#             'power': soup.find_all(class_='tbl-v02')[1].find_all('td')[9].text,
#             'people' : soup.find_all(class_='tbl-v02')[1].find_all('td')[11].text,
#             'storage' : soup.find_all(class_='tbl-v02')[1].find_all('td')[15].text}
#         dict_list.append(car_data)
#     return dict_list

# def generate_images(files):
#     images = {}
#     for i in files:
#         images[[i for i in os.listdir(i) if i.endswith('JPG')][0][:-6]] = [f"/Users/amd/{i}/{n}" for n in os.listdir(i) if n.endswith('JPG')]
#     return images

# def add_images(dict_list,images):
#     for i in dict_list:
#         i['images'] = images[i['car_ids']]
# folder_path = '/Users/amd/Downloads/lotte_2024_12_8/'
# htmls,files = generate_htmls_files(folder_path)
# data=parse_htmls(htmls)
# images = generate_images(files)
# add_images(data,images)
# process_model(data)
# for model in data:
#     for word in translated_models:
#         if model['models'] == word[0]:
#             model['models'] = word[1]
# for i in data:
#     for n in make_model_translated:
#         if i['models'] == n[1]:
#             i['make'] = n[2]
# process_title(data)
# proccess_data(data)
# Parser().export_json(data, f'lotte/lotte_final_json/detail_json_{TODAY}faqih1.json')



