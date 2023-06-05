/*
 Navicat Premium Data Transfer

 Source Server         : mysql8.0
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost
 Source Database       : lanyueliang

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : utf-8

 Date: 07/18/2021 10:07:33 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `mall_unit_order`
-- ----------------------------
DROP TABLE IF EXISTS `mall_unit_order`;
CREATE TABLE `mall_unit_order` (
  `order_id` varchar(255) NOT NULL,
  `order_source` varchar(128) DEFAULT NULL,
  `buyer_nick` varchar(128) DEFAULT NULL,
  `buyer_mobile` varchar(128) DEFAULT NULL,
  `province` varchar(128) DEFAULT NULL,
  `city` varchar(128) DEFAULT NULL,
  `pay_time` datetime DEFAULT NULL,
  `order_payment` decimal(12,2) DEFAULT NULL,
  `buy_num` int DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Records of `mall_unit_order`
-- ----------------------------
BEGIN;
INSERT INTO `mall_unit_order` VALUES ('1', '天猫', '1', '15071392053', '湖北', '武汉', '2020-07-07 15:31:53', '199.00', '3'), ('2', '淘宝', '1', '15071392053', '湖北', '武汉', '2020-07-09 15:34:45', '165.00', '5'), ('3', '天猫', '1', '15071392053', '湖北', '武汉', '2020-07-15 16:03:02', '168.00', '2'), ('4', '淘宝', '1', '15071392053', '湖北', '武汉', '2020-07-17 16:08:32', '225.00', '4'), ('5', '天猫', '2', '17865319086', '湖北', '黄石', '2020-07-07 16:17:53', '67.00', '1'), ('6', '淘宝', '1', '15071392053', '湖北', '武汉', '2021-07-07 16:34:16', '165.00', '4'), ('7', '天猫', '1', '15071392053', '湖南', '长沙', '2021-07-07 16:48:10', '178.00', '4');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
