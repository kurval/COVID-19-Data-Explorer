import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
import time

class WorldCases(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument('-headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
        self.wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)
        self.driver.get("http://localhost:8501/covid19dataexplorer.com/dev")

    def getElement(self, attr):
        wait = self.wait
        element = wait.until(EC.presence_of_element_located(attr))
        return element

    def moveAndClick(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).click().perform()
    
    def getClickElement(self, attr):
        wait = self.wait
        element = wait.until(EC.element_to_be_clickable(attr))
        return element
    
    def checkChart(self):
        wait = self.wait
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        self.assertTrue(chart.is_displayed())
    
    def movePage(self):
        button = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[4]/div[1]/div'))
        self.moveAndClick(button)
        time.sleep(2)

    # TEST CASES
    def test_chart_is_visible(self):
        self.movePage
        time.sleep(1)
        self.checkChart()
    
    def tearDown(self):
        self.driver.close()