from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
from mysql.connector import Error as MySQLError

from database import operations as db
from ui.helpers import export_csv_rows, parse_date_fr
from ui.tree_table import TreeTable


class PrescriptionsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._all_rows: list[tuple] = []
        self._patient_choices: list[tuple[int, str]] = []
        self._medecin_choices: list[tuple[int, str]] = []
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Prescriptions",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        self._err = ctk.CTkLabel(self, text="", text_color="#E57373")
        self._err.pack(anchor="w")

        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(form, text="Patient *", width=200, anchor="w").grid(
            row=0, column=0, padx=6, pady=4, sticky="w"
        )
        self.patient_menu = ctk.CTkOptionMenu(form, values=["—"])
        self.patient_menu.grid(row=0, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Médecin *", width=200, anchor="w").grid(
            row=1, column=0, padx=6, pady=4, sticky="w"
        )
        self.medecin_menu = ctk.CTkOptionMenu(form, values=["—"])
        self.medecin_menu.grid(row=1, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Date (AAAA-MM-JJ) *", width=200, anchor="w").grid(
            row=2, column=0, padx=6, pady=4, sticky="w"
        )
        self.ent_date = ctk.CTkEntry(form, width=320)
        self.ent_date.grid(row=2, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Médicament *", width=200, anchor="w").grid(
            row=3, column=0, padx=6, pady=4, sticky="w"
        )
        self.ent_med = ctk.CTkEntry(form, width=320)
        self.ent_med.grid(row=3, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Posologie *", width=200, anchor="w").grid(
            row=4, column=0, padx=6, pady=4, sticky="w"
        )
        self.ent_poso = ctk.CTkEntry(form, width=320)
        self.ent_poso.grid(row=4, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Durée (jours) *", width=200, anchor="w").grid(
            row=5, column=0, padx=6, pady=4, sticky="w"
        )
        self.ent_duree = ctk.CTkEntry(form, width=320)
        self.ent_duree.grid(row=5, column=1, padx=6, pady=4, sticky="w")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", pady=(0, 8))
        for txt, cmd in (
            ("Ajouter", self._add),
            ("Modifier", self._update),
            ("Supprimer", self._delete),
            ("Réinitialiser", self._clear_form),
        ):
            ctk.CTkButton(btns, text=txt, width=120, command=cmd).pack(
                side="left", padx=4
            )

        search_fr = ctk.CTkFrame(self, fg_color="transparent")
        search_fr.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(search_fr, text="Recherche (médicament, patient) :").pack(
            side="left", padx=(0, 8)
        )
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())
        ctk.CTkEntry(search_fr, textvariable=self.search_var, width=260).pack(
            side="left", padx=4
        )
        ctk.CTkButton(search_fr, text="Exporter CSV", width=130, command=self._export).pack(
            side="right", padx=4
        )

        host = tk.Frame(self)
        host.pack(fill="both", expand=True)
        self.table = TreeTable(
            host,
            columns=(
                "id",
                "date",
                "patient",
                "medecin",
                "medicament",
                "posologie",
                "duree",
            ),
            headings=(
                "ID",
                "Date",
                "Patient",
                "Médecin",
                "Médicament",
                "Posologie",
                "Jours",
            ),
            column_widths=(45, 95, 130, 150, 140, 180, 55),
        )
        self.table.pack(fill="both", expand=True)
        self.table.set_on_selection(self._on_row_selected)

    def _reload_menus(self) -> None:
        try:
            self._patient_choices = db.patients_options()
            self._medecin_choices = db.medecins_options()
        except MySQLError as e:
            messagebox.showerror("Base de données", str(e))
            self._patient_choices = []
            self._medecin_choices = []
        pv = [c[1] for c in self._patient_choices] or ["— Aucun patient —"]
        mv = [c[1] for c in self._medecin_choices] or ["— Aucun médecin —"]
        self.patient_menu.configure(values=pv)
        self.medecin_menu.configure(values=mv)
        self.patient_menu.set(pv[0])
        self.medecin_menu.set(mv[0])

    def on_show(self) -> None:
        self._reload_menus()
        self.refresh()

    def refresh(self) -> None:
        try:
            rows = db.prescriptions_fetch_all()
        except MySQLError as e:
            messagebox.showerror("Base de données", str(e))
            return
        self._all_rows = [
            (
                r["id"],
                str(r["date_prescription"]),
                r["patient_nom"],
                r["medecin_nom"],
                r["medicament"],
                r["posologie"],
                r["duree_jours"],
            )
            for r in rows
        ]
        self._apply_filter()

    def _apply_filter(self) -> None:
        q = (self.search_var.get() or "").strip().lower()
        if not q:
            self.table.set_rows(list(self._all_rows))
            return
        filtered = [
            row
            for row in self._all_rows
            if q in str(row[3]).lower()
            or q in str(row[2]).lower()
            or q in str(row[4]).lower()
        ]
        self.table.set_rows(filtered)

    def _pid_from_menu(self) -> int | None:
        lab = self.patient_menu.get()
        for i, lb in self._patient_choices:
            if lb == lab:
                return i
        return None

    def _mid_from_menu(self) -> int | None:
        lab = self.medecin_menu.get()
        for i, lb in self._medecin_choices:
            if lb == lab:
                return i
        return None

    def _on_row_selected(self) -> None:
        vals = self.table.selected_values()
        if not vals:
            return
        prid = int(vals[0])
        try:
            rows = db.prescriptions_fetch_all()
        except MySQLError:
            return
        row = next((x for x in rows if x["id"] == prid), None)
        if not row:
            return
        for i, lb in self._patient_choices:
            if i == row["patient_id"]:
                self.patient_menu.set(lb)
                break
        for i, lb in self._medecin_choices:
            if i == row["medecin_id"]:
                self.medecin_menu.set(lb)
                break
        self.ent_date.delete(0, "end")
        self.ent_date.insert(0, str(row["date_prescription"]))
        self.ent_med.delete(0, "end")
        self.ent_med.insert(0, row["medicament"])
        self.ent_poso.delete(0, "end")
        self.ent_poso.insert(0, row["posologie"])
        self.ent_duree.delete(0, "end")
        self.ent_duree.insert(0, str(row["duree_jours"]))

    def _clear_form(self) -> None:
        self._err.configure(text="")
        self.ent_date.delete(0, "end")
        self.ent_med.delete(0, "end")
        self.ent_poso.delete(0, "end")
        self.ent_duree.delete(0, "end")

    def _validate(self):
        self._err.configure(text="")
        pid = self._pid_from_menu()
        mid = self._mid_from_menu()
        if pid is None or mid is None:
            self._err.configure(text="Sélectionnez un patient et un médecin valides.")
            return None
        med = self.ent_med.get().strip()
        poso = self.ent_poso.get().strip()
        if not med or not poso:
            self._err.configure(text="Médicament et posologie obligatoires.")
            return None
        try:
            d = parse_date_fr(self.ent_date.get())
        except ValueError:
            self._err.configure(text="Date invalide (AAAA-MM-JJ).")
            return None
        try:
            dj = int(self.ent_duree.get().strip())
        except ValueError:
            self._err.configure(text="Durée en jours : entier requis.")
            return None
        if dj <= 0:
            self._err.configure(text="La durée doit être > 0.")
            return None
        return pid, mid, d, med, poso, dj

    def _add(self) -> None:
        v = self._validate()
        if not v:
            return
        try:
            db.prescriptions_insert(*v)
        except MySQLError as e:
            messagebox.showerror("Erreur MySQL", str(e))
            return
        messagebox.showinfo("Prescriptions", "Prescription ajoutée.")
        self._clear_form()
        self.refresh()

    def _update(self) -> None:
        prid = self.table.selected_id()
        if prid is None:
            messagebox.showwarning("Prescriptions", "Sélectionnez une ligne.")
            return
        v = self._validate()
        if not v:
            return
        try:
            db.prescriptions_update(prid, *v)
        except MySQLError as e:
            messagebox.showerror("Erreur MySQL", str(e))
            return
        messagebox.showinfo("Prescriptions", "Prescription mise à jour.")
        self.refresh()

    def _delete(self) -> None:
        prid = self.table.selected_id()
        if prid is None:
            messagebox.showwarning("Prescriptions", "Sélectionnez une ligne.")
            return
        if not messagebox.askyesno("Confirmation", "Supprimer cette prescription ?"):
            return
        try:
            db.prescriptions_delete(prid)
        except MySQLError as e:
            messagebox.showerror("Erreur MySQL", str(e))
            return
        messagebox.showinfo("Prescriptions", "Supprimée.")
        self._clear_form()
        self.refresh()

    def _export(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exporter les prescriptions affichées",
        )
        if not path:
            return
        headers = [
            "ID",
            "Date",
            "Patient",
            "Médecin",
            "Médicament",
            "Posologie",
            "Jours",
        ]
        try:
            export_csv_rows(path, headers, self.table.get_rows())
        except OSError as e:
            messagebox.showerror("Export", str(e))
            return
        messagebox.showinfo("Export", f"Fichier enregistré :\n{path}")
