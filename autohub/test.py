import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Raw cookie string
cookie_string = "SCOUTER=z17jecj34p6cmi; JSESSIONID=b2iaTxpSC6zU9EdH9mTRYe6li9lqpVnO5D1DFzRzCI6acAoYvUdn0orLTHuRSopU.QXV0b0F1Y3Rpb24vQXV0b0F1Y3Rpb24y; _ga=GA1.1.1557560032.1731844520; _ga_H9G80S9QWN=GS1.1.1731847308.2.0.1731847308.0.0.0"

# Convert cookie string to a dictionary
cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_string.split("; ")}

# Load URLs from the file
with open('/Users/amd/my_scrapping/autobell/autobell_data/detailed_file/autobell_2024_11_19.txt') as f:
    file_content = f.read()

soup = BeautifulSoup(file_content, 'html.parser')
lst_sections = soup.find_all(class_='item')

print(f"Found {len(lst_sections)} items.")

# Build URLs list
urls = []
for l in lst_sections:
    gn = l.find('a').attrs['gn'][:-2]
    urls.append(f'https://auction.autobell.co.kr/auction/exhibitView.do?acc=30&gn={gn}%3D%3D&rc=5100&atn=666')

# Selenium setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode if needed
driver = webdriver.Chrome(options=chrome_options)

# Open a domain to set cookies
driver.get("https://auction.autobell.co.kr")

# Add cookies to the driver
for name, value in cookies.items():
    driver.add_cookie({'name': name, 'value': value})

# Iterate through URLs
for i, url in enumerate(urls):
    print(f"Processing {i + 1} of {len(urls)}: {url}")

    # Navigate to URL
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'view-thumb'))
        )
        elements = driver.find_elements(By.CLASS_NAME, 'view-thumb')
        for el in elements:
            with open('/Users/amd/my_scrapping/autobell/autobell_data/detailed_file/detailed_text.txt','+a') as f:
                f.write(el.get_attribute('style'))  # Check if background-image is populated
    except Exception as e:
        print(f"Error waiting for elements: {e}")

# Quit the driver
driver.quit()
