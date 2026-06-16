import csv
import os

# Sicherer Pfad: Datei liegt im selben Ordner wie datenbank.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DATEI = os.path.join(BASE_DIR, "datenbank.csv")

def lade_eintraege(typ):
    # Debugging: Wir lassen uns den Pfad anzeigen, um zu sehen, wo er sucht
    if not os.path.exists(CSV_DATEI):
        # Das wird im Log der Streamlit App angezeigt, wenn es fehlschlägt
        print(f"DEBUG: Datei nicht gefunden unter: {CSV_DATEI}")
        return []
    
    eintraege = []
    with open(CSV_DATEI, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if typ is None or row.get('Typ') == typ:
                eintraege.append(row)
    return eintraege
    eintraege = []
    with open(CSV_DATEI, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Wir filtern nach Typ, falls gewünscht
            if typ is None or row.get('Typ') == typ:
                eintraege.append(row)
    return eintraege

def speichere_eintrag(typ, kategorie, betrag, datum, zusatz=""):
    """Schreibt einen neuen Eintrag in die CSV."""
    file_exists = os.path.isfile(CSV_DATEI)
    
    with open(CSV_DATEI, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['ID', 'Bereich', 'Typ', 'Kategorie', 'Betrag', 'Datum', 'Zusatz']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            'ID': '', # Hier könntest du eine Logik für IDs einbauen
            'Bereich': 'Mobile',
            'Typ': typ,
            'Kategorie': kategorie,
            'Betrag': betrag,
            'Datum': datum,
            'Zusatz': zusatz
        })
