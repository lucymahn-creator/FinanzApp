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
            # 2. Beträge zu Zahlen konvertieren
            df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce').fillna(0)
            
            # 3. Berechnungen mit explizitem float-Typ
            einnahmen = float(df[df['Typ'] == 'Einnahme']['Betrag'].sum())
            ausgaben = float(df[df['Typ'] == 'Ausgabe']['Betrag'].sum())
            saldo = einnahmen - ausgaben
            
            # 4. Sichere Anzeige (metric verlangt einfache Zahlen/Strings)
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:,.2f} €")
            col3.metric("Saldo", f"{saldo:,.2f} €")
        else:
            st.info("Noch keine Transaktionsdaten gefunden.")
