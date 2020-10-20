import requests
import os

from bs4 import BeautifulSoup

URL = 'https://sokme.ua/product-category/inshe'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
FOLDER = 'D:/meb'


def main():
    html = get_html(URL)
    get_url_item(html)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
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
                images = images_url.find_all('div', class_='woocommerce-product-gallery__image')
                for m in images:
                    n = m.find('a').get('href')
                    create_dir(text, n)


def create_dir(directory, n):
    name_dir = f'{FOLDER}/{directory}'
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
        if not check_image:
            p = requests.get(image, headers=HEADERS)
            out = open(f'{path}/{name}', "wb")
            out.write(p.content)
            out.close()


main()
