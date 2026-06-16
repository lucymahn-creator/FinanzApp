import easywebdav2
import pandas as pd
import io

REMOTE_PATH = "remote.php/dav/files/admin/Finanz-App/datenbank.csv"

def get_client(user, password):
    return easywebdav2.connect(
        "cloud.zagorko.com",
        username=user,
        password=password,
        protocol="https"
    )

def lade_eintraege(user, password, bereich=None):
    client = get_client(user, password)
    buffer = io.BytesIO()
    client.download(REMOTE_PATH, buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    if bereich:
        df = df[df['Bereich'] == bereich]
    return df.to_dict('records')

def speichere_eintrag(user, password, ber, typ, kat, betrag, dat, zus=""):
    client = get_client(user, password)
    # Lade aktuelle Daten
    buffer = io.BytesIO()
    client.download(REMOTE_PATH, buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    
    # Neue Zeile anhängen
    neue_zeile = {"ID": "", "Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": betrag, "Datum": dat, "Zusatz": zus}
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    # Hochladen
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    client.upload(csv_buffer.getvalue(), REMOTE_PATH)
