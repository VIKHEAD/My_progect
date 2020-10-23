import time

import requests
import os

import xlsxwriter
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

URL = 'https://sokme.ua/shop/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
FOLDER = 'D:/sokme'

adapter = HTTPAdapter(max_retries=3)
session = requests.Session()


def main():
    name_dir, url = get_category()
    html = get_html(url)
    get_url_item(name_dir, html)

def get_html(url):
    session.mount(url, adapter)
    r = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    time.sleep(8)
    if soup:
        return soup


def get_category():
    soup = get_html(URL)
    for li in soup.find_all('li', class_='category_thumbs'):
        name_dir = create_dir((li.get_text()).strip())
        return name_dir, li.a.get('href')


def get_url_item(name_dir, soup):
    block = soup.find_all('li', class_='category_thumbs category_list column')
    if block:
        for i in block:
            time.sleep(6)
            content_url = get_html(i.find('a').get('href'))
            sub_block = content_url.find('ul', id='products-grid').find_all('a', class_='product-title-link')
            for s in sub_block:
                time.sleep(3)
                images_url = get_html(s.get('href'))
                text = s.get_text()
                images = images_url.find_all('div', class_='woocommerce-product-gallery__image')
                for m in images:
                    time.sleep(5)
                    full_dir = create_dir(f'{name_dir}/{text}')
                    download_image(m.find('a').get('href'), full_dir)


def create_dir(directory):
    name_dir = f'{FOLDER}/{directory}'
    check_path = os.path.exists(name_dir)
    if not check_path:
        os.makedirs(name_dir)
    return name_dir


def download_image(image, path):
    if image:
        name = image.split("/")[-1]
        check_image = os.path.isfile(f'{path}/{name}')
        print(image, check_image)
        if not check_image:
            p = requests.get(image, headers=HEADERS)
            out = open(f'{path}/{name}', "wb")
            out.write(p.content)
            out.close()

# def write_exel(data_advert):
#     workbook = xlsxwriter.Workbook(f'{FOLDER}/sokme.xlsx')
#     worksheet = workbook.add_worksheet()
#     for data in data_advert:
#         worksheet.write('A' + str(data['number']), data['number'])
#         worksheet.write('B' + str(data['number']), data['name'])
#         worksheet.write('C' + str(data['number']), data['description'])
#     workbook.close()


main()
