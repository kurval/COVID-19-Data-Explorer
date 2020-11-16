import unittest
from test_cases.common import CommonMethods
from test_cases.resources.locators import PageLocators

class CompareCountries(unittest.TestCase):
    
    pl = PageLocators()
    cm = CommonMethods()
    def setUp(self):
        self.driver = self.cm.get_driver()

    def test_check_cases_text(self):
        cases = self.cm.get_element(self.pl.CASES_TEXT, self.driver)
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        deaths = self.cm.get_element(self.pl.DEATHS_TEXT, self.driver)
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        chart = self.cm.get_chart(self.pl.CHART, self.driver)
        self.assertTrue(chart.is_displayed())
    
    def test_log_scale(self):
        self.cm.move_and_click(self.pl.LOG_CHECKBOX, self.driver)
        chart = self.cm.get_chart(self.pl.CHART, self.driver)
        self.assertTrue(chart.is_displayed())

    # def test_add_country(self):
    #     self.cm.get_click_element(self.pl.COUNTRIES_DROP, self.driver).click()
    #     self.cm.move_and_click(self.pl.DROP_OPTION, self.driver)
    #     chart = self.cm.get_chart(self.pl.CHART, self.driver)
    #     self.assertTrue(chart.is_displayed())
    
    # def test_data_type(self):
    #     self.cm.get_click_element(self.pl.DATA_DROP, self.driver).click()
    #     self.cm.move_and_click(self.pl.DROP_OPTION, self.driver)
    #     chart = self.cm.get_chart(self.pl.CHART, self.driver)
    #     self.assertTrue(chart.is_displayed())
    
    # def test_chart_type(self):
    #     self.cm.get_click_element(self.pl.CHART_DROP, self.driver).click()
    #     self.cm.move_and_click(self.pl.DROP_OPTION, self.driver)
    #     chart = self.cm.get_chart(self.pl.CHART, self.driver)
    #     self.assertTrue(chart.is_displayed())

    def test_slider(self):
        self.cm.drag_slider(self.pl.SLIDER1, self.driver)
        chart = self.cm.get_chart(self.pl.CHART, self.driver)
        self.assertTrue(chart.is_displayed())

    def tearDown(self):
        self.driver.close()