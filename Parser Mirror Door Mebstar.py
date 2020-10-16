import requests
import os
import time
from bs4 import BeautifulSoup

URL = 'https://mebel-star.com/products/kupe/hm'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
FOLDER = 'D:\Download\Mebelstar\Fasad mirror'


def main():
    html = get_html(URL)
    get_content(html)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_content(soup):
    items = soup.find_all('div', class_='slide_params_am')
    for item in items:
        sub_class = item.find_all('a', class_='link_at_pict')
        get_image_url(sub_class)


def get_image_url(sub_class):
    for i in sub_class:
        image = i.get('href')
        create_dir(image)


def create_dir(image):
    check_path = os.path.exists(FOLDER)
    if not check_path:
        os.makedirs(FOLDER)
        print("###Created folder" + FOLDER)
    download_image(image, FOLDER)


def download_image(image, path):
    if image:
        name = image.split("/")[-1]
        check_image = os.path.isfile(path + '/' + name)
        print("##Check for availability: " + name + " - " + str(check_image))
        if not check_image:
            time.sleep(2)
            p = requests.get('https://mebel-star.com' + image, headers=HEADERS)
            out = open(path + '/' + name, "wb")
            out.write(p.content)
            out.close()
            print("##File downloaded: " + name)


main()
