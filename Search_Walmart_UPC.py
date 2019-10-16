import requests
from bs4 import BeautifulSoup
from lxml import html

import re
import csv
import os
import pandas as pd
import json
from datetime import date
today = date.today()
directory = os.path.dirname(r"""C:/Users/lakshmana.kolasani/OneDrive - Fred's Inc/projects/Completed/webscraping_result/""")

upcs = pd.read_csv("C:/Users/lakshmana.kolasani/OneDrive - Fred's Inc/projects/Completed/webscraping_result/UPCs.csv")[['UPC']]

##### extracting links of specific products pages ######
product_page_links = []
for i in upcs['UPC']:
    page = requests.get("https://www.walmart.com/search/?cat_id=0&query={}".format(str(i).zfill(14)[:13][-12:]),headers={"User-Agent":"Defined"})
    soup = BeautifulSoup(page.content, 'html.parser')
    divTag = soup.find_all("div", {"id": "mainSearchContent"})
    for tag in divTag:
        tdTags = tag.find_all("a", {"class": "display-block"})
        for tag in tdTags:
            print(tag.attrs['href'])
            product_page_links.append('https://www.walmart.com'+tag.attrs['href'])

product_page_links = list(set(product_page_links))
with open('product_page_links.txt', 'w') as f:
    for item in product_page_links:
        f.write("%s/n" % item)

with open('product_page_links.txt') as f:
    product_page_links = f.read().split('/n')[:-1]

##### extracting product information from each product page ######
labels = ['UPC', 'Product', 'Price', 'Date Retrieved']
global df
df = pd.DataFrame(columns=labels)
i=0

for url in product_page_links:
    try:
        i=i+1
        page_link = requests.get(url)
        soup = BeautifulSoup(page_link.content, 'html.parser')
        title = soup.find_all('h1',attrs={"class":'prod-ProductTitle'})[0]['content']
        price = soup.find_all('span',attrs={"itemprop":'price',"class":'price-characteristic'})[0]['content']
        upctag = soup.find_all('script',attrs={"id":'item'})
        upc = re.findall(r'"upc":"(\d{12})',upctag[0].text)[0]
        print("{}) UPC-{} {} is priced ${} on Walmart website as on {}".format(i, upc, title, price, today))
        df.loc[len(df)] = [upc, title, price, today]
        # Outputting to the file
        df.to_csv(os.path.join(directory+'/walmart_pricing_data_3943.csv'), index=False, encoding = 'utf-8', chunksize=1000000)
    except:
        pass


