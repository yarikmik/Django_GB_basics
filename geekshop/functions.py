import json


def get_json_data(page):
    with open('geekshop/json_data.json', encoding='utf-8-sig') as file:
        json_data = json.load(file)
    return json_data[page]


def get_json_products_data(file_path):
    with open(file_path, encoding='utf-8-sig') as file:
        json_data = json.load(file)
    return json_data


# print(get_json_products_data('geekshop/json_products_data.json'))
# print(get_json_data('products'))
