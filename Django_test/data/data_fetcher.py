from django.contrib.sites import requests

from Django_test.models import C02


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


def fetch_all_data_from_db():
    all_co2_data = C02.objects.all()
    return all_co2_data

def filter_co2_data():
    pass