import easywebdav2
import pandas as pd
import io

st.secrets["admin"]

REMOTE_PATH = "/Finanz-App/datenbank.csv"

def lade_eintraege(bereich=None):
    # Datei in einen Buffer laden
    buffer = io.BytesIO()
    client.download(REMOTE_PATH, buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    if bereich:
        df = df[df['Bereich'] == bereich]
    return df.to_dict('records')

def speichere_eintrag(ber, typ, kat, betrag, dat, zus=""):
    # 1. Daten laden
    buffer = io.BytesIO()
    client.download(REMOTE_PATH, buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    
    # 2. Neue Zeile anhängen
    neue_zeile = {"ID": "", "Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": betrag, "Datum": dat, "Zusatz": zus}
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    # 3. Datei zurückschreiben
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    client.upload(csv_buffer.getvalue(), REMOTE_PATH)
