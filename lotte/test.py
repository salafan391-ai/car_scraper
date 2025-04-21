import json

with open('/Users/amd/Desktop/my_scrapping/lotte/lotte_final_json/detail_json_2025-04-12alfaqih.json') as j:
    data = json.load(j)

[909,870]

new_data = [i for i in data if i['entry'] in [909,870]]

sorted_data = sorted(new_data, key=lambda x: x['order'])
with open('/Users/amd/Desktop/my_scrapping/lotte/lotte_final_json/detail_json_2025-04-12alfaqih_clean.json','w') as j:
    json.dump(sorted_data,j,ensure_ascii=False,indent=4)