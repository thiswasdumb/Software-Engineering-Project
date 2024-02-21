-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 14, 2024 at 02:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tradetalkerdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `ArticleID` int(11) NOT NULL,
  `CompanyID` int(11) NOT NULL,
  `Title` text NOT NULL,
  `Content` text NOT NULL,
  `PublicationDate` date NOT NULL,
  `URL` varchar(300) NOT NULL,
  `Source` varchar(100) NOT NULL,
  `Summary` text NOT NULL,
  `PredictionScore` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `articlecomment`
--

CREATE TABLE `articlecomment` (
  `CommentID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `ArticleID` int(11) NOT NULL,
  `Content` text NOT NULL,
  `Time` datetime NOT NULL,
  `ParentCommentID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookmark`
--

CREATE TABLE `bookmark` (
  `BookmarkID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `ArticleID` int(11) NOT NULL,
  `BookmarkDate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `CompanyID` int(11) NOT NULL,
  `CompanyName` varchar(100) NOT NULL,
  `StockSymbol` varchar(10) NOT NULL,
  `StockPrice` float NOT NULL,
  `Industry` varchar(200) NOT NULL,
  `CompanyDescription` text NOT NULL,
  `PredictedStockPrice` float NOT NULL,
  `StockVariance` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faq`
--

CREATE TABLE `faq` (
  `FAQID` int(11) NOT NULL,
  `Question` text NOT NULL,
  `Answer` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `follow`
--

CREATE TABLE `follow` (
  `FollowID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `CompanyID` int(11) NOT NULL,
  `FollowDate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `liketable`
--

CREATE TABLE `liketable` (
  `LikeID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `ArticleID` int(11) NOT NULL,
  `LikeDate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `NotificationID` int(11) NOT NULL,
  `ArticleID` int(11) NOT NULL,
  `Content` text NOT NULL,
  `Time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Preferences` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usernotificationread`
--

CREATE TABLE `usernotificationread` (
  `UserNotificationReadID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `NotificationID` int(11) NOT NULL,
  `IsRead` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userquestion`
--

CREATE TABLE `userquestion` (
  `UserQuestionID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Question` text NOT NULL,
  `Time` datetime NOT NULL,
  `IsAnswered` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`ArticleID`),
  ADD KEY `company_article_fk` (`CompanyID`);

--
-- Indexes for table `articlecomment`
--
ALTER TABLE `articlecomment`
  ADD PRIMARY KEY (`CommentID`),
  ADD KEY `article_articlec_fk` (`ArticleID`),
  ADD KEY `user_articlec_fk` (`UserID`),
  ADD KEY `parent_articlec_fk` (`ParentCommentID`);

--
-- Indexes for table `bookmark`
--
ALTER TABLE `bookmark`
  ADD PRIMARY KEY (`BookmarkID`),
  ADD KEY `user_bookmark_fk` (`UserID`),
  ADD KEY `article_bookmark_fk` (`ArticleID`);

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`CompanyID`),
  ADD UNIQUE KEY `stock_symbol_unique_index` (`StockSymbol`);

--
-- Indexes for table `faq`
--
ALTER TABLE `faq`
  ADD PRIMARY KEY (`FAQID`);

--
-- Indexes for table `follow`
--
ALTER TABLE `follow`
  ADD PRIMARY KEY (`FollowID`),
  ADD KEY `user_follow_fk` (`UserID`),
  ADD KEY `company_follow_fk` (`CompanyID`);

--
-- Indexes for table `liketable`
--
ALTER TABLE `liketable`
  ADD PRIMARY KEY (`LikeID`),
  ADD KEY `user_like_fk` (`UserID`),
  ADD KEY `article_like_fk` (`ArticleID`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`NotificationID`),
  ADD KEY `article_notification_fk` (`ArticleID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `username_unique_index` (`Username`),
  ADD UNIQUE KEY `email_unique_index` (`Email`);

--
-- Indexes for table `usernotificationread`
--
ALTER TABLE `usernotificationread`
  ADD PRIMARY KEY (`UserNotificationReadID`),
  ADD KEY `user_unr_fk` (`UserID`),
  ADD KEY `notification_unr_fk` (`NotificationID`);

--
-- Indexes for table `userquestion`
--
ALTER TABLE `userquestion`
  ADD PRIMARY KEY (`UserQuestionID`),
  ADD KEY `user_userq_fk` (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `article`
--
ALTER TABLE `article`
  MODIFY `ArticleID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `articlecomment`
--
ALTER TABLE `articlecomment`
  MODIFY `CommentID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookmark`
--
ALTER TABLE `bookmark`
  MODIFY `BookmarkID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `CompanyID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `faq`
--
ALTER TABLE `faq`
  MODIFY `FAQID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `follow`
--
ALTER TABLE `follow`
  MODIFY `FollowID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `liketable`
--
ALTER TABLE `liketable`
  MODIFY `LikeID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `NotificationID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usernotificationread`
--
ALTER TABLE `usernotificationread`
  MODIFY `UserNotificationReadID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `userquestion`
--
ALTER TABLE `userquestion`
  MODIFY `UserQuestionID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article`
--
ALTER TABLE `article`
  ADD CONSTRAINT `company_article_fk` FOREIGN KEY (`CompanyID`) REFERENCES `company` (`CompanyID`) ON UPDATE CASCADE;

--
-- Constraints for table `articlecomment`
--
ALTER TABLE `articlecomment`
  ADD CONSTRAINT `article_articlec_fk` FOREIGN KEY (`ArticleID`) REFERENCES `article` (`ArticleID`),
  ADD CONSTRAINT `parent_articlec_fk` FOREIGN KEY (`ParentCommentID`) REFERENCES `articlecomment` (`CommentID`),
  ADD CONSTRAINT `user_articlec_fk` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);

--
-- Constraints for table `bookmark`
--
ALTER TABLE `bookmark`
  ADD CONSTRAINT `article_bookmark_fk` FOREIGN KEY (`ArticleID`) REFERENCES `article` (`ArticleID`),
  ADD CONSTRAINT `user_bookmark_fk` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);

--
-- Constraints for table `follow`
--
ALTER TABLE `follow`
  ADD CONSTRAINT `company_follow_fk` FOREIGN KEY (`CompanyID`) REFERENCES `company` (`CompanyID`),
  ADD CONSTRAINT `user_follow_fk` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);

--
-- Constraints for table `liketable`
--
ALTER TABLE `liketable`
  ADD CONSTRAINT `article_like_fk` FOREIGN KEY (`ArticleID`) REFERENCES `article` (`ArticleID`),
  ADD CONSTRAINT `user_like_fk` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `article_notification_fk` FOREIGN KEY (`ArticleID`) REFERENCES `article` (`ArticleID`);

--
-- Constraints for table `usernotificationread`
--
ALTER TABLE `usernotificationread`
  ADD CONSTRAINT `notification_unr_fk` FOREIGN KEY (`NotificationID`) REFERENCES `notification` (`NotificationID`),
  ADD CONSTRAINT `user_unr_fk` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);

--
-- Constraints for table `userquestion`
--
ALTER TABLE `userquestion`
  ADD CONSTRAINT `user_userq_fk` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
