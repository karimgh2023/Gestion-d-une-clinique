# Gestion d'une clinique

Application desktop **Python 3.10+**, interface **CustomTkinter**, base **MySQL 8.x** via **mysql-connector-python** (projet académique).

## Prérequis

- Python 3.10 ou supérieur
- Serveur MySQL 8.x (WAMP, XAMPP, MySQL Server, etc.)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration MySQL

1. Créez la base et les tables : exécutez le script `sql/schema.sql` (phpMyAdmin, MySQL Workbench ou ligne de commande).

2. Copiez `config.example.ini` vers `config.ini` et renseignez `user`, `password`, `host`, `database` :

```ini
[mysql]
host = localhost
port = 3306
user = root
password = votre_mot_de_passe
database = clinique_db
```

Ne commitez pas `config.ini` (déjà ignoré par `.gitignore`).

## Lancement

À la racine du projet :

```bash
python main.py
```

## Fonctionnalités (cahier des charges)

- CRUD pour **Patients**, **Médecins**, **Rendez-vous**, **Prescriptions** (tableaux `ttk.Treeview`, scrollbars, confirmations de suppression).
- **Recherche** dynamique, **tri** par clic sur les en-têtes de colonnes, **export CSV** (données affichées) sur chaque module liste.
- Écran **Statistiques** (comptages, moyenne de durée des prescriptions).
- Requêtes SQL **paramétrées** ; paramètres de connexion **externalisés**.

## Structure du dépôt

- `main.py` — entrée
- `database/` — connexion et requêtes
- `ui/` — fenêtre principale, vues par entité, composant tableau
- `sql/schema.sql` — schéma + données de test

## Contrôle manuel (avant soutenance)

À vérifier une fois la base importée et `config.ini` renseigné :

- **Patients** : ajout avec champs vides (message d’erreur) ; doublon de **n° dossier** ou **email** (message MySQL clair) ; modification puis suppression (avec RDV existant : refus si FK).
- **Médecins** : email dupliqué ; suppression d’un médecin lié à un RDV (refus).
- **Rendez-vous** : même créneau pour le même médecin (contrainte `UNIQUE`) ; recherche / tri / export CSV sur les lignes filtrées.
- **Prescriptions** : durée ≤ 0 refusée ; export après filtre.
- **Statistiques** : bouton « Actualiser » après ajout de données.
