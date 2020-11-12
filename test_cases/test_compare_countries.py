import unittest
from selenium.webdriver.common.by import By
from test_cases.common import CommonMethods
from test_cases.resources.locators import PageLocators
import time

class CompareCountries(unittest.TestCase, CommonMethods, PageLocators):
    
    def setUp(self):
        self.cm = CommonMethods()
        self.pc = PageLocators()
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
        checkbox = self.cm.get_element((By.XPATH, self.pc.LOG_CHECKBOX), self.driver)
        self.cm.move_and_click(checkbox, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_add_country(self):
    #     countries = self.cm.get_click_element((By.XPATH, self.pc.COUNTRIES_DROP), self.driver)
    #     countries.click()
    #     country = self.cm.get_element((By.ID, self.pc.DROP_OPTION), self.driver)
    #     self.cm.move_and_click(country, self.driver)
    #     time.sleep(2)
    #     chart = self.cm.get_chart(self.driver)
    #     self.assertTrue(chart.is_displayed())
    
    def test_data_type(self):
        data_types = self.cm.get_click_element((By.XPATH, self.pc.DATA_DROP), self.driver)
        data_types.click()
        total_deaths = self.cm.get_element((By.ID, self.pc.DROP_OPTION), self.driver)
        self.cm.move_and_click(total_deaths, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_chart_type(self):
        chart_types = self.cm.get_click_element((By.XPATH, self.pc.CHART_DROP), self.driver)
        chart_types.click()
        bar_chart = self.cm.get_element((By.ID, self.pc.DROP_OPTION), self.driver)
        self.cm.move_and_click(bar_chart, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        slider = self.cm.get_element((By.XPATH, self.pc.SLIDER), self.driver)
        self.cm.drag_slider(slider, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()