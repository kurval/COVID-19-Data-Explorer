import unittest
from selenium.webdriver.common.by import By
from test_cases.helper_class import CommonMethods

class WorldCases(unittest.TestCase, CommonMethods):

    def setUp(self):
        self.h = CommonMethods()
        self.driver = self.h.get_driver()

    def test_chart_is_visible(self):
        self.h.move_to_world_cases_page(self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_check_header(self):
    #     h = CommonMethods()
    #     self.h.move_to_world_cases_page(self.driver)
    #     header = self.h.get_element((By.TAG_NAME, 'h2'), self.driver)
    #     self.assertEqual("COVID-19: new confirmed cases worldwide 🌐", header.text)
    
    def tearDown(self):
        self.driver.close()
