-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema trip_buddy
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `trip_buddy` ;

-- -----------------------------------------------------
-- Schema trip_buddy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `trip_buddy` DEFAULT CHARACTER SET utf8 ;
USE `trip_buddy` ;

-- -----------------------------------------------------
-- Table `trip_buddy`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_buddy`.`users` ;

CREATE TABLE IF NOT EXISTS `trip_buddy`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password_hash` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trip_buddy`.`trips`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_buddy`.`trips` ;

CREATE TABLE IF NOT EXISTS `trip_buddy`.`trips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(100) NULL,
  `start_date` DATE NULL,
  `end_date` DATE NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `plan` VARCHAR(255) NULL,
  `created_by` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trip_buddy`.`joined_trips`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_buddy`.`joined_trips` ;

CREATE TABLE IF NOT EXISTS `trip_buddy`.`joined_trips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `trips_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_joined_trips_trips_idx` (`trips_id` ASC) VISIBLE,
  INDEX `fk_joined_trips_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_joined_trips_trips`
    FOREIGN KEY (`trips_id`)
    REFERENCES `trip_buddy`.`trips` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_joined_trips_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `trip_buddy`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
