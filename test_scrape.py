from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import os
import logging
import time

# Set up logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Scrape:
    def __init__(self, url):
        self.url = url

    def start_driver(self):
        """Initialize the WebDriver with options."""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)

    def login(self, username, password):
        """Perform login using provided credentials."""
        try:
            logger.debug("Loading login page...")
            self.driver.set_page_load_timeout(30)
            self.driver.get(self.url)

            logger.debug("Waiting for page load...")
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(2)  # Allow JS to initialize

            logger.debug("Looking for login form...")
            form = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "login_form"))
            )
            logger.info("Login form found")

            # Fill username
            logger.debug("Filling username...")
            username_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.NAME, "i_sUserId"))
            )
            self.driver.execute_script("arguments[0].value = arguments[1]", username_field, username)

            # Fill password
            logger.debug("Filling password...")
            password_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.NAME, "i_sPswd"))
            )
            self.driver.execute_script("arguments[0].value = arguments[1]", password_field, password)

            # Click login button
            logger.debug("Clicking login button...")
            login_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login_full_btn"))
            )
            self.driver.execute_script("arguments[0].click();", login_button)

            # Wait for login success
            logger.debug("Waiting for login completion...")
            WebDriverWait(self.driver, 15).until(
                EC.url_changes(self.url)
            )
            logger.info("Login successful")

        except Exception as e:
            logger.error(f"Error occurred during login: {e}")