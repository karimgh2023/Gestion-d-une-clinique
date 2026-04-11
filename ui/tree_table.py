"""Tableau ttk.Treeview avec défilement et tri par en-tête (cahier des charges)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Sequence


class TreeTable(tk.Frame):
    def __init__(
        self,
        master,
        columns: Sequence[str],
        headings: Sequence[str],
        column_widths: Sequence[int] | None = None,
        height: int = 14,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self._col_ids = tuple(columns)
        self._headings = tuple(headings)
        self._sort_col: str | None = None
        self._sort_reverse = False
        self._rows: list[tuple] = []
        self._on_selection: Callable[[], None] | None = None

        wds = column_widths or [120] * len(columns)
        self.tree = ttk.Treeview(
            self, columns=self._col_ids, show="headings", height=height
        )
        for cid, title, w in zip(self._col_ids, self._headings, wds, strict=True):
            self.tree.heading(
                cid,
                text=title,
                command=lambda c=cid: self._sort_by(c),
            )
            self.tree.column(cid, width=w, minwidth=40, stretch=True)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def set_on_selection(self, callback: Callable[[], None] | None) -> None:
        self._on_selection = callback

    def _on_tree_select(self, _event=None) -> None:
        if self._on_selection:
            self._on_selection()

    def _sort_by(self, col: str) -> None:
        idx = self._col_ids.index(col)
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False

        def key_row(row: tuple):
            v = row[idx]
            if v is None:
                return ""
            if isinstance(v, (int, float)):
                return v
            return str(v).lower()

        self._rows.sort(key=key_row, reverse=self._sort_reverse)
        self._refresh_display()

    def set_rows(self, rows: list[tuple]) -> None:
        self._rows = list(rows)
        self._refresh_display()

    def get_rows(self) -> list[tuple]:
        return list(self._rows)

    def _refresh_display(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for row in self._rows:
            self.tree.insert("", tk.END, values=row)

    def clear(self) -> None:
        self._rows = []
        self._refresh_display()

    def selected_values(self) -> tuple | None:
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0], "values")

    def selected_id(self) -> int | None:
        vals = self.selected_values()
        if not vals:
            return None
        try:
            return int(vals[0])
        except (TypeError, ValueError):
            return None
