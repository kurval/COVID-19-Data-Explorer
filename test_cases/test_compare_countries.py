import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

class CompareCountries(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8501/")

    def test_check_cases_text(self):
        driver = self.driver
        cases = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'cases'))
        )
        self.assertIn("Confirmed Cases", cases.text)

    def test_check_deaths_text(self):
        driver = self.driver
        deaths = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'deaths'))
        )
        self.assertIn("Total Deaths", deaths.text)

    def test_chart_is_visible(self):
        driver = self.driver
        chart = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'marks'))
        )
        self.assertTrue(chart)
    
    def test_log_scale(self):
        driver = self.driver
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span'))
        )
        checkbox.click()
        self.test_chart_is_visible()
    
    def test_data_type(self):
        driver = self.driver
        data_types = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]'))
        )
        data_types.click()
        driver.find_element(By.ID, 'bui-10').click()
        self.test_chart_is_visible()
    
    def test_chart_type(self):
        driver = self.driver
        chart_types = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div/div/div[1]'))
        )
        chart_types.click()
        driver.find_element(By.ID, 'bui-10').click()
        self.test_chart_is_visible()

    def test_slider(self):
        element = self.driver.find_element(By.CSS_SELECTOR, "div[aria-valuenow='10']")
        target = self.driver.find_element(By.CSS_SELECTOR, "div[aria-valuenow='5']")
        action_chains = ActionChains(driver)
        action_chains.drag_and_drop(element, target).perform()
        self.test_chart_is_visible()
        pass

    def tearDown(self):
        self.driver.close()