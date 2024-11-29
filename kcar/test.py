from bs4 import BeautifulSoup as bs
from file_proccessor import FileProccessing
import logging
from datetime import date


TODAY = date.today()


with open('kcar/kcar_data/detailed_file/kcar_data_2024-11-27_urls.txt') as f:
    soup = bs(f.read(),'html.parser')

process_file = FileProccessing()
car_urls = []
car_ids = []
car_listings = soup.findAll(class_= "listbox")
count=0
for car in car_listings:
    try:
        car_id = car.find("a")
        id1 = car_id.attrs['id'].replace('CAR_','')
        id2 = car_id.attrs['href'].split(',')[1].replace("'",'')
        car_urls.append(f'https://www.kcarauction.com/kcar/auction/weekly_detail/auction_detail_view.do?PAGE_TYPE=wCfm&CAR_ID={id1}&AUC_CD={id2}')
        car_ids.append(car_id.attrs['id'])
        process_file.export_json({'ids':car_ids,'car_urls':car_urls},f'kcar/kcar_data/kcar_urls/kcar_{TODAY}.json')
        count+=1
        print(count,id1,id2)
    except Exception as e:
        logging.error(f"An error occurred while processing car listing: {e}")

 