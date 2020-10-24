from random import randint
import requests
import telebot
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from telebot import types

bot = telebot.TeleBot('1387361133:AAG2i-FJS1HCo8GYsPZB6ujTroOu9aqSMgg')
URL = 'https://burst.shopify.com/free-images'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'}
adapter = HTTPAdapter(max_retries=3)
session = requests.Session()
category = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('C:/Users/nebop/PycharmProjects/pythonProject/My_progect/BatmanComics_023.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, f"<b>Здороу був :-) {message.from_user.first_name} </b> \nКажи що хтівмсь...",
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'так' and 'хочу':
        bot.send_message(message.chat.id, "Вибирай з якоу категорії")
        html = get_html(URL)
        get_block(html)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        board = []
        for item in category:
            name = types.InlineKeyboardButton(item, callback_data=item)
            board.append(name)
        i = 0
        while len(board) > i:
            keyboard.add(board[i], board[i + 1])
            i += 2
        bot.send_message(message.chat.id, f'Вибери категорію картинок', reply_markup=keyboard)
    elif message.text.lower() == 'ні' and 'ніт' and 'не хочу':
        sti = open('C:/Users/nebop/PycharmProjects/pythonProject/My_progect/BatmanComics_011.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, 'Жуй сраку...))')
    elif message.text.lower() == 'папа' and 'бувай':
        sti2 = open('C:/Users/nebop/PycharmProjects/pythonProject/My_progect/BatmanComics_024.webp', 'rb')
        bot.send_sticker(message.chat.id, sti2)
        bot.send_message(message.chat.id, "Я умиваюсь звідсика поки поштарка Оксана не прийшла.....")
    elif message.text:
        bot.send_message(message.chat.id,
                         f"Ніц не можу помочи {message.from_user.first_name}\n Можу дати лише катринку... Хоч?\n инструкция проста Так, Ні, Папа...")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            url = f'{URL}{category[call.data]}'
            html = get_html(url)
            image = get_images(html, url)
            bot.send_photo(call.message.chat.id, image)
    except Exception as e:
        print(repr(e))


def get_html(url):
    session.mount(url, adapter)
    r = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_block(soup):
    block = soup.find_all('div',
                          class_='grid__item grid__item--tablet-up-half grid__item--desktop-up-third gutter-bottom')
    for item in block:
        category_name = item.find('h3').get_text()
        category_url = item.find('a').get('href')
        category.update({category_name: category_url})


def get_images(soup, url):
    block = soup.find_all('a', class_='photo-tile__image-wrapper')
    random_number = block[randint(0, len(block))]
    image_url = f"https://burst.shopify.com{random_number.get('href')}"
    html = get_html(image_url)
    img = html.find('img').get('src')
    return img


bot.polling(none_stop=True)
