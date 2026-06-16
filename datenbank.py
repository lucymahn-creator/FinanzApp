import pandas as pd
import os

# "datenbank.csv" liegt im selben Ordner wie diese Datei (datenbank.py)
CSV_PFAD = "datenbank.csv"

def lade_eintraege(typ=None):
    """Läd die Daten direkt aus dem Repository-Ordner."""
    if not os.path.exists(CSV_PFAD):
        print(f"DEBUG: Datei {CSV_PFAD} nicht gefunden!")
        return []
    
    try:
        df = pd.read_csv(CSV_PFAD)
        # Wenn ein Typ gefiltert werden soll
        if typ:
            df = df[df['Typ'] == typ]
        return df.to_dict('records')
    except Exception as e:
        print(f"Fehler beim Lesen der CSV: {e}")
        return []
