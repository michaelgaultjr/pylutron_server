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

# Web Interface
By default navigating to [`http://localhost:8080`](http://localhost:8080) will provide you with a simple web interface with a list of the scenes and their ids, and an `Activate` button to activate the respetive scene.

![Web Interface](/.github/images/web_interface.png)

<br>

# API

**Get Scenes**
----
  Returns a json array of scene ids.

* **Endpoint**

  `GET /api/scenes`

* **Success Response:**

  * **Code:** `200` <br />
    **Content:** `["1", "2", "3"]`
 

<br>

**Activate Scene**
----
  Activates a scene and returns scene id.

* **Endpoint**

  `POST /api/scenes`

* **Data Params**

  * `scene_id`: `string`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{scene_id}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `Scene '{scene_id}' not found"`

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `No 'scene_id' provided`

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `No body`
