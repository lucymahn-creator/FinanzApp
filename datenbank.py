import requests
import pandas as pd
import io

# Deine URL
CLOUD_CSV_URL = "https://cloud.zagorko.com/s/DeinGeheimerCode/download" # WICHTIG: /download am Ende!

def lade_eintraege(typ=None):
    """Läd die Daten von deiner Nextcloud."""
    try:
        r = requests.get(CLOUD_CSV_URL)
        r.raise_for_status() # Prüft, ob der Download erfolgreich war
        df = pd.read_csv(io.StringIO(r.text))
        
        if typ:
            # Filtert nach Typ, wenn einer angegeben wurde
            return df[df['Typ'] == typ].to_dict('records')
        return df.to_dict('records')
    except Exception as e:
        print(f"Fehler beim Laden: {e}")
        return []

def speichere_eintrag(typ, kategorie, betrag, datum, zusatz=""):
    """
    Hinweis: In der Streamlit Cloud kannst du keine Dateien überschreiben.
    Hier müsstest du eine Datenbank nutzen oder das Sheet manuell pflegen.
    """
    print("Schreiben in der Cloud ist aktuell deaktiviert.")
