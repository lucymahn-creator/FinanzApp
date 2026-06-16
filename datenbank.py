import pandas as pd
import os

CSV_DATEI = "datenbank.csv"

def lade_eintraege(typ):
    if not os.path.exists(CSV_DATEI):
        return []
    df = pd.read_csv(CSV_DATEI)
    # Filtern nach Typ, wenn übergeben
    if typ and 'Typ' in df.columns:
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
        df = pd.read_csv(CSV_DATEI)
        df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    df.to_csv(CSV_DATEI, index=False)
