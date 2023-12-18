-- MySQL dump 10.13  Distrib 8.0.34, for macos13 (x86_64)
--
-- Host: 127.0.0.1    Database: Food_Delievery
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `Cart_item`
--

DROP TABLE IF EXISTS `Cart_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cart_item` (
  `cart_item_id` int NOT NULL AUTO_INCREMENT,
  `member_id` varchar(45) COLLATE utf8_bin NOT NULL,
  `food_id` int NOT NULL,
  `food_name` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `food_price` int DEFAULT NULL,
  `food_quantity` int NOT NULL,
  `food_remark` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `cart_item_price` int NOT NULL,
  `restaurant_name` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`cart_item_id`),
  UNIQUE KEY `cart_item_id_UNIQUE` (`cart_item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cart_item`
--

LOCK TABLES `Cart_item` WRITE;
/*!40000 ALTER TABLE `Cart_item` DISABLE KEYS */;
INSERT INTO `Cart_item` VALUES (16,'jimmy',1,'小籠湯包',100,3,'',300,'鼎泰豐');
/*!40000 ALTER TABLE `Cart_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Food`
--

DROP TABLE IF EXISTS `Food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Food` (
  `food_id` int NOT NULL AUTO_INCREMENT,
  `restaurant_id` int NOT NULL,
  `food_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `food_price` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`food_id`),
  UNIQUE KEY `food_id_UNIQUE` (`food_id`),
  KEY `restaurant_id_idx` (`restaurant_id`),
  CONSTRAINT `restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Food`
--

LOCK TABLES `Food` WRITE;
/*!40000 ALTER TABLE `Food` DISABLE KEYS */;
INSERT INTO `Food` VALUES (1,1,'小籠湯包','100'),(2,1,'絲瓜湯包','120'),(3,2,'薯條','50'),(4,2,'大麥克','100'),(5,1,'肉包','50'),(6,1,'高麗菜包','30'),(7,2,'可樂','39'),(8,2,'檸檬紅茶','49');
/*!40000 ALTER TABLE `Food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order`
--

DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order` (
  `order_id` int unsigned NOT NULL AUTO_INCREMENT,
  `member_id` varchar(45) COLLATE utf8_bin NOT NULL,
  `total_price` varchar(45) COLLATE utf8_bin NOT NULL,
  `payment_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `order_status` varchar(45) COLLATE utf8_bin NOT NULL,
  `book_time` datetime NOT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order`
--

LOCK TABLES `Order` WRITE;
/*!40000 ALTER TABLE `Order` DISABLE KEYS */;
INSERT INTO `Order` VALUES (1,'jimmy','548','信用卡','submit','2023-12-18 23:17:28'),(2,'jimmy','200','LinePay','cancelled','2023-12-18 23:19:14'),(3,'jimmy','906','信用卡','cancelled','2023-12-18 23:29:32');
/*!40000 ALTER TABLE `Order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order_item`
--

DROP TABLE IF EXISTS `Order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order_item` (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `food_id` int NOT NULL,
  `food_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `food_price` int NOT NULL,
  `food_quantity` int NOT NULL,
  `food_remark` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `restaurant_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `order_item_price` int NOT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `food_id_idx` (`food_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order_item`
--

LOCK TABLES `Order_item` WRITE;
/*!40000 ALTER TABLE `Order_item` DISABLE KEYS */;
INSERT INTO `Order_item` VALUES (1,1,1,'小籠湯包',100,3,'','鼎泰豐',300),(2,1,5,'肉包',50,3,'肉','鼎泰豐',150),(3,1,8,'檸檬紅茶',49,2,'','麥當勞',98),(4,2,4,'大麥克',100,2,'酸黃瓜','麥當勞',200),(5,3,3,'薯條',50,4,'加大','麥當勞',200),(6,3,4,'大麥克',100,2,'加大','麥當勞',200),(7,3,7,'可樂',39,2,'加大','麥當勞',78),(8,3,8,'檸檬紅茶',49,2,'加大','麥當勞',98),(9,3,1,'小籠湯包',100,3,'','鼎泰豐',300),(10,3,6,'高麗菜包',30,1,'','鼎泰豐',30);
/*!40000 ALTER TABLE `Order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Payment`
--

DROP TABLE IF EXISTS `Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `payment_name` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE KEY `payment_method_name_UNIQUE` (`payment_name`),
  UNIQUE KEY `payment_method_id_UNIQUE` (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Payment`
--

LOCK TABLES `Payment` WRITE;
/*!40000 ALTER TABLE `Payment` DISABLE KEYS */;
INSERT INTO `Payment` VALUES (3,'LinePay'),(2,'信用卡'),(1,'現金');
/*!40000 ALTER TABLE `Payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Restaurant`
--

DROP TABLE IF EXISTS `Restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Restaurant` (
  `restaurant_id` int NOT NULL AUTO_INCREMENT,
  `restaurant_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `restaurant_address` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`restaurant_id`),
  UNIQUE KEY `restaurant_id_UNIQUE` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Restaurant`
--

LOCK TABLES `Restaurant` WRITE;
/*!40000 ALTER TABLE `Restaurant` DISABLE KEYS */;
INSERT INTO `Restaurant` VALUES (1,'鼎泰豐','台北市文山區曉明街20號'),(2,'麥當勞','新北市板橋區新興街10號');
/*!40000 ALTER TABLE `Restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `member_id` varchar(45) COLLATE utf8_bin NOT NULL,
  `member_password` varchar(500) COLLATE utf8_bin NOT NULL,
  `member_email` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('jimmy','$2b$10$ncc.ap.ncc/app4cc3/pp.sW8dJAyqm2sKcDV3qzlQ3eE997HR6DO','jimmyfu87@gmail.com');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-18 23:31:08
