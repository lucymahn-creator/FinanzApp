with tab2:
    st.subheader("Transaktion erfassen")
    
    # 1. Daten frisch laden
    df_trans = pd.DataFrame(datenbank.lade_eintraege("Transaktion"))
    
    # 2. Kategorien aus der Spalte 'Kategorie' holen, falls Daten da sind
    if not df_trans.empty:
        # Hier sammeln wir alle bisher genutzten Kategorien
        kats = sorted(df_trans['Kategorie'].dropna().unique().tolist())
    else:
        kats = ["Miete", "Lebensmittel", "Gehalt", "Sonstiges"]

    with st.form("transaktion_form", clear_on_submit=True):
        typ = st.selectbox("Typ", ["Ausgabe", "Einnahme"])
        
        # 3. Auswahlbox mit den Kategorien
        # Wir nutzen ein 'kombiniertes' Vorgehen:
        sel_kat = st.selectbox("Kategorie wählen", options=kats)
        
        # Falls man doch etwas ganz anderes eingeben will:
        manuell_kat = st.text_input("...oder neue Kategorie hier eintippen:")
        
        kategorie = manuell_kat if manuell_kat else sel_kat
        
        betrag = st.number_input("Betrag", min_value=0.0, format="%.2f")
        datum = st.date_input("Datum")
        
        if st.form_submit_button("Speichern"):
            datenbank.speichere_eintrag("Transaktion", typ, kategorie, betrag, datum.strftime("%d.%m.%Y"))
            st.success(f"Gespeichert: {kategorie}")
            st.rerun() # Wichtig: Lädt die Seite neu, damit die neue Kategorie sofort in der Liste auftaucht

    # Anzeige der Tabelle
    if not df_trans.empty:
        st.dataframe(df_trans.tail(5))