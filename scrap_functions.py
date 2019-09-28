from decimal import Decimal
import re


def create_dict(dictionary, id_link):
    dictionary.update({f'{id_link}': {
        'brand': [],
        'year': [],
        'engine': [],
        'price': [],
        'export': [],
        'diff': [],
        'link': [],
    }})


def get_id_link(car):
    link = [a['href'] for a in car.find_all('a', href=True) if a.text][0]
    link = f'{link[:21]}%{link[22:]}'
    return link


def get_link(link, car):
    temp_link = [a['href'] for a in car.find_all('a', href=True) if a.text][0]
    temp_link = f'{temp_link[:21]}%{temp_link[22:]}'
    link.append(temp_link)


def get_prices(price, export, difference, car):
    temp_price = [a.text for a in car.find_all('p') if '€' in a.text]
    diff = [Decimal(str(temp_price[0][2:])) - Decimal(str(temp_price[1][2:]))]
    price.append(temp_price[0])
    export.append(temp_price[1])
    difference.append(str(diff[0]))


def get_year(year, car):
    result = [a.text for a in car.find_all('span', {'class': "fltlt"})]
    find_year = re.search(r'201[6-9]', str(result[0]))
    if find_year:
        year_result = find_year.group()
    else:
        year_result = None
    year.append(year_result)


def get_engine(engine, car):
    result = [a.text for a in car.find_all('span', {'class': "fltlt"})]
    find_engine = re.search(r'fuel:\D+', str(result[1]))
    if find_engine:
        engine_result = find_engine.group()[5:].strip()
    else:
        engine_result = None
    engine.append(engine_result)


def get_brand(brand, car):
    car_brand = car.find('p', {'class': "merk"}).text[:-1]
    car_type = car.find('p', {'class': "type"}).text[1:-2]
    brand.append(f'{car_brand.capitalize()} {car_type.capitalize()}')
