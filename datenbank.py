import csv
import requests
import io
import pandas as pd
import os

# Statt CSV_DATEI = "datenbank.csv"
CLOUD_CSV_URL = "https://cloud.zagorko.com/index.php/apps/files/files/5670?dir=/Finanz-App&openfile=true/download"

def get_data(typ):
    # Debugging: Was kommt vom Server an?
    antwort = requests.get(CLOUD_CSV_URL)
    st.write("Server-Antwort Inhalt (ersten 100 Zeichen):", antwort.text[:100])
    return pd.read_csv(io.StringIO(antwort.text))
    
def _schreibe_alle(eintraege):
    with open(CLOUD_CSV_URL, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=KOPF)
        writer.writeheader()
        writer.writerows(eintraege)

def datenbank_vorbereiten():
    if not os.path.exists(CLOUD_CSV_URL): 
        _schreibe_alle([]) 

def get_data(bereich=None):
    if not os.path.exists(CLOUD_CSV_URL): return []
    with open(CSV_DATEI, 'r', encoding='utf-8') as f:
        return [row for row in csv.DictReader(f) if bereich is None or row.get("Bereich") == bereich]

def speichere_eintrag(ber, typ, kat, betrag, dat, zus=""):
    datenbank_vorbereiten()
    with open(CLOUD_CSV_URL, 'a', newline='', encoding='utf-8') as f:
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
