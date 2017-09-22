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
import xlsxwriter
import numpy as np

# change start and end to choose different period to make report for
container = pd.DataFrame()
num_rec = 0
start = '01.07.2017'
end = '01.08.2017'


# write date generator which takes start date and number of monthes
# we need our scraper to parse data for


def init_driver():
    driver = webdriver.Chrome('C:\\Users\\1\\chromedriver.exe')
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, start, end, page_num):
    global container
    url_params = "http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html?searchString=&morphology=on&pageNumber={0}&sortDirection=false&recordsPerPage=_50&fz94=on&fz223=on&inclusionDateFrom={1}&inclusionDateTo={2}&lastUpdateDateFrom=&lastUpdateDateTo=&sortBy=UPDATE_DATE".format(page_num, start, end)
    driver.get(url_params)
    
    # pages = 20

    # try:
    #     records = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/p')
    #     rec_text = records.get_attribute('innerText')
    #     num_rec = int(rec_text[-3:])
    #     pages = math.ceil(num_rec/50)
    # except:
    #     pass

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    data = []
    for tag in soup.find_all('tr'):
        text = tag.get_text()
        data.append(text)
        container = pd.DataFrame(data)

    # terminator = 1
    # while terminator <= pages:
    #     terminator += 1
    #     lookup(driver, start, end, terminator)

# get value of finded items divide it by 50 and ceil

if __name__ == "__main__":
    driver = init_driver()
    writer = pd.ExcelWriter('C:/Users/1/PyScripts/Scraper/output/dishonest_suppliers_{0}-{1}.xls'.format(start, end))
    for n in range(1, 21):
        lookup(driver, start, end, n)
        container.to_excel(writer, 'page{0}'.format(n))
        writer.save()
    time.sleep(2)
    driver.quit()