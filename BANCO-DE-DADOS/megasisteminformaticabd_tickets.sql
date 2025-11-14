-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: megasisteminformaticabd
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `id_ticket` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `nome_usuario` varchar(255) DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `descrição` text,
  `tipo` varchar(100) DEFAULT NULL,
  `data_criação` datetime DEFAULT NULL,
  `data_conclusão` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pendente',
  PRIMARY KEY (`id_ticket`),
  KEY `id_do_cliente` (`id`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (1,2,'USER_TESTE2','preço do milkshake erradp','preço do milkshake de morango esta 2 reais mais caro na matriz e na filial esta 0','informação errada','2025-11-14 15:21:44',NULL,'Concluído'),(2,2,'USER_TESTE2','TESTE-TICKET','primeiro ticket feito pelo AllTasks\n','Outros','2025-11-14 15:59:22',NULL,'Concluído'),(3,2,'USER_TESTE2','TICKET_TESTE_FINAL','ticket final com objetivo de testar o limite de caracteres:\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Sed facilisis neque orci, at volutpat turpis dictum vel. Aliquam pretium, metus at egestas aliquet, tortor odio tincidunt nisl, sit amet lacinia lacus neque non nisl. Phasellus vestibulum viverra felis. Sed id turpis lacinia, maximus turpis a, malesuada sem. Nunc eleifend tristique sem, sed porta velit porta vel. Nullam eget lectus non est imperdiet rhoncus sit amet non sem. Duis aliquet ultrices tempor. Quisque feugiat lacus ante, egestas scelerisque risus facilisis sit amet. Nunc molestie non mi eu dignissim. Aliquam erat volutpat.\n\nPraesent ut augue a nibh mollis semper eget nec orci. Duis id pretium nibh. Vivamus maximus sem a neque pulvinar tempus. Nunc vitae magna ut elit tempus dictum nec at sapien. Sed fermentum condimentum metus a vestibulum. Suspendisse facilisis rhoncus mauris, non suscipit nibh sagittis at. Suspendisse ullamcorper, elit vel ultrices porttitor, magna augue sagittis nunc, ac imperdiet justo lacus at augue. Duis nulla diam, eleifend quis lectus ac, auctor semper mauris. Suspendisse rutrum, elit id fermentum ornare, tellus nunc posuere tellus, ut semper lectus justo quis ante. Vivamus lacinia sed orci nec gravida. Maecenas semper pellentesque leo. Mauris commodo rutrum aliquet. Vivamus congue, libero non rhoncus accumsan, lorem dui volutpat nunc, quis vulputate nisl tortor nec diam. Fusce porttitor accumsan pulvinar. Donec at enim ut sapien tincidunt vehicula. Mauris elementum pulvinar lorem.\n','Outros','2025-11-14 17:25:32',NULL,'Pendente');
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-14 17:37:37
