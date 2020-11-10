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

class WorstHitCountries(unittest.TestCase, CommonMethods):

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        h = CommonMethods()
        self.driver = h.get_driver()

    def test_move_to_most_cases(self):
        h = CommonMethods()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'), self.driver)
        cases = h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[2]/div'), self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_check_header(self):
        h = CommonMethods()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'), self.driver)
        header = h.get_element((By.TAG_NAME, 'h2'), self.driver)
        self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", header.text)

    def test_data_type(self):
        h = CommonMethods()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'), self.driver)
        data_types = h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'), self.driver)
        data_types.click()
        total_deaths = h.get_element((By.ID, 'bui-10'), self.driver)
        h.move_and_click(total_deaths, self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_per_million(self):
        h = CommonMethods()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'), self.driver)
        check_box = h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'), self.driver)
        h.move_and_click(check_box, self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        h = CommonMethods()
        h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'), self.driver)
        slider = h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div'), self.driver)
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()