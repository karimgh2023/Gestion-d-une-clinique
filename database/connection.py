"""Connexion MySQL — paramètres lus depuis config.ini ou config.example.ini."""

from __future__ import annotations

import configparser
from pathlib import Path

import mysql.connector

_ROOT = Path(__file__).resolve().parent.parent


def read_db_config() -> dict:
    local = _ROOT / "config.ini"
    example = _ROOT / "config.example.ini"
    path = local if local.exists() else example
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    s = parser["mysql"]
    return {
        "host": s.get("host", "localhost"),
        "port": s.getint("port", fallback=3306),
        "user": s.get("user", "root"),
        "password": s.get("password", ""),
        "database": s.get("database", "clinique_db"),
    }


def get_connection():
    return mysql.connector.connect(**read_db_config())
