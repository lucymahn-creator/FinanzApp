import tkinter as tk
from dashboard import FinanzTrackerDashboard
from transaktionen import TransaktionenView
from budgets import BudgetsView
from sparziele import SparzieleView

class FinanzTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finanz-Tracker")
        self.root.geometry("1100x700")
        self.root.iconbitmap("images/logo.ico")

        self.farben = {"bg": "#f4f6f9", "sidebar": "#1e293b", "card": "white", "text": "#0f172a", "text_grey": "#64748b", "sidebar_text": "white", "sidebar_active": "#334155"}
        
        self.views = {
            "Dashboard": FinanzTrackerDashboard,
            "Transaktionen": TransaktionenView,
            "Budgets": BudgetsView,
            "Sparziele": SparzieleView
        }
        
        self.nav_buttons = {}

        sidebar = tk.Frame(self.root, bg=self.farben["sidebar"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="FinanzTracker", font=("Arial", 18, "bold"), fg="white", bg=self.farben["sidebar"]).pack(pady=30)
        beenden_btn = tk.Button(sidebar, text="Programm beenden", font=("Arial", 12, "bold"), fg="#ef4444", bg=self.farben["sidebar"], relief="flat", anchor="w", padx=20, cursor="hand2", command=self.root.destroy)
        beenden_btn.pack(side="bottom", fill="x", pady=20)

        for name in self.views.keys():
            btn = tk.Button(sidebar, text=name, font=("Arial", 12), fg=self.farben["sidebar_text"], bg=self.farben["sidebar"], relief="flat", anchor="w", padx=20, cursor="hand2", command=lambda n=name: self.zeige_view(n))
            btn.pack(fill="x", pady=5)
            self.nav_buttons[name] = btn

        self.content_frame = tk.Frame(self.root, bg=self.farben["bg"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.zeige_view("Dashboard")

    def zeige_view(self, view_name):

        for name, btn in self.nav_buttons.items():
            btn.configure(bg=self.farben["sidebar_active"] if name == view_name else self.farben["sidebar"])

        for widget in self.content_frame.winfo_children(): 
            widget.destroy()

        self.views[view_name](self.content_frame, self.farben)


if __name__ == "__main__":
    root = tk.Tk()
    FinanzTrackerApp(root)
    root.mainloop()