from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os




class Scrape:
    def __init__(self,url):
        self.url = url
        self.driver = webdriver.Chrome()
    def login(self,username,password,user_id,password_id):
        username = username
        password = password
        self.driver.implicitly_wait(10)

        self.driver.get(self.url)

        username_field = self.driver.find_element(By.ID,user_id)
        password_field = self.driver.find_element(By.ID,password_id)

        username_field.send_keys(username)
        password_field.send_keys(password)

        password_field.send_keys(Keys.RETURN)

        WebDriverWait(self.driver,20).until(EC.url_changes(url=self.url))
        if 'login' not in self.driver.current_url:
            logging.info('login successfull!')
        else:
            raise Exception('login faild.check your credintials!!')
        







        