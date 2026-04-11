from __future__ import annotations

import customtkinter as ctk
from mysql.connector import Error as MySQLError
from tkinter import messagebox

from database import operations as db


class StatsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._labels: dict[str, ctk.CTkLabel] = {}
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Statistiques",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w", pady=(0, 16))

        box = ctk.CTkFrame(self)
        box.pack(fill="x", pady=8)
        keys = [
            ("patients", "Nombre de patients"),
            ("medecins", "Nombre de médecins"),
            ("rendez_vous", "Nombre total de rendez-vous"),
            ("rdv_aujourdhui", "Rendez-vous aujourd'hui"),
            ("prescriptions", "Nombre de prescriptions"),
            ("duree_moyenne_prescription", "Durée moyenne des prescriptions (jours)"),
        ]
        for i, (k, title) in enumerate(keys):
            ctk.CTkLabel(box, text=f"{title} :", anchor="w", width=360).grid(
                row=i, column=0, padx=12, pady=8, sticky="w"
            )
            lab = ctk.CTkLabel(box, text="—", anchor="w", font=ctk.CTkFont(weight="bold"))
            lab.grid(row=i, column=1, padx=12, pady=8, sticky="w")
            self._labels[k] = lab

        ctk.CTkButton(self, text="Actualiser", width=160, command=self.refresh).pack(
            anchor="w", pady=16
        )

    def on_show(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        try:
            s = db.stats_summary()
        except MySQLError as e:
            messagebox.showerror("Base de données", str(e))
            return
        self._labels["patients"].configure(text=str(s["patients"]))
        self._labels["medecins"].configure(text=str(s["medecins"]))
        self._labels["rendez_vous"].configure(text=str(s["rendez_vous"]))
        self._labels["rdv_aujourdhui"].configure(text=str(s["rdv_aujourdhui"]))
        self._labels["prescriptions"].configure(text=str(s["prescriptions"]))
        dm = s["duree_moyenne_prescription"]
        self._labels["duree_moyenne_prescription"].configure(
            text=f"{dm:.2f}" if dm else "0"
        )
