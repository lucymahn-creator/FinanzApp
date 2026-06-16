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
        df = get_data("Transaktion")
        
        if not df.empty:
            # Spalten säubern
            df.columns = df.columns.str.strip()
            # Beträge erzwingen
            df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce').fillna(0)
            
            # --- Hier liegt der Fix ---
            # Wir extrahieren die Summen und erzwingen die Umwandlung in eine Python-Zahl
            einnahmen_df = df[df['Typ'] == 'Einnahme']['Betrag']
            ausgaben_df = df[df['Typ'] == 'Ausgabe']['Betrag']
            
            einnahmen = float(einnahmen_df.sum()) if not einnahmen_df.empty else 0.0
            ausgaben = float(ausgaben_df.sum()) if not ausgaben_df.empty else 0.0
            saldo = einnahmen - ausgaben
            
            # Anzeige
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:,.2f} €")
            col3.metric("Saldo", f"{saldo:,.2f} €")
        else:
            st.info("Noch keine Transaktionsdaten vorhanden.")
            st.info("Noch keine Daten vorhanden.")
