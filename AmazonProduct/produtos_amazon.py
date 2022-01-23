from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
description = []
price = []

chrome_options = Options()
chrome_options.add_argument('__lang=pr-BR')
chrome_options.add_argument('__disable-notifications')
browser = webdriver.Chrome(options=chrome_options)

def search():
    browser.get(URL)
    browser.maximize_window()
    wdw(browser, TIMEOUT_DEFAULT).until(
        EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox'))
    )
    pesquisar = browser.find_element(By.ID, 'twotabsearchtextbox')
    pesquisar.send_keys('iphone', Keys.ENTER)

def get_product():
        global description
        global price
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        result = soup.find_all('div', {'data-component-type':'s-search-result'})
        print(len(result))
        for x in range(len(result)):
            try:
                item = result[x]
                atag = item.h2.a
                descriptions = item.find('span', 'a-size-base-plus a-color-base a-text-normal').text
                description.append(descriptions)
                price_parent = item.find('span', 'a-price')
                prices = price_parent.find('span', 'a-offscreen').text
                price.append(prices)

            except Exception as e:
                price.append('sem preço')
        browser.quit()

def data_save():
    data = {'Descrição do Produto': description, 'Preço': price}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    with pd.ExcelWriter('Produtos.xlsx') as path:
        df.to_excel(path, index=False, encoding='utf-8')

if __name__ == '__main__':
    search()
    get_product()
    data_save()
    print('Programa executado com sucesso!!!')