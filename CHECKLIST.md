# Checklist — Gestion d’une clinique (CustomTkinter + MySQL)

Objectif : couvrir **tous** les points du cahier des charges et viser **20/20**. Coche au fur et à mesure.

---

## 1. Périmètre sujet (complexité « élevée »)

- [ ] **Entités principales** couvertes : Patients, Médecins, Rendez-vous, Prescriptions (et tables de liaison si besoin, ex. patient–médecin via RDV).
- [ ] **Relations métier** cohérentes : un RDV lie patient + médecin (+ éventuellement créneau / salle) ; prescriptions liées à un patient et idéalement à un médecin.
- [ ] **Une vue / onglet / frame dédié(e)** par entité principale (navigation claire).

---

## 2. Technologies (obligatoires)

- [ ] Python **3.10+** (indiquer la version dans le README).
- [ ] Interface **CustomTkinter** avec **thème cohérent** (mode clair/sombre, couleurs, police) sur toute l’app.
- [ ] MySQL **8.x** en local.
- [ ] Accès BDD **uniquement** via `mysql-connector-python` (pas SQLite / PostgreSQL / ORM).
- [ ] **Treeview** : le cahier des charges impose `ttk.Treeview` pour les tableaux → l’intégrer dans les fenêtres CustomTkinter (`tk.Frame` ou conteneur compatible).

---

## 3. CRUD par entité (6 pts — cœur du projet)

Pour **chaque** entité principale :

- [ ] **CREATE** : formulaire d’ajout + validation (champs vides, types, doublons où pertinent).
- [ ] **READ** : liste de **toutes** les lignes dans un **Treeview**.
- [ ] **UPDATE** : sélection d’une ligne → formulaire **pré-rempli** → enregistrement.
- [ ] **DELETE** : suppression avec **confirmation** `tkinter.messagebox.askyesno` (ou équivalent clair).

---

## 4. Fonctionnalités avancées — minimum **2 sur 4** (2 pts) ; viser **3–4** pour marge

- [ ] **Recherche / filtrage** dynamique sur **au moins un** champ (ex. nom patient, n° dossier).
- [ ] **Tri** : clic sur **en-tête de colonne** pour trier les données affichées.
- [ ] **Statistiques** : au moins un écran ou un bandeau avec comptages / somme / moyenne (ex. nb RDV du jour, nb patients actifs).
- [ ] **Export CSV** des données **actuellement affichées** (après filtre si applicable).

---

## 5. Navigation & optionnel valorisant

- [ ] **Menu** (barre) **ou** **sidebar** : accès explicite à chaque module (Patients, Médecins, RDV, Prescriptions).
- [ ] **Fenêtre principale** redimensionnable avec **taille minimale** définie (`minsize` / équivalent CTk).
- [ ] *(Optionnel mais valorisé)* **Authentification** : fenêtre de connexion, compte(s) utilisateur ; ne **jamais** stocker les mots de passe en clair (hash + sel, ou comptes de démo documentés hors code).

---

## 6. Base de données MySQL (4 pts connexion + intégration schéma)

- [ ] **Au moins 3 tables** reliées par **clés étrangères** (avec le sujet clinique, viser **4+** tables).
- [ ] Script `.sql` rendu avec **CREATE TABLE** + contraintes : **NOT NULL**, **UNIQUE**, **FOREIGN KEY**, **ON DELETE** (RESTRICT / CASCADE / SET NULL selon le cas métier).
- [ ] Fichier **INSERT** de **données de test** réalistes (cas limites : doublons impossibles, champs null interdits respectés).
- [ ] Paramètres de connexion **externalisés** : `config.py` ou `config.ini` (hors commit des secrets : voir `.gitignore`).

---

## 7. Code Python — connexion & sécurité (4 pts + 2 pts erreurs)

- [ ] **Requêtes paramétrées** partout : `%s` + tuple / `cursor.execute(query, params)` — **aucune** concaténation de valeurs utilisateur dans le SQL.
- [ ] Après chaque opération : **`cursor.close()`** et **`conn.close()`** (ou context managers `with` bien utilisés).
- [ ] **`try` / `except`** autour des accès BDD et actions critiques ; **messages d’erreur clairs** pour l’utilisateur (et éventuellement log en console pour le debug).
- [ ] **Aucun mot de passe** en clair dans le dépôt ; fichier d’exemple `config.example.ini` / `config.example.py` sans secrets réels.

---

## 8. Interface graphique (6 pts)

- [ ] **Scrollbars** verticale **et** horizontale sur les **Treeview** (données larges / nombreuses lignes).
- [ ] **messagebox** pour confirmations et erreurs « utilisateur ».
- [ ] **Labels** (ou texte CTk) pour les **erreurs de saisie** près des champs (validation côté UI avant envoi BDD quand c’est possible).
- [ ] Présentation **propre** : espacements, titres, boutons alignés, libellés en français cohérents.

---

## 9. Livrables zip (nom : `Nom_Prénom_Projet.zip`)

- [ ] Arborescence **`.py`** claire (ex. `main.py`, `database/`, `ui/`, `models/` — comme demandé par l’enseignant si précisé).
- [ ] **`schema.sql`** (ou équivalent) : création + inserts test.
- [ ] **`README.md`** : installation (`pip install -r requirements.txt`), création BDD, import SQL, configuration `config`, **commande de lancement**.

---

## 10. Intégrité & soutenance

- [ ] Code **original** ; toute ressource externe **citée en commentaire** dans le fichier concerné.
- [ ] Tests manuels documentés : champs vides, doublons, caractères spéciaux, suppression refusée si FK l’empêche (messages clairs).

---

## 11. Git professionnel (historique lisible sur GitHub)

- [ ] Dépôt : `https://github.com/karimgh2023/Gestion-d-une-clinique.git`, branche **`master`** (ou alignement avec l’enseignant si autre convention).
- [ ] **Petits commits** logiques (une fonctionnalité ou un correctif par commit quand c’est possible).
- [ ] **Messages de commit** explicites en anglais ou français, style conventionnel :
  - `feat: CRUD patients + Treeview`
  - `fix: fermeture connexion MySQL après UPDATE`
  - `docs: README installation MySQL`
- [ ] Après chaque commit local : **`git push origin master`** pour garder le distant à jour (ou regroupement raisonnable si tu es hors ligne, puis push groupé).
- [ ] Ne pas committer : `venv/`, `__pycache__/`, fichiers `config` avec mots de passe, `.env` secrets.

---

## 12. Barème — auto-contrôle

| Critère                         | Points | Vérifié |
|---------------------------------|--------|--------|
| CRUD complets et fonctionnels   | 6      | [ ]    |
| Connexion MySQL + connecteur    | 4      | [ ]    |
| Interface propre / ergonomique  | 6      | [ ]    |
| Erreurs & validations           | 2      | [ ]    |
| Fonctionnalités avancées (≥2)   | 2      | [ ]    |
| **Total**                       | **20** | [ ]    |

---

Bonne réalisation.
