import json
from db import start_connection, close_connection, insert_to_db

allowed_interfaces = [
    'Port-channel',
    'TenGigabitEthernet',
    'GigabitEthernet'
]


def insert_from_json(data_path):

    def open_json(data_path):
        with open(data_path) as json_file:
            data = json.loads(json_file.read())
        return data

    def parse_raw_data(data):
        port_channels = []
        interfaces = []
        raw_interfaces = data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']
        for key, interface_group in raw_interfaces.items():
            if not key in allowed_interfaces:
                continue

        return interfaces, port_channels

    conn, cursor = start_connection()
    data = open_json(data_path)
    print('Data extracted from input, parsing...')
    interfaces, port_channels = parse_raw_data(data)

    close_connection(conn, cursor)


insert_from_json('data/configClear_v2.json')
