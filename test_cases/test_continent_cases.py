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
from test_cases.helper_class import HelperM
import time

class ContinentCases(unittest.TestCase, HelperM):

    def setUp(self):
        options = Options()
        options.add_argument('-headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)
        self.driver.get("http://localhost:8501/covid19dataexplorer.com/dev")

    def test_chart_is_visible(self):
        h = HelperM()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[3]/div[1]/div'), self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_check_header(self):
        h = HelperM()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[3]/div[1]/div'), self.driver)
        header = h.get_element((By.TAG_NAME, 'h2'), self.driver)
        self.assertEqual("COVID-19: new confirmed cases by continent", header.text)
    
    def tearDown(self):
        self.driver.close()