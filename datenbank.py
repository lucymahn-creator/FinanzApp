import easywebdav2
import pandas as pd
import io
import uuid 

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
    
    # 1. Daten laden
    buffer = io.BytesIO()
    client.download(REMOTE_PATH, buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    
    # 2. Neue Zeile mit UUID erstellen
    # uuid.uuid4().hex generiert eine einzigartige, zufällige Zeichenfolge
    neue_zeile = {
        "ID": uuid.uuid4().hex, 
        "Bereich": ber, 
        "Typ": typ, 
        "Kategorie": kat, 
        "Betrag": betrag, 
        "Datum": dat, 
        "Zusatz": zus
    }
    
    # Zeile hinzufügen
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    # 3. Datei zurückschreiben (mit dem Puffer-Fix vom letzten Mal)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    client.upload(output, REMOTE_PATH)
