"""Parsing dates / export CSV."""

from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path


def parse_date_fr(s: str) -> date:
    s = (s or "").strip()
    return datetime.strptime(s, "%Y-%m-%d").date()


def parse_datetime_local(s: str) -> datetime:
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError("Format attendu : AAAA-MM-JJ HH:MM")


def export_csv_rows(path: str | Path, headers: list[str], rows: list[tuple]) -> None:
    path = Path(path)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(headers)
        w.writerows(rows)
