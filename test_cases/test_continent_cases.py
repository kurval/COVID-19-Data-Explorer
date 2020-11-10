import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from test_cases.helper_class import CommonMethods
import time
import warnings

class ContinentCases(unittest.TestCase, CommonMethods):

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        h = CommonMethods()
        self.driver =  h.get_driver()

    def test_chart_is_visible(self):
        h = CommonMethods()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[3]/div[1]/div'), self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_check_header(self):
    #     h = CommonMethods()
    #     h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[3]/div[1]/div'), self.driver)
    #     header = h.get_element((By.TAG_NAME, 'h2'), self.driver)
    #     self.assertEqual("COVID-19: new confirmed cases by continent", header.text)
    
    def tearDown(self):
        self.driver.close()