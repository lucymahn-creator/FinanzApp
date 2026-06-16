import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Konfiguration
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Hier kommt deine JSON-Datei ins Spiel
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("FinanzAppDB").worksheet("Transaktion")

def lade_eintraege(typ):
    data = sheet.get_all_records()
    return data

def speichere_eintrag(typ, kategorie, betrag, datum, zusatz=""):
    # Zeile an Google Sheet anhängen
    sheet.append_row(["", "Transaktion", typ, kategorie, betrag, datum, zusatz])
