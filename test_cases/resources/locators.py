from selenium.webdriver.common.by import By

class PageLocators(object):
    CHART = (By.CLASS_NAME, 'marks')
    HEADER = (By.TAG_NAME, 'h2')
    CASES_TEXT = (By.CSS_SELECTOR, "#cases")
    DEATHS_TEXT = (By.CSS_SELECTOR, "#deaths")
    LOG_CHECKBOX = (By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span')
    COUNTRIES_DROP = (By.XPATH,'//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[5]/div/div/div/div[1]')
    DATA_DROP = (By.XPATH,'//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div/div/div[1]')
    CHART_DROP = (By.XPATH,'//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div/div/div[1]')
    SLIDER = (By.XPATH,'//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div/div')
    DROP_OPTION = (By.ID, 'bui-10')
    M_CHECKBOX = (By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/label/span')
    MOST_RADIO = (By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[2]/div[1]/div')
    WORLD_RADIO = (By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[4]/div[1]/div')
    CONTINENT_RADIO = (By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div/label[3]/div[1]/div')