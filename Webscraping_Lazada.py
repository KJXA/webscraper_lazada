import os, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import numpy as np

#Construct the url to scrape from
url = 'https://www.lazada.sg/catalog/?'
search = input('Enter search term(s): ').replace(' ','+')
url += 'q=' + search

#Limit the search results fetched
page_limit = int(input('Enter the number of pages to search: '))

#Define the CSS selectors
price_CSS = 'div > '*11+'span[class]' 
title_CSS = 'div[data-item-id] a[title]'

#page=1 and page=2 returns the same search queries
page = 2

#Uses a headless browser
root = os.getcwd()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(os.path.join(root, 'chromedriver.exe'), chrome_options=chrome_options)
browser.get(url + '&page=' + str(page))

#List to store the price, name, and url of search queries
price_list = []
item_list = []
url_list = []

while page <= page_limit:
    print(browser.current_url)
    soup = BeautifulSoup(browser.page_source, 'html5lib')
    print("Check html:"+str(len(soup.getText())))
    price_soup = soup.select(price_CSS)
    title_soup = soup.select(title_CSS)
    print(title_soup[0])
    for i in range(len(price_soup)):
        if len(price_soup[i].contents)!=0 and 'SGD' in price_soup[i].contents[0]:
            price_list.append(price_soup[i].contents[0])
    for j in range(len(title_soup)):
        item_list.append(title_soup[j].get('title'))
        url_list.append(title_soup[j].get('href'))
    page += 1
    browser.get(url + '&page=' + str(page))

#Check that the results fetched match
##print("Number of prices: " + str(len(price_list)))
##print("Number of items: " + str(len(item_list)))
##print("Number of urls: " + str(len(url_list)))

#Preprocess the results
def convertprice(lst):
    return list(map(lambda x: float(re.sub('SGD','' ,x)), lst))
def converturl(lst):
    return list(map(lambda x: 'https://' + x, lst))
price_list = convertprice(price_list)
url_list = converturl(url_list)

#Sort and print out the items in accordance to prices
indices = np.argsort(price_list)
sorted_prices = np.array(price_list)[indices]
sorted_items = np.array(item_list)[indices]
sorted_urls = np.array(url_list)[indices]

for index, (item_sorted, price_sorted) in enumerate(zip(sorted_items, sorted_prices)):
    print("{0}){1}: ${2}".format(index+1, item_sorted, price_sorted))
    
#returns the item description and url according to the sorted index given
def geturl(index):
    print('{}: \n{}'.format(sorted_items[index-1], sorted_urls[index-1]))
    
browser.close()
browser.quit()
