# from concurrent.futures import ThreadPoolExecutor
# import pdfkit
# from jinja2 import Environment, FileSystemLoader
# import json
# import os

# base_dir = os.path.dirname(os.path.abspath(__file__))
# json_data = json.load(open("autobell_pdf.json", "r", encoding='utf-8'))

# # Extract car makes
# car_makes = list(set(i['make'] for i in json_data if 'make' in i))

# # Export to PDF function
# def export_to_pdf(make):
#     contents = [i for i in json_data if i.get('make') == make]

#     env = Environment(loader=FileSystemLoader("templates"))
#     template = env.get_template("index.html")
#     html_content = template.render(contents=contents)

#     html_file = f"pdfs/{make}.html"
#     pdf_file = f"pdfs/{make}.pdf"

#     with open(html_file, "w", encoding='utf-8') as f:
#         f.write(html_content)

#     options = {
#         'page-size': 'A4',
#         'margin-top': '0mm',
#         'margin-right': '0mm',
#         'margin-bottom': '0mm',
#         'margin-left': '0mm',
#         'encoding': 'UTF-8',
#         'enable-local-file-access': None,
#         'javascript-delay': 1000,
#         'dpi': 300,
#         'image-quality': 100,
#         'disable-smart-shrinking': True,
#         'quiet': ''
#     }

#     try:
#         pdfkit.from_file(html_file, pdf_file, options=options)
#         print(f"PDF generated for {make}!")
#     except Exception as e:
#         print(f"Error generating PDF for {make}: {e}")

# # Use ThreadPoolExecutor for parallel PDF generation
# with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust workers based on your system's CPU
#     executor.map(export_to_pdf, car_makes)

import requests
from bs4 import BeautifulSoup as bs

url = "https://www.sellcarauction.co.kr/newfront/onlineAuc/on/onlineAuc_on_detail.do?receivecd=RC202411270221"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, verify=False)
if response.status_code == 200:
    soup = bs(response.text,'html.parser')
    print(soup.find(class_='car_blueprint'))
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
