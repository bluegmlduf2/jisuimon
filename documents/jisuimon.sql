CREATE DATABASE  IF NOT EXISTS `jisuimon` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `jisuimon`;
-- MySQL dump 10.13  Distrib 8.0.24, for macos11 (x86_64)
--
-- Host: 127.0.0.1    Database: jisuimon
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment_reply_table`
--

DROP TABLE IF EXISTS `comment_reply_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_reply_table` (
  `comment_reply_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '대댓글id',
  `comment_reply_content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '대댓글내용',
  `comment_reply_create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '대댓글 작성날짜',
  `comment_reply_update_date` datetime DEFAULT NULL,
  `user_table_user_id` varchar(36) NOT NULL COMMENT '대댓글 작성자 id',
  `comment_table_comment_id` varchar(36) NOT NULL COMMENT '댓글id',
  PRIMARY KEY (`comment_reply_id`,`user_table_user_id`,`comment_table_comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comment_table`
--

DROP TABLE IF EXISTS `comment_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_table` (
  `comment_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '댓글id',
  `comment_content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '댓글내용',
  `comment_create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '댓글등록날짜',
  `comment_update_date` datetime DEFAULT NULL,
  `user_table_user_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '댓글작성자id',
  `post_table_post_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '게시물id',
  PRIMARY KEY (`comment_id`,`user_table_user_id`,`post_table_post_id`),
  KEY `fk_comment_table_post_table1_idx` (`post_table_post_id`),
  KEY `fk_comment_table_user_table1_idx` (`user_table_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `food_table`
--

DROP TABLE IF EXISTS `food_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_table` (
  `food_id` int NOT NULL,
  `food_name` varchar(100) NOT NULL,
  PRIMARY KEY (`food_id`),
  FULLTEXT KEY `idx_foodName_full_text` (`food_name`) /*!50100 WITH PARSER `ngram` */ 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ingredient_table`
--

DROP TABLE IF EXISTS `ingredient_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient_table` (
  `post_table_post_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ingredient_id` int NOT NULL COMMENT 'food_id와 동일값',
  `ingredient_amt` int NOT NULL COMMENT '재료수량',
  `ingredient_unit` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '재료단위',
  PRIMARY KEY (`ingredient_id`,`post_table_post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `post_detail_table`
--

DROP TABLE IF EXISTS `post_detail_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_detail_table` (
  `post_detail_id` varchar(36) NOT NULL COMMENT '게시글상세id',
  `post_table_post_id` varchar(36) NOT NULL COMMENT '게시글id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '게시글내용 (2만자가량)',
  PRIMARY KEY (`post_detail_id`,`post_table_post_id`),
  KEY `fk_post_detail_table_post_table_idx` (`post_table_post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `post_like_table`
--

DROP TABLE IF EXISTS `post_like_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_like_table` (
  `user_table_user_id` varchar(36) NOT NULL COMMENT '유저id',
  `post_table_post_id` varchar(36) NOT NULL COMMENT '게시글id',
  PRIMARY KEY (`user_table_user_id`,`post_table_post_id`),
  KEY `fk_post_like_table_user_table1_idx` (`user_table_user_id`),
  KEY `fk_post_like_table_post_table1_idx` (`post_table_post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `post_table`
--

DROP TABLE IF EXISTS `post_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_table` (
  `post_id` varchar(36) NOT NULL COMMENT '게시물id',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '제목',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '작성날짜',
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '수정날짜',
  `title_image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '제목이미지',
  `user_table_user_id` varchar(36) NOT NULL COMMENT '게시글작성자',
  PRIMARY KEY (`post_id`,`user_table_user_id`),
  KEY `fk_post_table_user_table1_idx` (`user_table_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_table`
--

DROP TABLE IF EXISTS `user_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_table` (
  `user_id` varchar(36) NOT NULL COMMENT '유저id',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-23 18:34:02
