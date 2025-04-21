from bs4 import BeautifulSoup as bs
import os
from datetime import datetime
from parser import Parser
from datetime import date
from transelations import makes, translated_models,kcar_options_ko,kcar_options,kcar_options_ko_dict
from utils import *
from parser import Parser
import pandas as pd

T = date.today()
# def generate_htmls_files(folder_path):
#     htmls=[]
#     files =[]
#     for i in os.listdir(folder_path):
#         if i.endswith('html'):
#             print(i)
#             htmls.append(f"{folder_path}{i}")
#         elif i.endswith('files'):
#             files.append(f"{folder_path}{i}")
#     return (htmls,files)
df = pd.read_csv('/Users/amd/Downloads/alfaqih_auction - sheet1 (13).csv')
with open(f'kcar/kcar_data/detailed_file/alfaqih_data2025-04-162.txt') as f:
    html = f.read()

order = df['order'].tolist()
print(order)
def get_matching_values(df,value,col):
    return df.loc[df['رقم الاعلان'] == value][col].values[0]


soup = bs(html,'lxml')
htmls = soup.find_all(class_='detail_carbox')
def parse_htmls(htmls):
    dict_list=[]
    for i in htmls:
        car_data={
            'auction_date':"17/04/2025 08:00 AM",
            'category':'auction',
            'car_ids' :i.find(class_="contents").find('table').find_all('tr')[5].text.split('\n')[2],
            'car_identifire': i.find(class_="contents").find('table').find_all('tr')[5].text.split('\n')[2],
            'title': i.find(class_='contents').find_all('tr')[2].find('td', {'colspan': "3"}).text,
            'price': float(i.find("strong", {"id": "auc_strt_prc"}).text.strip().split()[0].replace(',',''))*10000*0.0026,
            'year': int(i.find(class_="carinfo").find_all("p")[1].span.text),
            'mileage': i.find(class_="carinfo").find_all("p")[2].span.text,
            'fuel': i.find(class_="carinfo").find_all("p")[3].span.text,
            'entry': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[-1],
            'power': i.find(class_='cardetailinfo').find('table').find_all('tr')[4].find_all('td')[1].p.text,
            'color': i.find(class_='cardetailinfo').find('table').find_all('tr')[2].find_all('td')[3].text.split('/')[1].strip(),
            'mission': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].find_all("span")[2].text,
            'score': i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].find_all("span")[-1].text.split()[1],
            'door':i.find(class_='cardetailinfo').find_all(class_='table_notice')[6].p.text,
            'options': [
                label.text for checkbox in i.find_all("input", {"type": "checkbox", "checked": True})
                if (label := i.find("label", {"for": checkbox.get("id")}))],
            'images': [f"https://www.kcarauction.com{n['src']}" for n in i.find(class_="optionscreen").find_all("img")],
            # 'body':get_matching_values(df,int(i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[-1]),'الفحص'),
            # 'interior':get_matching_values(df,int(i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[-1]),'لون الداخلية'),
            # 'shipping':str(get_matching_values(df,int(i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[-1]),'سعر الشحن')),
            # 'price':float(get_matching_values(df,int(i.find(class_="carinfo").find_all("div")[2].find_all("p")[0].span.text.split()[-1]),'سعر السيارة '))


            
        }

        dict_list.append(car_data)
        for car in dict_list:
            car['make'] = car['title'].split()[0]
        translate_words('make',dict_list, makes)
        process_model(dict_list)
        for model in dict_list:
            for word in translated_models:
                if model['models'] == word[0]:
                    model['models'] = word[1]
        for car in dict_list:
            try:
                car['price'] = int(get_matching_values(df,int(car['entry']),'سعر السيارة '))
                car['body']=get_matching_values(df,int(car['entry']),'الفحص')
                car['interior'] = get_matching_values(df,int(car['entry']),'لون الداخلية')
                car['shipping'] = str(get_matching_values(df,int(car['entry']),'سعر الشحن'))
                car['order'] = int(get_matching_values(df,int(car['entry']),'order'))
                car['power'] = int(get_matching_values(df,int(car['entry']),'المحرك'))
                car['seats'] = int(get_matching_values(df,int(car['entry']),'عدد الركاب'))
                car['color']=(get_matching_values(df,int(car['entry']),'لون السيارة'))
            except Exception as e:
                print(e,car['entry'])
                continue

        for car in dict_list:

            
            # car['option'] = [item for sublist in car['options'] for item in sublist]
            car['option'] = [kcar_options_ko_dict[i] for i in car['options'] if i in kcar_options_ko_dict]
            
        
            
            


        print(len(dict_list))
        process_title(dict_list)
        proccess_data(dict_list)
        dict_list = sorted(dict_list, key=lambda x: x['order'])
        for seat in dict_list:
            seat['seats'] = int(get_matching_values(df,int(seat['entry']),'عدد الركاب'))
        Parser().export_json(dict_list, f'kcar/kcar_data/final_json/detail_json_{T}alfaqih.json')



    return dict_list

# def generate_images(files):
#     images = {}
#     for i in files:
#         images[[i for i in os.listdir(i) if i.endswith('JPG')][0][:10]] = [f"/Users/amd/{i}/{n}" for n in os.listdir(i) if n.endswith('JPG')]
#     return images

# def add_images(dict_list,images):
#     for i in dict_list:
#         i['images'] = images[i['car_ids']]
# folder_path = '/Users/amd/Downloads/kcar/'

# for i in parse_htmls(htmls):
#     print(i['option'])

parse_htmls(htmls)