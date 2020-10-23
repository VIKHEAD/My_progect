from datetime import time

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
FOLDER = 'D:/sokme'
insect = 0
adapter = HTTPAdapter(max_retries=3)
session = requests.Session()

def main():
    global insect
    while insect != 9:
        insect += 1
        html = get_html(URL[str(insect)])
        get_url_item(html)


def get_html(url):
    session.mount(url, adapter)
    r = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup:
        return soup


def get_url_item(soup):
    block = soup.find_all('li', class_='category_thumbs category_list column')
    if block:
        for i in block:
            content_url = get_html(i.find('a').get('href'))
            sub_block = content_url.find('ul', class_='products').find_all('a', class_='product-title-link')
            for s in sub_block:
                images_url = get_html(s.get('href'))
                text = s.get_text()
                # images = images_url.find_all('div', class_='woocommerce-product-gallery__image')
                description = images_url.find_all('div', class_='woocommerce-product-details__short-description')
                data_advert = []
                for a in description:
                    b = a.get_text()
                    data_advert.append(
                        {
                            'number': insect,
                            'name': text,
                            'description': b
                        }
                    )
                write_exel(data_advert)
                time.sleep(5)
                #
                # for m in images:
                # n = m.find('a').get('href')
                # create_dir(text, n)


# def get_advert():
#   data_advert.append(
#
#         )
#     write_exel(data_advert)


# def create_dir(directory, n):
#     name_dir = f'{FOLDER}/{insect}/{directory}'
#     check_path = os.path.exists(name_dir)
#     if not check_path:
#         print(name_dir)
#         os.makedirs(name_dir)
#     download_image(n, name_dir)
#
#
# def download_image(image, path):
#     if image:
#         name = image.split("/")[-1]
#         check_image = os.path.isfile(f'{path}/{name}')
#         print(image, check_image)
#         if not check_image:
#             p = requests.get(image, headers=HEADERS)
#             out = open(f'{path}/{name}', "wb")
#             out.write(p.content)
#             out.close()
#
def write_exel(data_advert):
    workbook = xlsxwriter.Workbook(f'{FOLDER}/Sokme.xlsx')
    worksheet = workbook.add_worksheet()
    for data in data_advert:
        worksheet.write('A' + str(data['number']), data['number'])
        worksheet.write('B' + str(data['number']), data['name'])
        worksheet.write('C' + str(data['number']), data['description'])
    workbook.close()


main()
