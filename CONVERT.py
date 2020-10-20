import glob
import os

from PIL import Image

FOLDER = 'D:/sokme1'

def main():
    for i in len(FOLDER):
        print(i)


def convert_image():
    size = 1200, 900
    for images in glob.glob('*.jpeg'):  ##FOLDER ORIGINAL +.jpg or .jpeg
        file, ext = os.path.splitext(images)
        image = Image.open(images)
        print('##This image: ' + images + ' - RESOLUTION - ' + str(image.size))
        image.thumbnail(size)
        image = image.convert('RGB')
        image.save(file + '.jpeg', 'webp')
        print('#### Converted to: ' + file + '.jpeg - NEW RESOLUTION - ' + str(image.size))


main()
