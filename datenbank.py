import pandas as pd
import io
import uuid
import requests
from requests.auth import HTTPBasicAuth

# Exakt derselbe WebDAV-Link wie in deiner anderen App!
NC_WEBDAV_URL = "https://cloud.zagorko.com/remote.php/webdav/Finanz-App/datenbank.csv"

def get_df_from_cloud(user, password):
    """Lädt die CSV direkt aus der Nextcloud in einen Pandas DataFrame."""
    response = requests.get(NC_WEBDAV_URL, auth=HTTPBasicAuth(user, password))
    
    if response.status_code == 200:
        # Die Datei wurde gefunden und heruntergeladen
        return pd.read_csv(io.BytesIO(response.content))
    else:
        # Falls die Datei nicht existiert, erstelle eine leere Tabelle
        return pd.DataFrame(columns=["ID", "Bereich", "Typ", "Kategorie", "Betrag", "Datum", "Zusatz"])

def lade_eintraege(user, password, bereich=None):
    df = get_df_from_cloud(user, password)
    if bereich and not df.empty and 'Bereich' in df.columns:
        df = df[df['Bereich'] == bereich]
    return df.to_dict('records')

def speichere_eintrag(user, password, ber, typ, kat, betrag, dat, zus=""):
    # 1. Aktuellste Version laden
    df = get_df_from_cloud(user, password)
    
    # 2. Neue Zeile anhängen
    neue_zeile = {
        "ID": uuid.uuid4().hex, 
        "Bereich": ber, 
        "Typ": typ, 
        "Kategorie": kat, 
        "Betrag": betrag, 
        "Datum": dat, 
        "Zusatz": zus
    }
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    # 3. Den DataFrame zurück in eine CSV im Arbeitsspeicher verwandeln
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # 4. CSV direkt als Datenstrom in die Nextcloud hochladen
    response = requests.put(
        NC_WEBDAV_URL, 
        auth=HTTPBasicAuth(user, password), 
        data=output.read()
    )
    
    if response.status_code not in [200, 201, 204]:
        print(f"Fehler beim Speichern! Status: {response.status_code}")
