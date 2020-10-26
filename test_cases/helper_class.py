import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time

class HelperM():
    
    # HELPER METHODS
    def get_element(self, attr, driver):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        wait = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)
        element = wait.until(EC.presence_of_element_located(attr))
        return element

    def move_and_click(self, element, driver):
        action_chains = ActionChains(driver)
        action_chains.move_to_element(element).click().perform()
    
    def get_click_element(self, attr, driver):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        wait = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)
        element = wait.until(EC.element_to_be_clickable(attr))
        return element
    
    def get_chart(self, driver):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        wait = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        return chart

    def move_page(self, attr, driver):
        button = self.get_element(attr, driver)
        self.move_and_click(button, driver)
        time.sleep(2)