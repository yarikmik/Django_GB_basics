import json


def get_json_data(page):
    with open('geekshop/json_data.json', encoding='utf-8-sig') as file:
        json_data = json.load(file)
    return json_data[page]

# print(get_json_data('index'))
