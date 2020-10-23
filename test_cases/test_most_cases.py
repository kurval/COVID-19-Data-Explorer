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
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
        self.driver.get("http://localhost:8501/covid19dataexplorer.com/dev")

    def getElement(self, attr):
        driver = self.driver
        ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
        element = WebDriverWait(driver, 15 ,ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located(attr)
        )
        return element

    def movePage(self):
        driver = self.driver
        button = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'))
        button.click()
        time.sleep(2)
        
    def checkChart(self):
        driver = self.driver
        chart = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'marks'))
        )
        self.assertTrue(chart.is_displayed())

    def test_move_to_most_cases(self):
        driver = self.driver
        self.movePage()
        cases = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[2]/div/h2'))
        self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", cases.text)
        self.checkChart()
    
    def test_data_type(self):
        driver = self.driver
        self.movePage()
        data_types = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'))
        data_types.click()
        total_deaths = self.getElement((By.ID, 'bui-10'))
        total_deaths.click()
        #time.sleep(1)
        #deaths = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[2]/div/h2'))
        #self.assertEqual("COVID-19: total deaths in the worst-hit countries", deaths.text)
        self.checkChart()

    def test_per_million(self):
        driver = self.driver
        self.movePage()
        check_box = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'))
        check_box.click()
        self.checkChart()

    def test_slider(self):
        driver = self.driver
        self.movePage()
        time.sleep(1)
        slider = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div'))
        action_chains = ActionChains(driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        self.checkChart()

    def tearDown(self):
        self.driver.close()