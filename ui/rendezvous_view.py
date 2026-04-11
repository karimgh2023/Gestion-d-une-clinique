from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from mysql.connector import Error as MySQLError
from mysql.connector import errorcode

from database import operations as db
from ui.helpers import export_csv_rows, parse_datetime_local
from ui.tree_table import TreeTable

_STATUTS = ["planifie", "termine", "annule"]


class RendezVousView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._all_rows: list[tuple] = []
        self._patient_choices: list[tuple[int, str]] = []
        self._medecin_choices: list[tuple[int, str]] = []
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self,
            text="Rendez-vous",
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

        ctk.CTkLabel(form, text="Date/heure (AAAA-MM-JJ HH:MM) *", width=200, anchor="w").grid(
            row=2, column=0, padx=6, pady=4, sticky="w"
        )
        self.ent_dt = ctk.CTkEntry(form, width=320)
        self.ent_dt.grid(row=2, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Motif *", width=200, anchor="w").grid(
            row=3, column=0, padx=6, pady=4, sticky="w"
        )
        self.ent_motif = ctk.CTkEntry(form, width=320)
        self.ent_motif.grid(row=3, column=1, padx=6, pady=4, sticky="w")

        ctk.CTkLabel(form, text="Statut *", width=200, anchor="w").grid(
            row=4, column=0, padx=6, pady=4, sticky="w"
        )
        self.statut_menu = ctk.CTkOptionMenu(form, values=_STATUTS)
        self.statut_menu.grid(row=4, column=1, padx=6, pady=4, sticky="w")
        self.statut_menu.set("planifie")

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
        ctk.CTkLabel(search_fr, text="Recherche (patient, médecin, motif) :").pack(
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
                "dt",
                "patient",
                "medecin",
                "motif",
                "statut",
            ),
            headings=("ID", "Date/heure", "Patient", "Médecin", "Motif", "Statut"),
            column_widths=(50, 140, 160, 180, 200, 90),
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
            rows = db.rendez_vous_fetch_all()
        except MySQLError as e:
            messagebox.showerror("Base de données", str(e))
            return
        self._all_rows = [
            (
                r["id"],
                str(r["date_heure"]),
                r["patient_nom"],
                r["medecin_nom"],
                r["motif"],
                r["statut"],
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
            if q in str(row[2]).lower()
            or q in str(row[3]).lower()
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
        rid = int(vals[0])
        try:
            rows = db.rendez_vous_fetch_all()
        except MySQLError:
            return
        row = next((x for x in rows if x["id"] == rid), None)
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
        self.ent_dt.delete(0, "end")
        dh = row["date_heure"]
        if isinstance(dh, datetime):
            self.ent_dt.insert(0, dh.strftime("%Y-%m-%d %H:%M"))
        else:
            s = str(dh).replace("T", " ")
            self.ent_dt.insert(0, s[:16] if len(s) >= 16 else s)
        self.ent_motif.delete(0, "end")
        self.ent_motif.insert(0, row["motif"])
        self.statut_menu.set(row["statut"])

    def _clear_form(self) -> None:
        self._err.configure(text="")
        self.ent_dt.delete(0, "end")
        self.ent_motif.delete(0, "end")
        self.statut_menu.set("planifie")

    def _validate(self):
        self._err.configure(text="")
        pid = self._pid_from_menu()
        mid = self._mid_from_menu()
        if pid is None or mid is None:
            self._err.configure(text="Sélectionnez un patient et un médecin valides.")
            return None
        motif = self.ent_motif.get().strip()
        if not motif:
            self._err.configure(text="Motif obligatoire.")
            return None
        try:
            dt = parse_datetime_local(self.ent_dt.get().strip())
        except ValueError as e:
            self._err.configure(text=str(e))
            return None
        st = self.statut_menu.get()
        if st not in _STATUTS:
            self._err.configure(text="Statut invalide.")
            return None
        return pid, mid, dt, motif, st

    def _add(self) -> None:
        v = self._validate()
        if not v:
            return
        try:
            db.rendez_vous_insert(*v)
        except MySQLError as e:
            self._mysql_err(e)
            return
        messagebox.showinfo("Rendez-vous", "Rendez-vous créé.")
        self._clear_form()
        self.refresh()

    def _update(self) -> None:
        rid = self.table.selected_id()
        if rid is None:
            messagebox.showwarning("Rendez-vous", "Sélectionnez une ligne.")
            return
        v = self._validate()
        if not v:
            return
        try:
            db.rendez_vous_update(rid, *v)
        except MySQLError as e:
            self._mysql_err(e)
            return
        messagebox.showinfo("Rendez-vous", "Rendez-vous mis à jour.")
        self.refresh()

    def _delete(self) -> None:
        rid = self.table.selected_id()
        if rid is None:
            messagebox.showwarning("Rendez-vous", "Sélectionnez une ligne.")
            return
        if not messagebox.askyesno("Confirmation", "Supprimer ce rendez-vous ?"):
            return
        try:
            db.rendez_vous_delete(rid)
        except MySQLError as e:
            messagebox.showerror("Erreur MySQL", str(e))
            return
        messagebox.showinfo("Rendez-vous", "Supprimé.")
        self._clear_form()
        self.refresh()

    def _mysql_err(self, e: MySQLError) -> None:
        if e.errno == errorcode.ER_DUP_ENTRY:
            messagebox.showerror(
                "Conflit", "Ce créneau est déjà pris pour ce médecin."
            )
        else:
            messagebox.showerror("Erreur MySQL", str(e))

    def _export(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exporter les rendez-vous affichés",
        )
        if not path:
            return
        headers = ["ID", "Date/heure", "Patient", "Médecin", "Motif", "Statut"]
        try:
            export_csv_rows(path, headers, self.table.get_rows())
        except OSError as e:
            messagebox.showerror("Export", str(e))
            return
        messagebox.showinfo("Export", f"Fichier enregistré :\n{path}")
