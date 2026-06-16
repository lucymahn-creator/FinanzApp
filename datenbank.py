import os
import pandas as pd

# 1. Wir lassen uns den Pfad ausgeben, den Streamlit wirklich sieht
print(f"Aktuelles Arbeitsverzeichnis: {os.getcwd()}")
print(f"Dateien im Verzeichnis: {os.listdir('.')}")

# 2. Versuch, die Datei explizit zu laden
def lade_eintraege():
    try:
        # Wir laden die Datei direkt aus dem Hauptverzeichnis
        df = pd.read_csv("datenbank.csv")
        return df
    except Exception as e:
        print(f"FEHLER beim Laden der CSV: {e}")
        return pd.DataFrame() # Leeres DataFrame bei Fehler
