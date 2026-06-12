import tkinter as tk
from tkinter import ttk
import datenbank

class BudgetsView:
    def __init__(self, parent_frame, farben):
        self.parent, self.farben = parent_frame, farben
        self.ui_erstellen()

    def ui_erstellen(self):
        f = tk.Frame(self.parent, bg=self.farben["bg"])
        f.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(f, text="Budgetverwaltung", font=("Arial", 20, "bold"), bg=self.farben["bg"], fg=self.farben["text"]).pack(anchor="w", pady=(0, 15))

        self.tv = ttk.Treeview(f, columns=("Kategorie", "Betrag", "Zeitraum", "Status", "Edit", "Del"), show="headings")
        for col, w in zip(self.tv["columns"], [150, 100, 100, 200, 40, 40]):
            self.tv.heading(col, text=col)
            self.tv.column(col, width=w, anchor="w" if col in ("Kategorie", "Status") else "center")
            
        self.tv.pack(fill="both", expand=True)
        self.tv.bind("<ButtonRelease-1>", self.klick)

        tk.Button(self.parent, text="+", font=("Arial", 24), bg="#2563eb", fg="white", relief="flat", command=lambda: BudgetPopup(self.parent, self.farben, self.laden)).place(relx=0.96, rely=0.94, anchor="se")
        self.laden()

    def laden(self):
        for row in self.tv.get_children(): self.tv.delete(row)

        ausgaben = {}
        for t in datenbank.lade_eintraege("Transaktion"):
            if t.get("Typ") == "Ausgabe":
                ausgaben[t.get("Kategorie")] = ausgaben.get(t.get("Kategorie"), 0) + float(t.get("Betrag", 0) or 0)

        for b in datenbank.lade_eintraege("Budget"):
            kat = b.get("Kategorie", "")
            try:
                betrag = float(b.get("Betrag", 0))
                warn = float(b.get("Zusatz", "80"))
            except ValueError: betrag, warn = 0.0, 80.0

            proz = (ausgaben.get(kat, 0.0) / betrag * 100) if betrag > 0 else 0
            status = f"⚠️ {proz:.0f}% verbraucht!" if proz >= warn else f"Ok ({proz:.0f}%)"

            self.tv.insert("", "end", iid=b.get("ID"), values=(kat, f"{betrag:.2f} €", b.get("Typ", ""), status, "📝", "🗑️"))

    def klick(self, event):
        if self.tv.identify("region", event.x, event.y) == "cell":
            col, e_id = self.tv.identify_column(event.x), self.tv.identify_row(event.y)
            if col == "#5": 
                e = next((x for x in datenbank.lade_eintraege("Budget") if x.get("ID") == e_id), None)
                if e: BudgetPopup(self.parent, self.farben, self.laden, e)
            elif col == "#6": 
                datenbank.loesche_eintrag(e_id)
                self.laden()


class BudgetPopup:
    def __init__(self, parent, farben, on_save, daten=None):
        self.on_save, self.daten = on_save, daten
        self.p = tk.Toplevel(parent)
        self.p.title("Budget")
        self.p.geometry("300x400")
        self.p.iconbitmap("images/budgets.ico")
        self.p.configure(bg=farben["bg"])
        self.p.grab_set()

        self.inputs = {}

        felder = [
            ("Kategorie", "Kategorie", ttk.Combobox, ["Miete", "Lebensmittel", "Transport", "Versicherung", "Streaming", "Shopping", "Gesundheit", "Sonstiges"]),
            ("Betrag (EUR)", "Betrag", tk.Entry, None),
            ("Zeitraum", "Typ", ttk.Combobox, ["Monatlich", "Jährlich"]),
            ("Warnschwelle (%)", "Zusatz", tk.Entry, None)
        ]

        for text, db_key, widget_class, values in felder:
            tk.Label(self.p, text=text, bg=farben["bg"], fg=farben["text"]).pack(anchor="w", padx=20, pady=(10, 0))
            
            if widget_class == ttk.Combobox:
                w = ttk.Combobox(self.p, values=values, font=("Arial", 10), state="readonly")
                if not daten: w.set(values[0])
            else:
                w = tk.Entry(self.p, font=("Arial", 10), bg=farben["card"], fg=farben["text"])
                if not daten and db_key == "Zusatz": w.insert(0, "80")

            w.pack(fill="x", padx=20, pady=5)
            self.inputs[db_key] = w

            if daten:
                if widget_class == ttk.Combobox: w.set(str(daten.get(db_key, "")))
                else: w.insert(0, str(daten.get(db_key, "")))

        tk.Button(self.p, text="Speichern", font=("Arial", 10, "bold"), bg="#2563eb", fg="white", relief="flat", command=self.speichern).pack(fill="x", padx=20, pady=25)

    def speichern(self):
        try:
            kat = self.inputs["Kategorie"].get()
            betrag = float(self.inputs["Betrag"].get().replace(",", ".") or 0)
            zeitraum = self.inputs["Typ"].get()
            warn = float(self.inputs["Zusatz"].get().replace(",", ".") or 80)

            if not kat or betrag <= 0: return

            if self.daten: datenbank.update_eintrag(self.daten.get("ID"), "Budget", zeitraum, kat, betrag, "", str(warn))
            else: datenbank.speichere_eintrag("Budget", zeitraum, kat, betrag, "", str(warn))

            self.p.destroy()
            self.on_save()
        except ValueError:
            pass