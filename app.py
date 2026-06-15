import streamlit as st
import pandas as pd
import datenbank

# Konfiguration
st.set_page_config(page_title="Finanz-Tracker", layout="wide")

st.title("💰 Finanz-Tracker")

# Navigation
menu = ["Dashboard", "Transaktionen", "Budgets", "Sparziele"]
choice = st.sidebar.selectbox("Navigation", menu)

# Daten laden (als Funktion, um immer aktuell zu sein)
def get_data(typ):
    return pd.DataFrame(datenbank.lade_eintraege(typ))

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
