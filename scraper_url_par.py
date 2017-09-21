import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# make search to take url parameters like this:
# http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html?searchString=&morphology=on&pageNumber=1&sortDirection=false&recordsPerPage=_50&fz94=on&fz223=on&inclusionDateFrom=01.09.2017&inclusionDateTo=20.09.2017&lastUpdateDateFrom=&lastUpdateDateTo=&sortBy=UPDATE_DATEs 
container = []


def init_driver():
    driver = webdriver.Chrome('C:\\Users\\1\\chromedriver.exe')
    # driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, start, end):
    page_num = 1
    url_params = "http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html?searchString=&morphology=on&pageNumber={0}&sortDirection=false&recordsPerPage=_50&fz94=on&fz223=on&inclusionDateFrom={1}&inclusionDateTo={2}&lastUpdateDateFrom=&lastUpdateDateTo=&sortBy=UPDATE_DATE".format(page_num, start, end)
    driver.get(url_params)
    global container
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # parse data in td.greyText
    for tag in soup.find_all('tr'):
        text = tag.get_text()
        container.append(text)


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, '01072017', '01082017')
    container = pd.DataFrame(container)
    writer = pd.ExcelWriter('C:/Users/1/PyScripts/Scraper/output/dishonest_suppliers.xls')
    container.to_excel(writer, 'July 17')
    writer.save()
    time.sleep(5)
    driver.quit()