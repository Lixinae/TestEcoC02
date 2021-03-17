# from Django_test.models import C02
import datetime
import json
from typing import List


def grab_data_from_api(start_time, end_time):
    """
    Récupère la data à partir de l'api d'ecoco2
    "http://api-recrutement.ecoco2.com/v1/data/?start_time="
    :param start_time: Date de début des données
    :param end_time: Date de fin des données
    """
    url = "http://api-recrutement.ecoco2.com/v1/data/"
    payload = {
        "start_time": start_time,
        "end_time": end_time,
    }
    headers = {
        # 'Authorization': 'Bearer SECRET_KEY',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response)
    json_data = response.json()
    # Pour chaque valeur json dans le tableau renvoyé
    # Créer une entrée dans la BDD

    return json_data


# def fetch_all_data_from_db():
#     all_co2_data = C02.objects.all()
#     return all_co2_data


# Format des données
co2_data = [
    {
        "datetime": "2016-01-01T00:00:00",
        "co2_rate": 36
    },
    {
        "datetime": "2016-01-01T00:30:00",
        "co2_rate": 49
    },
    {
        "datetime": "2016-01-01T01:00:00",
        "co2_rate": 44
    },
    {
        "datetime": "2016-01-01T01:30:00",
        "co2_rate": 40
    },
    {
        "datetime": "2016-01-01T02:00:00",
        "co2_rate": 37
    },
    {
        "datetime": "2016-01-01T02:30:00",
        "co2_rate": 36
    },
    {
        "datetime": "2016-01-01T03:00:00",
        "co2_rate": 48
    },
]


def filter_by_hour(value: json):
    date_splits = value["datetime"].split(":")
    # On sais que le 2e argument sera les minutes, 0 min -> heure pleine
    return date_splits[1] == "00"


def filter_co2_data_to_one_hour_frequence(all_co2_data: List):
    filtered_data = list(filter(filter_by_hour, all_co2_data))
    return filtered_data


def convert_date_time_to_time_stamp(date_time: str):
    return datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S').timestamp()


def interpolate_data(current_data, previous_data, next_data):
    current_data_time = convert_date_time_to_time_stamp(current_data["datetime"])  # X
    current_data_co2_rate = current_data["co2_rate"]  # On cherche à calculer cette valeur, Y

    previous_time = convert_date_time_to_time_stamp(previous_data["datetime"])  # X1
    previous_co2_rate = previous_data["co2_rate"]  # Y1

    next_time = convert_date_time_to_time_stamp(next_data["datetime"])  # X2
    next_co2_rate = next_data["co2_rate"]  # Y2
    # y = y1 + ((x – x1) / (x2 - x1) × (y2 - y1))
    co2_rate = previous_co2_rate + (
            (current_data_time - previous_time) / (next_time - previous_time) *
            (next_co2_rate - previous_co2_rate)
    )
    return co2_rate


# Données en entré filtré par heure
def interpolate_data_aux(filtered_data):
    interpolated_data_tmp = generate_tmp_interpolated_data(filtered_data)
    interpolated_data = interpolate_all_data_from_tmp(interpolated_data_tmp)
    return interpolated_data


def interpolate_all_data_from_tmp(interpolated_data_tmp):
    interpolated_data = []
    index = 0
    for data_tmp in interpolated_data_tmp:
        if data_tmp["co2_rate"] == -1:
            previous_data = interpolated_data_tmp[index - 1]
            next_data = interpolated_data_tmp[index + 1]
            data_interpolated = {
                'datetime': data_tmp["datetime"],
                'co2_rate': interpolate_data(current_data=data_tmp, previous_data=previous_data, next_data=next_data)
            }
            interpolated_data.append(data_interpolated)
        else:
            interpolated_data.append(data_tmp)
        index += 1
    return interpolated_data


def generate_tmp_interpolated_data(filtered_data):
    interpolated_data_tmp = []
    i = 0
    for data in filtered_data:
        interpolated_data_tmp.append(data)
        # On ne peut interpoler que si l'on a la donnée précédente et suivante
        # Donc le dernier élément ne doit pas être ajouté
        if i + 1 < len(filtered_data):
            date_splits = data["datetime"].split(":")
            date_splits[1] = "30"
            date_time = ":".join(date_splits)
            new_data_to_interpolate = {
                'datetime': date_time,
                'co2_rate': -1
            }
            interpolated_data_tmp.append(new_data_to_interpolate)
        i += 1
    return interpolated_data_tmp


filtered_data = filter_co2_data_to_one_hour_frequence(co2_data)
interpolated_data = interpolate_data_aux(filtered_data)

print(co2_data)
print(interpolated_data)
data_difference = [{
    'datetime': x["datetime"],
    'difference_abs': abs(x["co2_rate"] - y["co2_rate"])
} for x, y in zip(co2_data, interpolated_data)]

print(data_difference)
