from aifc import Error
from datetime import datetime
import time
from random import randint

import requests
import os
import xlsxwriter
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

URL = {
    '1': 'https://sokme.ua/product-category/kukhni/',
    '2': 'https://sokme.ua/product-category/inshe/',
    '3': 'https://sokme.ua/product-category/vitalni/',
    '4': 'https://sokme.ua/product-category/dytiachi-yunacki-systemy/',
    '5': 'https://sokme.ua/product-category/peredpokoi/',
    '6': 'https://sokme.ua/product-category/spalni/',
    '7': 'https://sokme.ua/product-category/modulni-systemy/systema-oregon/',
    '8': 'https://sokme.ua/product-category/modulni-systemy/systema-bari/'
}

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
FOLDER = 'D:/sokme1'
insect = 0
data_advert = []
adapter = HTTPAdapter(max_retries=3)
session = requests.Session()


def main():
    global insect
    while insect != 8:
        insect += 1
        html = get_html(URL[str(insect)])
        get_url_item(html)


def get_html(url, params=None):
    session.mount(url, adapter)
    now = datetime.now().time()
    try:
        print(f'Try request...{now} - {url}')
        r = session.get(url, headers=HEADERS, params=params, timeout=3)
        if r.status_code != 200:
            print("r")
            get_html(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except Error as e:
        print(f'Error: {e}')
        get_html(url)


def get_url_item(soup):
    iteration = 0
    block = soup.find_all('li', class_='category_thumbs category_list column')
    if block:
        for i in block:
            content_url = get_html(i.find('a').get('href'))
            sub_block = content_url.find('ul', class_='products').find_all('a', class_='product-title-link')
            iteration += 1
            for s in sub_block:
                images_url = get_html(s.get('href'))
                text = s.get_text()
                # description = images_url.find_all('div', class_='woocommerce-product-details__short-description')
                # for a in description:
                #     iteration += 1
                #     print(iteration)
                #     b = a.get_text()
                #     data_advert.append(
                #         {
                #             'number': insect,
                #             'iteration': iteration,
                #             'name': text,
                #             'description': b
                #         }
                #     )
                #     write_exel(data_advert)
                images = images_url.find_all('div', class_='woocommerce-product-gallery__image')
                for m in images:
                    n = m.find('a').get('href')
                    create_dir(n, iteration)


def create_dir(n, text):
    name_dir = f'{FOLDER}/{insect}/{text}'
    check_path = os.path.exists(name_dir)
    if not check_path:
        print(name_dir)
        os.makedirs(name_dir)
    download_image(n, name_dir)


def download_image(image, path):
    if image:
        name = image.split("/")[-1]
        check_image = os.path.isfile(f'{path}/{name}')
        print(image, check_image)
        session.mount(image, adapter)
        if not check_image:
            try:
                p = session.get(image, headers=HEADERS)
                if p.status_code != 200:
                    print(p)
                    download_image(image, path)
                out = open(f'{path}/{name}', "wb")
                out.write(p.content)
                out.close()
            except Error as e:
                print(f"ERROR; {e}")


def write_exel(data_advert):
    workbook = xlsxwriter.Workbook(f'{FOLDER}/Sokme{insect}.xlsx')
    worksheet = workbook.add_worksheet()
    for data in data_advert:
        worksheet.write('A' + str(data['iteration']), data['number'])
        worksheet.write('B' + str(data['iteration']), data['iteration'])
        worksheet.write('C' + str(data['iteration']), data['name'])
        worksheet.write('D' + str(data['iteration']), data['description'])
    workbook.close()


main()
