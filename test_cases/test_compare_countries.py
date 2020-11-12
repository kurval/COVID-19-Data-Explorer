import unittest
from selenium.webdriver.common.by import By
from test_cases.common import CommonMethods
from test_cases.resources.locators import PageLocators
import time

class CompareCountries(unittest.TestCase, CommonMethods, PageLocators):
    
    def setUp(self):
        self.cm = CommonMethods()
        self.pl = PageLocators()
        self.driver = self.cm.get_driver()

    def test_check_cases_text(self):
        cases = self.cm.get_element((By.CSS_SELECTOR, "#cases"), self.driver)
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        deaths = self.cm.get_element((By.CSS_SELECTOR, "#deaths"), self.driver)
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        time.sleep(1)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_log_scale(self):
        self.cm.move_and_click((By.XPATH, self.pl.LOG_CHECKBOX), self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_add_country(self):
    #     self.cm.get_click_element((By.XPATH, self.pl.COUNTRIES_DROP), self.driver).click()
    #     self.cm.move_and_click((By.ID, self.pl.DROP_OPTION), self.driver)
    #     time.sleep(2)
    #     chart = self.cm.get_chart(self.driver)
    #     self.assertTrue(chart.is_displayed())
    
    # def test_data_type(self):
    #     self.cm.get_click_element((By.XPATH, self.pl.DATA_DROP), self.driver).click()
    #     self.cm.move_and_click((By.ID, self.pl.DROP_OPTION), self.driver)
    #     chart = self.cm.get_chart(self.driver)
    #     self.assertTrue(chart.is_displayed())
    
    def test_chart_type(self):
        self.cm.get_click_element((By.XPATH, self.pl.CHART_DROP), self.driver).click()
        self.cm.move_and_click((By.ID, self.pl.DROP_OPTION), self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        slider = self.cm.get_element((By.XPATH, self.pl.SLIDER), self.driver)
        self.cm.drag_slider(slider, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()