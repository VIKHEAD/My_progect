import os
from pdf2image import convert_from_path

FILE = 'D:/PATHer/MS_kitch_2k19.pdf'
SAVE_FOLDER = 'D:/Download/Miromark_catalog'


def from_pdf_to_webp():
    iteration = 0
    images = convert_from_path(FILE, size=(1200, None))
    check_path = os.path.exists(SAVE_FOLDER)
    if not check_path:
        os.makedirs(SAVE_FOLDER)
    for image in images:
        iteration += 1
        image = image.convert('RGB')
        image.save(f'{SAVE_FOLDER}/{iteration}.jpeg', 'webp')


from_pdf_to_webp()
