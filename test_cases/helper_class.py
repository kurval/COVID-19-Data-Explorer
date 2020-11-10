import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
import time

class CommonMethods():
    
    # HELPER METHODS
    def get_driver(self):
        driver = webdriver.Firefox(options=self.get_options())
        driver.get("http://localhost:8501/covid19dataexplorer.com/dev")
        return driver

    def get_options(self):
        options = Options()
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

    def move_page(self, attr, driver):
        button = self.get_element(attr, driver)
        self.move_and_click(button, driver)
        time.sleep(2)