# frinx-parser

## Prerequisites:
- Python 3.6+
- PostgreSQL 10+

## Database model:
- id SERIAL PRIMARY KEY,
- connection INTEGER,
- name VARCHAR(255) NOT NULL,
- description VARCHAR(255),
- config json,
- type VARCHAR(50),
- infra_type VARCHAR(50),
- port_channel_id INTEGER,
- max_frame_size INTEGER

## Description:
You need to extract device interface configuration from config.json file and store relevant
data to database. There are 10 BDI, 1 Loopback, 2 Port-channel, 4 TenGigabitEthernet
and 3 GigabitEthernet interfaces.
We are interested only on Port-channels and Ethernet interfaces. BDI and Loopback can
be ignored for now, but you solution should be able to handle BDI and Loopback in future.
In database we want to fill this fields, other can be null:
- id
- name
  - interface group name + interface name, for example &quot;TenGigabitEthernet0/0/5&quot;
- description
  - optional, interface description, for example &quot;member of Portchannel20&quot;
- max_frame_size
  - optional, mtu from interface configuration
- config
  - whole interface configuration
- port_channel_id
  - link Ethernet interfaces to Port-channel. This is defined in configuration by:
```
"Cisco-IOS-XE-ethernet:channel-group": {
  "number": 20,
  "mode": "active";
}
```
