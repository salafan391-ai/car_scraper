# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# # Keep browser open
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

# # Start browser session
# driver = webdriver.Chrome(options=chrome_options)

# # Open the target website first (this is required before adding cookies)
# driver.get("https://auction.autobell.co.kr")  # Change URL if needed

# # Define cookies
# cookies = [
#     {"name": "_ga", "value": "GA1.1.2115862608.1738868412", "domain": ".autobell.co.kr"},
#     {"name": "_ga_H9G80S9QWN", "value": "GS1.1.1740049859.10.1.1740049862.0.0.0", "domain": ".autobell.co.kr"},
#     {"name": "JSESSIONID", "value": "AT81AuhyvHN1g1zzrTKsCVR9sj9dYemAAiPKEwSoVzRNedr1vtMe1l8i1yiCO6Kl.QXV0b0F1Y3Rpb24vQXV0b0F1Y3Rpb24y", "domain": "auction.autobell.co.kr"},
#     {"name": "SCOUTER", "value": "z8e4nhvfq4tuo", "domain": "auction.autobell.co.kr"},
# ]

# # Add cookies
# for cookie in cookies:
#     driver.add_cookie(cookie)

# # Refresh to apply cookies
# driver.refresh()

# print("Cookies have been set. The browser will remain open.")


import json
with open('autobell/autobell_data/final_json/detail_json_2025-05-12.json') as j:
    data = json.load(j)

print([i['entry'] for i in data if 'car_ids' not in i])