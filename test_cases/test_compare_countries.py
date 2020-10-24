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

class CompareCountries(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument('-headless')
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
        self.wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)
        self.driver.get("http://localhost:8501/covid19dataexplorer.com/dev")

    def getElement(self, attr):
        wait = self.wait
        element = wait.until(EC.presence_of_element_located(attr))
        return element
    
    def getClickElement(self, attr):
        wait = self.wait
        element = wait.until(EC.element_to_be_clickable(attr))
        return element
    
    def checkChart(self):
        wait = self.wait
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        self.assertTrue(chart.is_displayed())

    def test_check_cases_text(self):
        cases = self.getClickElement((By.CSS_SELECTOR, "#cases"))
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        deaths = self.getClickElement((By.CSS_SELECTOR, "#deaths"))
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        time.sleep(1)
        self.checkChart()
    
    def test_log_scale(self):
        action_chains = ActionChains(self.driver)
        checkbox = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'))
        action_chains.move_to_element(checkbox).click().perform()
        self.checkChart()
    
    def test_data_type(self):
        data_types = self.getClickElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'))
        data_types.click()
        total_deaths = self.getClickElement((By.ID, 'bui-10'))
        total_deaths.click()
        self.checkChart()
    
    def test_chart_type(self):
        chart_types = self.getClickElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div/div/div[1]'))
        chart_types.click()
        bar_chart = self.getClickElement((By.ID, 'bui-10'))
        bar_chart.click()
        self.checkChart()

    def test_slider(self):
        slider = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div/div'))
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        self.checkChart()

    def tearDown(self):
        self.driver.close()