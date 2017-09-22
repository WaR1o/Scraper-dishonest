import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

pages = 1
container = []

def init_driver():
    driver = webdriver.Chrome('C:\\Users\\1\\chromedriver.exe')
    # driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, start, end, page_num):
    url_params = "http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html?searchString=&morphology=on&pageNumber={0}&sortDirection=false&recordsPerPage=_50&fz94=on&fz223=on&inclusionDateFrom={1}&inclusionDateTo={2}&lastUpdateDateFrom=&lastUpdateDateTo=&sortBy=UPDATE_DATE".format(page_num, start, end)
    driver.get(url_params)
    try:
      
        global container
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        data = []
        for tag in soup.find_all('tr'):
            container.append(tag)
            text = tag.get_text()
            data.append(text)
            container.append(data)

    except TimeoutException:
        print("Page zakupki.gov.ru is not fully loaded")
 

if __name__ == "__main__":
    driver = init_driver()
    start = '01.09.2016' # dates must be dot separated
    end = '01.10.2016'
    url_params = "http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html?searchString=&morphology=on&pageNumber={0}&sortDirection=false&recordsPerPage=_50&fz94=on&fz223=on&inclusionDateFrom={1}&inclusionDateTo={2}&lastUpdateDateFrom=&lastUpdateDateTo=&sortBy=UPDATE_DATE".format(1, start, end)
    driver.get(url_params)

    records = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/p')
    rec_text = records.get_attribute('innerText')
    num_rec = int(rec_text[-3:])
    pages = math.ceil(num_rec/50)

    for i in range(1, pages):
        lookup(driver, start, end, i)
        
    container = pd.DataFrame(container)
    writer = pd.ExcelWriter('C:/Users/1/PyScripts/Scraper/output/dishonest_suppliers{0}-{1}.xls'.format(start, end))
    container.to_excel(writer, 'result')
    writer.save()
    time.sleep(3)
    driver.quit()