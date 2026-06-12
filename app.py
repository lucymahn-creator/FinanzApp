import streamlit as st
import pandas as pd
import datenbank

# --- SEITENKONFIGURATION ---
st.set_page_config(page_title="Finanz-Tracker Mobile", layout="wide")
st.title("💰 Finanz-Tracker")

# Daten laden
transaktionen = pd.DataFrame(datenbank.lade_eintraege("Transaktion"))
budgets = pd.DataFrame(datenbank.lade_eintraege("Budget"))
sparziele = pd.DataFrame(datenbank.lade_eintraege("Sparziel"))

# --- NAVIGATION ---
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Transaktionen", "Budgets", "Sparziele"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.subheader("Übersicht")
    if not transaktionen.empty:
        einnahmen = transaktionen[transaktionen['Typ'] == 'Einnahme']['Betrag'].astype(float).sum()
        ausgaben = transaktionen[transaktionen['Typ'] == 'Ausgabe']['Betrag'].astype(float).sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("Einnahmen", f"{einnahmen:.2f} €")
        col2.metric("Ausgaben", f"{ausgaben:.2f} €")
        col3.metric("Saldo", f"{einnahmen - ausgaben:.2f} €")
    else:
        st.write("Keine Transaktionsdaten.")

# --- TAB 2: TRANSAKTIONEN ---
with tab2:
    st.subheader("Transaktion erfassen")
    with st.form("transaktion_form"):
        kategorie = st.text_input("Kategorie")
        betrag = st.number_input("Betrag", min_value=0.0)
        typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
        if st.form_submit_button("Speichern"):
            datenbank.speichere_eintrag("Transaktion", typ, kategorie, betrag, pd.Timestamp.now().strftime("%d.%m.%Y"))
            st.rerun()
    st.dataframe(transaktionen.tail(5))

# --- TAB 3: BUDGETS ---
with tab3:
    st.subheader("Budgets verwalten")
    with st.form("budget_form"):
        kat = st.text_input("Kategorie (Budget)")
        limit = st.number_input("Limit Betrag", min_value=0.0)
        if st.form_submit_button("Budget setzen"):
            # Speichere als Budget
            datenbank.speichere_eintrag("Budget", "Monatlich", kat, limit, "")
            st.rerun()
    st.dataframe(budgets)

# --- TAB 4: SPARZIELE ---
with tab4:
    st.subheader("Sparziele")
    with st.form("sparziel_form"):
        name = st.text_input("Ziel Name")
        ziel_betrag = st.number_input("Zielbetrag", min_value=0.0)
        aktuell = st.number_input("Aktuell gespart", min_value=0.0)
        if st.form_submit_button("Speichern"):
            # Zusatz speichern wir als "aktueller_stand|ziel"
            zusatz = f"{aktuell}"
            datenbank.speichere_eintrag("Sparziel", "Ziel", name, ziel_betrag, "", zusatz)
            st.rerun()
    st.dataframe(sparziele)