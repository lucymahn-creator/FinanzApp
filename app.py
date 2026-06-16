import streamlit as st
import pandas as pd
import datenbank

st.set_page_config(page_title="Finanz-Tracker", layout="wide")

USER = st.secrets.get("NEXTCLOUD_USER")
PASS = st.secrets.get("NEXTCLOUD_PASS")

st.title("💰 Finanz-Tracker")
choice = st.sidebar.selectbox("Navigation", ["Dashboard", "Transaktionen"])

if choice == "Transaktionen":
    st.subheader("Transaktion erfassen")
    with st.form("trans_form"):
        col_a, col_b = st.columns(2)
        kat = col_a.text_input("Kategorie")
        betrag = col_b.number_input("Betrag", min_value=0.0)
        typ = col_a.selectbox("Typ", ["Ausgabe", "Einnahme"])
        datum = col_b.date_input("Datum")
        zusatz = st.text_input("Zusatz")
        if st.form_submit_button("Speichern"):
            datenbank.speichere_eintrag(USER, PASS, "Transaktion", typ, kat, betrag, str(datum), zusatz)
            st.success("Gespeichert!")
            st.rerun()

    st.write("---")
    st.subheader("Bestehende Transaktionen")
    data = datenbank.lade_eintraege(USER, PASS, "Transaktion")
    df = pd.DataFrame(data)
    if not df.empty:
        for index, row in df.iterrows():
            c1, c2 = st.columns([5, 1])
            c1.write(f"{row['Datum']} | {row['Kategorie']} | {row['Betrag']} € ({row['Typ']})")
            if c2.button("🗑️", key=f"del_{row['ID']}"):
                datenbank.loesche_eintrag(USER, PASS, row['ID'])
                st.rerun()
