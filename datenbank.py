import csv
import os
import uuid


def datenbank_vorbereiten():
    if not os.path.exists(CSV_DATEI):
        # Initialisierung...
        pass

CSV_DATEI = "datenbank.csv"
KOPF = ["ID", "Bereich", "Typ", "Kategorie", "Betrag", "Datum", "Zusatz"]

def _schreibe_alle(eintraege):
    with open(CSV_DATEI, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=KOPF)
        writer.writeheader()
        writer.writerows(eintraege)

def datenbank_vorbereiten():
    if not os.path.exists(CSV_DATEI): 
        _schreibe_alle([]) 

def lade_eintraege(bereich=None):
    if not os.path.exists(CSV_DATEI): return []
    with open(CSV_DATEI, 'r', encoding='utf-8') as f:
        return [row for row in csv.DictReader(f) if bereich is None or row.get("Bereich") == bereich]

def speichere_eintrag(ber, typ, kat, betrag, dat, zus=""):
    datenbank_vorbereiten()
    with open(CSV_DATEI, 'a', newline='', encoding='utf-8') as f:
        csv.DictWriter(f, fieldnames=KOPF).writerow({
            "ID": uuid.uuid4().hex, "Bereich": ber, "Typ": typ, 
            "Kategorie": kat, "Betrag": str(betrag), "Datum": dat, "Zusatz": zus
        })

def loesche_eintrag(e_id):
    _schreibe_alle([e for e in lade_eintraege() if e.get("ID") != e_id])

def update_eintrag(e_id, ber, typ, kat, betrag, dat, zus=""):
    eintraege = lade_eintraege()
    for e in eintraege:
        if e["ID"] == e_id: 
            e.update({"Bereich": ber, "Typ": typ, "Kategorie": kat, "Betrag": str(betrag), "Datum": dat, "Zusatz": zus})
    _schreibe_alle(eintraege)
