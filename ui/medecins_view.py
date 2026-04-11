from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
from mysql.connector import Error as MySQLError
from mysql.connector import errorcode

from database import operations as db
from ui.helpers import export_csv_rows
from ui.tree_table import TreeTable


class MedecinsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._all_rows: list[tuple] = []
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(
            self, text="Médecins", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", pady=(0, 8))

        self._err = ctk.CTkLabel(self, text="", text_color="#E57373")
        self._err.pack(anchor="w")

        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 8))

        self.ent_nom = self._row(form, 0, "Nom *")
        self.ent_prenom = self._row(form, 1, "Prénom *")
        self.ent_spec = self._row(form, 2, "Spécialité *")
        self.ent_email = self._row(form, 3, "Email *")
        self.ent_tel = self._row(form, 4, "Téléphone *")

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
        ctk.CTkLabel(search_fr, text="Recherche (nom, spécialité) :").pack(
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
            columns=("id", "nom", "prenom", "specialite", "email", "tel"),
            headings=("ID", "Nom", "Prénom", "Spécialité", "Email", "Téléphone"),
            column_widths=(50, 110, 110, 140, 200, 110),
        )
        self.table.pack(fill="both", expand=True)
        self.table.set_on_selection(self._on_row_selected)

    def _row(self, parent, row: int, label: str) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, width=200, anchor="w").grid(
            row=row, column=0, padx=6, pady=4, sticky="w"
        )
        e = ctk.CTkEntry(parent, width=340)
        e.grid(row=row, column=1, padx=6, pady=4, sticky="w")
        return e

    def on_show(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        try:
            rows = db.medecins_fetch_all()
        except MySQLError as e:
            messagebox.showerror("Base de données", str(e))
            return
        self._all_rows = [
            (r["id"], r["nom"], r["prenom"], r["specialite"], r["email"], r["telephone"])
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
            if q in str(row[1]).lower()
            or q in str(row[2]).lower()
            or q in str(row[3]).lower()
        ]
        self.table.set_rows(filtered)

    def _on_row_selected(self) -> None:
        vals = self.table.selected_values()
        if not vals:
            return
        self.ent_nom.delete(0, "end")
        self.ent_nom.insert(0, vals[1])
        self.ent_prenom.delete(0, "end")
        self.ent_prenom.insert(0, vals[2])
        self.ent_spec.delete(0, "end")
        self.ent_spec.insert(0, vals[3])
        self.ent_email.delete(0, "end")
        self.ent_email.insert(0, vals[4])
        self.ent_tel.delete(0, "end")
        self.ent_tel.insert(0, vals[5])

    def _clear_form(self) -> None:
        for e in (
            self.ent_nom,
            self.ent_prenom,
            self.ent_spec,
            self.ent_email,
            self.ent_tel,
        ):
            e.delete(0, "end")
        self._err.configure(text="")

    def _validate(self) -> tuple[str, str, str, str, str] | None:
        self._err.configure(text="")
        nom = self.ent_nom.get().strip()
        prenom = self.ent_prenom.get().strip()
        spec = self.ent_spec.get().strip()
        email = self.ent_email.get().strip()
        tel = self.ent_tel.get().strip()
        if not all([nom, prenom, spec, email, tel]):
            self._err.configure(text="Champs obligatoires manquants.")
            return None
        if "@" not in email:
            self._err.configure(text="Email invalide.")
            return None
        return nom, prenom, spec, email, tel

    def _add(self) -> None:
        v = self._validate()
        if not v:
            return
        try:
            db.medecins_insert(*v)
        except MySQLError as e:
            self._mysql_err(e)
            return
        messagebox.showinfo("Médecins", "Médecin ajouté.")
        self._clear_form()
        self.refresh()

    def _update(self) -> None:
        mid = self.table.selected_id()
        if mid is None:
            messagebox.showwarning("Médecins", "Sélectionnez une ligne.")
            return
        v = self._validate()
        if not v:
            return
        try:
            db.medecins_update(mid, *v)
        except MySQLError as e:
            self._mysql_err(e)
            return
        messagebox.showinfo("Médecins", "Médecin mis à jour.")
        self.refresh()

    def _delete(self) -> None:
        mid = self.table.selected_id()
        if mid is None:
            messagebox.showwarning("Médecins", "Sélectionnez une ligne.")
            return
        if not messagebox.askyesno(
            "Confirmation", "Supprimer ce médecin ? (bloqué s'il a des RDV ou prescriptions.)"
        ):
            return
        try:
            db.medecins_delete(mid)
        except MySQLError as e:
            self._mysql_err(e)
            return
        messagebox.showinfo("Médecins", "Médecin supprimé.")
        self._clear_form()
        self.refresh()

    def _mysql_err(self, e: MySQLError) -> None:
        if e.errno == errorcode.ER_DUP_ENTRY:
            messagebox.showerror("Doublon", "Cet email est déjà utilisé.")
        elif e.errno == errorcode.ER_ROW_IS_REFERENCED_2:
            messagebox.showerror(
                "Suppression impossible", "Ce médecin est encore référencé."
            )
        else:
            messagebox.showerror("Erreur MySQL", str(e))

    def _export(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exporter les médecins affichés",
        )
        if not path:
            return
        headers = ["ID", "Nom", "Prénom", "Spécialité", "Email", "Téléphone"]
        try:
            export_csv_rows(path, headers, self.table.get_rows())
        except OSError as e:
            messagebox.showerror("Export", str(e))
            return
        messagebox.showinfo("Export", f"Fichier enregistré :\n{path}")
