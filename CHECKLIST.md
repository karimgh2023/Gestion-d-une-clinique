# Checklist — Gestion d’une clinique (CustomTkinter + MySQL)

Objectif : couvrir **tous** les points du cahier des charges et viser **20/20**. Coche au fur et à mesure.

_Dernière revue : application lancée avec succès (MySQL + GUI)._

---

## 1. Périmètre sujet (complexité « élevée »)

- [x] **Entités principales** couvertes : Patients, Médecins, Rendez-vous, Prescriptions (et tables de liaison si besoin, ex. patient–médecin via RDV).
- [x] **Relations métier** cohérentes : un RDV lie patient + médecin (+ éventuellement créneau / salle) ; prescriptions liées à un patient et idéalement à un médecin.
- [x] **Une vue / onglet / frame dédié(e)** par entité principale (navigation claire).

---

## 2. Technologies (obligatoires)

- [x] Python **3.10+** (indiquer la version dans le README).
- [x] Interface **CustomTkinter** avec **thème cohérent** (mode clair/sombre, couleurs, police) sur toute l’app.
- [x] MySQL **8.x** en local.
- [x] Accès BDD **uniquement** via `mysql-connector-python` (pas SQLite / PostgreSQL / ORM).
- [x] **Treeview** : le cahier des charges impose `ttk.Treeview` pour les tableaux → l’intégrer dans les fenêtres CustomTkinter (`tk.Frame` ou conteneur compatible).

---

## 3. CRUD par entité (6 pts — cœur du projet)

Pour **chaque** entité principale :

- [x] **CREATE** : formulaire d’ajout + validation (champs vides, types, doublons où pertinent).
- [x] **READ** : liste de **toutes** les lignes dans un **Treeview**.
- [x] **UPDATE** : sélection d’une ligne → formulaire **pré-rempli** → enregistrement.
- [x] **DELETE** : suppression avec **confirmation** `tkinter.messagebox.askyesno` (ou équivalent clair).

---

## 4. Fonctionnalités avancées — minimum **2 sur 4** (2 pts) ; viser **3–4** pour marge

- [x] **Recherche / filtrage** dynamique sur **au moins un** champ (ex. nom patient, n° dossier).
- [x] **Tri** : clic sur **en-tête de colonne** pour trier les données affichées.
- [x] **Statistiques** : au moins un écran ou un bandeau avec comptages / somme / moyenne (ex. nb RDV du jour, nb patients actifs).
- [x] **Export CSV** des données **actuellement affichées** (après filtre si applicable).

---

## 5. Navigation & optionnel valorisant

- [x] **Menu** (barre) **ou** **sidebar** : accès explicite à chaque module (Patients, Médecins, RDV, Prescriptions).
- [x] **Fenêtre principale** redimensionnable avec **taille minimale** définie (`minsize` / équivalent CTk).
- [ ] *(Optionnel mais valorisé)* **Authentification** : fenêtre de connexion, compte(s) utilisateur ; ne **jamais** stocker les mots de passe en clair (hash + sel, ou comptes de démo documentés hors code).

---

## 6. Base de données MySQL (4 pts connexion + intégration schéma)

- [x] **Au moins 3 tables** reliées par **clés étrangères** (avec le sujet clinique, viser **4+** tables).
- [x] Script `.sql` rendu avec **CREATE TABLE** + contraintes : **NOT NULL**, **UNIQUE**, **FOREIGN KEY**, **ON DELETE** (RESTRICT / CASCADE / SET NULL selon le cas métier).
- [x] Fichier **INSERT** de **données de test** réalistes (cas limites : doublons impossibles, champs null interdits respectés).
- [x] Paramètres de connexion **externalisés** : `config.py` ou `config.ini` (hors commit des secrets : voir `.gitignore`).

---

## 7. Code Python — connexion & sécurité (4 pts + 2 pts erreurs)

- [x] **Requêtes paramétrées** partout : `%s` + tuple / `cursor.execute(query, params)` — **aucune** concaténation de valeurs utilisateur dans le SQL.
- [x] Après chaque opération : **`cursor.close()`** et **`conn.close()`** (ou context managers `with` bien utilisés).
- [x] **`try` / `except`** autour des accès BDD et actions critiques ; **messages d’erreur clairs** pour l’utilisateur (et éventuellement log en console pour le debug).
- [x] **Aucun mot de passe** en clair dans le dépôt ; fichier d’exemple `config.example.ini` / `config.example.py` sans secrets réels.

---

## 8. Interface graphique (6 pts)

- [x] **Scrollbars** verticale **et** horizontale sur les **Treeview** (données larges / nombreuses lignes).
- [x] **messagebox** pour confirmations et erreurs « utilisateur ».
- [x] **Labels** (ou texte CTk) pour les **erreurs de saisie** près des champs (validation côté UI avant envoi BDD quand c’est possible).
- [x] Présentation **propre** : espacements, titres, boutons alignés, libellés en français cohérents.

---

## 9. Livrables zip (nom : `Nom_Prénom_Projet.zip`)

- [x] Arborescence **`.py`** claire (ex. `main.py`, `database/`, `ui/`, `models/` — comme demandé par l’enseignant si précisé).
- [x] **`schema.sql`** (ou équivalent) : création + inserts test.
- [x] **`README.md`** : installation (`pip install -r requirements.txt`), création BDD, import SQL, configuration `config`, **commande de lancement**.
- [ ] **Archive .zip** finale à générer **au moment du rendu** (inclure tout le code + `sql/` + README ; exclure `venv/`, `__pycache__/`, `config.ini`).

---

## 10. Intégrité & soutenance

- [x] Code **original** ; toute ressource externe **citée en commentaire** dans le fichier concerné (voir `main.py` — doc officielle CustomTkinter).
- [x] Tests manuels : scénarios suggérés dans le **README** (section « Contrôle manuel ») ; à rejouer avant soutenance.

---

## 11. Git professionnel (historique lisible sur GitHub)

- [x] Dépôt : `https://github.com/karimgh2023/Gestion-d-une-clinique.git`, branche **`master`** (ou alignement avec l’enseignant si autre convention).
- [x] **Petits commits** logiques (une fonctionnalité ou un correctif par commit quand c’est possible).
- [x] **Messages de commit** explicites en anglais ou français, style conventionnel :
  - `feat: CRUD patients + Treeview`
  - `fix: fermeture connexion MySQL après UPDATE`
  - `docs: README installation MySQL`
- [x] Après chaque commit local : **`git push origin master`** pour garder le distant à jour (ou regroupement raisonnable si tu es hors ligne, puis push groupé).
- [x] Ne pas committer : `venv/`, `__pycache__/`, fichiers `config` avec mots de passe, `.env` secrets.

---

## 12. Barème — auto-contrôle

| Critère                         | Points | Vérifié |
|---------------------------------|--------|--------|
| CRUD complets et fonctionnels   | 6      | [x]    |
| Connexion MySQL + connecteur    | 4      | [x]    |
| Interface propre / ergonomique  | 6      | [x]    |
| Erreurs & validations           | 2      | [x]    |
| Fonctionnalités avancées (≥2)   | 2      | [x]    |
| **Total**                       | **20** | [x]    |

---

## Prochaine étape recommandée

- [ ] **Authentification** (login + mot de passe hashé) — optionnel mais valorisé au cahier des charges.
- [ ] **Rendu** : générer l’archive `Nom_Prénom_Projet.zip` selon consignes enseignant.

Bonne réalisation.
