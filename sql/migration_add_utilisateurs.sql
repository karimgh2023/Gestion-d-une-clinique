-- À exécuter si votre base existait AVANT l'ajout de l'authentification
-- (phpMyAdmin : importer ce fichier sur la base clinique_db).

USE clinique_db;

CREATE TABLE IF NOT EXISTS utilisateurs (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  login VARCHAR(64) NOT NULL,
  pass_salt_hex CHAR(32) NOT NULL COMMENT '16 octets en hexadécimal',
  pass_hash_hex CHAR(64) NOT NULL COMMENT '32 octets PBKDF2-SHA256 en hex',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_utilisateurs_login (login)
) ENGINE=InnoDB;

INSERT IGNORE INTO utilisateurs (login, pass_salt_hex, pass_hash_hex) VALUES
  (
    'admin',
    'a1b2c3d4e5f60718293a4b5c6d7e8f09',
    '9c7614a27265336dbaf777e618f7ccd8a0bb71c0c966bbdbbfa8bd63d5e7c2ed'
  );
