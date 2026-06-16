import streamlit as st
import pandas as pd
import datenbank
import uuid

# 1. Konfiguration
st.set_page_config(page_title="Finanz-Tracker", layout="wide")

# 2. Passwort-Logik
def check_password():
    def password_entered():
        if st.session_state["password_input"] == "Roterrp2004_":
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False
            st.error("Passwort falsch!")

    if st.session_state.get("password_correct", False):
        return True

    st.text_input("Passwort eingeben", type="password", on_change=password_entered, key="password_input")
    return False

# 3. Hauptprogramm
if check_password():
    st.title("💰 Finanz-Tracker")
    
    # Navigation
    choice = st.sidebar.selectbox("Navigation", ["Dashboard", "Transaktionen", "Budgets", "Sparziele"])
    
    # Daten laden
    df = pd.DataFrame(datenbank.lade_eintraege()) # Lade alle Daten
    
    if choice == "Dashboard":
        st.subheader("Übersicht")
        if not df.empty:
            einnahmen = df[df['Typ'] == 'Einnahme']['Betrag'].sum()
            ausgaben = df[df['Typ'] == 'Ausgabe']['Betrag'].sum()
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:.2f} €")
            col3.metric("Saldo", f"{einnahmen - ausgaben:.2f} €")
        
    elif choice == "Transaktionen":
        st.subheader("Transaktionen verwalten")
        with st.form("trans_form"):
            kat = st.text_input("Kategorie")
            betrag = st.number_input("Betrag", min_value=0.0)
            typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
            datum = st.date_input("Datum")
            if st.form_submit_button("Speichern"):
                datenbank.speichere_eintrag("Transaktion", typ, kat, betrag, str(datum))
                st.success("Gespeichert!")
                st.rerun()
        st.dataframe(df[df['Bereich'] == 'Transaktion'])

    elif choice == "Budgets":
        st.subheader("Budgets")
        # Hier die Budget-Logik aus budgets.py einfügen
        st.info("Budget-Ansicht in Arbeit.")

    elif choice == "Sparziele":
        st.subheader("Sparziele")
        # Hier die Sparziel-Logik aus sparziele.py einfügen
        st.info("Sparziel-Ansicht in Arbeit.")
