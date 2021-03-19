from unittest import TestCase

from app.data.data_fetcher import *


class TestDataFetcher(TestCase):
    def test_grab_data_from_api_ok(self):
        ouput_data = grab_data_from_api("2017-01-01T00:00:00", "2017-01-02T00:00:00")
        self.assertEqual(200, ouput_data[0])
        self.assertEqual(48, len(ouput_data[1]))

    def test_grab_data_from_api_no_data(self):
        ouput_data = grab_data_from_api("2011-01-01T00:00:00", "2012-01-02T00:00:00")
        self.assertEqual(200, ouput_data[0])
        self.assertEqual(0, len(ouput_data[1]))

    def test_grab_data_from_api_wrong_input(self):
        ouput_data = None
        try:
            ouput_data = grab_data_from_api("blabla", "hello")
        except ValueError:
            self.assertTrue(ouput_data is None)
        self.assertTrue(ouput_data is None)

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
        output_data = filter_co2_data_to_one_hour_frequence(self.input_data)
        expected = [{'datetime': '2016-01-01T00:00:00', 'co2_rate': 36},
                    {'datetime': '2016-01-01T01:00:00', 'co2_rate': 44},
                    {'datetime': '2016-01-01T02:00:00', 'co2_rate': 37},
                    {'datetime': '2016-01-01T03:00:00', 'co2_rate': 48}]
        self.assertEqual(len(expected), len(output_data))
        i = 0
        for element in output_data:
            self.assertEqual(element, expected[i])
            i += 1
        self.assertEqual(len(expected), len(output_data))

    def test_convert_date_time_to_timestamp_ok(self):
        timestamp = convert_date_time_to_timestamp("2017-01-01T00:00:00")
        self.assertEqual(1483228800.0,timestamp)

    def test_convert_date_time_to_timestamp_wrong_input(self):
        timestamp = None
        try:
            timestamp = convert_date_time_to_timestamp("2017-01-01T:00:00")
        except ValueError:
            self.assertTrue(timestamp is None)
        self.assertTrue(timestamp is None)

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
