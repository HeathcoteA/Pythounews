-- MySQL Script generated by MySQL Workbench
-- ven. 12 janv. 2018 11:45:01 CET
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


DROP SCHEMA IF EXISTS `pythounews`;

CREATE SCHEMA IF NOT EXISTS `pythounews` DEFAULT CHARACTER SET utf8 ;
USE `pythounews` ;

-- -----------------------------------------------------
-- Table `pythounews`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pythounews`.`user` ;

CREATE TABLE IF NOT EXISTS `pythounews`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `user_nom` TINYTEXT NOT NULL,
  `user_login`VARCHAR(45) NOT NULL,
  `user_bio` MEDIUMTEXT NULL,
  `user_promo`INT(4) NULL,
  `user_spe` TEXT NULL,
  `user_email` TINYTEXT NULL,
  `user_password` VARCHAR(100) NULL,
  `user_publication_id` INT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_login_UNIQUE` (`user_login` ASC),
  CONSTRAINT `fk_publication2_id`
	FOREIGN KEY (`user_publication_id`)
    REFERENCES publication(`publication_id`))
ENGINE = InnoDB;	

-- -----------------------------------------------------
-- Table `pythounews`.`publication`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pythounews`.`publication` ;

CREATE TABLE IF NOT EXISTS `pythounews`.`publication` (
	`publication_id` INT NOT NULL AUTO_INCREMENT,
    `publication_date` TEXT NULL,
    `publication_nom` VARCHAR(80) NOT NULL,
    `publication_lien` MEDIUMTEXT NOT NULL,
    `publication_texte` TEXT NULL,
    `publication_titre_url` TEXT NULL,
    `publication_description_url` TEXT NULL,
    `publi_user_id` INT NOT NULL,
    PRIMARY KEY (`publication_id`),
    CONSTRAINT `fk_publi_user_id`
    FOREIGN KEY (`publi_user_id`)
    REFERENCES `user`(`user_id`))
ENGINE = InnoDB;
  

-- -----------------------------------------------------
-- Table `pythounews`.`fluxrss`
-- -----------------------------------------------------

DROP TABLE IF EXISTS `pythounews`.`fluxrss` ;

CREATE TABLE IF NOT EXISTS `pythounews`.`fluxrss` (
	`fluxrss_id` INT NOT NULL AUTO_INCREMENT,
	`fluxrss_lien` MEDIUMTEXT NOT NULL,
    `fluxrss_titre` MEDIUMTEXT NOT NULL,
    `fluxrss_adresse_site` MEDIUMTEXT NOT NULL,


  PRIMARY KEY (`fluxrss_id`))
    ENGINE = InnoDB;
    
-- -----------------------------------------------------
-- Table `pythounews`.`sujet_fluxrss`
-- -----------------------------------------------------

DROP TABLE IF EXISTS `pythounews`.`sujet_fluxrss` ;

CREATE TABLE IF NOT EXISTS `pythounews`.`sujet_fluxrss` (
	`sujet_fluxrss_id` INT NOT NULL AUTO_INCREMENT,
    `sujet_fluxrss_fluxrss_id` INT NOT NULL,
    `sujet_fluxrss_motscles_id` INT NOT NULL,
    PRIMARY KEY (`sujet_fluxrss_id`),
    CONSTRAINT `fk_fluxrss_id`
		FOREIGN KEY (`sujet_fluxrss_fluxrss_id`)
		REFERENCES fluxrss(`fluxrss_id`),
	 CONSTRAINT `fk_motscles_id`
		FOREIGN KEY (`sujet_fluxrss_motscles_id`)
		REFERENCES motscles(`motscles_id`))
		
    ENGINE = InnoDB;
    
-- -----------------------------------------------------
-- Table `pythounews`.`motscles`
-- -----------------------------------------------------
    
DROP TABLE IF EXISTS `pythounews`.`motscles`;

CREATE TABLE IF NOT EXISTS `pythounews`.`motscles` (
	`motscles_id` INT NOT NULL AUTO_INCREMENT,
    `motscles_nom` VARCHAR(20),
    PRIMARY KEY (`motscles_id`))
    ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `pythounews`.`sujet_publi`
-- -----------------------------------------------------    
DROP TABLE IF EXISTS `pythounews`.`sujet_publi` ;

CREATE TABLE IF NOT EXISTS `pythounews`.`sujet_publi` (
	`sujet_publi_id` INT NOT NULL AUTO_INCREMENT,
    `sujet_publi_publication_id` INT NOT NULL,
    `sujet_publi_motscles_id` INT NOT NULL,
    PRIMARY KEY (`sujet_publi_id`),
    CONSTRAINT `fk_publication_id`
		FOREIGN KEY (`sujet_publi_publication_id`)
        REFERENCES publication(`publication_id`),
	CONSTRAINT `fk_motscles2_id`
		FOREIGN KEY (`sujet_publi_motscles_id`)
        REFERENCES motscles(`motscles_id`))
ENGINE = InnoDB;






	
