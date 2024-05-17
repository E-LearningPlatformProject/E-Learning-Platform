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
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(220) NOT NULL,
  `is_admin` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`teachers_additinal_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`teachers_additinal_info` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `phone_number` INT(11) NOT NULL,
  `linked_in_account` VARCHAR(45) NOT NULL,
  `is_approved` TINYINT(4) NOT NULL DEFAULT 0,
  `users_id` INT(11) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `image` BLOB NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC) VISIBLE,
  UNIQUE INDEX `linked_in_account_UNIQUE` (`linked_in_account` ASC) VISIBLE,
  INDEX `fk_teachers_additinal_info_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_teachers_additinal_info_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(60) NOT NULL,
  `description` TEXT NOT NULL,
  `level` VARCHAR(20) NOT NULL,
  `image` BLOB NULL DEFAULT NULL,
  `author_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_courses_teachers_additinal_info1_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_teachers_additinal_info1`
    FOREIGN KEY (`author_id`)
    REFERENCES `e-learning`.`teachers_additinal_info` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`tags` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`courses_has_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses_has_tags` (
  `course_id` INT(11) NOT NULL,
  `tag_id` INT(11) NOT NULL,
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
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`students` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_id` INT(11) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_students_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_students_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`enrollments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`enrollments` (
  `courses_id` INT(11) NOT NULL,
  `students_id` INT(11) NOT NULL,
  PRIMARY KEY (`courses_id`, `students_id`),
  INDEX `fk_courses_has_students_students2_idx` (`students_id` ASC) VISIBLE,
  INDEX `fk_courses_has_students_courses2_idx` (`courses_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_students_courses2`
    FOREIGN KEY (`courses_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_students_students2`
    FOREIGN KEY (`students_id`)
    REFERENCES `e-learning`.`students` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`sections` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(60) NOT NULL,
  `type_file` VARCHAR(45) NOT NULL,
  `course_id` INT(11) NOT NULL,
  `source` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sections_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_sections_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`progress`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`progress` (
  `students_id` INT(11) NOT NULL,
  `sections_id` INT(11) NOT NULL,
  `status` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`students_id`, `sections_id`),
  INDEX `fk_students_has_sections_sections1_idx` (`sections_id` ASC) VISIBLE,
  INDEX `fk_students_has_sections_students1_idx` (`students_id` ASC) VISIBLE,
  CONSTRAINT `fk_students_has_sections_sections1`
    FOREIGN KEY (`sections_id`)
    REFERENCES `e-learning`.`sections` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_students_has_sections_students1`
    FOREIGN KEY (`students_id`)
    REFERENCES `e-learning`.`students` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`ratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`ratings` (
  `courses_id` INT(11) NOT NULL,
  `students_id` INT(11) NOT NULL,
  `rating` TINYINT(4) NOT NULL,
  PRIMARY KEY (`courses_id`, `students_id`),
  INDEX `fk_courses_has_students_students1_idx` (`students_id` ASC) VISIBLE,
  INDEX `fk_courses_has_students_courses1_idx` (`courses_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_students_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `e-learning`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_students_students1`
    FOREIGN KEY (`students_id`)
    REFERENCES `e-learning`.`students` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
