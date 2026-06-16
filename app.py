import streamlit as st
import pandas as pd
import datenbank

# 1. Konfiguration - IMMER ganz oben
st.set_page_config(page_title="Finanz-Tracker", layout="wide")

# 2. Passwort-Funktion
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

# 3. Hauptprogramm - ALLES muss hier drin stehen!
if check_password():
    st.title("💰 Finanz-Tracker")
    
    # Navigation wird hier definiert, damit 'choice' existiert
    menu = ["Dashboard", "Transaktionen", "Budgets", "Sparziele"]
    choice = st.sidebar.selectbox("Navigation", menu)
    
    # Hilfsfunktion für Daten
    def get_data(bereich):
        data = datenbank.lade_eintraege(bereich)
        return pd.DataFrame(data)

    USER = st.secrets["username"]
    PAS = st.secrets["password"]

    if choice == "Dashboard":
        st.subheader("Übersicht")
        df = get_data("Transaktion")
        
        if not df.empty:
            df.columns = df.columns.str.strip()
            df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce').fillna(0)
            
            # Sichere Summenbildung
            ein_df = df[df['Typ'] == 'Einnahme']['Betrag']
            aus_df = df[df['Typ'] == 'Ausgabe']['Betrag']
            
            einnahmen = float(ein_df.sum()) if not ein_df.empty else 0.0
            ausgaben = float(aus_df.sum()) if not aus_df.empty else 0.0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:,.2f} €")
            col3.metric("Saldo", f"{einnahmen - ausgaben:,.2f} €")
        else:
            st.info("Noch keine Transaktionsdaten vorhanden.")
            
    elif choice == "Transaktionen":
        st.subheader("Transaktion erfassen")
        with st.form("trans_form"):
            kat = st.text_input("Kategorie")
            betrag = st.number_input("Betrag", min_value=0.0)
            typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
            datum = st.date_input("Datum")
            # NEU: Eingabefeld für den Zusatz
            zusatz = st.text_input("Zusatz / Notiz") 
            
            if st.form_submit_button("Speichern"):
                # Funktion anpassen, um den 'zusatz' mitzugeben
                datenbank.speichere_eintrag("Transaktion", typ, kat, betrag, str(datum), zusatz)
                st.success("Gespeichert!")
                st.rerun()
        
       
        st.write("Vorhandene Transaktionen:")
        st.dataframe(get_data("Transaktion"))

    else:
        st.write(f"Bereich {choice} ist in Entwicklung.")
