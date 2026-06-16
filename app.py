import streamlit as st
import pandas as pd
import datenbank

# Konfiguration
st.set_page_config(page_title="Finanz-Tracker", layout="wide")

# Passwort-Logik
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

# Hauptprogramm
if check_password():
    st.title("💰 Finanz-Tracker")
    
    # Navigation
    choice = st.sidebar.selectbox("Navigation", ["Dashboard", "Transaktionen", "Budgets", "Sparziele"])
    
    # Secrets holen
    USER = st.secrets["NEXTCLOUD_USER"]
    PASS = st.secrets["NEXTCLOUD_PASS"]
    
    # Bereich laden
    if choice == "Dashboard":
        st.subheader("Übersicht")
        data = datenbank.lade_eintraege(USER, PASS, "Transaktion")
        df = pd.DataFrame(data)
        
        if not df.empty:
            df.columns = df.columns.str.strip()
            df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce').fillna(0)
            
            ein_df = df[df['Typ'] == 'Einnahme']['Betrag']
            aus_df = df[df['Typ'] == 'Ausgabe']['Betrag']
            
            einnahmen = float(ein_df.sum()) if not ein_df.empty else 0.0
            ausgaben = float(aus_df.sum()) if not aus_df.empty else 0.0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:,.2f} €")
            col3.metric("Saldo", f"{einnahmen - ausgaben:,.2f} €")
        else:
            st.info("Keine Daten vorhanden.")
            
    elif choice == "Transaktionen":
        st.subheader("Transaktion erfassen")
        # 1. Das Formular zum Erfassen bleibt
        with st.form("trans_form"):
            # ... (deine Felder für kat, betrag, typ, datum, zusatz)
            if st.form_submit_button("Speichern"):
                datenbank.speichere_eintrag(USER, PASS, "Transaktion", typ, kat, betrag, str(datum), zusatz)
                st.success("Gespeichert!")
                st.rerun()
        
        st.divider() # Trennlinie für Ordnung
        
        # 2. Die Liste zum Verwalten kommt DARUNTER
        st.subheader("Bestehende Transaktionen")
        data = datenbank.lade_eintraege(USER, PASS, "Transaktion")
        df = pd.DataFrame(data)
        
        if not df.empty:
            for index, row in df.iterrows():
                # Wir erstellen Spalten für eine schöne Anordnung
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{row['Kategorie']}**: {row['Betrag']}€ - {row['Typ']} ({row['Datum']})")
                
                # Der Lösch-Button für jede Zeile
                if col2.button("Löschen", key=row['ID']):
                    datenbank.loesche_eintrag(USER, PASS, row['ID'])
                    st.rerun() # App neu laden, damit Zeile sofort weg ist
        else:
            st.info("Keine Transaktionen gefunden.")
