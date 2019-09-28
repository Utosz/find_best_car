#!/usr/bin/python3
import os
import bs4
import yagmail
import requests
import pymongo
import scrap_functions, db_functions, template


def connect_to_db():
    try:
        client = pymongo.MongoClient("localhost", 27017)
    except Exception as e:
        print(f'Problem with establishing connection to MongoDB : {e}')
    else:
        print(f'Successfully connected to MongoDB!')
        db = client['test_cars_db_2']
        print(f'Existing collections: {db.list_collection_names()}')
        return db


def connect_to_site(url):
    try:
        r = requests.get(url, headers={'User-agent': 'Super Bot 9000'})
    except Exception as e:
        print(f'Problem with establishing connection to site : {e}')
    else:
        print(f'Successfully connected to: {url}')
        return r.text


def find_cars():
    soup = bs4.BeautifulSoup(connector[0], "html.parser")
    all_divs = soup.find_all('div', {'class': "object3"})
    return all_divs


def runner():
    print('========================== Find Best Car ==========================')
    db_client = connect_to_db()
    site = connect_to_site(url)
    cars = db_client['cars']
    print('===================================================================')
    return site, cars


def temp_data():
    for car in find_cars():
        if car.find('p', {'class': "exportprijs"}):
            id_link = scrap_functions.get_id_link(car)
            scrap_functions.create_dict(cars_data, id_link)
            scrap_functions.get_link(cars_data[f'{id_link}']['link'], car)
            scrap_functions.get_prices(cars_data[f'{id_link}']['price'], cars_data[f'{id_link}']['export'],
                                       cars_data[f'{id_link}']['diff'], car)
            scrap_functions.get_year(cars_data[f'{id_link}']['year'], car)
            scrap_functions.get_brand(cars_data[f'{id_link}']['brand'], car)
            scrap_functions.get_engine(cars_data[f'{id_link}']['engine'], car)


def compare():
    data_to_email = {}
    for key in cars_data:
        car_status = db_functions.find_in_db(connector, {key: cars_data[key]})
        if not car_status:
            db_functions.add_to_db({key: cars_data[key]}, connector)
            data_to_email.update({key: cars_data[key]})
    return data_to_email


def data_creator():
    with open('template_data.txt', 'w', encoding='utf-8') as f:
        counter = 0
        for key in data_to_send:
            counter += 1
            f.write(f'============= Model {counter} =============\n')
            f.write(template.template_content(data_to_send[key]['brand'][0], data_to_send[key]['year'][0],
                                              data_to_send[key]['engine'][0], data_to_send[key]['price'][0],
                                              data_to_send[key]['export'][0],
                                              data_to_send[key]['diff'][0], data_to_send[key]['link'][0],
                                              'https://www.schadeautos.nl'))
            f.write('\n')


def send_email():
    receiver = "@gmail.com"
    with open('template_data.txt', 'r', encoding='utf-8') as f:
        body = f.read()
    yag = yagmail.SMTP("@gmail.com")
    yag.send(
        to=receiver,
        subject="Lista nowych samochodów",
        contents=body,
    )


url = 'https://www.schadeautos.nl/en/search/damaged/passenger%20cars+2016+2019/1/1/0/0/0/0/1/0?p=2016-2019'
connector = runner()

all_export = []
cars_data = {}
temp_data()
data_to_send = compare()
data_creator()
if data_to_send:
    print(f'Data to sending via email: {data_to_send}')
    send_email()
try:
    os.remove('template_data.txt')
except OSError as e:
    print(f'{e}')
