import pandas as pd
import json

def get_unscrapped():
    with open('autohub/autuhub_data/autohub_urls/autohub_urls_2025-03-04.json') as j:
        data1 = json.load(j)

    with open('autohub/autuhub_data/autohub_urls/autohub_urls_2025-03-05.json') as j:
        data2 = json.load(j)


    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    urls = df1[~df1['car_urls'].isin(df2['car_urls'])]['car_urls'].to_list()

    return urls

