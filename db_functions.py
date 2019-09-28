import pprint


def add_to_db(dict_input, connector):
    cars = connector[1]
    car_id = cars.insert_one(dict_input).inserted_id
    return car_id


def find_in_db(connector, dict_input=None):
    if not dict_input:
        existing_car = connector[1].find()
    else:
        existing_car = connector[1].find_one(dict_input)
    pprint.pprint(existing_car)
    if existing_car:
        return True
    else:
        return False
