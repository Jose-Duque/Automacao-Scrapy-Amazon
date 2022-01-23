from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wdw
from bs4 import BeautifulSoup
import pandas as pd


__author__ = 'José Carlos Duque Filho'
__email__ = 'joseduquefilho03@gmail.com'

TIMEOUT_DEFAULT = 10
URL = 'https://www.amazon.com.br/'

browser = webdriver.Chrome()

def search():
    browser.get(URL)
    wdw(browser, TIMEOUT_DEFAULT).until(
        EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox'))
    )
    pesquisar = browser.find_element(By.ID, 'twotabsearchtextbox')
    pesquisar.send_keys('iphone', Keys.ENTER)

def get_product():

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        result = soup.find_all('div', {'data-component-type':'s-search-result'})
        for x in range(len(result)):
            try:
                item = result[x]
                atag = item.h2.a
                descricao = atag.text.strip()
                price_parent = item.find('span', 'a-price')
                preco = price_parent.find('span', 'a-offscreen')
                print(descricao, preco.text.strip())
            except Exception as e:
                print(e)
search()
get_product()
# browser.quit()