"""
Point d'entrée — Gestion d'une clinique (CustomTkinter + MySQL).
Lancer depuis la racine du projet : python main.py

Réf. interface : documentation officielle CustomTkinter
https://customtkinter.tomschimansky.com/documentation/
"""

from __future__ import annotations

import customtkinter as ctk

from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    while True:
        login = LoginWindow()
        login.mainloop()
        if not login.success:
            break
        app = MainWindow()
        app.mainloop()
        if not app.wants_relogin:
            break


if __name__ == "__main__":
    main()
