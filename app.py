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
            # 1. Spalten säubern
            df.columns = df.columns.str.strip()
            
            # 2. Betrag zu numerischen Werten konvertieren
            df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce').fillna(0)
            
            # 3. Berechnungen erzwingen als float
            # Wir nehmen das erste Element, wenn es eine Series ist, oder direkt die Summe
            einnahmen_series = df[df['Typ'] == 'Einnahme']['Betrag'].sum()
            ausgaben_series = df[df['Typ'] == 'Ausgabe']['Betrag'].sum()
            
            einnahmen = float(einnahmen_series) if pd.notnull(einnahmen_series) else 0.0
            ausgaben = float(ausgaben_series) if pd.notnull(ausgaben_series) else 0.0
            saldo = einnahmen - ausgaben
            
            # 4. Anzeige
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:,.2f} €")
            col3.metric("Saldo", f"{saldo:,.2f} €")
        else:
            st.info("Noch keine Daten vorhanden.")
