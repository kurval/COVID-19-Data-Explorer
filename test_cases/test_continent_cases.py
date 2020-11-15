import unittest
from test_cases.common import CommonMethods
from test_cases.resources.locators import PageLocators

class ContinentCases(unittest.TestCase):

    cm = CommonMethods()
    pl = PageLocators()
    def setUp(self):
        self.driver =  self.cm.get_driver()

    def test_chart_is_visible(self):
        self.cm.move_page(self.pl.CONTINENT_RADIO, self.driver)
        chart = self.cm.get_chart(self.pl.CHART, self.driver)
        self.assertTrue(chart.is_displayed())

    def test_check_header(self):
        self.cm.move_page(self.pl.CONTINENT_RADIO, self.driver)
        header = self.cm.get_title(self.pl.HEADER, "COVID-19: new confirmed cases", self.driver)
        self.assertEqual("COVID-19: new confirmed cases by continent", header.text)
    
    def tearDown(self):
        self.driver.close()