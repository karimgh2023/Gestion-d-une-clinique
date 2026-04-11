from __future__ import annotations

import customtkinter as ctk

from ui.medecins_view import MedecinsView
from ui.patients_view import PatientsView
from ui.prescriptions_view import PrescriptionsView
from ui.rendezvous_view import RendezVousView
from ui.stats_view import StatsView


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Gestion d'une clinique")
        self.minsize(1080, 720)
        self.geometry("1240x780")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        nav = ctk.CTkFrame(self, width=210, corner_radius=0)
        nav.grid(row=0, column=0, sticky="nsew")
        nav.grid_propagate(False)

        ctk.CTkLabel(
            nav,
            text="Clinique",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(24, 8), padx=16, anchor="w")

        self._content = ctk.CTkFrame(self, fg_color="transparent")
        self._content.grid(row=0, column=1, sticky="nsew", padx=14, pady=14)
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_rowconfigure(0, weight=1)

        self._views: dict[str, ctk.CTkFrame] = {}
        self._current: str | None = None

        specs: list[tuple[str, str, type]] = [
            ("patients", "Patients", PatientsView),
            ("medecins", "Médecins", MedecinsView),
            ("rdv", "Rendez-vous", RendezVousView),
            ("presc", "Prescriptions", PrescriptionsView),
            ("stats", "Statistiques", StatsView),
        ]

        for key, label, cls in specs:
            ctk.CTkButton(
                nav,
                text=label,
                anchor="w",
                height=36,
                command=lambda k=key: self.show_view(k),
            ).pack(fill="x", padx=12, pady=6)

            view = cls(self._content, fg_color="transparent")
            view.grid(row=0, column=0, sticky="nsew")
            view.grid_remove()
            self._views[key] = view

        self.show_view("patients")

    def show_view(self, key: str) -> None:
        if self._current and self._current in self._views:
            self._views[self._current].grid_remove()
        self._current = key
        v = self._views[key]
        v.grid(row=0, column=0, sticky="nsew")
        on_show = getattr(v, "on_show", None)
        if callable(on_show):
            on_show()
