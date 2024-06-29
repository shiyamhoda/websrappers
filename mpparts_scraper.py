import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import date 


cur_date = str(date.today())


# Get a copy of the default headers that requests would use
headers = requests.utils.default_headers()

# Update the headers with your custom ones
# You don't have to worry about case-sensitivity with
# the dictionary keys, because default_headers uses a custom
# CaseInsensitiveDict implementation within requests' source code.
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

r = requests.get('https://mpparts.com/heavy-duty-truck-parts/air-systems')

soup = BeautifulSoup(r.text, 'html.parser')

products_list = soup.find_all('div', class_= "d-flex flex-column" )
products_list

product_links = []

for item in products_list:
    for link in item.find_all('a',href=True):
        #print(link['href'])
        product_links.append(link['href'])

product_links_cleaned = set(item for item in product_links if item not in (None, '') and not (isinstance(item, str) and item.isspace()))

items_list = []

for link in product_links_cleaned:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    part_number = soup.find_all('span', class_="g-font-weight-600")[1].text.strip()
    part_description = soup.find('h1', class_='h3 g-font-weight-400 mb-4').text.strip()
    uom = soup.find('span', class_ = 'g-font-weight-600').text.strip()
    unit_price = soup.find('span', class_ = 'g-color-black g-font-weight-500 g-font-size-28 mr-2 mt-1').text.strip()

    item = {
    'part_number': part_number,
    'part_description' : part_description,
    'uom' :uom,
    'unit_price': unit_price
    }
    items_list.append(item)
    print(f"Saving {item['part_number']}")

df = pd.DataFrame(items_list)

file_name = f'mpparts-{cur_date}.csv'

df.to_csv(file_name)