import pandas as pd
import os

# Pfad zur Datei im Repository
CSV_DATEI = "datenbank.csv"

def lade_eintraege(typ):
    """Liest die CSV-Datei und gibt sie als Liste von Dictionaries zurück."""
    if not os.path.exists(CSV_DATEI):
        return []
    
    df = pd.read_csv(CSV_DATEI)
    
    # Filtere nach dem übergebenen Typ, falls Daten vorhanden
    if 'Typ' in df.columns:
        df = df[df['Typ'] == typ]
        
    return df.to_dict('records')

def speichere_eintrag(datenbank_typ, typ, kategorie, betrag, datum):
    """Speichert einen neuen Eintrag in die CSV."""
    neue_zeile = {
        'ID': '', 
        'Bereich': datenbank_typ, 
        'Typ': typ, 
        'Kategorie': kategorie, 
        'Betrag': betrag, 
        'Datum': datum, 
        'Zusatz': ''
    }
    
    # Wenn Datei nicht existiert, neue erstellen
    if not os.path.exists(CSV_DATEI):
        df = pd.DataFrame([neue_zeile])
        df.to_csv(CSV_DATEI, index=False)
    else:
        # Bestehende Datei laden, neue Zeile anhängen und speichern
        df = pd.read_csv(CSV_DATEI)
        df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
        df.to_csv(CSV_DATEI, index=False)
