import unittest
from selenium.webdriver.common.by import By
from test_cases.common import CommonMethods

class WorstHitCountries(unittest.TestCase, CommonMethods):

    def setUp(self):
        self.cm = CommonMethods()
        self.driver = self.cm.get_driver()

    def test_move_to_most_cases(self):
        self.cm.move_to_most_cases_page(self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_check_header(self):
    #     self.cm.move_to_most_cases_page(self.driver)
    #     header = self.cm.get_element((By.TAG_NAME, 'h2'), self.driver)
    #     self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", header.text)

    def test_data_type(self):
        self.cm.move_to_most_cases_page(self.driver)
        data_types = self.cm.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'), self.driver)
        data_types.click()
        total_deaths = self.cm.get_element((By.ID, 'bui-10'), self.driver)
        self.cm.move_and_click(total_deaths, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_per_million(self):
        self.cm.move_to_most_cases_page(self.driver)
        check_box = self.cm.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'), self.driver)
        self.cm.move_and_click(check_box, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        self.cm.move_to_most_cases_page(self.driver)
        slider = self.cm.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div'), self.driver)
        self.cm.drag_slider(slider, self.driver)
        chart = self.cm.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()