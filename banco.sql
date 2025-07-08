-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: monitor_vazamentos
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `level` varchar(20) NOT NULL,
  `message` varchar(500) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_log_timestamp` (`timestamp`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (1,'2025-07-07 16:10:55','INFO','Aplicação iniciada e logger configurado.',NULL),(2,'2025-07-07 16:10:56','INFO','Aplicação iniciada e logger configurado.',NULL),(3,'2025-07-07 16:11:07','INFO','Consulta iniciada para o e-mail: \'alainx42@gmail.com\'',7),(4,'2025-07-07 16:11:08','WARNING','Resultado para \'alainx42@gmail.com\': VAZAMENTO ENCONTRADO.',7),(5,'2025-07-07 16:11:18','INFO','Consulta iniciada para o e-mail: \'alainxavier11@gmail.com\'',7),(6,'2025-07-07 16:11:19','INFO','Resultado para \'alainxavier11@gmail.com\': Nenhum vazamento conhecido encontrado.',7),(7,'2025-07-07 16:14:21','INFO','Novo usuário cadastrado: \'alaintest@gmail.com\'',NULL),(8,'2025-07-07 16:14:30','INFO','Usuário \'alaintest@gmail.com\' logado com sucesso.',8);
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitored_email`
--

DROP TABLE IF EXISTS `monitored_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monitored_email` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_monitored_email_email` (`email`),
  CONSTRAINT `monitored_email_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitored_email`
--

LOCK TABLES `monitored_email` WRITE;
/*!40000 ALTER TABLE `monitored_email` DISABLE KEYS */;
INSERT INTO `monitored_email` VALUES (25,'alainx42@gmail.com',6),(36,'alainx42@gmail.com',7),(37,'alainxavier11@gmail.com',7),(38,'alainx42@gmail.com',8);
/*!40000 ALTER TABLE `monitored_email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(256) DEFAULT NULL,
  `role` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'alainx42@gmail.com','pbkdf2:sha256:600000$7tBsoiOy81IZjwY3$1f6003dc0567b689645c9660360bc3ff22bd95637907819f007919ca210b88ea','user'),(3,'alain930@gmail.com','pbkdf2:sha256:600000$PI5EyBz2IePnhw2X$54b1622fa6188a0eddf17327707e6d879202cb1dc67f68a0d5c7eb8ef521ad89','user'),(4,'alain123@hotmail.com','pbkdf2:sha256:600000$bSkRjdcaJZ4thFg4$128904019df383287cc1d6b6be430842816ea82dab40fcdd7868587605e0b28b','user'),(5,'test@gmail.com','pbkdf2:sha256:600000$i0K2wQAQStfbD2GB$c46fa8c521c675107edf8b27edde42dd41f6baaf1e80e8f86a329f9317e60489','user'),(6,'alain123@gmail.com','pbkdf2:sha256:600000$OpBHACA858GHQQHe$2b3c93bf75cc6e3ec673b129a611a4d51a042beb7ccf6698ff3c8090c66baa29','user'),(7,'alainxavier11@gmail.com','pbkdf2:sha256:600000$vRHPVq2QzwxbTavt$a55d082d8253b89a684ce935c6abad47a9f179f276757210120ef1cf9054fc6b','admin'),(8,'alaintest@gmail.com','pbkdf2:sha256:600000$NxkHPYcXOnEthshq$7390ca023a03335d7dab728232c7e3673d472b3427bbb7d5df99237f559c0c81','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-07 23:20:37
