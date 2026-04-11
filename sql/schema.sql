-- Gestion d'une clinique — MySQL 8.x
-- Exécuter ce script pour créer la base et les données de test.

CREATE DATABASE IF NOT EXISTS clinique_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE clinique_db;

-- Médecins
CREATE TABLE IF NOT EXISTS medecins (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  specialite VARCHAR(120) NOT NULL,
  email VARCHAR(255) NOT NULL,
  telephone VARCHAR(40) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_medecins_email (email)
) ENGINE=InnoDB;

-- Patients
CREATE TABLE IF NOT EXISTS patients (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  date_naissance DATE NOT NULL,
  telephone VARCHAR(40) NOT NULL,
  email VARCHAR(255) NULL,
  numero_dossier VARCHAR(32) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_patients_dossier (numero_dossier),
  UNIQUE KEY uq_patients_email (email)
) ENGINE=InnoDB;

-- Rendez-vous
CREATE TABLE IF NOT EXISTS rendez_vous (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  patient_id INT UNSIGNED NOT NULL,
  medecin_id INT UNSIGNED NOT NULL,
  date_heure DATETIME NOT NULL,
  motif VARCHAR(500) NOT NULL,
  statut ENUM('planifie', 'termine', 'annule') NOT NULL DEFAULT 'planifie',
  CONSTRAINT fk_rdv_patient
    FOREIGN KEY (patient_id) REFERENCES patients (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rdv_medecin
    FOREIGN KEY (medecin_id) REFERENCES medecins (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  UNIQUE KEY uq_medecin_creneau (medecin_id, date_heure)
) ENGINE=InnoDB;

-- Prescriptions
CREATE TABLE IF NOT EXISTS prescriptions (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  patient_id INT UNSIGNED NOT NULL,
  medecin_id INT UNSIGNED NOT NULL,
  date_prescription DATE NOT NULL,
  medicament VARCHAR(255) NOT NULL,
  posologie VARCHAR(500) NOT NULL,
  duree_jours INT UNSIGNED NOT NULL,
  CONSTRAINT fk_presc_patient
    FOREIGN KEY (patient_id) REFERENCES patients (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_presc_medecin
    FOREIGN KEY (medecin_id) REFERENCES medecins (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT chk_duree CHECK (duree_jours > 0)
) ENGINE=InnoDB;

-- Comptes application (mot de passe = hash PBKDF2, jamais en clair)
CREATE TABLE IF NOT EXISTS utilisateurs (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  login VARCHAR(64) NOT NULL,
  pass_salt_hex CHAR(32) NOT NULL COMMENT '16 octets en hexadécimal',
  pass_hash_hex CHAR(64) NOT NULL COMMENT '32 octets PBKDF2-SHA256 en hex',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_utilisateurs_login (login)
) ENGINE=InnoDB;

-- Données de test
INSERT INTO medecins (nom, prenom, specialite, email, telephone) VALUES
  ('Benali', 'Leila', 'Cardiologie', 'l.benali@clinique.local', '0612340001'),
  ('Alaoui', 'Omar', 'Pédiatrie', 'o.alaoui@clinique.local', '0612340002'),
  ('Idrissi', 'Sanae', 'Médecine générale', 's.idrissi@clinique.local', '0612340003');

INSERT INTO patients (nom, prenom, date_naissance, telephone, email, numero_dossier) VALUES
  ('Ghazi', 'Karim', '1998-05-12', '0622000001', 'karim.ghazi@email.test', 'DOS-2024-001'),
  ('Tazi', 'Amal', '2001-11-03', '0622000002', 'amal.tazi@email.test', 'DOS-2024-002'),
  ('Fassi', 'Youssef', '1975-08-20', '0622000003', NULL, 'DOS-2024-003');

INSERT INTO rendez_vous (patient_id, medecin_id, date_heure, motif, statut) VALUES
  (1, 1, '2026-04-15 09:00:00', 'Contrôle tension', 'planifie'),
  (2, 2, '2026-04-15 10:30:00', 'Vaccination', 'planifie'),
  (3, 3, '2026-04-16 14:00:00', 'Consultation générale', 'termine');

INSERT INTO prescriptions (patient_id, medecin_id, date_prescription, medicament, posologie, duree_jours) VALUES
  (1, 1, '2026-04-10', 'Bisoprolol 2,5 mg', '1 comprimé le matin', 30),
  (3, 3, '2026-04-16', 'Paracétamol 500 mg', '1 à 2 cp toutes les 6 h si douleur', 7);

-- Compte démo : login `admin`, mot de passe `admin123` (à changer en production)
-- Généré avec PBKDF2-HMAC-SHA256, 150000 itérations (voir auth/passwords.py)
INSERT INTO utilisateurs (login, pass_salt_hex, pass_hash_hex) VALUES
  (
    'admin',
    'a1b2c3d4e5f60718293a4b5c6d7e8f09',
    '9c7614a27265336dbaf777e618f7ccd8a0bb71c0c966bbdbbfa8bd63d5e7c2ed'
  );
