import unittest
from selenium.webdriver.common.by import By
from test_cases.helper_class import CommonMethods

class WorldCases(unittest.TestCase, CommonMethods):

    def setUp(self):
        self.h = CommonMethods()
        self.driver = self.h.get_driver()

    def test_chart_is_visible(self):
        self.h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[4]/div[1]/div'), self.driver)
        chart = self.h.get_chart(self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_check_header(self):
    #     h = CommonMethods()
    #     self.h.move_page((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[4]/div[1]/div'), self.driver)
    #     header = self.h.get_element((By.TAG_NAME, 'h2'), self.driver)
    #     self.assertEqual("COVID-19: new confirmed cases worldwide 🌐", header.text)
    
    def tearDown(self):
        self.driver.close()
