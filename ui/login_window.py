from __future__ import annotations

import customtkinter as ctk
from mysql.connector import Error as MySQLError

from auth.passwords import verify_password
from database import operations as db


class LoginWindow(ctk.CTk):
    """Fenêtre de connexion affichée avant l'application principale."""

    def __init__(self) -> None:
        super().__init__()
        self.success = False
        self.title("Connexion — Gestion clinique")
        self.geometry("420x320")
        self.minsize(400, 300)
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Connexion",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(28, 8))

        ctk.CTkLabel(
            self,
            text="Identifiant",
            anchor="w",
        ).pack(fill="x", padx=40, pady=(12, 4))
        self.ent_login = ctk.CTkEntry(self, width=280, placeholder_text="login")
        self.ent_login.pack(padx=40)

        ctk.CTkLabel(
            self,
            text="Mot de passe",
            anchor="w",
        ).pack(fill="x", padx=40, pady=(12, 4))
        self.ent_password = ctk.CTkEntry(self, width=280, show="*", placeholder_text="••••••••")
        self.ent_password.pack(padx=40)

        self._err = ctk.CTkLabel(self, text="", text_color="#E57373")
        self._err.pack(pady=(10, 6))

        ctk.CTkButton(self, text="Se connecter", width=200, command=self._try_login).pack(
            pady=16
        )

        self.ent_login.bind("<Return>", lambda e: self._try_login())
        self.ent_password.bind("<Return>", lambda e: self._try_login())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self) -> None:
        self.success = False
        self.destroy()

    def _try_login(self) -> None:
        self._err.configure(text="")
        login = (self.ent_login.get() or "").strip()
        password = self.ent_password.get() or ""
        if not login or not password:
            self._err.configure(text="Saisissez identifiant et mot de passe.")
            return
        try:
            row = db.auth_fetch_by_login(login)
        except MySQLError as e:
            self._err.configure(text="Erreur base de données. Vérifiez MySQL et la table utilisateurs.")
            return
        if not row:
            self._err.configure(text="Identifiant ou mot de passe incorrect.")
            return
        if not verify_password(
            password,
            row["pass_salt_hex"],
            row["pass_hash_hex"],
        ):
            self._err.configure(text="Identifiant ou mot de passe incorrect.")
            return
        self.success = True
        self.destroy()
