import unittest
from selenium.webdriver.common.by import By
from test_cases.common import CommonMethods
from test_cases.resources.locators import PageLocators

class WorstHitCountries(unittest.TestCase, CommonMethods, PageLocators):

    def setUp(self):
        self.cm = CommonMethods()
        self.pl = PageLocators()
        self.driver = self.cm.get_driver()

    def test_move_to_most_cases(self):
        self.cm.move_page(self.pl.MOST_RADIO, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_check_header(self):
    #     self.cm.move_page(self.pl.MOST_RADIO, self.driver)
    #     header = self.cm.get_element((By.TAG_NAME, 'h2'), self.driver)
    #     self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", header.text)

    def test_data_type(self):
        self.cm.move_page(self.pl.MOST_RADIO, self.driver)
        self.cm.get_click_element((By.XPATH, self.pl.DATA_DROP), self.driver).click
        self.cm.move_and_click((By.ID, self.pl.DROP_OPTION), self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_per_million(self):
        self.cm.move_page(self.pl.MOST_RADIO, self.driver)
        self.cm.move_and_click((By.XPATH, self.pl.M_CHECKBOX), self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        self.cm.move_page(self.pl.MOST_RADIO, self.driver)
        slider = self.cm.get_element((By.XPATH, self.pl.SLIDER), self.driver)
        self.cm.drag_slider(slider, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()