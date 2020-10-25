import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
import time

class WorldCases(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument('-headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)
        self.driver.get("http://localhost:8501/covid19dataexplorer.com/dev")

    # TEST CASES
    def test_chart_is_visible(self):
        self.move_page
        self.check_chart()

    def test_check_header(self):
        self.move_page()
        header = self.get_element((By.TAG_NAME, 'h2'))
        self.assertEqual("COVID-19: new confirmed cases worldwide 🌐", header.text)
    
    def tearDown(self):
        self.driver.close()

    # HELPER METHODS
    def get_element(self, attr):
        wait = self.wait
        element = wait.until(EC.presence_of_element_located(attr))
        return element

    def move_and_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).click().perform()
    
    def get_click_element(self, attr):
        wait = self.wait
        element = wait.until(EC.element_to_be_clickable(attr))
        return element
    
    def check_chart(self):
        wait = self.wait
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        self.assertTrue(chart.is_displayed())
    
    def move_page(self):
        button = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[4]/div[1]/div'))
        self.move_and_click(button)
        time.sleep(2)
