import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from test_cases.helper_class import CommonMethods

class WorstHitCountries(unittest.TestCase, CommonMethods):

    def setUp(self):
        self.h = CommonMethods()
        self.driver = self.h.get_driver()

    def test_move_to_most_cases(self):
        self.h.move_to_most_cases_page(self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_check_header(self):
    #     self.h.move_to_most_cases_page(self.driver)
    #     header = self.h.get_element((By.TAG_NAME, 'h2'), self.driver)
    #     self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", header.text)

    def test_data_type(self):
        self.h.move_to_most_cases_page(self.driver)
        data_types = self.h.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'), self.driver)
        data_types.click()
        total_deaths = self.h.get_element((By.ID, 'bui-10'), self.driver)
        self.h.move_and_click(total_deaths, self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_per_million(self):
        self.h.move_to_most_cases_page(self.driver)
        check_box = self.h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'), self.driver)
        self.h.move_and_click(check_box, self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def test_slider(self):
        self.h.move_to_most_cases_page(self.driver)
        slider = self.h.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div'), self.driver)
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()