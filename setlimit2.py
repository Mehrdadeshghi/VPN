import requests
import json
import uuid
from datetime import datetime, timedelta

# Server-URL und API-Key
SERVER_URL = "http://171.22.27.175:10086/api/savePeerScheduleJob"
API_KEY = "7VltsIi42nWtPF56qILcuf_mjFwUYDl34mErL5tEQe0"

# Benutzer nach Peer-Informationen fragen
configuration_name = input("Gib den Namen der Konfiguration ein: ")
peer_public_key = input("Gib den Public Key des Peers ein: ")
data_limit_gb = input("Gib das Datenlimit in GB ein: ")
expiry_days = int(input("Gib die Anzahl der Tage bis zum Ablaufdatum ein: "))

# Aktuelles Datum und Ablaufdatum berechnen
creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime("%Y-%m-%d %H:%M:%S")

# Generiere zwei eindeutige Job-IDs
job_id_limit = str(uuid.uuid4())
job_id_expiry = str(uuid.uuid4())

# Daten für das Datenlimit-Job
data_limit = {
    "Job": {
        "JobID": job_id_limit,
        "Configuration": configuration_name,
        "Peer": peer_public_key,
        "Field": "total_data",
        "Operator": "lgt",  # 'lgt' steht für 'größer als'
        "Value": str(data_limit_gb),
        "CreationDate": "",
        "ExpireDate": expiry_date,  # Ablaufdatum setzen
        "Action": "restrict"  # Aktion, die ausgeführt wird, wenn das Limit erreicht ist
    }
}

# Daten für das Ablaufdatum-Job
data_expiry = {
    "Job": {
        "JobID": job_id_expiry,
        "Configuration": configuration_name,
        "Peer": peer_public_key,
        "Field": "date",
        "Operator": "lgt",  # 'egt' steht für 'größer oder gleich'
        "Value": expiry_date,
        "CreationDate": "",
        "ExpireDate": expiry_date,
        "Action": "disable"  # Aktion, die ausgeführt wird, wenn das Ablaufdatum erreicht ist
    }
}

# Header für die Anfrage
headers = {
    "Content-Type": "application/json",
    "wg-dashboard-apikey": API_KEY
}

# Debugging: Gesendete Anfragen anzeigen
print("\n--- Gesendete Anfrage für Datenlimit ---")
print("URL:", SERVER_URL)
print("Headers:", json.dumps(headers, indent=4))
print("Daten:", json.dumps(data_limit, indent=4))

# POST-Anfrage für das Datenlimit senden
response_limit = requests.post(SERVER_URL, headers=headers, json=data_limit)

print("\n--- Empfangene Antwort für Datenlimit ---")
print("Status Code:", response_limit.status_code)
print("Headers:", json.dumps(dict(response_limit.headers), indent=4))
try:
    print("Antwort JSON:", json.dumps(response_limit.json(), indent=4))
except json.JSONDecodeError:
    print("Antwort Text:", response_limit.text)

# Debugging: Gesendete Anfrage für Ablaufdatum anzeigen
print("\n--- Gesendete Anfrage für Ablaufdatum ---")
print("Daten:", json.dumps(data_expiry, indent=4))

# POST-Anfrage für das Ablaufdatum senden
response_expiry = requests.post(SERVER_URL, headers=headers, json=data_expiry)

print("\n--- Empfangene Antwort für Ablaufdatum ---")
print("Status Code:", response_expiry.status_code)
print("Headers:", json.dumps(dict(response_expiry.headers), indent=4))
try:
    print("Antwort JSON:", json.dumps(response_expiry.json(), indent=4))
except json.JSONDecodeError:
    print("Antwort Text:", response_expiry.text)

# Antwort ausgeben
if response_limit.status_code == 200 and response_limit.json().get("status") and response_expiry.status_code == 200 and response_expiry.json().get("status"):
    print("Datenlimit und Ablaufdatum erfolgreich gesetzt.")
else:
    print("Fehler beim Setzen des Limits oder Ablaufdatums:")
    print(f"Datenlimit Status Code: {response_limit.status_code}")
    print(f"Datenlimit Response: {response_limit.text}")
    print(f"Ablaufdatum Status Code: {response_expiry.status_code}")
    print(f"Ablaufdatum Response: {response_expiry.text}")
