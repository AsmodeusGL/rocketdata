import json
import requests


def parse_ziko(url):
    response = requests.get(url).text
    data = json.loads(response)
    return data


with open('ziko.json', 'w', encoding='utf-8') as file:
    main_arr = []
    for key, value in parse_ziko('https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies').items():
        dictionary = {'name': value['title'], 'latlon': [float(value['lat']), float(value['lng'])], 'address': value['address'], 'working_hours': value['mp_pharmacy_hours'].replace('<br>', '  ')}
        main_arr.append(dictionary)
    json.dump(main_arr, file, ensure_ascii=False, indent=3)
