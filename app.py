import streamlit as st
import pandas as pd
import datenbank

# Konfiguration
st.set_page_config(page_title="Finanz-Tracker", layout="wide")

st.title("💰 Finanz-Tracker")

# Navigation via Sidebar
menu = ["Dashboard", "Transaktionen", "Budgets", "Sparziele"]
choice = st.sidebar.selectbox("Navigation", menu)

def check_password():
    """Gibt True zurück, wenn das Passwort korrekt ist."""
    # 1. Funktion, die aufgerufen wird, wenn das Eingabefeld sich ändert
    def password_entered():
        if st.session_state["password_input"] == "Roterrp2004_":
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]  # Passwort aus dem Speicher löschen
        else:
            st.session_state["password_correct"] = False
            st.error("Passwort falsch!")

    # 2. Überprüfen, ob bereits eingeloggt
    if st.session_state.get("password_correct", False):
        return True

    # 3. EINZIGES Eingabefeld - mit einem eindeutigen key
    st.text_input(
        "Passwort eingeben", 
        type="password", 
        on_change=password_entered, 
        key="password_input"
    )
    return False

    # 3. EINZIGES Eingabefeld - mit einem eindeutigen key
    st.text_input(
        "Passwort eingeben", 
        type="password", 
        on_change=password_entered, 
        key="password_input"
    )
    return False

# Daten laden
def get_data(bereich):
    data = datenbank.lade_eintraege(bereich)
    return pd.DataFrame(data)

# --- DASHBOARD LOGIK (aus dashboard.py) ---
if choice == "Dashboard":
    st.subheader("Übersicht")
    df = get_data("Transaktion")
    if not df.empty:
        # Berechnungen wie in deinem alten Dashboard
        einnahmen = df[df['Typ'] == 'Einnahme']['Betrag'].sum()
        ausgaben = df[df['Typ'] == 'Ausgabe']['Betrag'].sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("Einnahmen", f"{einnahmen:.2f} €")
        col2.metric("Ausgaben", f"{ausgaben:.2f} €")
        col3.metric("Saldo", f"{einnahmen - ausgaben:.2f} €")
    else:
        st.info("Noch keine Daten vorhanden.")

# --- TRANSAKTIONEN LOGIK (aus transaktionen.py) ---
elif choice == "Transaktionen":
    st.subheader("Transaktion erfassen")
    with st.form("trans_form"):
        kategorie = st.text_input("Kategorie")
        betrag = st.number_input("Betrag", min_value=0.0)
        typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
        datum = st.date_input("Datum")
        if st.form_submit_button("Speichern"):
            datenbank.speichere_eintrag("Transaktion", typ, kategorie, betrag, str(datum))
            st.success("Gespeichert!")
            st.rerun()
    st.dataframe(get_data("Transaktion"))

# ... Analog dazu kannst du Budgets und Sparziele einbauen ...
