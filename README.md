# pylutron_server
A simple http server written to interact with a [Lutron Caseta Wireless Smart Bridge](https://www.amazon.com/Lutron-Caseta-Wireless-Bridge-L-BDG2-WH/dp/B00XPW67ZM) to list and activate scenes (and possibly devices in the future) via http

# Installation / Usage
1. Clone the Repository
```
$ git clone https://github.com/michaelgaultjr/pylutron_server.git
```
2. Enter Directory
```
$ cd pylutron_server
```
3. Install required packages
```
$ pip3 install -r requirements.txt
```
5. Set `BRIDGE_HOST` environment variable (in `.env` or `export`)
```
BRIDGE_HOST=(your lutron bridge ip)
```
6. Press the pairing button on your Lutron Caseta Bridge then run `get_certs.py` (not required if you already have the certificates)
```
$ python3 get_certs.py
```
7. Start server
```
$ python3 main.py
```

# Environment Variables
```dosini
# Required
BRIDGE_HOST="192.168.1.1" # Lutron Castea Bridge IP

# Optional
HOST="0.0.0.0" # Server Host
PORT=8080 # Server Port
CASETA_KEY="caseta.key" # Lutron Caseta Certificate Key File
CASETA_CERT="caseta.crt" # Lutron Caseta Certificate File
BRIDGE_CERT="caseta-bridge.crt" # Lutron Caseta Bridge Certificate File
LEAP_PORT=8081 # Lutron Caseta LEAP Protocol Port
```