import csv
import os

# Pfad zur CSV-Datei
CSV_DATEI = "datenbank.csv"

def lade_eintraege(typ):
    """Liest alle Einträge aus der CSV."""
    if not os.path.exists(CSV_DATEI):
        return []
    
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
