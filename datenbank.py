from webdav3.client import Client
import pandas as pd
import io
import csv

st.secrets["admin"]

client = Client(options)
REMOTE_PATH = "/Finanz-App/datenbank.csv"

def lade_eintraege(bereich=None):
    buffer = io.BytesIO()
    client.download_from(remote_path=REMOTE_PATH, local_path=buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    if bereich:
        df = df[df['Bereich'] == bereich]
    return df.to_dict('records')

def speichere_eintrag(ber, typ, kat, betrag, dat, zus=""):
    # 1. Aktuelle Daten laden
    df = pd.read_csv(io.BytesIO(client.content(REMOTE_PATH)))
    
    # 2. Neue Zeile hinzufügen
    neue_zeile = {"ID": "", "Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": betrag, "Datum": dat, "Zusatz": zus}
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    # 3. Zurück zur Nextcloud hochladen
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    client.upload_to(remote_path=REMOTE_PATH, local_path=csv_buffer.getvalue().encode('utf-8'))
