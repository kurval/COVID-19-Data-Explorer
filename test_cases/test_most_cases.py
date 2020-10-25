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
import warnings

class WorstHitCountries(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        options = Options()
        options.add_argument('-headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)
        self.driver.get("http://localhost:8501/covid19dataexplorer.com/dev")

    # TEST CASES
    def test_move_to_most_cases(self):
        self.move_page()
        cases = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[2]/div'))
        self.checkChart()

    def test_check_header(self):
        self.move_page()
        header = self.get_element((By.TAG_NAME, 'h2'))
        self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", header.text)

    def test_data_type(self):
        self.move_page()
        data_types = self.get_click_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'))
        data_types.click()
        total_deaths = self.get_element((By.ID, 'bui-10'))
        self.move_and_click(total_deaths)
        self.check_chart()

    def test_per_million(self):
        self.move_page()
        check_box = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'))
        self.move_and_click(check_box)
        self.check_chart()

    def test_slider(self):
        self.move_page()
        slider = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div'))
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        self.check_chart()

    def tearDown(self):
        self.driver.close()

    # HELPER METHODS
    def get_element(self, attr):
        wait = self.wait
        element = wait.until(EC.presence_of_element_located(attr))
        return element
    
    def get_click_element(self, attr):
        wait = self.wait
        element = wait.until(EC.element_to_be_clickable(attr))
        return element

    def move_and_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).click().perform()

    def move_page(self):
        button = self.get_element((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'))
        self.move_and_click(button)
        time.sleep(2)
        
    def check_chart(self):
        wait = self.wait
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        self.assertTrue(chart.is_displayed())