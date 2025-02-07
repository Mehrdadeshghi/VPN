import requests
import json

# Server-URL und API-Schlüssel
SERVER_URL = "http://171.22.27.175:10086/api/addPeers/wg1"
API_KEY = "7VltsIi42nWtPF56qILcuf_mjFwUYDl34mErL5tEQe0"

# Benutzer nach dem Namen fragen
username = input("Gib den Benutzernamen ein: ")

# Beispielwerte für die anderen Parameter (diese sollten angepasst werden)
data = {
    "name": username,
    "allowed_ips": ["20.0.0.10/32"],
    "private_key": "EN6sCa50h0PHVdv7eBnY8siPSofmnJWEOmv4E9RnQXM=",
    "public_key": "k9g3jvLOkkjYUVQIgSOzvipikQBe7+el2u5dHzd2yAg=",
    "preshared_key": "Fwgw5H8xenVgyqOVr/rVEIy+vBi2nNiybjXiP45S5Rw=",
    "DNS": "1.1.1.1",
    "endpoint_allowed_ip": "0.0.0.0/0",
    "keepalive": 21,
    "mtu": 1420
}

# Header für die Anfrage
headers = {
    "Content-Type": "application/json",
    "wg-dashboard-apikey": API_KEY
}

# POST-Anfrage senden
response = requests.post(SERVER_URL, headers=headers, json=data)

# Antwort ausgeben
if response.status_code == 200:
    print("Benutzer erfolgreich hinzugefügt:", response.json())
else:
    print("Fehler beim Hinzufügen des Benutzers:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Text: {response.text}")
