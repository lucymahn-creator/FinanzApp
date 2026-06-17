import streamlit as st
import pandas as pd
import datenbank
from datetime import datetime

# Konfiguration
st.set_page_config(page_title="Finanz-Tracker Pro", layout="wide")

# --- KATEGORIEN DEFINIEREN ---
STANDARD_KATEGORIEN = [
    "Gehalt", "Miete", "Lebensmittel", "Freizeit", 
    "Auto/Transport", "Getränke", "Einkauf L", "Sonstiges"
]

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
    choice = st.sidebar.radio("Navigation", ["Dashboard", "Transaktionen", "Budgets", "Sparziele"])
    
    # Secrets holen
    USER = st.secrets["NEXTCLOUD_USER"]
    PASS = st.secrets["NEXTCLOUD_PASS"]
    
    # --- DASHBOARD ---
    if choice == "Dashboard":
        st.subheader("Übersicht")
        data = datenbank.lade_eintraege(USER, PASS, "Transaktion")
        df = pd.DataFrame(data)
        
        if not df.empty:
            df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce').fillna(0)
            ein_df = df[df['Typ'] == 'Einnahme']['Betrag']
            aus_df = df[df['Typ'] == 'Ausgabe']['Betrag']
            
            einnahmen = float(ein_df.sum()) if not ein_df.empty else 0.0
            ausgaben = float(aus_df.sum()) if not aus_df.empty else 0.0
            saldo = einnahmen - ausgaben
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Einnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Ausgaben", f"{ausgaben:,.2f} €")
            col3.metric("Saldo", f"{saldo:,.2f} €", delta=f"{saldo:,.2f} €", delta_color="normal" if saldo >= 0 else "inverse")
        else:
            st.info("Noch keine Transaktionen vorhanden.")
            
    # --- TRANSAKTIONEN ---
    elif choice == "Transaktionen":
        tab1, tab2 = st.tabs(["📋 Übersicht & Bearbeiten", "➕ Neu erfassen"])
        
        with tab1:
            data = datenbank.lade_eintraege(USER, PASS, "Transaktion")
            if data:
                st.dataframe(pd.DataFrame(data).drop(columns=['ID']), use_container_width=True)
                
                st.divider()
                st.subheader("✏️ Eintrag bearbeiten oder löschen")
                
                # Dropdown zur Auswahl des Eintrags
                options = {f"{d['Datum']} | {d['Kategorie']} | {d['Betrag']} € ({d['Typ']})": d for d in data}
                selected_label = st.selectbox("Wähle einen Eintrag aus:", list(options.keys()))
                auswahl = options[selected_label]
                
                # Datumstext in ein echtes Datum umwandeln
                try:
                    default_date = datetime.strptime(auswahl['Datum'], "%Y-%m-%d").date()
                except ValueError:
                    default_date = datetime.today().date()
                
                # Sicherheitslogik: Falls die gespeicherte Kategorie alt/unbekannt ist, füge sie der Liste hinzu
                aktuelle_kategorie = str(auswahl['Kategorie'])
                kategorie_liste = STANDARD_KATEGORIEN.copy()
                if aktuelle_kategorie not in kategorie_liste:
                    kategorie_liste.append(aktuelle_kategorie)
                kat_index = kategorie_liste.index(aktuelle_kategorie)
                
                # Bearbeitungs-Formular
                with st.form("edit_form"):
                    kat_ed = st.selectbox("Kategorie", kategorie_liste, index=kat_index)
                    betrag_ed = st.number_input("Betrag", value=float(auswahl['Betrag']), min_value=0.0)
                    typ_ed = st.selectbox("Typ", ["Ausgabe", "Einnahme"], index=0 if auswahl['Typ'] == "Ausgabe" else 1)
                    datum_ed = st.date_input("Datum", value=default_date)
                    zus_ed = st.text_input("Zusatz", value=str(auswahl.get('Zusatz', '')))
                    
                    colA, colB = st.columns(2)
                    submit_edit = colA.form_submit_button("💾 Änderungen speichern")
                    submit_del = colB.form_submit_button("🗑️ Eintrag löschen")
                    
                    if submit_edit:
                        datenbank.update_eintrag(USER, PASS, auswahl['ID'], "Transaktion", typ_ed, kat_ed, betrag_ed, str(datum_ed), zus_ed)
                        st.success("Eintrag erfolgreich aktualisiert!")
                        st.rerun()
                        
                    if submit_del:
                        datenbank.loesche_eintrag(USER, PASS, auswahl['ID'])
                        st.success("Eintrag wurde gelöscht!")
                        st.rerun()
            else:
                st.info("Keine Transaktionen gefunden.")
                
        with tab2:
            st.subheader("Neue Transaktion anlegen")
            with st.form("trans_form"):
                kat = st.selectbox("Kategorie", STANDARD_KATEGORIEN)
                betrag = st.number_input("Betrag", min_value=0.0, format="%.2f")
                typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
                datum = st.date_input("Datum", value=datetime.today().date())
                zusatz = st.text_input("Zusatz")
                
                if st.form_submit_button("Speichern"):
                    datenbank.speichere_eintrag(USER, PASS, "Transaktion", typ, kat, betrag, str(datum), zusatz)
                    st.success("Transaktion gespeichert!")
                    st.rerun()

  # --- BUDGETS ---
    elif choice == "Budgets":
        st.subheader("Budgets verwalten")
        st.info("Hier kannst du Limits für deine Kategorien festlegen.")
        
        with st.form("budget_form"):
            kat = st.selectbox("Kategorie", STANDARD_KATEGORIEN)
            limit = st.number_input("Monatliches Limit (€)", min_value=0.0)
            
            # WICHTIG: Dieser Button MUSS eingerückt sein, 
            # damit Streamlit weiß, dass er zum Formular gehört!
            submit_budget = st.form_submit_button("💾 Budget speichern")
            
            if submit_budget:
                datenbank.speichere_eintrag(USER, PASS, "Budget", "Limit", kat, limit, str(datetime.today().date()), "Monatsbudget")
                st.success("Budget gespeichert!")
                st.rerun()

        # Budgets anzeigen (Das steht wieder außerhalb des Formulars)
        budget_data = datenbank.lade_eintraege(USER, PASS, "Budget")
        if budget_data:
            st.dataframe(pd.DataFrame(budget_data)[["Kategorie", "Betrag", "Datum"]])
