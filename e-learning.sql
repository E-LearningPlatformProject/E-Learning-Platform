-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema e-learning
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema e-learning
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `e-learning` DEFAULT CHARACTER SET utf8mb4 ;
USE `e-learning` ;

-- -----------------------------------------------------
-- Table `e-learning`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(220) NOT NULL,
  `role` VARCHAR(15) NOT NULL DEFAULT 'student',
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `image` BLOB NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`teachers_additinal_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`teachers_additinal_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `phone_number` INT NOT NULL,
  `linked_in_account` VARCHAR(45) NOT NULL,
  `is_approved` TINYINT NOT NULL DEFAULT 0,
  `teacher_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC) VISIBLE,
  UNIQUE INDEX `linked_in_account_UNIQUE` (`linked_in_account` ASC) VISIBLE,
  INDEX `fk_teachers_additinal_info_users1_idx` (`teacher_id` ASC) VISIBLE,
  CONSTRAINT `fk_teachers_additinal_info_users1`
    FOREIGN KEY (`teacher_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(60) NOT NULL,
  `description` TEXT NOT NULL,
  `level` VARCHAR(20) NOT NULL,
  `image` BLOB NULL DEFAULT NULL,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_courses_users1_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_users1`
    FOREIGN KEY (`author_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`enrollments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`enrollments` (
  `course_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`course_id`, `user_id`),
  INDEX `fk_courses_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_courses_has_users_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_users_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`ratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`ratings` (
  `course_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `rating` TINYINT NOT NULL,
  PRIMARY KEY (`course_id`, `user_id`),
  INDEX `fk_courses_has_users_users2_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_courses_has_users_courses2_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_users_courses2`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_users_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`sections` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(60) NOT NULL,
  `content` TEXT NOT NULL,
  `course_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sections_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_sections_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`users_view`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users_view` (
  `user_id` INT NOT NULL,
  `section_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `section_id`),
  INDEX `fk_users_has_sections_sections1_idx` (`section_id` ASC) VISIBLE,
  INDEX `fk_users_has_sections_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_sections_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_sections_sections1`
    FOREIGN KEY (`section_id`)
    REFERENCES `e-learning`.`sections` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`objectives`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`objectives` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `course_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_objectives_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_objectives_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`tags` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-learning`.`courses_has_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses_has_tags` (
  `course_id` INT NOT NULL,
  `tag_id` INT NOT NULL,
  PRIMARY KEY (`course_id`, `tag_id`),
  INDEX `fk_courses_has_tags_tags1_idx` (`tag_id` ASC) VISIBLE,
  INDEX `fk_courses_has_tags_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_tags_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_tags_tags1`
    FOREIGN KEY (`tag_id`)
    REFERENCES `e-learning`.`tags` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
