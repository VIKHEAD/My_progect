import glob
import os

from PIL import Image

size = 1200, 900
convert_from_format = 'jpg'
"""CONVERT AND RESIZE PICTURES IN CURRENT FOLDER(SAVE PROPORTIONS, DON`T DELETE ORIGINAL FILE)"""


def convert_image():
    for images in glob.glob(f'*.{convert_from_format}'):
        file, ext = os.path.splitext(images)
        image = Image.open(images)
        image.thumbnail(size)
        image = image.convert('RGB')
        image.save(f'{file}.jpeg', 'webp')


convert_image()
