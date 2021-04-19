-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 19, 2021 at 05:01 AM
-- Server version: 5.7.33
-- PHP Version: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cms`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_school`
--

CREATE TABLE `auth_school` (
  `id` varchar(32) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `auth_school`
--

INSERT INTO `auth_school` (`id`, `name`) VALUES
('105610101', '马克思主义学院'),
('105610201', '经济与金融学院'),
('105610301', '法学院'),
('105610403', '体育学院'),
('105610502', '外国语学院'),
('105610503', '新闻与传播学院'),
('105610504', '艺术学院'),
('105610701', '数学学院'),
('105610702', '物理与光电学院'),
('105610710', '生物科学与工程学院'),
('105610802', '自动化科学与工程学院'),
('105610805', '材料科学与工程学院'),
('105610808', '电力学院'),
('105610809', '电子与信息学院'),
('105610812', '计算机科学与工程学院'),
('105610813', '建筑学院'),
('105610814', '土木与交通学院'),
('105610817', '化学与化工学院'),
('105610822', '轻工科学与工程学院'),
('105610830', '环境与能源学院'),
('105610832', '食品科学与工程学院'),
('105611001', '医学院'),
('105611202', '工商管理学院'),
('105611204', '公共管理学院');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_school`
--
ALTER TABLE `auth_school`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
