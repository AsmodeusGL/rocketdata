import json
import requests
from bs4 import BeautifulSoup


def parse_monomah(url):
    response = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    return [item.text.strip() for item in soup.find('body').find_all(class_='shop')]


with open('monomah.json', 'w', encoding='utf-8') as file:
    main_arr = []
    for item in parse_monomah('https://monomax.by/map'):
        dictionary = {'address': item.partition("\n")[0], 'phones': item.partition("\n")[2]}
        main_arr.append(dictionary)
    json.dump(main_arr, file, ensure_ascii=False, indent=3)
