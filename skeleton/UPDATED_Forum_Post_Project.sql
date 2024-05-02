-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema forum_post
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_post
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_post` DEFAULT CHARACTER SET latin1 ;
USE `forum_post` ;

-- -----------------------------------------------------
-- Table `forum_post`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`categories` (
  `category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `is_locked` TINYINT(4) NULL DEFAULT 0,
  `is_private` TINYINT(4) NULL DEFAULT 0,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `forum_post`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `is_admin` TINYINT(4) NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username` (`username`) VISIBLE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `forum_post`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`messages` (
  `message_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `sender_id` INT(11) NULL DEFAULT NULL,
  `receiver_id` INT(11) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`message_id`),
  INDEX `sender_id` (`sender_id`) VISIBLE,
  INDEX `receiver_id` (`receiver_id`) VISIBLE,
  CONSTRAINT `message_ibfk_1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_post`.`users` (`user_id`),
  CONSTRAINT `message_ibfk_2`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `forum_post`.`users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `forum_post`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`topics` (
  `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `category_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  `best_reply` INT(11) NULL DEFAULT NULL,
  `is_locked` TINYINT(4) NULL DEFAULT 0,
  PRIMARY KEY (`topic_id`),
  INDEX `category_id` (`category_id`) VISIBLE,
  INDEX `user_id` (`user_id`) VISIBLE,
  CONSTRAINT `topic_ibfk_1`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_post`.`categories` (`category_id`),
  CONSTRAINT `topic_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_post`.`users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `forum_post`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `topic_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`reply_id`),
  INDEX `topic_id` (`topic_id`) VISIBLE,
  INDEX `user_id` (`user_id`) VISIBLE,
  CONSTRAINT `reply_ibfk_1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_post`.`topics` (`topic_id`),
  CONSTRAINT `reply_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_post`.`users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `forum_post`.`users_category_access`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`users_category_access` (
  `user_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `access_level` ENUM('Read', 'Write') NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `category_id`),
  INDEX `category_id` (`category_id`) VISIBLE,
  CONSTRAINT `user_category_access_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_post`.`users` (`user_id`),
  CONSTRAINT `user_category_access_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_post`.`categories` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `forum_post`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_post`.`votes` (
  `user_user_id` INT(11) NOT NULL,
  `reply_reply_id` INT(11) NOT NULL,
  `vote_type` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`user_user_id`, `reply_reply_id`),
  INDEX `fk_user_has_reply_reply1_idx` (`reply_reply_id`) VISIBLE,
  INDEX `fk_user_has_reply_user1_idx` (`user_user_id`) VISIBLE,
  CONSTRAINT `fk_user_has_reply_reply1`
    FOREIGN KEY (`reply_reply_id`)
    REFERENCES `forum_post`.`replies` (`reply_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_reply_user1`
    FOREIGN KEY (`user_user_id`)
    REFERENCES `forum_post`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
