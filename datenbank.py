import os
import uuid
import csv
import requests
from requests.auth import HTTPBasicAuth
import threading  # NEU: Das ist der Schlüssel gegen das Aufhängen!

# --- DEINE ZUGANGSDATEN ---
NC_USER = "DEIN_NEXTCLOUD_BENUTZERNAME"
NC_PASS = "DEIN_APP_PASSWORT" 
NC_WEBDAV_URL = "https://cloud.zagorko.com/remote.php/webdav/Finanz-App/datenbank.csv"

# --- LOKALER CACHE ---
LOKALE_CSV = "datenbank_lokal.csv"
KOPF = ["ID", "Bereich", "Typ", "Kategorie", "Betrag", "Datum", "Zusatz"]

def lade_von_cloud():
    """Holt Updates aus der Cloud (z.B. von der Web-App) und speichert sie lokal."""
    try:
        # timeout=3 verhindert, dass die App bei schlechtem WLAN ewig wartet
        response = requests.get(NC_WEBDAV_URL, auth=HTTPBasicAuth(NC_USER, NC_PASS), timeout=3)
        if response.status_code == 200:
            with open(LOKALE_CSV, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print("Keine Verbindung zur Cloud (Lade lokale Daten).", e)

def _upload_im_hintergrund():
    """Lädt die Datei hoch, OHNE die Benutzeroberfläche einzufrieren."""
    try:
        with open(LOKALE_CSV, 'rb') as f:
            requests.put(NC_WEBDAV_URL, auth=HTTPBasicAuth(NC_USER, NC_PASS), data=f, timeout=5)
        print("Cloud-Sync im Hintergrund erfolgreich!")
    except Exception as e:
        print("Fehler beim Cloud-Upload:", e)

def speichere_in_cloud():
    """Startet den Upload auf einem separaten Zeitstrahl (Thread)."""
    threading.Thread(target=_upload_im_hintergrund).start()

# --- DATENBANK LOGIK ---
def _schreibe_alle(eintraege):
    # 1. Blitzschnelles lokales Speichern (Die App läuft sofort weiter)
    with open(LOKALE_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=KOPF)
        writer.writeheader()
        writer.writerows(eintraege)
    
    # 2. Stößt den Upload im Hintergrund an
    speichere_in_cloud()

def datenbank_vorbereiten():
    if not os.path.exists(LOKALE_CSV): 
        _schreibe_alle([]) 

def lade_eintraege(bereich=None):
    # Aktualisiert den lokalen Cache mit neuen Web-Einträgen
    lade_von_cloud()
    
    if not os.path.exists(LOKALE_CSV): 
        return []
        
    # Liest die Daten reibungslos von der lokalen Festplatte
    with open(LOKALE_CSV, 'r', encoding='utf-8') as f:
        return [row for row in csv.DictReader(f) if bereich is None or row.get("Bereich") == bereich]

def speichere_eintrag(ber, typ, kat, betrag, dat, zus=""):
    datenbank_vorbereiten()
    eintraege = lade_eintraege()
    neue_zeile = {
        "ID": uuid.uuid4().hex, "Bereich": ber, "Typ": typ, 
        "Kategorie": kat, "Betrag": str(betrag), "Datum": dat, "Zusatz": zus
    }
    eintraege.append(neue_zeile)
    _schreibe_alle(eintraege)

def loesche_eintrag(e_id):
    _schreibe_alle([e for e in lade_eintraege() if e.get("ID") != e_id])

def update_eintrag(e_id, ber, typ, kat, betrag, dat, zus=""):
    eintraege = lade_eintraege()
    for e in eintraege:
        if e["ID"] == e_id: 
            e.update({"Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": str(betrag), "Datum": dat, "Zusatz": zus})
    _schreibe_alle(eintraege)
