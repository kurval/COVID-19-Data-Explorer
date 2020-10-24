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

    def movePage(self):
        button = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div'))
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(button).click().perform()
        time.sleep(2)
        
    def checkChart(self):
        wait = self.wait
        chart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'marks')))
        self.assertTrue(chart.is_displayed())

    def test_move_to_most_cases(self):
        self.movePage()
        cases = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[2]/div/h2'))
        self.assertEqual("COVID-19: total confirmed cases in the worst-hit countries", cases.text)
        self.checkChart()
    
    def test_data_type(self):
        self.movePage()
        data_types = getClickElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'))
        data_types.click()
        total_deaths = getClickElement((By.ID, 'bui-10'))
        total_deaths.click()
        time.sleep(1)
        deaths = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[2]/div/h2'))
        self.assertEqual("COVID-19: total deaths in the worst-hit countries", deaths.text)
        self.checkChart()

    def test_per_million(self):
        self.movePage()
        check_box = self.getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'))
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(check_box).click().perform()
        self.checkChart()

    def test_slider(self):
        self.movePage()
        time.sleep(1)
        slider = getElement((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div'))
        action_chains = ActionChains(self.driver)
        action_chains.click_and_hold(slider).move_by_offset(-40, 0).release().perform()
        self.checkChart()

    def tearDown(self):
        self.driver.close()