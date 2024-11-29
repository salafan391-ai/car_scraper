from datetime import date,datetime
from translate import Translate
from parser import Parser
from utils import *
from transelations import translated_models,makes,make_model_translated
from junks import junks
import requests
import aiohttp
import asyncio
import re



TODAY = date.today()
class AutobellParser(Parser):
    def __init__(self):
        super().__init__()
        self.html = f'/Users/amd/my_scrapping/autobell/autobell_data/detailed_file/autobell_2024_11_28.txt'
        self.images =[]

    def get_price(self,price):
        return float(price.replace(',',''))*10000*0.0027

    def get_inspection_image(self,image):
        id1 = image.split('2F')[-1].split('.')[0][:-3]
        id2 = image.split('3F')[-1].split('&')[0]
        id0 = id1[1:5]
        return f'https://auction.autobell.co.kr/FileUpDown/1100/valimg/{id0}/{id1}.jpg?={id2}'
    
    def get_auction_date(self):
        with open(self.html,'r',encoding='utf-8') as file:
            html = file.read()
        date = self.get_soup(html).find_all(class_='select-area large')[0].find('option',selected=True).text.strip()
        date = str(datetime.strptime(date.split()[-2],'%Y-%m-%d'))
        return date

    # def get_onload_images(self,id):
    #     m=[]
    #     for i in range(1):
    #         if i < 10:
    #             i= f"0{i}"
    #         else:
    #             i=i
    #         count=0
    #         while count < 32:
    #             count+=1
    #             try:
    #                 m.append(f"https://img-auction.autobell.co.kr/OBmZCjL58I?src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id[0]}2Fcarimg%2F{id[1]}%2F{id[2]}%2F{id[2]}_02_{count}.jpg%3F{id[3]}{i}&type=m&w=1280&h=800&quality=90&ttype=jpg")
    #             except:
    #                 continue
    #     return m
    def get_onload_images(self,id):
        images = []
        id_part1, id_part2, id_part3, id_part4 = id  # Unpack for readability
        
        # Generate URLs for the first set of images (_02_)
        for count in range(1, 33):  # From 1 to 32 inclusive
            try:
                padded_count = f"{count:02}"  # Zero-pad the count
                images.append(
                    f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
                    f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_{padded_count}.jpg%3F{id_part4}01"
                    f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
                )
            except Exception as e:
                # Optionally log the exception for debugging
                print(f"Error generating image URL for count {count}: {e}")
        
        # Generate URLs for the second set of images (_02_99_)
        for count in range(1, 14):  # From 1 to 14 inclusive
            try:
                padded_count = f"{count:02}"  # Zero-pad the count
                images.append(
                    f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
                    f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_99_{padded_count}.jpg%3F{id_part4}01"
                    f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
                )
            except Exception as e:
                # Optionally log the exception for debugging
                print(f"Error generating image URL for count {count}: {e}")
        
        return images

    

    def extract_year_and_generation(self,car_list):
        car_details = []
        
        for car in car_list:
            # Search for year and generation in the car name
            year = re.search(r'\b(19|20)\d{2}\b', car)  # Matches years like 2008, 2019
            generation = re.search(r'\b(\d+세대)\b', car)  # Matches Korean generation notation like '2세대'
            
            # Extract year and generation if found, else set them as None
            car_year = year.group(0) if year else None
            car_generation = generation.group(0) if generation else None
            
            # Remove year and generation from the car name
            car_model = re.sub(r'\b(19|20)\d{2}\b', '', car)  # Remove year
            car_model = re.sub(r'\b\d+세대\b', '', car_model)  # Remove generation
            
            # Clean up extra whitespace
            car_model = car_model.strip()
            
            # Append the details as a dictionary
            car_details.append({
                "model": car_model,
                "year": car_year,
                "generation": car_generation
            })
        
        return car_details



    def parse_ids(self,image):
        try:
            id = image.split('2F')[4]
            id1 = image.split('2F')[-1].split('.')[0][:-6]
            id2 = image.split('3F')[-1].split('&')[0]
            id0 = id1[1:5]
            return (id,id0,id1,id2)
        except IndexError:
            return None
    async def check_url(self,session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return url
        except Exception as e:
            print(f"Error checking {url}: {e}")

    async def main(self,dict_list):
        async with aiohttp.ClientSession() as session:
            tasks = [self.check_url(session, i) for i in dict_list]
            return await asyncio.gather(*tasks)
    def run_checker(self,dict_list):
        return asyncio.run(self.main(dict_list))
        
    def parsing_detail(self) -> None:
        car_class= self.getting_class(self.html,"item")
        # print(auction_date)
        dict_list = []
        count=0
        for i in car_class:
            count+=1
            print(f"{count} of {len(car_class)}")
            try:
                car_data = self.parse_data(
                    image=i.find('img')['src'],
                    icon='https://scontent.fjed6-1.fna.fbcdn.net/v/t39.30808-6/248067471_107015228472423_10446852770529522_n.png?_nc_cat=104&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=AUVFc6zhpHoQ7kNvgFY6J1V&_nc_oc=AdhttuqxX6pnC6Z2PgCGKCMnXUfY3b_JbVrXvm6Wz3g-KB842YlxzGm8__FhhGCNdROXpXqQ7rTXGsYPrMYLkXAZ&_nc_zt=23&_nc_ht=scontent.fjed6-1.fna&_nc_gid=AI8RdztmlzbeZw31KlHQS7-&oh=00_AYBEfZ_hKI2U_aJYVSyJNIhRL8kmJ7Z0TQx1uoabSTWl6Q&oe=673686E4',
                    auction_name="autobell",
                    auction_date=self.get_auction_date(),
                    title=i.find(class_='car-name').text,
                    price=self.get_price(i.find(class_='price-box').find(class_='num').text.strip()),
                    year=i.find(class_='option').span.text,
                    mileage=i.find(class_='option').find_all('span')[3].text.strip().split()[0],
                    feul=i.find(class_='option').find_all('span')[5].text,
                    entry=i.find(class_='entry-info').text.split()[-1],
                    power=i.find(class_='option').find_all('span')[2].text,
                    color=i.find(class_='option').find_all('span')[4].text.strip(),
                    mission=i.find(class_='option').find_all('span')[1].text,
                    score=i.find(class_='option').find_all('span')[7].text,
                )
                dict_list.append(car_data)
            except AttributeError as e:
                print(f"Error parsing car data: {e}")
                continue
        count=0
        for i in dict_list:
            count+=1
            print(f"{count} of {len(dict_list)}")
            try:
                ids = self.parse_ids(i['image'])
                images = self.get_onload_images(ids)
                i['images'] = self.run_checker(images)
                i['inspection_image'] = f"<img src='{self.get_inspection_image(i['image'])}'><img>"
                i['make'] = i['title'].split()[0].replace('[','').replace(']','')
                i['model'] = i['title'].split()[1:]
                i['car_ids'] = ids[2]
            except Exception as e:
                print(f"Error parsing car data: {e}")
                continue
        print(dict_list[0]['make'])
     
        untranslated_makes=[]
        for i in (set([i['make'] for i in dict_list])):
            if i not in [n[0] for n in makes]:
                untranslated_makes.append(i)
        print(untranslated_makes)
        translate_words('make',dict_list,makes)
        process_model(dict_list)
        for i in dict_list:
            for n in translated_models:
                if i['models'] == n[0]:
                    i['models']= n[1]
        process_title(dict_list)
        proccess_data(dict_list)
        self.export_json(dict_list,f'autobell/autobell_data/final_json/detail_json_{TODAY}.json')
    

        
