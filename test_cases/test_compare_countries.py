import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from test_cases.helper_class import CommonMethods
import time

class CompareCountries(unittest.TestCase, CommonMethods):
        
    def setUp(self):
        self.h = CommonMethods()
        self.driver = self.h.get_driver()

    def test_check_cases_text(self):
        cases = self.h.get_element((By.CSS_SELECTOR, "#cases"), self.driver)
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        deaths = self.h.get_element((By.CSS_SELECTOR, "#deaths"), self.driver)
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        time.sleep(1)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_log_scale(self):
        checkbox = self.h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'), self.driver)
        self.h.move_and_click(checkbox, self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_add_country(self):
        countries = self.h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[5]/div/div/div/div[1]'), self.driver)
        countries.click()
        country = self.h.get_element((By.ID, 'bui-10'), self.driver)
        self.h.move_and_click(country, self.driver)
        time.sleep(2)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_data_type(self):
        data_types = self.h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'), self.driver)
        data_types.click()
        total_deaths = self.h.get_element((By.ID, 'bui-10'), self.driver)
        self.h.move_and_click(total_deaths, self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_chart_type(self):
        chart_types = self.h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div/div/div[1]'), self.driver)
        chart_types.click()
        bar_chart = self.h.get_element((By.ID, 'bui-10'), self.driver)
        self.h.move_and_click(bar_chart, self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        slider = self.h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div/div'), self.driver)
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()