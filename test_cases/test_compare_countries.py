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

class CompareCountries(unittest.TestCase, CommonMethods):

    def setUp(self):
        h = CommonMethods()
        self.driver = h.get_driver()

    def test_check_cases_text(self):
        h = CommonMethods()
        cases = h.get_element((By.CSS_SELECTOR, "#cases"), self.driver)
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        h = CommonMethods()
        deaths = h.get_element((By.CSS_SELECTOR, "#deaths"), self.driver)
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        h = CommonMethods()
        time.sleep(1)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_log_scale(self):
        h = CommonMethods()
        checkbox = h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'), self.driver)
        h.move_and_click(checkbox, self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_add_country(self):
        h = CommonMethods()
        countries = h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[5]/div/div/div/div[1]'), self.driver)
        countries.click()
        country = h.get_element((By.ID, 'bui-10'), self.driver)
        h.move_and_click(country, self.driver)
        time.sleep(2)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_data_type(self):
        h = CommonMethods()
        data_types = h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'), self.driver)
        data_types.click()
        total_deaths = h.get_element((By.ID, 'bui-10'), self.driver)
        h.move_and_click(total_deaths, self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_chart_type(self):
        h = CommonMethods()
        chart_types = h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div/div/div[1]'), self.driver)
        chart_types.click()
        bar_chart = h.get_element((By.ID, 'bui-10'), self.driver)
        h.move_and_click(bar_chart, self.driver)
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        h = CommonMethods()
        slider = h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div/div'), self.driver)
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        chart = h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()