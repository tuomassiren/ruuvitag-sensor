"""
Get data for sensors using rx and write it to InfluxDB

Check guide and requirements from post_to_influxdb.py
"""

from influxdb import InfluxDBClient
from ruuvitag_sensor.ruuvi_rx import RuuviTagReactive

client = InfluxDBClient(host='localhost', port=8086, database='ruuvi')

def write_to_influxdb(received_data):
    """
    Convert data into RuuviCollecor naming schme and scale
    """
    dataFormat = received_data[1]['data_format'] if ('data_format' in received_data[1]) else None
    fields = {}
    fields['temperature']               = received_data[1]['temperature'] if ('temperature' in received_data[1]) else None
    fields['humidity']                  = received_data[1]['humidity'] if ('humidity' in received_data[1]) else None
    fields['pressure']                  = received_data[1]['pressure'] if ('pressure' in received_data[1]) else None
    fields['accelerationX']             = received_data[1]['acceleration_x'] if ('acceleration_x' in received_data[1]) else None
    fields['accelerationY']             = received_data[1]['acceleration_y'] if ('acceleration_y' in received_data[1]) else None
    fields['accelerationZ']             = received_data[1]['acceleration_z'] if ('acceleration_z' in received_data[1]) else None
    fields['batteryVoltage']            = received_data[1]['battery']/1000.0 if ('battery' in received_data[1]) else None
    fields['txPower']                   = received_data[1]['tx_power'] if ('tx_power' in received_data[1]) else None
    fields['movementCounter']           = received_data[1]['movement_counter'] if ('movement_counter' in received_data[1]) else None
    fields['measurementSequenceNumber'] = received_data[1]['measurement_sequence_number'] if ('measurement_sequence_number' in received_data[1]) else None
    fields['tagID']                     = received_data[1]['tagID'] if ('tagID' in received_data[1]) else None
    fields['rssi']                      = received_data[1]['rssi'] if ('rssi' in received_data[1]) else None
    json_body = [
        {
            'measurement': 'ruuvi_measurements',
            'tags': {
                'mac': received_data[0],
                'dataFormat': dataFormat
            },
            'fields': fields
        }
    ]
    client.write_points(json_body)


interval_in_ms = 5000

ruuvi_rx = RuuviTagReactive()

# Makes separate write to influxdb for each sensor as each subject generated by group_by is handled separately
ruuvi_rx.get_subject().\
    group_by(lambda x: x[0]).\
    subscribe(lambda x: x.sample(interval_in_ms).subscribe(write_to_influxdb))
