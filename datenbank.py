import easywebdav2
import pandas as pd
import io
import uuid

REMOTE_PATH = "remote.php/dav/files/admin/Finanz-App/datenbank.csv" 

def get_client(user, password):
    return easywebdav2.connect("cloud.zagorko.com", username=user, password=password, protocol="https")

def get_df_from_cloud(client):
    buffer = io.BytesIO()
    try:
        client.download(REMOTE_PATH, buffer)
        buffer.seek(0)
        return pd.read_csv(buffer)
    except:
        # Falls Datei nicht existiert, erstelle neue Struktur
        df = pd.DataFrame(columns=["ID", "Bereich", "Typ", "Kategorie", "Betrag", "Datum", "Zusatz"])
        return df

def lade_eintraege(user, password, bereich=None):
    client = get_client(user, password)
    df = get_df_from_cloud(client)
    if bereich and not df.empty:
        df = df[df['Bereich'] == bereich]
    return df.to_dict('records')

def speichere_eintrag(user, password, ber, typ, kat, betrag, dat, zus=""):
    client = get_client(user, password)
    df = get_df_from_cloud(client)
    
    neue_zeile = {"ID": uuid.uuid4().hex, "Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": betrag, "Datum": dat, "Zusatz": zus}
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    client.upload(output, REMOTE_PATH)
