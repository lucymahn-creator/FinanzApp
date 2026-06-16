import easywebdav2
import pandas as pd
import io
import uuid # WICHTIG: Das Modul für eindeutige IDs

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
