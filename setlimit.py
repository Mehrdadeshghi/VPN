import requests
import json
import uuid
from datetime import datetime

# Server-URL und API-Key
SERVER_URL = "http://171.22.27.175:10086/api/savePeerScheduleJob"
API_KEY = "7VltsIi42nWtPF56qILcuf_mjFwUYDl34mErL5tEQe0"

# Benutzer nach Peer-Informationen fragen
configuration_name = input("Gib den Namen der Konfiguration ein: ")
peer_public_key = input("Gib den Public Key des Peers ein: ")
data_limit_gb = input("Gib das Datenlimit in GB ein: ")

# Aktuelles Datum und Uhrzeit
creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Generiere eine eindeutige Job-ID
job_id = str(uuid.uuid4())

# Daten für die Anfrage
data = {
    "Job": {
        "JobID": job_id,
        "Configuration": configuration_name,
        "Peer": peer_public_key,
        "Field": "total_data",
        "Operator": "lgt",  # 'eqt' steht für 'gleich'
        "Value": str(data_limit_gb),
        "CreationDate": "",
        "ExpireDate": "",  # Optional: Ablaufdatum des Jobs
        "Action": "restrict"  # Aktion, die ausgeführt wird, wenn das Limit erreicht ist
    }
}

# Header für die Anfrage
headers = {
    "Content-Type": "application/json",
    "wg-dashboard-apikey": API_KEY
}

# Debugging: Gesendete Anfrage anzeigen
print("\n--- Gesendete Anfrage ---")
print("URL:", SERVER_URL)
print("Headers:", json.dumps(headers, indent=4))
print("Daten:", json.dumps(data, indent=4))

# POST-Anfrage senden
response = requests.post(SERVER_URL, headers=headers, json=data)

# Debugging: Empfangene Antwort anzeigen
print("\n--- Empfangene Antwort ---")
print("Status Code:", response.status_code)
print("Headers:", json.dumps(dict(response.headers), indent=4))
try:
    print("Antwort JSON:", json.dumps(response.json(), indent=4))
except json.JSONDecodeError:
    print("Antwort Text:", response.text)

# Antwort ausgeben
if response.status_code == 200 and response.json().get("status"):
    print("Datenlimit erfolgreich gesetzt:", response.json())
else:
    print("Fehler beim Setzen des Datenlimits:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Text: {response.text}")
