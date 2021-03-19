import json
from rest_framework.test import APITestCase

from app.data.data_fetcher import convert_date_time_to_timestamp
from app.models import RealDataC02, FilteredDataC02


class TestCo2RateData(APITestCase):
    def test_get_work_db_empty(self):
        response = self.client.get('/api/Get_Co2_Rate_Data/', {})
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.content))

    def test_get_work_data_in_db(self):
        input_data = [
            {"datetime": "2016-01-01T00:00:00", "co2_rate": 36},
            {"datetime": "2016-01-01T00:30:00", "co2_rate": 49},
            {"datetime": "2016-01-01T01:00:00", "co2_rate": 44},
            {"datetime": "2016-01-01T01:30:00", "co2_rate": 40},
            {"datetime": "2016-01-01T02:00:00", "co2_rate": 37},
            {"datetime": "2016-01-01T02:30:00", "co2_rate": 36},
            {"datetime": "2016-01-01T03:00:00", "co2_rate": 48},
            {"datetime": "2016-01-01T03:30:00", "co2_rate": 48},
        ]
        input_data_with_timestamp = [{
            "datetime": convert_date_time_to_timestamp(x["datetime"]),
            "co2_rate": x["co2_rate"]
        } for x in input_data]
        input_data_to_insert = [
            RealDataC02(datetime=data["datetime"], co2_rate=data["co2_rate"]) for data in input_data_with_timestamp
        ]
        RealDataC02.objects.bulk_create(input_data_to_insert)

        filtered_data = [
            {"datetime": "2016-01-01T00:00:00", "co2_rate": 36},
            {"datetime": "2016-01-01T01:00:00", "co2_rate": 44},
            {"datetime": "2016-01-01T02:00:00", "co2_rate": 37},
            {"datetime": "2016-01-01T03:00:00", "co2_rate": 48},
        ]
        filtered_data_with_timestamp = [{
            "datetime": convert_date_time_to_timestamp(x["datetime"]),
            "co2_rate": x["co2_rate"]
        } for x in filtered_data]
        filtered_data_data_to_insert = [
            FilteredDataC02(datetime=data["datetime"], co2_rate=data["co2_rate"]) for data in
            filtered_data_with_timestamp
        ]
        FilteredDataC02.objects.bulk_create(filtered_data_data_to_insert)

        response = self.client.get('/api/Get_Co2_Rate_Data/', {})
        json_data = json.loads(response.content)
        expected = [{'dt': '2016-01-01T01:00:00',
                     'r': 36, 'i': 36, 'dif': 0, 'm_jo_r': 36.0, 'm_we_r': 0, 'm_jo_i': 36.0, 'm_we_i': 0},
                    {'dt': '2016-01-01T01:30:00',
                     'r': 49, 'i': 40.0, 'dif': 9.0, 'm_jo_r': 42.5, 'm_we_r': 0, 'm_jo_i': 38.0, 'm_we_i': 0},
                    {'dt': '2016-01-01T02:00:00',
                     'r': 44, 'i': 44, 'dif': 0, 'm_jo_r': 43.0, 'm_we_r': 0, 'm_jo_i': 40.0, 'm_we_i': 0},
                    {'dt': '2016-01-01T02:30:00',
                     'r': 40, 'i': 40.5, 'dif': -0.5, 'm_jo_r': 42.25, 'm_we_r': 0, 'm_jo_i': 40.12, 'm_we_i': 0},
                    {'dt': '2016-01-01T03:00:00',
                     'r': 37, 'i': 37, 'dif': 0, 'm_jo_r': 41.2, 'm_we_r': 0, 'm_jo_i': 39.5, 'm_we_i': 0},
                    {'dt': '2016-01-01T03:30:00',
                     'r': 36, 'i': 42.5, 'dif': -6.5, 'm_jo_r': 40.33, 'm_we_r': 0, 'm_jo_i': 40.0, 'm_we_i': 0},
                    {'dt': '2016-01-01T04:00:00',
                     'r': 48, 'i': 48, 'dif': 0, 'm_jo_r': 41.43, 'm_we_r': 0, 'm_jo_i': 41.14, 'm_we_i': 0}]
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(expected), len(json_data))
        i = 0
        for element in json_data:
            self.assertEqual(element, expected[i])
            i += 1
