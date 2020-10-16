import requests
import os
from bs4 import BeautifulSoup

URL = 'https://sokme.ua/product-category/kukhni/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
FOLDER = 'sokme/'


def main():
    html = get_html(URL)
    get_url_item(html)

    # get_content(html)


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
            sub_block = content_url.find('ul', id='products-grid')
            for s in sub_block:
                second_url = s.find_all('a', class_='product-title-link')
                # name = s.find_all('h3')
                print(second_url)
                # images_url = get_html(second_url)
                # images = images_url.find_all('div', id='product-gallery')
        #         for m in images:
        #             print(m)


# def get_content(soup):
#     items = soup.find_all('div', class_='item-page')
#     for item in items:
#         sub_class = item.find_all('a')
#         for i in sub_class:
#             image = i.get('href')
#             if str(image).find('.jpg')!=-1:
#                 create_dir(image)
#
#
# def create_dir(image):
#     check_path = os.path.exists(FOLDER)
#     if not check_path:
#         os.makedirs(FOLDER)
#     download_image(image, FOLDER)
#
#
# def download_image(image, path):
#     if image:
#         name = image.split("/")[-1]
#         check_image = os.path.isfile(path + '/' + name)
#         print(image, check_image)
#         if not check_image:
#             p = requests.get('https://mebel-star.com' + image, headers=HEADERS)
#             out = open(path + '/' + name, "wb")
#             out.write(p.content)
#             out.close()


main()
