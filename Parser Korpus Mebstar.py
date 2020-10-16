import requests
import os
from bs4 import BeautifulSoup

URL = 'https://mebel-star.com/products/kupe/info'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
FOLDER = 'Mebelstar'

iteration = 1


def main():
    html = get_html(URL)
    get_content(html)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_content(soup):
    items = soup.find_all('li', class_='uk-open')
    for item in items:
        title = item.find('a', class_='uk-accordion-title')
        if title:
            title = title.get_text()
        get_sub_content(item, title)


def get_sub_content(item, title, iteration=0):
    sub_folder = item.find_all('div', class_='uk-width-1-3@s')
    for sub_item in sub_folder:
        iteration += 1
        grid_line = sub_item.find('h2', class_='titles_grid')
        image = sub_item.find('a')
        if grid_line:
            grid_line = grid_line.get_text()
        if image:
            image = image.get('href')
        create_dir(title, grid_line, image)


def create_dir(folder_name, product_name, image):
    if folder_name == None:
        folder_name = "Folder" + '-' + str(iteration)
    if product_name == None:
        product_name = "Product" + '-' + str(iteration)
    path = FOLDER + '/' + folder_name + '/' + product_name
    check_path = os.path.exists(path)
    if not check_path:
        os.makedirs(path)
    download_image(image, path)


def download_image(image, path):
    if image:
        name = image.split("/")[-1]
        check_image = os.path.isfile(path + '/' + name)
        if not check_image:
            p = requests.get(image, headers=HEADERS)
            out = open(path + '/' + name, "wb")
            out.write(p.content)
            out.close()


main()
