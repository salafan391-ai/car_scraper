import pandas as pd
import json
from .autohub_scraper import scrap_autohub_chunks_async

def get_unscrapped(new_path,old_path):
    with open(old_path) as j:
        data1 = json.load(j)

    with open(new_path) as j:
        data2 = json.load(j)


    df1 = pd.DataFrame(data1)
    print(len(df1))
    df2 = pd.DataFrame(data2)
    print(len(df2))

    urls = df2[~df2['car_urls'].isin(df1['car_urls'])]['car_urls'].to_list()

    return urls


urls = get_unscrapped('/Volumes/ahmed/car_auction_data/autohub/jsion_data/autohub_urls_2025-05-27-12.json','/Volumes/ahmed/car_auction_data/autohub/jsion_data/autohub_urls_2025-05-27-03.json')
print(len(urls))
scrap_autohub_chunks_async(urls, selector='.car_blueprintnew', output_file='/Volumes/ahmed/car_auction_data/autohub/text_data/autohub_data_2025-05-271.txt')