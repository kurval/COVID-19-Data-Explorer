import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as Options1
from selenium.webdriver.chrome.options import Options as Options2
import time
import warnings

# HELPER METHODS
class CommonMethods():
    # Default browser
    BROWSER = "firefox"
    
    def get_driver(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        if self.BROWSER == "firefox":
            driver = webdriver.Firefox(options=self.get_options())
        elif self.BROWSER == "chrome":
            driver = webdriver.Chrome(options=self.get_options())
        driver.get("http://localhost:8501/covid19dataexplorer.com/dev")
        return driver

    def get_options(self):
        if self.BROWSER == "firefox":
            options = Options1()
        elif self.BROWSER == "chrome":
            options = Options2()
            options.add_experimental_option('w3c', False)
        options.add_argument('-headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        return options
    
    def get_exeptions(self):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        return ignored_exceptions

    def get_element(self, attr, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        element = wait.until(EC.presence_of_element_located(attr))
        return element

    def move_and_click(self, element, driver):
        action_chains = ActionChains(driver)
        action_chains.move_to_element(element).click().perform()
    
    def get_click_element(self, attr, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        element = wait.until(EC.element_to_be_clickable(attr))
        return element
    
    def get_chart(self, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        return chart

    def move_to_most_cases_page(self, driver):
        button = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'), driver)
        self.move_and_click(button, driver)
        time.sleep(2)

    def move_to_continent_page(self, driver):
        button = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[3]/div[1]/div'), driver)
        self.move_and_click(button, driver)
        time.sleep(2)

    def move_to_world_cases_page(self, driver):
        button = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[4]/div[1]/div'), driver)
        self.move_and_click(button, driver)
        time.sleep(2)