import xml.etree.ElementTree as ET

import requests
import urllib.request


r = urllib.request.urlopen('https://sokme.ua/product-category/kukhni').read()

# tree = ET.fromstring(r)
# root = tree.getroot()

print(r)
