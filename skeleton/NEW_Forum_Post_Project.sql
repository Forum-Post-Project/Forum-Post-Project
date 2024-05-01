-- MySQL Workbench Synchronization
-- Generated: 2024-05-01 12:08
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: Veselin Totev

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;

ALTER TABLE `forum_post_project`.`Votes` 
DROP FOREIGN KEY `fk_User_has_Reply_Reply1`,
DROP FOREIGN KEY `fk_User_has_Reply_User1`;

CREATE TABLE IF NOT EXISTS `forum_post_project`.`categories` (
  `category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `is_locked` TINYINT(4) NULL DEFAULT 0,
  `is_private` TINYINT(4) NULL DEFAULT 0,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `forum_post_project`.`messages` (
  `message_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `sender_id` INT(11) NULL DEFAULT NULL,
  `receiver_id` INT(11) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`message_id`),
  INDEX `sender_id` (`sender_id` ASC) VISIBLE,
  INDEX `receiver_id` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `message_ibfk_1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_post_project`.`users` (`user_id`),
  CONSTRAINT `message_ibfk_2`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `forum_post_project`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `forum_post_project`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `topic_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`reply_id`),
  INDEX `topic_id` (`topic_id` ASC) VISIBLE,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `reply_ibfk_1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_post_project`.`topics` (`topic_id`),
  CONSTRAINT `reply_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_post_project`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `forum_post_project`.`topics` (
  `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `category_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  `best_reply` INT(11) NULL DEFAULT NULL,
  `is_locked` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`topic_id`),
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `topic_ibfk_1`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_post_project`.`categories` (`category_id`),
  CONSTRAINT `topic_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_post_project`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `forum_post_project`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `is_admin` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `forum_post_project`.`users_category_access` (
  `user_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `access_level` ENUM('Read', 'Write') NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `category_id`),
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  CONSTRAINT `user_category_access_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_post_project`.`users` (`user_id`),
  CONSTRAINT `user_category_access_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_post_project`.`categories` (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

ALTER TABLE `forum_post_project`.`Votes` 
DROP COLUMN `replies_reply_id`,
DROP COLUMN `users_user_id`,
ADD COLUMN `users_user_id` INT(11) NOT NULL FIRST,
ADD COLUMN `replies_reply_id` INT(11) NOT NULL AFTER `users_user_id`;
ALTER TABLE `forum_post_project`.`votes` ALTER INDEX `PRIMARY` VISIBLE;
ALTER TABLE `forum_post_project`.`votes` ALTER INDEX `fk_User_has_Reply_Reply1_idx` VISIBLE;
ALTER TABLE `forum_post_project`.`votes` ALTER INDEX `fk_User_has_Reply_User1_idx` VISIBLE;

ALTER TABLE `forum_post_project`.`Votes` 
ADD CONSTRAINT `fk_User_has_Reply_Reply1`
  FOREIGN KEY (`replies_reply_id`)
  REFERENCES `forum_post_project`.`replies` (`reply_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_User_has_Reply_User1`
  FOREIGN KEY (`users_user_id`)
  REFERENCES `forum_post_project`.`users` (`user_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
