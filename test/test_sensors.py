import pytest

from apps import sensors

class TestSensorData:
    def test_grouped_sensor_data(self):
        sensor_input = [
            [{'details': [],
              'install_date': '2017-09-02 00:00:00',
              'mwater_id': 5691533,
              'removal_date': '2018-10-09 09:55:00',
              'sensor_barcode': '6025'},
             {'details': {'sensor_uptime': 1, 'site_uptime': 0.14, 'status_id': 1},
              'install_date': '2018-10-09 10:24:00',
              'mwater_id': 5691533,
              'removal_date': None,
              'sensor_barcode': '7162'}],
              [{'details': {'sensor_uptime': 1, 'site_uptime': 0.08, 'status_id': 3},
               'install_date': '2018-08-14 07:43:00',
               'mwater_id': 15362287,
               'removal_date': None,
               'sensor_barcode': '7216'}]
        ]
            
        output = sensors.get_grouped_sensor_data(sensor_input)
        assert output[0][0]["barcode"] == '6025' 
        assert output[0][1]["barcode"] == '7216' 
        assert output[1][0]["barcode"] == '7162'
