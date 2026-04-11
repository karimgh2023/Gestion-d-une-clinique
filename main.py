"""
Point d'entrée — Gestion d'une clinique (CustomTkinter + MySQL).
Lancer depuis la racine du projet : python main.py
"""

from __future__ import annotations

import customtkinter as ctk

from ui.main_window import MainWindow


def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
