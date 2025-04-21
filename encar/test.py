import json
from utils import *

from datetime import date


TODAY = date.today()


with open(f'/Users/amd/my_scrapping/encar/encar_data/final_json/cars_details2025-03-15.json') as j:
    data = json.load(j)
print(len(data))
data =[car for car in data if car['price'] !='9,999']
process_model(data)
for model in data:
    
    for word in translated_models:
        if model['models'] == word[0]:
            model['models'] = word[1]
for i in data:
    i['price'] = round(int(i['price'].replace(',',''))*10000*0.00070)
for i in data:
    splitted=i['title'].split()
    if i['make'] == 'benz':
        if len(splitted)>1:
            if splitted[1].startswith('W') or splitted[1].startswith('X') or splitted[1].startswith('C') :
                i['models'] = f"{i['models']} {splitted[1][4:]}"
            else:
                i['models'] = f"{i['models']} {splitted[1]}"
        else:
            i['models'] = f"{i['models']} {splitted[0].replace('SL-클래스','')}"

outlairs = ['38674700','39054853',
 '39051952',
 '38932018',
 '38931477',
 '39173273',
 '38239687',
 '38554074',
 '37663668',
 '39193424',
 '39192153',
 '38662552',
 '38657038',
 '39121294',
 '39026825',
 '39198661',
 '39191279',
 '39179308',
 '39232589',
 '39171252',
 '39220701',
 '39220458',
 '39006939',
 '39227034',
 '39140959',
 '38902416',
 '38932117',
 '38466817',
 '38972754',
 '38911484',
 '38905372',
 '39086643',
 '39082000',
 '39212404',
 '39204973',
 '35773315',
 '39099544',
 '38918420',
 '38885798',
 '38876935',
 '38700281',
 '39186009',
 '39108147',
 '39199867',
 '38577856',
 '39124254',
 '39178328',
 '39177627',
 '37779015',
 '38991045',
 '38392543',
 '39211683',
 '38386697',
 '39180834',
 '39180198',
 '38388482',
 '38356979',
 '39171705',
 '38799494',
 '38627951',
 '39192644',
 '38366461',
 '37945819',
 '39229305',
 '39107485',
 '38387127',
 '38122854',
 '38004076',
 '38000298',
 '38741608',
 '39044150',
 '38738842',
 '39202091']
data=[car for car in data if car['car_ids'] not in outlairs]
print(len(data))
with open(f'/Users/amd/my_scrapping/encar/encar_data/final_json/cars_details_mnaf{TODAY}.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)