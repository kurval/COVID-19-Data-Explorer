import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time

class CompareCountries(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("prefs",{"download.default_directory":"/databricks/driver"})
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://localhost:8501/http://covid19dataexplorer.com/dev")

    def getElement(self, attr):
        driver = self.driver
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        element = WebDriverWait(driver, 15,ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located(attr)
        )
        return element
    
    def checkChart(self):
        driver = self.driver
        chart = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'marks'))
        )
        self.assertTrue(chart.is_displayed())

    def test_check_cases_text(self):
        driver = self.driver
        cases = self.getElement((By.ID, 'cases'))
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        driver = self.driver
        deaths = self.getElement((By.ID, 'deaths'))
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        time.sleep(1)
        driver = self.driver
        self.checkChart()
    
    def test_log_scale(self):
        driver = self.driver
        checkbox = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'))
        checkbox.click()
        self.checkChart()
    
    def test_data_type(self):
        driver = self.driver
        data_types = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'))
        data_types.click()
        total_deaths = self.getElement((By.ID, 'bui-10'))
        total_deaths.click()
        self.checkChart()
    
    def test_chart_type(self):
        driver = self.driver
        chart_types = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div/div/div[1]'))
        chart_types.click()
        bar_chart = self.getElement((By.ID, 'bui-10'))
        bar_chart.click()
        self.checkChart()

    def test_slider(self):
        driver = self.driver
        slider = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div/div'))
        action_chains = ActionChains(driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        self.checkChart()

    def tearDown(self):
        self.driver.close()