"""Requêtes paramétrées — patients, médecins, rendez-vous, prescriptions, statistiques."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from mysql.connector import Error

from database.connection import get_connection


def _run(query: str, params: tuple | None = None, fetch: str | None = None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch == "all":
            return cursor.fetchall()
        if fetch == "one":
            return cursor.fetchone()
        conn.commit()
        return cursor.lastrowid
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


# --- Patients ---
def patients_fetch_all() -> list[dict[str, Any]]:
    rows = _run(
        """
        SELECT id, nom, prenom, date_naissance, telephone, email, numero_dossier
        FROM patients
        ORDER BY nom, prenom
        """,
        fetch="all",
    )
    return rows or []


def patients_insert(
    nom: str,
    prenom: str,
    date_naissance: date,
    telephone: str,
    email: str | None,
    numero_dossier: str,
) -> int:
    return _run(
        """
        INSERT INTO patients (nom, prenom, date_naissance, telephone, email, numero_dossier)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (nom, prenom, date_naissance, telephone, email or None, numero_dossier),
    )


def patients_update(
    pid: int,
    nom: str,
    prenom: str,
    date_naissance: date,
    telephone: str,
    email: str | None,
    numero_dossier: str,
) -> None:
    _run(
        """
        UPDATE patients
        SET nom=%s, prenom=%s, date_naissance=%s, telephone=%s, email=%s, numero_dossier=%s
        WHERE id=%s
        """,
        (nom, prenom, date_naissance, telephone, email or None, numero_dossier, pid),
    )


def patients_delete(pid: int) -> None:
    _run("DELETE FROM patients WHERE id=%s", (pid,))


# --- Médecins ---
def medecins_fetch_all() -> list[dict[str, Any]]:
    rows = _run(
        """
        SELECT id, nom, prenom, specialite, email, telephone
        FROM medecins
        ORDER BY nom, prenom
        """,
        fetch="all",
    )
    return rows or []


def medecins_insert(
    nom: str, prenom: str, specialite: str, email: str, telephone: str
) -> int:
    return _run(
        """
        INSERT INTO medecins (nom, prenom, specialite, email, telephone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nom, prenom, specialite, email, telephone),
    )


def medecins_update(
    mid: int, nom: str, prenom: str, specialite: str, email: str, telephone: str
) -> None:
    _run(
        """
        UPDATE medecins
        SET nom=%s, prenom=%s, specialite=%s, email=%s, telephone=%s
        WHERE id=%s
        """,
        (nom, prenom, specialite, email, telephone, mid),
    )


def medecins_delete(mid: int) -> None:
    _run("DELETE FROM medecins WHERE id=%s", (mid,))


# --- Rendez-vous ---
def rendez_vous_fetch_all() -> list[dict[str, Any]]:
    rows = _run(
        """
        SELECT r.id, r.date_heure, r.motif, r.statut,
               r.patient_id, r.medecin_id,
               CONCAT(p.nom, ' ', p.prenom) AS patient_nom,
               CONCAT(m.nom, ' ', m.prenom) AS medecin_nom
        FROM rendez_vous r
        INNER JOIN patients p ON p.id = r.patient_id
        INNER JOIN medecins m ON m.id = r.medecin_id
        ORDER BY r.date_heure DESC
        """,
        fetch="all",
    )
    return rows or []


def rendez_vous_insert(
    patient_id: int,
    medecin_id: int,
    date_heure: datetime,
    motif: str,
    statut: str,
) -> int:
    return _run(
        """
        INSERT INTO rendez_vous (patient_id, medecin_id, date_heure, motif, statut)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (patient_id, medecin_id, date_heure, motif, statut),
    )


def rendez_vous_update(
    rid: int,
    patient_id: int,
    medecin_id: int,
    date_heure: datetime,
    motif: str,
    statut: str,
) -> None:
    _run(
        """
        UPDATE rendez_vous
        SET patient_id=%s, medecin_id=%s, date_heure=%s, motif=%s, statut=%s
        WHERE id=%s
        """,
        (patient_id, medecin_id, date_heure, motif, statut, rid),
    )


def rendez_vous_delete(rid: int) -> None:
    _run("DELETE FROM rendez_vous WHERE id=%s", (rid,))


# --- Prescriptions ---
def prescriptions_fetch_all() -> list[dict[str, Any]]:
    rows = _run(
        """
        SELECT pr.id, pr.date_prescription, pr.medicament, pr.posologie, pr.duree_jours,
               pr.patient_id, pr.medecin_id,
               CONCAT(p.nom, ' ', p.prenom) AS patient_nom,
               CONCAT(m.nom, ' ', m.prenom) AS medecin_nom
        FROM prescriptions pr
        INNER JOIN patients p ON p.id = pr.patient_id
        INNER JOIN medecins m ON m.id = pr.medecin_id
        ORDER BY pr.date_prescription DESC
        """,
        fetch="all",
    )
    return rows or []


def prescriptions_insert(
    patient_id: int,
    medecin_id: int,
    date_prescription: date,
    medicament: str,
    posologie: str,
    duree_jours: int,
) -> int:
    return _run(
        """
        INSERT INTO prescriptions
          (patient_id, medecin_id, date_prescription, medicament, posologie, duree_jours)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (patient_id, medecin_id, date_prescription, medicament, posologie, duree_jours),
    )


def prescriptions_update(
    prid: int,
    patient_id: int,
    medecin_id: int,
    date_prescription: date,
    medicament: str,
    posologie: str,
    duree_jours: int,
) -> None:
    _run(
        """
        UPDATE prescriptions
        SET patient_id=%s, medecin_id=%s, date_prescription=%s,
            medicament=%s, posologie=%s, duree_jours=%s
        WHERE id=%s
        """,
        (
            patient_id,
            medecin_id,
            date_prescription,
            medicament,
            posologie,
            duree_jours,
            prid,
        ),
    )


def prescriptions_delete(prid: int) -> None:
    _run("DELETE FROM prescriptions WHERE id=%s", (prid,))


# --- Listes pour formulaires ---
def patients_options() -> list[tuple[int, str]]:
    rows = patients_fetch_all()
    return [(r["id"], f"{r['nom']} {r['prenom']} (#{r['numero_dossier']})") for r in rows]


def medecins_options() -> list[tuple[int, str]]:
    rows = medecins_fetch_all()
    return [(r["id"], f"Dr {r['prenom']} {r['nom']} — {r['specialite']}") for r in rows]


# --- Statistiques ---
def stats_summary() -> dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        out: dict[str, Any] = {}
        cursor.execute("SELECT COUNT(*) AS n FROM patients")
        out["patients"] = cursor.fetchone()["n"]
        cursor.execute("SELECT COUNT(*) AS n FROM medecins")
        out["medecins"] = cursor.fetchone()["n"]
        cursor.execute("SELECT COUNT(*) AS n FROM rendez_vous")
        out["rendez_vous"] = cursor.fetchone()["n"]
        cursor.execute(
            "SELECT COUNT(*) AS n FROM rendez_vous WHERE DATE(date_heure) = CURDATE()"
        )
        out["rdv_aujourdhui"] = cursor.fetchone()["n"]
        cursor.execute("SELECT COUNT(*) AS n FROM prescriptions")
        out["prescriptions"] = cursor.fetchone()["n"]
        cursor.execute("SELECT AVG(duree_jours) AS m FROM prescriptions")
        row = cursor.fetchone()
        out["duree_moyenne_prescription"] = (
            float(row["m"]) if row and row["m"] is not None else 0.0
        )
        return out
    finally:
        cursor.close()
        conn.close()
