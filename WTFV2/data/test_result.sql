/*
Navicat MySQL Data Transfer

Source Server         : con133
Source Server Version : 50649
Source Host           : 172.16.9.133:3306
Source Database       : test_result

Target Server Type    : MYSQL
Target Server Version : 50649
File Encoding         : 65001

Date: 2021-01-12 12:12:01
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for woniuboss_test_result
-- ----------------------------
DROP TABLE IF EXISTS `woniuboss_test_result`;
CREATE TABLE `woniuboss_test_result` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `case_version` varchar(20) NOT NULL,
  `case_id` varchar(50) NOT NULL,
  `module_name` varchar(50) NOT NULL,
  `test_type` varchar(20) NOT NULL,
  `api_url` varchar(100) DEFAULT NULL,
  `request_method` varchar(20) DEFAULT NULL,
  `case_desc` varchar(200) DEFAULT NULL,
  `case_params` varchar(200) DEFAULT NULL,
  `expect` varchar(100) DEFAULT NULL,
  `case_time` datetime NOT NULL,
  `error_msg` varchar(100) DEFAULT NULL,
  `error_img_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for woniusales_test_result
-- ----------------------------
DROP TABLE IF EXISTS `woniusales_test_result`;
CREATE TABLE `woniusales_test_result` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `case_version` varchar(20) NOT NULL,
  `case_id` varchar(50) NOT NULL,
  `module_name` varchar(50) NOT NULL,
  `test_type` varchar(20) NOT NULL,
  `api_url` varchar(100) DEFAULT NULL,
  `request_method` varchar(20) DEFAULT NULL,
  `case_desc` varchar(200) DEFAULT NULL,
  `case_params` varchar(200) DEFAULT NULL,
  `expect` varchar(100) DEFAULT NULL,
  `case_time` datetime NOT NULL,
  `error_msg` varchar(100) DEFAULT NULL,
  `error_img_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
