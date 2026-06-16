import pandas as pd
import os

# Wir nutzen eine CSV, die direkt im selben Ordner wie datenbank.py liegt
CSV_DATEI = "datenbank.csv" 

def lade_eintraege(typ):
    # Wenn die Datei existiert, lade sie
    if os.path.exists(CSV_DATEI):
        df = pd.read_csv(CSV_DATEI)
        # Filtern nach Typ, falls gewünscht
        if typ:
            return df[df['Typ'] == typ].to_dict('records')
        return df.to_dict('records')
    else:
        return []

# HINWEIS: Schreiben in eine Datei in der Cloud ist kompliziert. 
# Für den Anfang: Fokus auf das Lesen der Daten!
