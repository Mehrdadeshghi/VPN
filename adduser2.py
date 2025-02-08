import sqlite3
import requests
import subprocess

# Server-URL und API-Schlüssel
SERVER_URL = "http://171.22.27.175:10086/api/addPeers/wg1"
API_KEY = "7VltsIi42nWtPF56qILcuf_mjFwUYDl34mErL5tEQe0"

# Verbindung zur SQLite-Datenbank
DB_PATH = "/root/WGDashboard/src/db/wgdashboard.db"

def generate_wireguard_keys():
    """
    Erstellt einen neuen privaten und öffentlichen Schlüssel für WireGuard.
    """
    private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
    public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode().strip()
    preshared_key = subprocess.check_output("wg genpsk", shell=True).decode().strip()
    return private_key, public_key, preshared_key

def get_next_available_ip():
    """
    Ermittelt die nächste verfügbare IP-Adresse im Format 20.0.0.X/32.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Bestehende IPs aus der Datenbank abrufen
    cursor.execute("SELECT allowed_ip FROM wg1")
    used_ips = {row[0].split('/')[0] for row in cursor.fetchall() if row[0]}

    conn.close()

    # IPs im Bereich 20.0.0.X durchgehen
    base_ip = "20.0.0."
    for i in range(1, 255):  # IP-Bereich von 20.0.0.1 bis 20.0.0.254
        new_ip = f"{base_ip}{i}"
        if new_ip not in used_ips:
            return f"{new_ip}/32"

    return None  # Falls kein freier Platz verfügbar ist

# Benutzer nach dem Namen fragen
username = input("Gib den Benutzernamen ein: ")

# Nächste freie IP-Adresse abrufen
next_ip = get_next_available_ip()

if not next_ip:
    print("Fehler: Keine verfügbaren IP-Adressen mehr.")
    exit(1)

# **NEU:** Dynamische Generierung der Keys
private_key, public_key, preshared_key = generate_wireguard_keys()

# Beispielwerte für die anderen Parameter (angepasst)
data = {
    "name": username,
    "allowed_ips": [next_ip],
    "private_key": private_key,
    "public_key": public_key,
    "preshared_key": preshared_key,
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
    print(f"Benutzer {username} erfolgreich hinzugefügt mit IP {next_ip}:")
    print(response.json())
else:
    print("Fehler beim Hinzufügen des Benutzers:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Text: {response.text}")
