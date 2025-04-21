import json
from datetime import date,datetime
import pandas as pd
today = date.today()
df = pd.read_csv('/Users/amd/Downloads/alfaqih - sheet1 (4).csv')

with open(f'lotte/lotte_final_json/detailed_json_2025-04-19mnaf.json') as j:
    data = json.load(j)
print(len(df))
urls = [car['car_ids'] for car in data if car['entry'] in df['رقم الاعلان'].tolist()]
all_urls = []
for car in urls:
    # print(type(car['entry']))
    all_urls.append(f"https://www.lotteautoauction.net/hp/auct/myp/entry/selectMypEntryCarDetPop.do?searchMngDivCd={car[:2]}&searchMngNo={car}&searchExhiRegiSeq=1")


with open(f'lotte/alfaqih_urls/lotte_urls{today}.json','w') as j:
    json.dump(all_urls,j,ensure_ascii=False,indent=4)