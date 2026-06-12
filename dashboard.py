import tkinter as tk
from datetime import datetime
import datenbank

class FinanzTrackerDashboard:
    def __init__(self, parent_frame, farben):
        self.parent, self.farben = parent_frame, farben
        self.ui_erstellen()
    
    def berechne_summe(self, transaktionen, typ):
        summe = sum(float(x.get("Betrag", 0)) for x in transaktionen if x.get("Typ") == typ)
        return summe

    def berechne_kategorien(self, transaktionen):
        kats = {}
        for x in transaktionen:
            if x.get("Typ") == "Ausgabe": 
                kats[x.get("Kategorie", "")] = kats.get(x.get("Kategorie", ""), 0) + float(x.get("Betrag", 0))
        sortiert = sorted(kats.items(), key=lambda x: x[1], reverse=True)
        return sortiert

    def berechne_sparziel_fortschritt(self, sparziele):
        t_ist = sum(float(str(x.get("Zusatz", "0")).split("|")[0] or 0) for x in sparziele)
        t_max = sum(float(x.get("Betrag", 0) or 0) for x in sparziele)
        prozent = (t_ist / t_max * 100) if t_max > 0 else 0
        return prozent

    def lade_daten(self):
        transaktionen = datenbank.lade_eintraege("Transaktion")
        sparziele = datenbank.lade_eintraege("Sparziel")

        self.ein = self.berechne_summe(transaktionen, "Einnahme")
        self.aus = self.berechne_summe(transaktionen, "Ausgabe")
        self.kats = self.berechne_kategorien(transaktionen)
        self.ziel_proz = self.berechne_sparziel_fortschritt(sparziele)

        self.budg = []
        for b in datenbank.lade_eintraege("Budget"):
            k = b.get("Kategorie", "")
            max_b = float(b.get("Betrag", 0) or 0)
            ist = 0
            for k_name, wert in self.kats:
                if k_name == k: ist = wert
            proz = (ist / max_b * 100) if max_b > 0 else 0
            self.budg.append((k, ist, max_b, proz, proz >= float(b.get("Zusatz", 80) or 80)))
        self.budg.sort(key=lambda x: x[3], reverse=True)

        self.ziele = [(x.get("Kategorie"), float(str(x.get("Zusatz", "0")).split("|")[0] or 0), float(x.get("Betrag", 0) or 0)) for x in sparziele]

    def ui_erstellen(self):
        self.lade_daten()
        f = tk.Frame(self.parent, bg=self.farben["bg"])
        f.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(f, text="Dashboard", font=("Arial", 20, "bold"), bg=self.farben["bg"], fg=self.farben["text"]).pack(anchor="w")
        tk.Label(f, text=datetime.now().strftime("%A, %d. %B %Y"), fg=self.farben["text_grey"], bg=self.farben["bg"]).pack(anchor="w", pady=(0, 20))

        c_frame = tk.Frame(f, bg=self.farben["bg"])
        c_frame.pack(fill="x", pady=(0, 20))
        
        verm = self.ein - self.aus
        kachel_daten = [("Einnahmen", self.ein, "€"), ("Ausgaben", self.aus, "€"), ("Vermögen", verm, "€"), ("Sparziele", self.ziel_proz, "%")]
        
        for titel, wert, zeichen in kachel_daten:
            k = tk.Frame(c_frame, bg=self.farben["card"], relief="groove", bd=1)
            k.pack(side="left", fill="x", expand=True, padx=5) 
            tk.Label(k, text=f"{wert:.0f} {zeichen}", font=("Arial", 16, "bold"), bg=self.farben["card"], fg=self.farben["text"]).pack(anchor="w", padx=15, pady=(15, 0))
            tk.Label(k, text=titel, font=("Arial", 11), fg=self.farben["text_grey"], bg=self.farben["card"]).pack(anchor="w", padx=15, pady=(0, 15))

        b_frame = tk.Frame(f, bg=self.farben["bg"])
        b_frame.pack(fill="both", expand=True)

        b_frame.grid_columnconfigure(0, weight=1)
        b_frame.grid_columnconfigure(1, weight=1)
        b_frame.grid_rowconfigure(0, weight=1)
        b_frame.grid_rowconfigure(1, weight=1)

        self.box(b_frame, "Gesamtbilanz", 0, 0, [f"Bilanz: {verm:.2f} €"])
        self.box(b_frame, "Top Ausgaben", 0, 1, [f"{k}: {v:.0f} €" for k, v in self.kats[:4]]) 
        
        warn = any(b[4] for b in self.budg)
        b_text = [f"{k}: {ist:.0f} / {m:.0f} € {'⚠️' if w else ''}" for k, ist, m, p, w in self.budg[:4]]
        self.box(b_frame, "⚠️ Budget-Warnungen!" if warn else "Budgets", 1, 0, b_text, "#ef4444" if warn else self.farben["text"])
        
        z_text = [f"{n}: {i:.0f} / {m:.0f} € ({(i/m*100) if m>0 else 0:.0f}%)" for n, i, m in self.ziele[:4]]
        self.box(b_frame, "Sparziele", 1, 1, z_text)

    def box(self, parent, titel, row, col, zeilen, t_color=None):
        b = tk.Frame(parent, bg=self.farben["card"], relief="groove", bd=1)
        b.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        tk.Label(b, text=titel, font=("Arial", 14, "bold"), bg=self.farben["card"], fg=t_color or self.farben["text"]).pack(anchor="w", padx=20, pady=(15, 10))
        
        if not zeilen or not zeilen[0]:
            tk.Label(b, text="Keine Daten vorhanden.", font=("Arial", 11), fg=self.farben["text_grey"], bg=self.farben["card"]).pack(padx=20, anchor="w")
            return
            
        for z in zeilen:
            tk.Label(b, text=z, font=("Arial", 11), bg=self.farben["card"], fg=self.farben["text"]).pack(anchor="w", padx=20, pady=4)