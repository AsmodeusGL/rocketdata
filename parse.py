import json
import requests


def parse_kfc(url):
    response = requests.get(url).text
    data = json.loads(response)
    list_ = [item['storePublic'] for item in data['searchResults']]
    return list_


with open('kfc.json', 'w', encoding='utf-8') as file:
    main_arr = []
    for item in parse_kfc('https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'):
        dictionary = {'name': item['title']['ru'], 'latlon': item['contacts']['coordinates']['geometry']['coordinates'], 'phones': item['contacts']['phoneNumber']}
        try:
            dictionary['address'] = item['contacts']['streetAddress']['ru']
        except KeyError:
            dictionary['address'] = item['contacts']['streetAddress']
        if item['openNow'] == True:
            timetable = []
            for days in item['openingHours']['regularDaily']:
                timetable.append(days['weekDayName'] + '    ' + days['timeFrom'] + '-' + days['timeTill'])
            dictionary['working_hours'] = timetable
        else:
            dictionary['working_hours'] = 'closed'
        main_arr.append(dictionary)
    json.dump(main_arr, file, ensure_ascii=False, indent=3)
