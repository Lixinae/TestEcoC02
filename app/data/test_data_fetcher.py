from unittest import TestCase

from app.data.data_fetcher import *


class TestDataFetcher(TestCase):
    def test_grab_data_from_api_ok(self):
        json_data = grab_data_from_api("2017-01-01T00:00:00","2017-01-02T00:00:00")
        self.assertEqual(48,len(json_data))

    def test_grab_data_from_api_no_data(self):
        json_data = grab_data_from_api("2010-01-01T00:00:00","2011-01-02T00:00:00")
        self.assertEqual(0,len(json_data))

    def test_filter_by_hour_ok(self):
        data = {
            'datetime': "2017-01-01T00:00:00"
        }
        out = filter_by_hour(data)
        self.assertTrue(out)

    def test_filter_by_hour_no_datetime(self):
        data = {
            'wrong_key_name': "2017-01-01T00:00:00"
        }
        out = filter_by_hour(data)
        self.assertFalse(out)

    def test_filter_by_hour_wrong_format(self):
        data = {
            'datetime': "2017-01-01T00:00:00"
        }
        out = filter_by_hour(data)
        self.assertFalse(out)

    def test_filter_co2_data_to_one_hour_frequence(self):
        self.fail()

    def test_convert_date_time_to_timestamp(self):
        self.fail()

    def test_interpolate_data(self):
        self.fail()

    def test_interpolate_all_data_from_tmp(self):
        self.fail()

    def test_generate_tmp_interpolated_data(self):
        self.fail()

    def test_interpolate_data_aux(self):
        self.fail()

    def setUp(self) -> None:
        self.input_data = [
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

        pass
