import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd


container = []

def init_driver():
    driver = webdriver.Chrome('C:\\Users\\1\\chromedriver.exe')
    # driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, start, end):
    driver.get('http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html#')
    try:
        ext_search = driver.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="setParametersLink"]/a')))
        ext_search.click()

        more_elems = driver.wait.until(EC.presence_of_element_located(
            (By.ID, '_50')))
        more_elems.click()
        # # select 50 elements from dropdown #_50
        start_box = driver.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="inclusionDateFrom"]')))
        time.sleep(1)
        start_box.click()
        start_box.send_keys(start)
        time.sleep(0.5)
                
        end_box = driver.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="inclusionDateTo"]')))
        end_box.click()
        end_box.send_keys(end)
        end_box.send_keys(Keys.RETURN)
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="searchButtonsBlock"]/div/span[2]')))
        button.click()

        global container
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # parse data in td.greyText
        for tag in soup.find_all('tr'):
            container.append(tag)

    except TimeoutException:
        print("Box or Button not found in zakupki.gov.ru")
 

if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, '01072017', '01082017')
    container = pd.DataFrame(container)
    writer = pd.ExcelWriter('C:/Users/1/PyScripts/Scraper/output/dishonest_suppliers.xls')
    container.to_excel(writer, 'July 17')
    writer.save()
    time.sleep(5)
    driver.quit()