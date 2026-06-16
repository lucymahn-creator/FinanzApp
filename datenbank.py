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
    
    # 1. Daten laden
    buffer = io.BytesIO()
    client.download(REMOTE_PATH, buffer)
    buffer.seek(0)
    df = pd.read_csv(buffer)
    
    # 2. Neue Zeile anhängen
    neue_zeile = {"ID": "", "Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": betrag, "Datum": dat, "Zusatz": zus}
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    
    # 3. Datei zurückschreiben - HIER IST DIE KORREKTUR
    # Wir erstellen ein BytesIO Objekt, in das wir die CSV schreiben
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0) # Zurück an den Anfang des Puffers springen
    
    # Wir übergeben den Puffer anstatt des langen Strings
    client.upload(output, REMOTE_PATH)
