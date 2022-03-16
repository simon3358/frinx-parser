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
            for interface in interface_group:
                interface_dic = {}
                interface_dic['name'] = key + str(interface['name'])
                interface_dic['config'] = json.dumps(interface)
                if interface.get('description'):
                    interface_dic['description'] = interface['description']
                else:
                    interface_dic['description'] = None
                if interface.get('mtu'):
                    interface_dic['max_frame_size'] = interface['mtu']
                else:
                    interface_dic['max_frame_size'] = None
                if interface.get('Cisco-IOS-XE-ethernet:channel-group'):
                    channel_number = interface['Cisco-IOS-XE-ethernet:channel-group']['number']
                    if not any(item['number'] == channel_number for item in port_channels):
                        channel_mode = interface['Cisco-IOS-XE-ethernet:channel-group']['mode']
                        channel_id = port_channels[-1]['number'] + 1 if port_channels else 1
                        port_channels.append({'id': channel_id, 'number': channel_number, 'mode': channel_mode})
                    else:
                        channel_id = next(item for item in port_channels if item["number"] == channel_number)['id']
                    interface_dic['port_channel_id'] = channel_id
                else:
                    interface_dic['port_channel_id'] = None
                interfaces.append(interface_dic)
        return interfaces, port_channels

    conn, cursor = start_connection()
    data = open_json(data_path)
    print('Data extracted from input, parsing...')
    interfaces, port_channels = parse_raw_data(data)
    print(f"Parsing ended, {len(interfaces)} interfaces and {len(port_channels)} port-channels finded.")
    insert_to_db(conn, cursor, interfaces, port_channels)
    print('Data inserted to database.')
    close_connection(conn, cursor)


insert_from_json('data/configClear_v2.json')
