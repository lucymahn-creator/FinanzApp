import streamlit as st
import pandas as pd
import datenbank

# 1. Passwort-Check-Funktion
def check_password():
    """Gibt True zurück, wenn das Passwort korrekt ist."""
    def password_entered():
        if st.session_state["password"] == "Roterrp2004_": # Hier dein Passwort
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Passwort aus dem Speicher löschen
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Erster Aufruf: Zeige Passwortfeld
        st.text_input("Passwort eingeben", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Passwort war falsch
        st.text_input("Passwort eingeben", type="password", on_change=password_entered, key="password")
        st.error("Passwort falsch")
        return False
    else:
        # Passwort war korrekt
        return True

# 2. Hauptprogramm nur ausführen, wenn eingeloggt
if check_password():
    st.title("💰 Finanz-Tracker")
    # ... hier kommt dein gesamter restlicher Code (Navigation, Tabs, etc.) ...

# Konfiguration
st.set_page_config(page_title="Finanz-Tracker", layout="wide")


# Navigation
menu = ["Dashboard", "Transaktionen", "Budgets", "Sparziele"]
choice = st.sidebar.selectbox("Navigation", menu)

# Daten laden (als Funktion, um immer aktuell zu sein)
def get_data(typ):
    return pd.DataFrame(datenbank.get_data(typ))

# --- DASHBOARD ---
if choice == "Dashboard":
    st.subheader("Übersicht")
    df = get_data("Transaktion")
    if not df.empty:
        einnahmen = df[df['Typ'] == 'Einnahme']['Betrag'].sum()
        ausgaben = df[df['Typ'] == 'Ausgabe']['Betrag'].sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("Einnahmen", f"{einnahmen:.2f} €")
        col2.metric("Ausgaben", f"{ausgaben:.2f} €")
        col3.metric("Saldo", f"{einnahmen - ausgaben:.2f} €")
    else:
        st.info("Noch keine Daten vorhanden.")

# --- TRANSAKTIONEN ---
elif choice == "Transaktionen":
    st.subheader("Transaktion erfassen")
    with st.form("trans_form"):
        kategorie = st.text_input("Kategorie")
        betrag = st.number_input("Betrag", min_value=0.0)
        typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
        if st.form_submit_button("Speichern"):
            datenbank.speichere_eintrag("Transaktion", typ, kategorie, betrag, "heute")
            st.success("Gespeichert!")
            st.rerun()
    st.dataframe(get_data("Transaktion"))

# --- BUDGETS ---
elif choice == "Budgets":
    st.subheader("Budgets")
    # Hier analog zu Transaktionen verfahren...
    st.dataframe(get_data("Budget"))

# --- SPARZIELE ---
elif choice == "Sparziele":
    st.subheader("Sparziele")
    st.dataframe(get_data("Sparziel"))
