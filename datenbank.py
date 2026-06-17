import pandas as pd
import io
import uuid
import requests
from requests.auth import HTTPBasicAuth

# Dein WebDAV-Link
NC_WEBDAV_URL = "https://cloud.zagorko.com/remote.php/webdav/Finanz-App/datenbank.csv"

def get_df_from_cloud(user, password):
    """Lädt die CSV direkt aus der Nextcloud in einen Pandas DataFrame."""
    response = requests.get(NC_WEBDAV_URL, auth=HTTPBasicAuth(user, password))
    if response.status_code == 200:
        return pd.read_csv(io.BytesIO(response.content))
    else:
        return pd.DataFrame(columns=["ID", "Bereich", "Typ", "Kategorie", "Betrag", "Datum", "Zusatz"])

def _upload_df(user, password, df):
    """Hilfsfunktion: Schiebt den DataFrame zurück in die Cloud."""
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    requests.put(NC_WEBDAV_URL, auth=HTTPBasicAuth(user, password), data=output.read())

def lade_eintraege(user, password, bereich=None):
    df = get_df_from_cloud(user, password)
    if bereich and not df.empty and 'Bereich' in df.columns:
        df = df[df['Bereich'] == bereich]
    return df.to_dict('records')

def speichere_eintrag(user, password, ber, typ, kat, betrag, dat, zus=""):
    df = get_df_from_cloud(user, password)
    neue_zeile = {
        "ID": uuid.uuid4().hex, "Bereich": ber, "Typ": typ, 
        "Kategorie": kat, "Betrag": betrag, "Datum": dat, "Zusatz": zus
    }
    df = pd.concat([df, pd.DataFrame([neue_zeile])], ignore_index=True)
    _upload_df(user, password, df)

def loesche_eintrag(user, password, e_id):
    """Löscht einen Eintrag anhand seiner ID."""
    df = get_df_from_cloud(user, password)
    df = df[df['ID'] != e_id]
    _upload_df(user, password, df)

def update_eintrag(user, password, e_id, ber, typ, kat, betrag, dat, zus=""):
    """Überschreibt einen bestehenden Eintrag mit neuen Werten."""
    df = get_df_from_cloud(user, password)
    idx = df.index[df['ID'] == e_id].tolist()
    if idx:
        df.at[idx[0], 'Bereich'] = ber
        df.at[idx[0], 'Typ'] = typ
        df.at[idx[0], 'Kategorie'] = kat
        df.at[idx[0], 'Betrag'] = betrag
        df.at[idx[0], 'Datum'] = dat
        df.at[idx[0], 'Zusatz'] = zus
    _upload_df(user, password, df)
