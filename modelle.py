import datenbank

class Transaktion:
    def __init__(self, typ, kategorie, betrag, datum, zusatz="", e_id=None):
        self.id = e_id
        self.bereich = "Transaktion"
        self.typ = typ
        self.kategorie = kategorie
        self.betrag = float(betrag)
        self.datum = datum
        self.zusatz = zusatz

    def ist_ausgabe(self):
        return self.typ == "Ausgabe"

    def info_ausgeben(self):
        vorzeichen = "-" if self.ist_ausgabe() else "+"
        return f"[{self.datum}] {self.kategorie}: {vorzeichen}{self.betrag:.2f} €"

    def in_db_speichern(self):
        if self.id:
            datenbank.update_eintrag(self.id, self.bereich, self.typ, self.kategorie, self.betrag, self.datum, self.zusatz)
        else:
            datenbank.speichere_eintrag(self.bereich, self.typ, self.kategorie, self.betrag, self.datum, self.zusatz)

    def aus_db_loeschen(self):
        if self.id:
            datenbank.loesche_eintrag(self.id)