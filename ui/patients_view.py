from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
from mysql.connector import Error as MySQLError
from mysql.connector import errorcode

from database import operations as db
from ui.helpers import export_csv_rows, parse_date_fr
from ui.tree_table import TreeTable


class PatientsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._all_rows: list[tuple] = []
        self._build()

    def _build(self) -> None:
        title = ctk.CTkLabel(self, text="Patients", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(anchor="w", pady=(0, 8))

        self._err = ctk.CTkLabel(self, text="", text_color="#E57373")
        self._err.pack(anchor="w")

        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 8))

        self.ent_nom = self._row(form, 0, "Nom *")
        self.ent_prenom = self._row(form, 1, "Prénom *")
        self.ent_naissance = self._row(form, 2, "Naissance (AAAA-MM-JJ) *")
        self.ent_tel = self._row(form, 3, "Téléphone *")
        self.ent_email = self._row(form, 4, "Email (optionnel)")
        self.ent_dossier = self._row(form, 5, "N° dossier *")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", pady=(0, 8))
        ctk.CTkButton(btns, text="Ajouter", width=120, command=self._add).pack(
            side="left", padx=4
        )
        ctk.CTkButton(btns, text="Modifier", width=120, command=self._update).pack(
            side="left", padx=4
        )
        ctk.CTkButton(btns, text="Supprimer", width=120, command=self._delete).pack(
            side="left", padx=4
        )
        ctk.CTkButton(btns, text="Réinitialiser", width=120, command=self._clear_form).pack(
            side="left", padx=4
        )

        search_fr = ctk.CTkFrame(self, fg_color="transparent")
        search_fr.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(search_fr, text="Recherche (nom ou n° dossier) :").pack(
            side="left", padx=(0, 8)
        )
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())
        ctk.CTkEntry(search_fr, textvariable=self.search_var, width=280).pack(
            side="left", padx=4
        )
        ctk.CTkButton(search_fr, text="Exporter CSV", width=130, command=self._export).pack(
            side="right", padx=4
        )

        host = tk.Frame(self)
        host.pack(fill="both", expand=True)
        self.table = TreeTable(
            host,
            columns=("id", "nom", "prenom", "naissance", "telephone", "email", "dossier"),
            headings=("ID", "Nom", "Prénom", "Naissance", "Téléphone", "Email", "N° dossier"),
            column_widths=(50, 110, 110, 100, 110, 160, 120),
        )
        self.table.pack(fill="both", expand=True)
        self.table.set_on_selection(self._on_row_selected)

    def _row(self, parent, row: int, label: str) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, width=220, anchor="w").grid(
            row=row, column=0, padx=6, pady=4, sticky="w"
        )
        e = ctk.CTkEntry(parent, width=320)
        e.grid(row=row, column=1, padx=6, pady=4, sticky="w")
        return e

    def on_show(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        try:
            rows = db.patients_fetch_all()
        except MySQLError as e:
            messagebox.showerror("Base de données", str(e))
            return
        self._all_rows = [
            (
                r["id"],
                r["nom"],
                r["prenom"],
                str(r["date_naissance"]),
                r["telephone"],
                r["email"] or "",
                r["numero_dossier"],
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
            if q in str(row[1]).lower()
            or q in str(row[6]).lower()
            or q in str(row[0]).lower()
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
        self.ent_naissance.delete(0, "end")
        self.ent_naissance.insert(0, vals[3])
        self.ent_tel.delete(0, "end")
        self.ent_tel.insert(0, vals[4])
        self.ent_email.delete(0, "end")
        self.ent_email.insert(0, vals[5])
        self.ent_dossier.delete(0, "end")
        self.ent_dossier.insert(0, vals[6])

    def _clear_form(self) -> None:
        for e in (
            self.ent_nom,
            self.ent_prenom,
            self.ent_naissance,
            self.ent_tel,
            self.ent_email,
            self.ent_dossier,
        ):
            e.delete(0, "end")
        self._err.configure(text="")

    def _validate(self) -> tuple[str, str, object, str, str | None, str] | None:
        self._err.configure(text="")
        nom = self.ent_nom.get().strip()
        prenom = self.ent_prenom.get().strip()
        dn_s = self.ent_naissance.get().strip()
        tel = self.ent_tel.get().strip()
        email = self.ent_email.get().strip() or None
        dossier = self.ent_dossier.get().strip()
        if not all([nom, prenom, dn_s, tel, dossier]):
            self._err.configure(text="Champs obligatoires manquants.")
            return None
        try:
            d = parse_date_fr(dn_s)
        except ValueError:
            self._err.configure(text="Date de naissance invalide (AAAA-MM-JJ).")
            return None
        if email and "@" not in email:
            self._err.configure(text="Email invalide.")
            return None
        return nom, prenom, d, tel, email, dossier

    def _add(self) -> None:
        v = self._validate()
        if not v:
            return
        nom, prenom, d, tel, email, dossier = v
        try:
            db.patients_insert(nom, prenom, d, tel, email, dossier)
        except MySQLError as e:
            self._handle_mysql(e)
            return
        messagebox.showinfo("Patients", "Patient ajouté.")
        self._clear_form()
        self.refresh()

    def _update(self) -> None:
        pid = self.table.selected_id()
        if pid is None:
            messagebox.showwarning("Patients", "Sélectionnez une ligne à modifier.")
            return
        v = self._validate()
        if not v:
            return
        nom, prenom, d, tel, email, dossier = v
        try:
            db.patients_update(pid, nom, prenom, d, tel, email, dossier)
        except MySQLError as e:
            self._handle_mysql(e)
            return
        messagebox.showinfo("Patients", "Patient mis à jour.")
        self.refresh()

    def _delete(self) -> None:
        pid = self.table.selected_id()
        if pid is None:
            messagebox.showwarning("Patients", "Sélectionnez une ligne à supprimer.")
            return
        if not messagebox.askyesno(
            "Confirmation", "Supprimer ce patient ? (impossible s'il a des rendez-vous.)"
        ):
            return
        try:
            db.patients_delete(pid)
        except MySQLError as e:
            self._handle_mysql(e)
            return
        messagebox.showinfo("Patients", "Patient supprimé.")
        self._clear_form()
        self.refresh()

    def _handle_mysql(self, e: MySQLError) -> None:
        if e.errno == errorcode.ER_DUP_ENTRY:
            messagebox.showerror("Doublon", "N° dossier ou email déjà utilisé.")
        elif e.errno == errorcode.ER_ROW_IS_REFERENCED_2:
            messagebox.showerror(
                "Suppression impossible",
                "Ce patient est référencé par un rendez-vous ou autre enregistrement.",
            )
        else:
            messagebox.showerror("Erreur MySQL", str(e))

    def _export(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exporter les patients affichés",
        )
        if not path:
            return
        headers = ["ID", "Nom", "Prénom", "Naissance", "Téléphone", "Email", "N° dossier"]
        try:
            export_csv_rows(path, headers, self.table.get_rows())
        except OSError as e:
            messagebox.showerror("Export", str(e))
            return
        messagebox.showinfo("Export", f"Fichier enregistré :\n{path}")
