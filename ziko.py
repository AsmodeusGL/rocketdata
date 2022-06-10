import json
import requests
from bs4 import BeautifulSoup


def parse_ziko(url):
    response = requests.get(url).text
    data = json.loads(response)
    return data


def bs4_ziko(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
    return [item.text for item in soup.find_all(class_='mp-table-address')]


with open('phones.txt', 'w', encoding='utf-8') as file:
    for el in bs4_ziko('https://www.ziko.pl/lokalizator/'):
        file.write(el)
        file.write('\n')


with open('ziko.json', 'w', encoding='utf-8') as file:
    main_arr = []
    for key, value in parse_ziko('https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies').items():
        dictionary = {'name': value['title'], 'latlon': [float(value['lat']), float(value['lng'])], 'address': value['address'], 'working_hours': value['mp_pharmacy_hours'].replace('<br>', '  ')}
        with open('phones.txt', 'r+', encoding='utf-8') as phones:
            for line in phones.readlines():
                if value['address'] in line:
                    line = line.partition('tel. ')[2]
                    index = line.find('Infolinia')
                    dictionary['phones'] = [line[:index], line.partition('Infolinia')[1] + line.partition('Infolinia')[2].strip()]
        main_arr.append(dictionary)
    json.dump(main_arr, file, ensure_ascii=False, indent=3)
