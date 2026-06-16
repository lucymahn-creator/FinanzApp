import pandas as pd
import os

CSV_DATEI = "datenbank.csv"

def lade_eintraege(typ):
    # Pfad zur Datei im selben Verzeichnis wie app.py
    CSV_DATEI = "datenbank.csv" 
    if not os.path.exists(CSV_DATEI):
        return []
    
    # Datei einlesen
    df = pd.read_csv(CSV_DATEI)
    
    # Spaltennamen bereinigen, um Leerzeichen zu entfernen
    df.columns = df.columns.str.strip() 
    
    # Sicherstellen, dass 'Typ' existiert, bevor gefiltert wird
    if 'Typ' in df.columns and typ:
        df = df[df['Typ'] == typ]
    return df.to_dict('records')

def speichere_eintrag(datenbank_typ, typ, kategorie, betrag, datum, zusatz=""):
    neue_zeile = {
        'ID': '', 'Bereich': datenbank_typ, 'Typ': typ, 
        'Kategorie': kategorie, 'Betrag': betrag, 'Datum': datum, 'Zusatz': zusatz
    }
    if not os.path.exists(CSV_DATEI):
        df = pd.DataFrame([neue_zeile])
    else:
        df = pd.read_csv(CSV_DATEI, sep=';')
        df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    df.to_csv(CSV_DATEI, index=False)
