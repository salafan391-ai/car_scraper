import json
from datetime import date   
import pandas as pd


TODAY = date.today()


def read_urls(lane):
    with open(f'kcar/kcar_data/kcar_urls/kcar_{TODAY}{lane}.json') as j:
        return json.load(j)



def loop_data(*args):
    all_data = []
    for i in args:
        all_data.extend(read_urls(i)['ids'])
    return all_data


excel_df_a= pd.read_html('/Users/amd/Downloads/WEEKLY_CAR_LIST_20250416.xls')
excel_df_b = pd.read_html('/Users/amd/Downloads/WEEKLY_CAR_LIST_20250416 (1).xls')
df_a=excel_df_a[1][excel_df_a[1][1].str.isdigit()]
df_b=excel_df_b[1][excel_df_b[1][1].str.isdigit()]
combined_df = pd.concat([df_a,df_b],ignore_index=True)
# combined_df[1] = combined_df[1].astype(int)
print(len(combined_df[1]))



