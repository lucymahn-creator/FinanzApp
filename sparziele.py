import tkinter as tk
from tkinter import ttk
import datenbank

class SparzieleView:
    def __init__(self, parent_frame, farben):
        self.parent, self.farben = parent_frame, farben
        self.ui_erstellen()

    def ui_erstellen(self):
        f = tk.Frame(self.parent, bg=self.farben["bg"])
        f.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(f, text="Sparziele", font=("Arial", 20, "bold"), bg=self.farben["bg"], fg=self.farben["text"]).pack(anchor="w", pady=(0, 15))

        self.tv = ttk.Treeview(f, columns=("Name", "Zielbetrag", "Aktuell", "Prozent", "Edit", "Del"), show="headings")
        for col, w in zip(self.tv["columns"], [200, 100, 100, 100, 40, 40]):
            self.tv.heading(col, text=col)
            self.tv.column(col, width=w, anchor="w" if col == "Name" else "center")
        
        self.tv.pack(fill="both", expand=True)
        self.tv.bind("<ButtonRelease-1>", self.klick)

        tk.Button(self.parent, text="+", font=("Arial", 24), bg="#2563eb", fg="white", relief="flat", command=lambda: SparzielPopup(self.parent, self.farben, self.laden)).place(relx=0.96, rely=0.94, anchor="se")
        self.laden()

    def laden(self):
        for row in self.tv.get_children(): self.tv.delete(row)
        for e in datenbank.lade_eintraege("Sparziel"):
            try:
                ziel = float(e.get("Betrag", 0))
                aktuell = float(str(e.get("Zusatz", "0")).split("|")[0] or 0)
                proz = f"{(aktuell / ziel * 100):.0f}%" if ziel > 0 else "0%"
            except ValueError: ziel, aktuell, proz = 0.0, 0.0, "0%"

            self.tv.insert("", "end", iid=e.get("ID"), values=(e.get("Kategorie"), f"{ziel:.2f} €", f"{aktuell:.2f} €", proz, "📝", "🗑️"))

    def klick(self, event):
        if self.tv.identify("region", event.x, event.y) == "cell":
            col, e_id = self.tv.identify_column(event.x), self.tv.identify_row(event.y)
            if col == "#5": 
                e = next((x for x in datenbank.lade_eintraege("Sparziel") if x.get("ID") == e_id), None)
                if e: SparzielPopup(self.parent, self.farben, self.laden, e)
            elif col == "#6": 
                datenbank.loesche_eintrag(e_id)
                self.laden()


class SparzielPopup:
    def __init__(self, parent, farben, on_save, daten=None):
        self.on_save, self.daten = on_save, daten
        self.p = tk.Toplevel(parent)
        self.p.title("Sparziel")
        self.p.geometry("300x320")
        self.p.iconbitmap("images/sparziele.ico")
        self.p.configure(bg=farben["bg"])
        self.p.grab_set()

        self.entries = {}

        for text, key in [("Name *", "Kategorie"), ("Zielbetrag *", "Betrag"), ("Bereits gespart", "Zusatz")]:
            tk.Label(self.p, text=text, bg=farben["bg"], fg=farben["text"]).pack(anchor="w", padx=20, pady=(10, 0))
            e = tk.Entry(self.p, font=("Arial", 10), bg=farben["card"], fg=farben["text"])
            e.pack(fill="x", padx=20, pady=5)
            self.entries[key] = e
            if daten: e.insert(0, str(daten.get(key, "")).split("|")[0])

        tk.Button(self.p, text="Speichern", font=("Arial", 10, "bold"), bg="#2563eb", fg="white", relief="flat", command=self.speichern).pack(fill="x", padx=20, pady=25)

    def speichern(self):
        try:
            name = self.entries["Kategorie"].get().strip()
            ziel = float(self.entries["Betrag"].get().replace(",", ".") or 0)
            aktuell = float(self.entries["Zusatz"].get().replace(",", ".") or 0)
            
            if not name or ziel <= 0: return 

            if self.daten:
                datenbank.update_eintrag(self.daten.get("ID"), "Sparziel", "Ziel", name, ziel, "", str(aktuell))
            else:
                datenbank.speichere_eintrag("Sparziel", "Ziel", name, ziel, "", str(aktuell))

            self.p.destroy()
            self.on_save()
        except ValueError:
            pass 