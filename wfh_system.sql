-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 12, 2026 at 03:56 AM
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
-- Database: `wfh_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `announcements`
--

CREATE TABLE `announcements` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `sender_role` enum('admin','leader') NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `announcements`
--

INSERT INTO `announcements` (`id`, `title`, `message`, `sender_role`, `created_by`, `created_at`) VALUES
(2, 'asga', 'asgszga', 'admin', 'Aung Thura Khant', '2026-03-30 08:04:44'),
(3, 'leader', 'i am leader but girl', 'leader', 'Aung Thura Khant', '2026-03-30 08:05:45'),
(4, 'evening ', 'good evening but hot', 'admin', 'Aung Thura Khant', '2026-03-30 08:16:50'),
(5, 'evening', 'i am boy', 'leader', 'Aung Thura Khant', '2026-03-30 08:18:55'),
(7, 'tmw', 'aaa', 'admin', 'Aung Thura Khant', '2026-04-02 09:01:05'),
(8, 'ffff', 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', 'admin', 'Aung Thura Khant', '2026-04-07 09:04:28'),
(9, 'today4/8/26', 'morning everyone', 'admin', 'Aung Thura Khant', '2026-04-08 02:16:21'),
(10, '4/8/2026', 'Morning Members', 'leader', 'Aye', '2026-04-08 02:17:57'),
(11, '4/8/2026', 'today is hot', 'admin', 'Aung Thura Khant', '2026-04-08 05:05:44'),
(12, 'project wfh', 'aung assign to login part', 'leader', 'Aye', '2026-04-08 05:07:14'),
(13, 'Argent Meeting', 'All Mebers', 'admin', 'Aung Thura Khant', '2026-05-07 02:03:41'),
(14, 'Morning 5/12/2026', 'EveryBody Wake Up', 'admin', '1', '2026-05-12 01:05:03'),
(15, 'a', 'a', 'admin', '1', '2026-05-12 01:13:41'),
(16, 'b', 'b', 'leader', 'Aye', '2026-05-12 01:14:07'),
(17, 'abc', 'abc', 'admin', '1', '2026-05-12 01:27:00'),
(18, 'bca', 'bca', 'leader', 'Aye', '2026-05-12 01:27:32'),
(19, 'ccc', 'ccc', 'admin', '1', '2026-05-12 01:32:29'),
(20, 'vvv', 'vvv', 'leader', 'Aye', '2026-05-12 01:33:25'),
(21, 'sdasd', 'asfdfd', 'admin', 'Aung Thura Khant', '2026-05-12 01:53:35');

-- --------------------------------------------------------

--
-- Table structure for table `announcement_replies`
--

CREATE TABLE `announcement_replies` (
  `id` int(11) NOT NULL,
  `announcement_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `announcement_replies`
--

INSERT INTO `announcement_replies` (`id`, `announcement_id`, `message`, `created_by`, `created_at`) VALUES
(1, 11, 'hiiii', 'Aye', '2026-04-29 04:13:40'),
(2, 4, 'aaaa', 'Aung Thura Khant', '2026-05-07 01:59:45'),
(3, 2, 'aaa', 'Aung Thura Khant', '2026-05-07 01:59:52'),
(4, 12, 'blah blah\nblah blah 2', 'aa', '2026-05-11 07:37:55'),
(5, 12, 'blah blah3', 'aa', '2026-05-11 07:38:17'),
(6, 12, 'sdfipoifopiksdiopaiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiadsfk;kasdl;fjjjjjjjjjjjjjjjjjjjjjjjjjjjj', 'aa', '2026-05-11 07:38:28'),
(7, 12, 'sdfsadfsdfsdf', 'aa', '2026-05-11 07:39:01'),
(8, 12, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'aa', '2026-05-11 07:40:20'),
(9, 12, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'aa', '2026-05-11 07:41:00'),
(10, 12, 'hi', 'HH', '2026-05-11 08:48:31'),
(11, 10, 'sdfgds', 'aa', '2026-05-11 09:07:16');

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `attendance_date` date NOT NULL,
  `check_in` time DEFAULT NULL,
  `check_out` time DEFAULT NULL,
  `location_type` enum('Office','WFH') DEFAULT 'Office',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `work_mode` varchar(20) DEFAULT 'Office'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `user_id`, `attendance_date`, `check_in`, `check_out`, `location_type`, `created_at`, `work_mode`) VALUES
(25, 10, '2026-04-10', '12:00:53', '15:38:59', 'Office', '2026-04-10 05:30:53', 'Office'),
(26, 1, '2026-04-10', '15:38:37', NULL, 'WFH', '2026-04-10 09:08:37', 'Office'),
(28, 12, '2026-04-10', '16:21:10', '16:21:14', 'Office', '2026-04-10 09:51:10', 'Office'),
(30, 13, '2026-04-10', '16:32:27', NULL, 'WFH', '2026-04-10 10:02:27', 'Office'),
(31, 13, '2026-04-11', '22:13:22', NULL, 'Office', '2026-04-11 15:43:22', 'Office'),
(32, 12, '2026-04-11', '23:28:50', NULL, 'Office', '2026-04-11 16:58:50', 'Office'),
(33, 10, '2026-04-12', '08:22:05', NULL, 'Office', '2026-04-12 01:52:05', 'Office'),
(34, 12, '2026-04-12', '10:05:15', NULL, 'Office', '2026-04-12 03:35:15', 'Office'),
(35, 12, '2026-04-13', '12:30:27', NULL, 'Office', '2026-04-13 06:00:27', 'Office'),
(36, 12, '2026-04-14', '20:28:32', '23:10:57', 'WFH', '2026-04-14 13:58:32', 'Office'),
(37, 10, '2026-04-14', '20:29:18', NULL, 'Office', '2026-04-14 13:59:18', 'Office'),
(38, 12, '2026-04-19', '16:59:32', '17:12:44', 'Office', '2026-04-19 10:29:34', 'Office'),
(39, 12, '2026-04-20', '10:30:34', '10:44:50', 'Office', '2026-04-20 04:00:36', 'Office'),
(40, 13, '2026-04-20', '10:56:34', '10:56:45', 'WFH', '2026-04-20 04:26:35', 'Office'),
(41, 18, '2026-04-20', '11:02:40', '11:03:49', 'Office', '2026-04-20 04:32:41', 'Office'),
(42, 12, '2026-04-23', '13:34:34', '13:35:22', 'Office', '2026-04-23 07:04:33', 'Office'),
(43, 18, '2026-04-23', '13:37:13', NULL, 'Office', '2026-04-23 07:07:12', 'Office'),
(44, 13, '2026-04-23', '13:44:50', NULL, 'WFH', '2026-04-23 07:14:50', 'Office'),
(45, 21, '2026-04-23', '14:01:27', NULL, 'Office', '2026-04-23 07:31:26', 'Office'),
(46, 27, '2026-04-23', '14:04:45', '14:06:14', 'Office', '2026-04-23 07:34:44', 'Office'),
(47, 12, '2026-04-24', '08:29:33', '08:30:26', 'Office', '2026-04-24 01:59:32', 'Office'),
(48, 21, '2026-04-24', '08:31:07', '08:31:45', 'Office', '2026-04-24 02:01:06', 'Office'),
(49, 13, '2026-04-24', '13:16:30', NULL, 'Office', '2026-04-24 06:46:30', 'Office'),
(50, 28, '2026-04-24', '13:37:34', NULL, 'Office', '2026-04-24 07:07:34', 'Office'),
(51, 12, '2026-04-27', '10:23:45', '10:24:47', 'WFH', '2026-04-27 03:53:45', 'Office'),
(52, 13, '2026-04-27', '10:40:46', NULL, 'Office', '2026-04-27 04:10:46', 'Office'),
(53, 27, '2026-04-28', '11:33:06', '11:43:34', 'WFH', '2026-04-28 05:03:07', 'Office'),
(54, 13, '2026-04-28', '11:34:40', NULL, 'WFH', '2026-04-28 05:04:40', 'Office'),
(55, 18, '2026-04-28', '11:42:51', NULL, 'WFH', '2026-04-28 05:12:50', 'Office'),
(56, 20, '2026-04-28', '11:44:34', NULL, 'Office', '2026-04-28 05:14:34', 'Office'),
(57, 28, '2026-04-28', '11:46:42', NULL, 'WFH', '2026-04-28 05:16:42', 'Office'),
(58, 18, '2026-05-03', '08:22:46', NULL, 'Office', '2026-05-03 01:52:46', 'Office'),
(59, 12, '2026-05-07', '08:32:43', '08:36:55', 'Office', '2026-05-07 02:02:43', 'Office'),
(60, 21, '2026-05-07', '08:49:07', '11:14:27', 'Office', '2026-05-07 02:19:07', 'Office'),
(61, 18, '2026-05-07', '11:19:23', NULL, 'WFH', '2026-05-07 04:49:23', 'Office'),
(62, 10, '2026-05-07', '11:23:54', '11:27:50', 'Office', '2026-05-07 04:53:54', 'Office'),
(63, 20, '2026-05-07', '11:26:34', NULL, 'Office', '2026-05-07 04:56:34', 'Office'),
(64, 12, '2026-05-11', '13:48:44', NULL, 'Office', '2026-05-11 07:18:44', 'Office'),
(65, 18, '2026-05-11', '13:54:27', NULL, 'WFH', '2026-05-11 07:24:26', 'Office');

-- --------------------------------------------------------

--
-- Table structure for table `daily_reports`
--

CREATE TABLE `daily_reports` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `report_date` date NOT NULL,
  `category` varchar(100) NOT NULL,
  `tasks` text NOT NULL,
  `hours` decimal(4,2) DEFAULT 0.00,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `daily_reports`
--

INSERT INTO `daily_reports` (`id`, `user_id`, `report_date`, `category`, `tasks`, `hours`, `created_at`) VALUES
(6, 12, '2026-03-01', 'python', 'afy', 2.00, '2026-04-02 09:14:38'),
(7, 12, '2026-03-01', 'meeting', 'zhfhz', 6.00, '2026-04-02 09:14:38'),
(18, 13, '2026-04-27', 'apple', 'e', 4.00, '2026-04-27 14:53:40'),
(19, 13, '2026-04-27', 'genexus', 'f', 4.00, '2026-04-27 14:53:40'),
(20, 12, '2026-04-28', 'genexus', 'nnk', 8.00, '2026-04-28 08:04:21'),
(21, 12, '2026-04-29', 'genexus', 'HI', 8.00, '2026-04-28 09:33:00'),
(27, 20, '2026-05-07', 'meeting', 'Project Meeting', 1.00, '2026-05-07 05:10:14'),
(28, 20, '2026-05-07', 'python', 'Python Training', 2.00, '2026-05-07 05:10:14'),
(29, 20, '2026-05-07', 'Java', 'Java WFH Project', 4.00, '2026-05-07 05:10:14'),
(30, 20, '2026-05-07', 'genexus', 'Genexus Training', 1.00, '2026-05-07 05:10:14'),
(31, 20, '2026-05-06', 'genexus', 'Genexus Training', 2.00, '2026-05-07 05:10:55'),
(32, 20, '2026-05-06', 'python', 'Python Training', 2.00, '2026-05-07 05:10:55'),
(33, 18, '2026-05-11', 'meeting', 'Team Meeting', 0.50, '2026-05-11 07:53:23'),
(34, 18, '2026-05-11', 'Java', 'Training', 2.00, '2026-05-11 07:53:23'),
(35, 18, '2026-05-11', 'genexus', 'Training', 2.00, '2026-05-11 07:53:23'),
(36, 18, '2026-05-11', 'python', 'OJT', 3.50, '2026-05-11 07:53:23');

-- --------------------------------------------------------

--
-- Table structure for table `leave_requests`
--

CREATE TABLE `leave_requests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `leave_type` enum('Sick Leave','Casual Leave','Vacation','Medical','Personal','Maternity/Paternity') DEFAULT 'Sick Leave',
  `shift_type` enum('Full Day','Morning','Evening') DEFAULT 'Full Day',
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` text NOT NULL,
  `total_days` decimal(4,1) NOT NULL,
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_requests`
--

INSERT INTO `leave_requests` (`id`, `user_id`, `leave_type`, `shift_type`, `start_date`, `end_date`, `reason`, `total_days`, `status`, `created_at`, `updated_at`) VALUES
(41, 12, 'Vacation', 'Full Day', '2026-05-11', '2026-05-11', 'sdff', 1.0, 'Rejected', '2026-05-11 07:46:00', '2026-05-11 07:47:49'),
(42, 18, 'Personal', 'Full Day', '2026-05-12', '2026-05-12', 'Personal Case', 1.0, 'Rejected', '2026-05-11 07:46:07', '2026-05-11 07:47:45'),
(43, 13, 'Casual Leave', '', '2026-05-11', '2026-05-15', '11 to 15 day leave over wall 5 days leave', 5.0, 'Approved', '2026-05-11 07:46:57', '2026-05-11 07:47:42'),
(44, 18, 'Vacation', 'Full Day', '2026-05-12', '2026-05-12', 'Family Time', 1.0, 'Approved', '2026-05-11 07:47:10', '2026-05-11 07:47:40'),
(45, 13, 'Casual Leave', '', '2026-05-20', '2026-05-20', ',mn,', 0.5, 'Rejected', '2026-05-11 07:50:39', '2026-05-11 07:50:47'),
(46, 13, 'Casual Leave', '', '2026-05-20', '2026-05-20', 'hjhjh', 0.5, 'Rejected', '2026-05-11 07:51:00', '2026-05-11 07:51:04'),
(47, 13, 'Casual Leave', 'Full Day', '2026-05-20', '2026-05-20', 'kkkkk', 1.0, 'Rejected', '2026-05-11 07:51:35', '2026-05-11 08:46:47'),
(48, 13, 'Casual Leave', 'Full Day', '2026-05-27', '2026-05-27', 'xxx', 1.0, 'Approved', '2026-05-11 08:21:57', '2026-05-11 08:28:43'),
(49, 13, 'Casual Leave', '', '2026-06-01', '2026-06-02', 'ddd', 2.0, 'Approved', '2026-05-11 08:44:40', '2026-05-11 08:46:27'),
(50, 13, 'Vacation', 'Full Day', '2026-06-18', '2026-06-18', 'sa', 1.0, 'Pending', '2026-05-11 09:03:52', '2026-05-11 09:03:52'),
(51, 13, 'Casual Leave', '', '2026-05-11', '2026-05-12', 'gg', 2.0, 'Pending', '2026-05-11 09:15:38', '2026-05-11 09:15:38'),
(52, 13, 'Casual Leave', '', '2026-05-11', '2026-05-12', 'ff', 2.0, 'Pending', '2026-05-11 09:16:02', '2026-05-11 09:16:02'),
(53, 13, 'Casual Leave', 'Full Day', '2026-05-11', '2026-05-11', 'uu', 1.0, 'Pending', '2026-05-11 09:17:15', '2026-05-11 09:17:15'),
(54, 13, 'Casual Leave', '', '2026-05-19', '2026-05-19', 'nn', 0.5, 'Pending', '2026-05-11 09:22:13', '2026-05-11 09:22:13'),
(55, 13, 'Casual Leave', '', '2026-05-20', '2026-05-20', 'hh', 0.5, 'Pending', '2026-05-11 09:22:39', '2026-05-11 09:22:39');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `request_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `notif_type` enum('New_Request','Status_Update','System') DEFAULT 'System',
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `request_id`, `message`, `notif_type`, `is_read`, `created_at`) VALUES
(168, 18, NULL, 'New Overtime Request for 2026-05-11.', 'System', 1, '2026-05-11 07:45:51'),
(169, 10, 41, 'aa requested 1.0 days leave.', 'System', 1, '2026-05-11 07:46:00'),
(170, 17, 41, 'aa requested 1.0 days leave.', 'System', 0, '2026-05-11 07:46:00'),
(172, 10, 42, 'member123 requested 1.0 days leave.', 'System', 1, '2026-05-11 07:46:07'),
(173, 17, 42, 'member123 requested 1.0 days leave.', 'System', 0, '2026-05-11 07:46:07'),
(175, 18, NULL, 'New Overtime Request for 2026-05-12.', 'System', 1, '2026-05-11 07:46:10'),
(176, 10, NULL, 'member123 submitted a new overtime request.', 'System', 1, '2026-05-11 07:46:17'),
(177, 17, NULL, 'member123 submitted a new overtime request.', 'System', 0, '2026-05-11 07:46:17'),
(179, 10, NULL, 'member123 submitted a new overtime request.', 'System', 1, '2026-05-11 07:46:20'),
(180, 17, NULL, 'member123 submitted a new overtime request.', 'System', 0, '2026-05-11 07:46:20'),
(182, 10, 43, 'HH requested 5.0 days leave.', 'System', 1, '2026-05-11 07:46:57'),
(183, 17, 43, 'HH requested 5.0 days leave.', 'System', 0, '2026-05-11 07:46:57'),
(185, 12, NULL, 'New Overtime Request for 2026-05-13.', 'System', 1, '2026-05-11 07:46:59'),
(186, 18, NULL, 'New Overtime Request for 2026-05-13.', 'System', 1, '2026-05-11 07:47:08'),
(187, 10, 44, 'member123 requested 1.0 days leave.', 'System', 1, '2026-05-11 07:47:10'),
(188, 17, 44, 'member123 requested 1.0 days leave.', 'System', 0, '2026-05-11 07:47:10'),
(190, 10, NULL, 'aa submitted a new overtime request.', 'System', 1, '2026-05-11 07:47:19'),
(191, 17, NULL, 'aa submitted a new overtime request.', 'System', 0, '2026-05-11 07:47:19'),
(193, 10, NULL, 'member123 submitted a new overtime request.', 'System', 1, '2026-05-11 07:47:24'),
(194, 17, NULL, 'member123 submitted a new overtime request.', 'System', 0, '2026-05-11 07:47:24'),
(196, 18, NULL, 'Leave request Approved by Team Leader.', 'System', 1, '2026-05-11 07:47:40'),
(197, 13, NULL, 'Leave request Approved by Team Leader.', 'System', 1, '2026-05-11 07:47:42'),
(198, 18, NULL, 'Leave request Rejected by Team Leader.', 'System', 1, '2026-05-11 07:47:45'),
(199, 12, NULL, 'Leave request Rejected by Team Leader.', 'System', 1, '2026-05-11 07:47:49'),
(200, 10, 45, 'HH requested 0.5 days leave.', 'System', 1, '2026-05-11 07:50:39'),
(201, 17, 45, 'HH requested 0.5 days leave.', 'System', 0, '2026-05-11 07:50:39'),
(203, 13, NULL, 'Leave request Rejected by Team Leader.', 'System', 1, '2026-05-11 07:50:47'),
(204, 10, 46, 'HH requested 0.5 days leave.', 'System', 1, '2026-05-11 07:51:00'),
(205, 17, 46, 'HH requested 0.5 days leave.', 'System', 0, '2026-05-11 07:51:00'),
(207, 13, NULL, 'Leave request Rejected by Team Leader.', 'System', 1, '2026-05-11 07:51:04'),
(208, 10, 47, 'HH requested 1.0 days leave.', 'System', 1, '2026-05-11 07:51:35'),
(209, 17, 47, 'HH requested 1.0 days leave.', 'System', 0, '2026-05-11 07:51:35'),
(211, 10, 48, 'HH requested 1.0 days leave.', 'System', 1, '2026-05-11 08:21:57'),
(212, 17, 48, 'HH requested 1.0 days leave.', 'System', 0, '2026-05-11 08:21:57'),
(214, 13, NULL, 'Leave request Approved by Team Leader.', 'System', 1, '2026-05-11 08:28:43'),
(215, 10, 49, 'HH requested 2.0 days leave.', 'System', 1, '2026-05-11 08:44:40'),
(216, 17, 49, 'HH requested 2.0 days leave.', 'System', 0, '2026-05-11 08:44:40'),
(218, 13, NULL, 'Leave request Approved by Team Leader.', 'System', 1, '2026-05-11 08:46:27'),
(219, 13, NULL, 'Leave request Rejected by Team Leader.', 'System', 1, '2026-05-11 08:46:47'),
(220, 10, 50, 'HH requested 1.0 days leave.', 'System', 1, '2026-05-11 09:03:52'),
(221, 17, 50, 'HH requested 1.0 days leave.', 'System', 0, '2026-05-11 09:03:52'),
(223, 21, NULL, 'New Overtime Request for 2026-05-11.', 'System', 1, '2026-05-11 09:08:31'),
(224, 10, NULL, 'member20 submitted a new overtime request.', 'System', 1, '2026-05-11 09:09:45'),
(225, 17, NULL, 'member20 submitted a new overtime request.', 'System', 0, '2026-05-11 09:09:45'),
(227, 10, 51, 'HH requested 2.0 days leave.', 'System', 1, '2026-05-11 09:15:38'),
(228, 17, 51, 'HH requested 2.0 days leave.', 'System', 0, '2026-05-11 09:15:38'),
(230, 10, 52, 'HH requested 2.0 days leave.', 'System', 1, '2026-05-11 09:16:02'),
(231, 17, 52, 'HH requested 2.0 days leave.', 'System', 0, '2026-05-11 09:16:02'),
(233, 10, 53, 'HH requested 1.0 days leave.', 'System', 1, '2026-05-11 09:17:15'),
(234, 17, 53, 'HH requested 1.0 days leave.', 'System', 0, '2026-05-11 09:17:15'),
(236, 10, 54, 'HH requested 0.5 days leave.', 'System', 1, '2026-05-11 09:22:13'),
(237, 17, 54, 'HH requested 0.5 days leave.', 'System', 0, '2026-05-11 09:22:13'),
(239, 10, 55, 'HH requested 0.5 days leave.', 'System', 1, '2026-05-11 09:22:39'),
(240, 17, 55, 'HH requested 0.5 days leave.', 'System', 0, '2026-05-11 09:22:39'),
(242, 22, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(243, 10, NULL, 'New Announcement: Morning 5/12/2026', 'System', 1, '2026-05-12 01:05:03'),
(244, 12, NULL, 'New Announcement: Morning 5/12/2026', 'System', 1, '2026-05-12 01:05:03'),
(245, 13, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(246, 16, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(247, 17, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(248, 18, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(249, 20, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(250, 21, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(251, 27, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(252, 28, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(253, 29, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(254, 11, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(255, 14, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(256, 19, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(257, 23, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(258, 24, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(259, 25, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(260, 26, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(261, 31, NULL, 'New Announcement: Morning 5/12/2026', 'System', 0, '2026-05-12 01:05:03'),
(273, 22, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(274, 10, NULL, 'New Announcement: a', 'System', 1, '2026-05-12 01:13:41'),
(275, 12, NULL, 'New Announcement: a', 'System', 1, '2026-05-12 01:13:41'),
(276, 13, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(277, 16, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(278, 17, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(279, 18, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(280, 20, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(281, 21, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(282, 27, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(283, 28, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(284, 29, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(285, 11, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(286, 14, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(287, 19, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(288, 23, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(289, 24, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(290, 25, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(291, 26, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(292, 31, NULL, 'New Announcement: a', 'System', 0, '2026-05-12 01:13:41'),
(304, 12, NULL, 'New Team Announcement: b', 'System', 1, '2026-05-12 01:14:07'),
(305, 13, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(306, 14, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(307, 16, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(308, 18, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(309, 19, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(310, 20, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(311, 21, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(312, 23, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(313, 24, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(314, 25, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(315, 26, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(316, 27, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(317, 28, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(318, 29, NULL, 'New Team Announcement: b', 'System', 0, '2026-05-12 01:14:07'),
(319, 22, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(320, 10, NULL, 'New Announcement: abc', 'System', 1, '2026-05-12 01:27:00'),
(321, 12, NULL, 'New Announcement: abc', 'System', 1, '2026-05-12 01:27:00'),
(322, 13, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(323, 16, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(324, 17, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(325, 18, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(326, 20, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(327, 21, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(328, 27, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(329, 28, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(330, 29, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(331, 11, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(332, 14, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(333, 19, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(334, 23, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(335, 24, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(336, 25, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(337, 26, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(338, 31, NULL, 'New Announcement: abc', 'System', 0, '2026-05-12 01:27:00'),
(350, 12, NULL, 'New Team Announcement: bca', 'System', 1, '2026-05-12 01:27:32'),
(351, 13, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(352, 14, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(353, 16, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(354, 18, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(355, 19, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(356, 20, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(357, 21, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(358, 23, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(359, 24, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(360, 25, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(361, 26, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(362, 27, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(363, 28, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(364, 29, NULL, 'New Team Announcement: bca', 'System', 0, '2026-05-12 01:27:32'),
(365, 22, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(366, 10, NULL, 'New Announcement: ccc', 'System', 1, '2026-05-12 01:32:29'),
(367, 12, NULL, 'New Announcement: ccc', 'System', 1, '2026-05-12 01:32:29'),
(368, 13, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(369, 16, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(370, 17, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(371, 18, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(372, 20, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(373, 21, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(374, 27, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(375, 28, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(376, 29, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(377, 11, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(378, 14, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(379, 19, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(380, 23, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(381, 24, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(382, 25, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(383, 26, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(384, 31, NULL, 'New Announcement: ccc', 'System', 0, '2026-05-12 01:32:29'),
(396, 12, NULL, 'New Team Announcement: vvv', 'System', 1, '2026-05-12 01:33:25'),
(397, 13, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(398, 14, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(399, 16, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(400, 18, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(401, 19, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(402, 20, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(403, 21, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(404, 23, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(405, 24, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(406, 25, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(407, 26, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(408, 27, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(409, 28, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(410, 29, NULL, 'New Team Announcement: vvv', 'System', 0, '2026-05-12 01:33:25'),
(411, 22, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(412, 10, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(413, 12, NULL, 'New Announcement: sdasd', 'System', 1, '2026-05-12 01:53:35'),
(414, 13, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(415, 16, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(416, 17, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(417, 18, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(418, 20, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(419, 21, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(420, 27, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(421, 28, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(422, 29, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(423, 11, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(424, 14, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(425, 19, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(426, 23, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(427, 24, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(428, 25, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(429, 26, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35'),
(430, 31, NULL, 'New Announcement: sdasd', 'System', 0, '2026-05-12 01:53:35');

-- --------------------------------------------------------

--
-- Table structure for table `overtime_requests`
--

CREATE TABLE `overtime_requests` (
  `id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `ot_date` date DEFAULT NULL,
  `hours` decimal(4,2) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('Pending','Accepted','Rejected') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `rejected_reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `overtime_requests`
--

INSERT INTO `overtime_requests` (`id`, `member_id`, `project_id`, `ot_date`, `hours`, `reason`, `status`, `created_at`, `rejected_reason`) VALUES
(82, 18, 7, '2026-05-11', 2.00, '3', 'Accepted', '2026-05-11 07:45:51', NULL),
(83, 18, 7, '2026-05-12', 3.00, 't', 'Accepted', '2026-05-11 07:46:10', NULL),
(84, 12, 7, '2026-05-13', 2.00, 'e', 'Accepted', '2026-05-11 07:46:59', NULL),
(85, 18, 11, '2026-05-13', 2.00, '2', 'Accepted', '2026-05-11 07:47:08', NULL),
(86, 21, 12, '2026-05-11', 2.00, 'www', 'Accepted', '2026-05-11 09:08:31', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `progress_history`
--

CREATE TABLE `progress_history` (
  `id` int(11) NOT NULL,
  `task_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `member_name` varchar(100) DEFAULT NULL,
  `progress` int(11) DEFAULT NULL,
  `update_date` date DEFAULT NULL,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `progress_history`
--

INSERT INTO `progress_history` (`id`, `task_id`, `project_id`, `member_name`, `progress`, `update_date`, `note`) VALUES
(1, 19, 11, 'member123', 10, '2026-04-29', 'hi'),
(2, 18, 11, 'aung', 30, '2026-05-07', 'Still developing'),
(3, 19, 11, 'member123', 30, '2026-05-07', 'hi'),
(5, 16, 10, 'aa', 5, '2026-04-28', 'dfsf'),
(6, 16, 10, 'aa', 10, '2026-04-28', 'gdfg'),
(7, 20, 10, 'aa', 100, '2026-05-11', 'h'),
(9, 21, 12, 'aa', 0, '2026-05-11', ''),
(10, 21, 12, 'aa', 0, '2026-05-12', ''),
(11, 21, 12, 'aa', 0, '2026-05-12', ''),
(12, 21, 12, 'aa', 100, '2026-05-12', '');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `id` int(11) NOT NULL,
  `project_name` varchar(255) NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`id`, `project_name`, `created_by`, `team_id`, `status`, `created_at`) VALUES
(2, 'a', 'Aung Thura Khant', NULL, 'Completed (100%)', '2026-03-31 01:30:53'),
(3, 'abc', 'Aung Thura Khant', NULL, 'In Progress (35%)', '2026-03-31 01:50:12'),
(6, 'ccc', 'Aye', NULL, 'In Progress (11%)', '2026-04-02 07:23:28'),
(7, 'a', 'Aye', 3, 'In Progress (31%)', '2026-04-02 08:02:59'),
(8, 'vvv', 'Aye', 3, 'In Progress (28%)', '2026-04-02 09:06:19'),
(9, 'fff', 'Ko', 4, 'In Progress (0%)', '2026-04-07 08:31:32'),
(10, 'WFH project', 'Aye', 3, 'In Progress (55%)', '2026-04-08 02:33:40'),
(11, 'Genexus', 'Aye', 3, 'In Progress (35%)', '2026-04-08 05:13:16'),
(12, 'TEST', 'Aye', 3, 'Completed (100%)', '2026-05-11 08:37:02');

-- --------------------------------------------------------

--
-- Table structure for table `report_categories`
--

CREATE TABLE `report_categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `report_categories`
--

INSERT INTO `report_categories` (`id`, `name`) VALUES
(4, 'apple'),
(2, 'genexus'),
(7, 'Java'),
(1, 'meeting'),
(3, 'python'),
(6, 'sfasdfasdasdf'),
(5, 'ssssss');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `id` int(11) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `assigned_to` varchar(100) DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `progress` int(11) DEFAULT 0,
  `status` varchar(50) DEFAULT 'Todo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`id`, `project_id`, `task_name`, `assigned_to`, `deadline`, `progress`, `status`) VALUES
(3, 2, 'a', 'Aung Thura Khant', NULL, 100, 'Todo'),
(4, 2, 'aa', 'Aung Thura Khant', NULL, 100, 'Todo'),
(6, 2, 'xx', 'Aung Thura Khant', NULL, 100, 'Todo'),
(7, 2, 'gg', 'abc', NULL, 100, 'Todo'),
(10, 3, 'cc', 'win', NULL, 44, 'Todo'),
(11, 3, 'ddddd', 'win', NULL, 1, 'Todo'),
(12, 3, 'cc', 'abc', NULL, 60, 'Todo'),
(13, 6, 'aa', 'aa', '2026-04-02', 11, 'Todo'),
(14, 7, 'a', 'aa', '2026-04-14', 31, 'Todo'),
(15, 8, 'xxx', 'aa', '2026-04-17', 28, 'Todo'),
(16, 10, 'login', 'aa', '2026-04-30', 15, 'Todo'),
(17, 10, 'logout', 'member123', '2026-04-28', 50, 'Todo'),
(18, 11, 'login', 'aung', '2026-04-10', 30, 'Todo'),
(19, 11, 'logout', 'member123', '2026-04-10', 40, 'Todo'),
(20, 10, 'design', 'aa', '2026-05-01', 100, 'Todo'),
(21, 12, 'dsfsdfsdfsd', 'aa', '2026-05-11', 100, 'Todo');

-- --------------------------------------------------------

--
-- Table structure for table `teams`
--

CREATE TABLE `teams` (
  `team_id` int(11) NOT NULL,
  `team_name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teams`
--

INSERT INTO `teams` (`team_id`, `team_name`, `created_at`) VALUES
(3, 'Team-10', '2026-04-02 08:27:09'),
(4, 'Team-2', '2026-04-02 08:27:15'),
(5, 'Team-3', '2026-04-02 08:28:14'),
(6, 'Team-4', '2026-04-02 08:28:23'),
(8, 'Team-5', '2026-04-08 11:39:06'),
(10, 'Team5', '2026-05-11 14:08:23');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `employee_id` varchar(50) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','leader','member') NOT NULL,
  `batch` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `current_status` enum('Office','WFH') DEFAULT 'Office',
  `team_id` int(11) DEFAULT NULL,
  `status` enum('active','away','offline') DEFAULT 'offline',
  `last_activity` timestamp NULL DEFAULT NULL,
  `in_call` tinyint(1) DEFAULT 0,
  `mouse_keyboard_locked` tinyint(1) DEFAULT 0,
  `checked_in` tinyint(1) DEFAULT 0,
  `work_mode` varchar(20) DEFAULT 'Office',
  `check_in_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `employee_id`, `full_name`, `username`, `password`, `role`, `batch`, `created_at`, `current_status`, `team_id`, `status`, `last_activity`, `in_call`, `mouse_keyboard_locked`, `checked_in`, `work_mode`, `check_in_time`) VALUES
(1, 'ADM-001', 'Aung Thura Khant', 'admin', 'admin', 'admin', NULL, '2026-03-30 07:02:03', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(10, 'L-01', 'Aye', 'leader', 'leader', 'leader', 'N/A', '2026-04-02 06:18:12', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(11, 'L-002', 'Ko', 'leader1', 'leader1', 'leader', 'N/A', '2026-04-02 06:18:45', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(12, 'E1', 'aa', 'member', 'member', 'member', 'Batch 1', '2026-04-02 06:19:34', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(13, 'E2', 'HH', 'member1', 'member1', 'member', 'Batch 1', '2026-04-02 06:20:02', 'WFH', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(14, 'E3', 'FF', 'member2', 'member2', 'member', 'Batch 1', '2026-04-02 06:20:27', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(16, '1', '1', '11', '1', 'member', 'N/A', '2026-04-02 09:20:25', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(17, '100000', 'admin123', 'admin123', 'admin123', 'leader', 'N/A', '2026-04-08 02:20:26', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(18, '22222', 'member123', 'member123', 'member123', 'member', 'Batch 12', '2026-04-08 02:21:00', 'WFH', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(19, '111111', 'memeber22', 'memeber22', 'memeber22', 'member', 'Batch 13', '2026-04-08 02:21:36', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(20, '1234', 'aung', 'aung', 'aung', 'member', 'Batch 13', '2026-04-08 05:09:29', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(21, '111112', 'member20', 'member20', 'Member20', 'member', 'Batch 13', '2026-04-23 07:19:12', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(22, '111113', 'admin1', 'admin1', 'Admin1', 'admin', 'N/A', '2026-04-23 07:19:30', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(23, '111114', 'member21', 'member21', 'Member21', 'member', 'Batch 13', '2026-04-23 07:21:01', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(24, '111115', 'member22', 'member22', 'Member22', 'member', 'Batch 13', '2026-04-23 07:21:41', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(25, '111116', 'member23', 'member23', 'Member23', 'member', 'Batch 13', '2026-04-23 07:22:20', 'Office', 6, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(26, '111117', 'member24', 'member24', 'Member24', 'member', 'Batch 13', '2026-04-23 07:23:00', 'Office', 6, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(27, '111118', 'member25', 'member25', 'Member25', 'member', 'Batch 13', '2026-04-23 07:23:46', 'WFH', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(28, '111119', 'member26', 'member26', 'Member26', 'member', 'Batch 13', '2026-04-23 07:24:16', 'WFH', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(29, '111120', 'member27', 'member27', 'Member17', 'member', 'Batch 13', '2026-04-23 07:24:48', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(31, '111121', 'Winn Thuzar', 'winn', 'Win123', 'leader', 'N/A', '2026-05-11 09:25:53', 'Office', 6, 'offline', NULL, 0, 0, 0, 'Office', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `wfh_schedules`
--

CREATE TABLE `wfh_schedules` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `leader_id` int(11) NOT NULL,
  `schedule_date` date NOT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wfh_schedules`
--

INSERT INTO `wfh_schedules` (`id`, `user_id`, `leader_id`, `schedule_date`, `status`) VALUES
(882, 12, 10, '2026-04-01', 'Office'),
(883, 13, 10, '2026-04-01', 'Office'),
(884, 16, 10, '2026-04-01', 'Office'),
(885, 18, 10, '2026-04-01', 'WFH'),
(886, 20, 10, '2026-04-01', 'WFH'),
(887, 12, 10, '2026-04-02', 'WFH'),
(888, 13, 10, '2026-04-02', 'Office'),
(889, 16, 10, '2026-04-02', 'Office'),
(890, 18, 10, '2026-04-02', 'Office'),
(891, 20, 10, '2026-04-02', 'Office'),
(892, 12, 10, '2026-04-03', 'Office'),
(893, 13, 10, '2026-04-03', 'WFH'),
(894, 16, 10, '2026-04-03', 'Office'),
(895, 18, 10, '2026-04-03', 'Office'),
(896, 20, 10, '2026-04-03', 'Office'),
(897, 12, 10, '2026-04-06', 'Office'),
(898, 13, 10, '2026-04-06', 'Office'),
(899, 16, 10, '2026-04-06', 'Office'),
(900, 18, 10, '2026-04-06', 'Office'),
(901, 20, 10, '2026-04-06', 'WFH'),
(902, 12, 10, '2026-04-07', 'Office'),
(903, 13, 10, '2026-04-07', 'Office'),
(904, 16, 10, '2026-04-07', 'Office'),
(905, 18, 10, '2026-04-07', 'WFH'),
(906, 20, 10, '2026-04-07', 'WFH'),
(907, 12, 10, '2026-04-08', 'Office'),
(908, 13, 10, '2026-04-08', 'Office'),
(909, 16, 10, '2026-04-08', 'Office'),
(910, 18, 10, '2026-04-08', 'Office'),
(911, 20, 10, '2026-04-08', 'Office'),
(912, 12, 10, '2026-04-09', 'Office'),
(913, 13, 10, '2026-04-09', 'WFH'),
(914, 16, 10, '2026-04-09', 'Office'),
(915, 18, 10, '2026-04-09', 'Office'),
(916, 20, 10, '2026-04-09', 'Office'),
(917, 12, 10, '2026-04-10', 'Office'),
(918, 13, 10, '2026-04-10', 'WFH'),
(919, 16, 10, '2026-04-10', 'WFH'),
(920, 18, 10, '2026-04-10', 'WFH'),
(921, 20, 10, '2026-04-10', 'Office'),
(922, 12, 10, '2026-04-13', 'Office'),
(923, 13, 10, '2026-04-13', 'WFH'),
(924, 16, 10, '2026-04-13', 'WFH'),
(925, 18, 10, '2026-04-13', 'Office'),
(926, 20, 10, '2026-04-13', 'WFH'),
(927, 12, 10, '2026-04-14', 'WFH'),
(928, 13, 10, '2026-04-14', 'WFH'),
(929, 16, 10, '2026-04-14', 'WFH'),
(930, 18, 10, '2026-04-14', 'WFH'),
(931, 20, 10, '2026-04-14', 'Office'),
(932, 12, 10, '2026-04-15', 'Office'),
(933, 13, 10, '2026-04-15', 'WFH'),
(934, 16, 10, '2026-04-15', 'Office'),
(935, 18, 10, '2026-04-15', 'WFH'),
(936, 20, 10, '2026-04-15', 'Office'),
(937, 12, 10, '2026-04-16', 'Office'),
(938, 13, 10, '2026-04-16', 'WFH'),
(939, 16, 10, '2026-04-16', 'WFH'),
(940, 18, 10, '2026-04-16', 'Office'),
(941, 20, 10, '2026-04-16', 'Office'),
(942, 12, 10, '2026-04-17', 'WFH'),
(943, 13, 10, '2026-04-17', 'WFH'),
(944, 16, 10, '2026-04-17', 'WFH'),
(945, 18, 10, '2026-04-17', 'WFH'),
(946, 20, 10, '2026-04-17', 'WFH'),
(947, 12, 10, '2026-04-20', 'Office'),
(948, 13, 10, '2026-04-20', 'WFH'),
(949, 16, 10, '2026-04-20', 'Office'),
(950, 18, 10, '2026-04-20', 'Office'),
(951, 20, 10, '2026-04-20', 'WFH'),
(952, 12, 10, '2026-04-21', 'WFH'),
(953, 13, 10, '2026-04-21', 'WFH'),
(954, 16, 10, '2026-04-21', 'WFH'),
(955, 18, 10, '2026-04-21', 'WFH'),
(956, 20, 10, '2026-04-21', 'WFH'),
(957, 12, 10, '2026-04-22', 'WFH'),
(958, 13, 10, '2026-04-22', 'Office'),
(959, 16, 10, '2026-04-22', 'Office'),
(960, 18, 10, '2026-04-22', 'Office'),
(961, 20, 10, '2026-04-22', 'Office'),
(962, 12, 10, '2026-04-23', 'Office'),
(963, 13, 10, '2026-04-23', 'WFH'),
(964, 16, 10, '2026-04-23', 'Office'),
(965, 18, 10, '2026-04-23', 'Office'),
(966, 20, 10, '2026-04-23', 'Office'),
(967, 12, 10, '2026-04-24', 'Office'),
(968, 13, 10, '2026-04-24', 'Office'),
(969, 16, 10, '2026-04-24', 'Office'),
(970, 18, 10, '2026-04-24', 'WFH'),
(971, 20, 10, '2026-04-24', 'WFH'),
(972, 12, 10, '2026-04-27', 'WFH'),
(973, 13, 10, '2026-04-27', 'Office'),
(974, 16, 10, '2026-04-27', 'Office'),
(975, 18, 10, '2026-04-27', 'Office'),
(976, 20, 10, '2026-04-27', 'Office'),
(977, 12, 10, '2026-04-28', 'Office'),
(978, 13, 10, '2026-04-28', 'WFH'),
(979, 16, 10, '2026-04-28', 'WFH'),
(980, 18, 10, '2026-04-28', 'WFH'),
(981, 20, 10, '2026-04-28', 'Office'),
(982, 12, 10, '2026-04-29', 'Office'),
(983, 13, 10, '2026-04-29', 'WFH'),
(984, 16, 10, '2026-04-29', 'WFH'),
(985, 18, 10, '2026-04-29', 'WFH'),
(986, 20, 10, '2026-04-29', 'WFH'),
(987, 12, 10, '2026-04-30', 'WFH'),
(988, 13, 10, '2026-04-30', 'WFH'),
(989, 16, 10, '2026-04-30', 'WFH'),
(990, 18, 10, '2026-04-30', 'Office'),
(991, 20, 10, '2026-04-30', 'WFH'),
(992, 21, 10, '2026-04-01', 'WFH'),
(993, 27, 10, '2026-04-01', 'Office'),
(994, 28, 10, '2026-04-01', 'WFH'),
(995, 29, 10, '2026-04-01', 'WFH'),
(996, 21, 10, '2026-04-02', 'Office'),
(997, 27, 10, '2026-04-02', 'WFH'),
(998, 28, 10, '2026-04-02', 'WFH'),
(999, 29, 10, '2026-04-02', 'Office'),
(1000, 21, 10, '2026-04-03', 'Office'),
(1001, 27, 10, '2026-04-03', 'WFH'),
(1002, 28, 10, '2026-04-03', 'Office'),
(1003, 29, 10, '2026-04-03', 'WFH'),
(1004, 21, 10, '2026-04-06', 'WFH'),
(1005, 27, 10, '2026-04-06', 'Office'),
(1006, 28, 10, '2026-04-06', 'Office'),
(1007, 29, 10, '2026-04-06', 'WFH'),
(1008, 21, 10, '2026-04-07', 'WFH'),
(1009, 27, 10, '2026-04-07', 'Office'),
(1010, 28, 10, '2026-04-07', 'WFH'),
(1011, 29, 10, '2026-04-07', 'Office'),
(1012, 21, 10, '2026-04-08', 'Office'),
(1013, 27, 10, '2026-04-08', 'Office'),
(1014, 28, 10, '2026-04-08', 'WFH'),
(1015, 29, 10, '2026-04-08', 'Office'),
(1016, 21, 10, '2026-04-09', 'WFH'),
(1017, 27, 10, '2026-04-09', 'Office'),
(1018, 28, 10, '2026-04-09', 'Office'),
(1019, 29, 10, '2026-04-09', 'Office'),
(1020, 21, 10, '2026-04-10', 'Office'),
(1021, 27, 10, '2026-04-10', 'WFH'),
(1022, 28, 10, '2026-04-10', 'WFH'),
(1023, 29, 10, '2026-04-10', 'WFH'),
(1024, 21, 10, '2026-04-13', 'Office'),
(1025, 27, 10, '2026-04-13', 'WFH'),
(1026, 28, 10, '2026-04-13', 'WFH'),
(1027, 29, 10, '2026-04-13', 'WFH'),
(1028, 21, 10, '2026-04-14', 'WFH'),
(1029, 27, 10, '2026-04-14', 'Office'),
(1030, 28, 10, '2026-04-14', 'WFH'),
(1031, 29, 10, '2026-04-14', 'Office'),
(1032, 21, 10, '2026-04-15', 'WFH'),
(1033, 27, 10, '2026-04-15', 'Office'),
(1034, 28, 10, '2026-04-15', 'Office'),
(1035, 29, 10, '2026-04-15', 'Office'),
(1036, 21, 10, '2026-04-16', 'Office'),
(1037, 27, 10, '2026-04-16', 'WFH'),
(1038, 28, 10, '2026-04-16', 'WFH'),
(1039, 29, 10, '2026-04-16', 'WFH'),
(1040, 21, 10, '2026-04-17', 'Office'),
(1041, 27, 10, '2026-04-17', 'WFH'),
(1042, 28, 10, '2026-04-17', 'Office'),
(1043, 29, 10, '2026-04-17', 'WFH'),
(1044, 21, 10, '2026-04-20', 'WFH'),
(1045, 27, 10, '2026-04-20', 'WFH'),
(1046, 28, 10, '2026-04-20', 'Office'),
(1047, 29, 10, '2026-04-20', 'WFH'),
(1048, 21, 10, '2026-04-21', 'WFH'),
(1049, 27, 10, '2026-04-21', 'Office'),
(1050, 28, 10, '2026-04-21', 'Office'),
(1051, 29, 10, '2026-04-21', 'WFH'),
(1052, 21, 10, '2026-04-22', 'WFH'),
(1053, 27, 10, '2026-04-22', 'Office'),
(1054, 28, 10, '2026-04-22', 'WFH'),
(1055, 29, 10, '2026-04-22', 'Office'),
(1056, 21, 10, '2026-04-23', 'WFH'),
(1057, 27, 10, '2026-04-23', 'WFH'),
(1058, 28, 10, '2026-04-23', 'Office'),
(1059, 29, 10, '2026-04-23', 'WFH'),
(1060, 21, 10, '2026-04-24', 'Office'),
(1061, 27, 10, '2026-04-24', 'Office'),
(1062, 28, 10, '2026-04-24', 'Office'),
(1063, 29, 10, '2026-04-24', 'Office'),
(1064, 21, 10, '2026-04-27', 'Office'),
(1065, 27, 10, '2026-04-27', 'WFH'),
(1066, 28, 10, '2026-04-27', 'Office'),
(1067, 29, 10, '2026-04-27', 'WFH'),
(1068, 21, 10, '2026-04-28', 'Office'),
(1069, 27, 10, '2026-04-28', 'WFH'),
(1070, 28, 10, '2026-04-28', 'WFH'),
(1071, 29, 10, '2026-04-28', 'WFH'),
(1072, 21, 10, '2026-04-29', 'WFH'),
(1073, 27, 10, '2026-04-29', 'Office'),
(1074, 28, 10, '2026-04-29', 'WFH'),
(1075, 29, 10, '2026-04-29', 'Office'),
(1076, 21, 10, '2026-04-30', 'Office'),
(1077, 27, 10, '2026-04-30', 'WFH'),
(1078, 28, 10, '2026-04-30', 'WFH'),
(1079, 29, 10, '2026-04-30', 'WFH'),
(1080, 12, 10, '2026-05-01', 'Office'),
(1081, 13, 10, '2026-05-01', 'Office'),
(1082, 16, 10, '2026-05-01', 'WFH'),
(1083, 18, 10, '2026-05-01', 'Office'),
(1084, 20, 10, '2026-05-01', 'WFH'),
(1085, 21, 10, '2026-05-01', 'WFH'),
(1086, 27, 10, '2026-05-01', 'Office'),
(1087, 28, 10, '2026-05-01', 'Office'),
(1088, 29, 10, '2026-05-01', 'WFH'),
(1089, 12, 10, '2026-05-04', 'WFH'),
(1090, 13, 10, '2026-05-04', 'WFH'),
(1091, 16, 10, '2026-05-04', 'WFH'),
(1092, 18, 10, '2026-05-04', 'WFH'),
(1093, 20, 10, '2026-05-04', 'Office'),
(1094, 21, 10, '2026-05-04', 'Office'),
(1095, 27, 10, '2026-05-04', 'Office'),
(1096, 28, 10, '2026-05-04', 'WFH'),
(1097, 29, 10, '2026-05-04', 'Office'),
(1098, 12, 10, '2026-05-05', 'Office'),
(1099, 13, 10, '2026-05-05', 'WFH'),
(1100, 16, 10, '2026-05-05', 'Office'),
(1101, 18, 10, '2026-05-05', 'Office'),
(1102, 20, 10, '2026-05-05', 'WFH'),
(1103, 21, 10, '2026-05-05', 'Office'),
(1104, 27, 10, '2026-05-05', 'WFH'),
(1105, 28, 10, '2026-05-05', 'WFH'),
(1106, 29, 10, '2026-05-05', 'WFH'),
(1107, 12, 10, '2026-05-06', 'WFH'),
(1108, 13, 10, '2026-05-06', 'Office'),
(1109, 16, 10, '2026-05-06', 'WFH'),
(1110, 18, 10, '2026-05-06', 'WFH'),
(1111, 20, 10, '2026-05-06', 'Office'),
(1112, 21, 10, '2026-05-06', 'Office'),
(1113, 27, 10, '2026-05-06', 'WFH'),
(1114, 28, 10, '2026-05-06', 'Office'),
(1115, 29, 10, '2026-05-06', 'Office'),
(1116, 12, 10, '2026-05-07', 'Office'),
(1117, 13, 10, '2026-05-07', 'Office'),
(1118, 16, 10, '2026-05-07', 'Office'),
(1119, 18, 10, '2026-05-07', 'WFH'),
(1120, 20, 10, '2026-05-07', 'Office'),
(1121, 21, 10, '2026-05-07', 'Office'),
(1122, 27, 10, '2026-05-07', 'WFH'),
(1123, 28, 10, '2026-05-07', 'Office'),
(1124, 29, 10, '2026-05-07', 'WFH'),
(1125, 12, 10, '2026-05-08', 'Office'),
(1126, 13, 10, '2026-05-08', 'WFH'),
(1127, 16, 10, '2026-05-08', 'Office'),
(1128, 18, 10, '2026-05-08', 'Office'),
(1129, 20, 10, '2026-05-08', 'Office'),
(1130, 21, 10, '2026-05-08', 'WFH'),
(1131, 27, 10, '2026-05-08', 'Office'),
(1132, 28, 10, '2026-05-08', 'Office'),
(1133, 29, 10, '2026-05-08', 'WFH'),
(1134, 12, 10, '2026-05-11', 'Office'),
(1135, 13, 10, '2026-05-11', 'Office'),
(1136, 16, 10, '2026-05-11', 'Office'),
(1137, 18, 10, '2026-05-11', 'WFH'),
(1138, 20, 10, '2026-05-11', 'Office'),
(1139, 21, 10, '2026-05-11', 'Office'),
(1140, 27, 10, '2026-05-11', 'WFH'),
(1141, 28, 10, '2026-05-11', 'WFH'),
(1142, 29, 10, '2026-05-11', 'WFH'),
(1143, 12, 10, '2026-05-12', 'Office'),
(1144, 13, 10, '2026-05-12', 'WFH'),
(1145, 16, 10, '2026-05-12', 'Office'),
(1146, 18, 10, '2026-05-12', 'WFH'),
(1147, 20, 10, '2026-05-12', 'Office'),
(1148, 21, 10, '2026-05-12', 'WFH'),
(1149, 27, 10, '2026-05-12', 'WFH'),
(1150, 28, 10, '2026-05-12', 'WFH'),
(1151, 29, 10, '2026-05-12', 'WFH'),
(1152, 12, 10, '2026-05-13', 'Office'),
(1153, 13, 10, '2026-05-13', 'Office'),
(1154, 16, 10, '2026-05-13', 'Office'),
(1155, 18, 10, '2026-05-13', 'Office'),
(1156, 20, 10, '2026-05-13', 'WFH'),
(1157, 21, 10, '2026-05-13', 'WFH'),
(1158, 27, 10, '2026-05-13', 'WFH'),
(1159, 28, 10, '2026-05-13', 'WFH'),
(1160, 29, 10, '2026-05-13', 'Office'),
(1161, 12, 10, '2026-05-14', 'WFH'),
(1162, 13, 10, '2026-05-14', 'Office'),
(1163, 16, 10, '2026-05-14', 'WFH'),
(1164, 18, 10, '2026-05-14', 'WFH'),
(1165, 20, 10, '2026-05-14', 'WFH'),
(1166, 21, 10, '2026-05-14', 'WFH'),
(1167, 27, 10, '2026-05-14', 'Office'),
(1168, 28, 10, '2026-05-14', 'Office'),
(1169, 29, 10, '2026-05-14', 'Office'),
(1170, 12, 10, '2026-05-15', 'WFH'),
(1171, 13, 10, '2026-05-15', 'Office'),
(1172, 16, 10, '2026-05-15', 'WFH'),
(1173, 18, 10, '2026-05-15', 'WFH'),
(1174, 20, 10, '2026-05-15', 'WFH'),
(1175, 21, 10, '2026-05-15', 'Office'),
(1176, 27, 10, '2026-05-15', 'WFH'),
(1177, 28, 10, '2026-05-15', 'WFH'),
(1178, 29, 10, '2026-05-15', 'WFH'),
(1179, 12, 10, '2026-05-18', 'WFH'),
(1180, 13, 10, '2026-05-18', 'Office'),
(1181, 16, 10, '2026-05-18', 'Office'),
(1182, 18, 10, '2026-05-18', 'Office'),
(1183, 20, 10, '2026-05-18', 'WFH'),
(1184, 21, 10, '2026-05-18', 'Office'),
(1185, 27, 10, '2026-05-18', 'WFH'),
(1186, 28, 10, '2026-05-18', 'Office'),
(1187, 29, 10, '2026-05-18', 'Office'),
(1188, 12, 10, '2026-05-19', 'Office'),
(1189, 13, 10, '2026-05-19', 'WFH'),
(1190, 16, 10, '2026-05-19', 'WFH'),
(1191, 18, 10, '2026-05-19', 'WFH'),
(1192, 20, 10, '2026-05-19', 'WFH'),
(1193, 21, 10, '2026-05-19', 'Office'),
(1194, 27, 10, '2026-05-19', 'Office'),
(1195, 28, 10, '2026-05-19', 'Office'),
(1196, 29, 10, '2026-05-19', 'WFH'),
(1197, 12, 10, '2026-05-20', 'Office'),
(1198, 13, 10, '2026-05-20', 'WFH'),
(1199, 16, 10, '2026-05-20', 'WFH'),
(1200, 18, 10, '2026-05-20', 'WFH'),
(1201, 20, 10, '2026-05-20', 'WFH'),
(1202, 21, 10, '2026-05-20', 'WFH'),
(1203, 27, 10, '2026-05-20', 'Office'),
(1204, 28, 10, '2026-05-20', 'Office'),
(1205, 29, 10, '2026-05-20', 'WFH'),
(1206, 12, 10, '2026-05-21', 'WFH'),
(1207, 13, 10, '2026-05-21', 'WFH'),
(1208, 16, 10, '2026-05-21', 'WFH'),
(1209, 18, 10, '2026-05-21', 'WFH'),
(1210, 20, 10, '2026-05-21', 'WFH'),
(1211, 21, 10, '2026-05-21', 'Office'),
(1212, 27, 10, '2026-05-21', 'WFH'),
(1213, 28, 10, '2026-05-21', 'Office'),
(1214, 29, 10, '2026-05-21', 'WFH'),
(1215, 12, 10, '2026-05-22', 'WFH'),
(1216, 13, 10, '2026-05-22', 'WFH'),
(1217, 16, 10, '2026-05-22', 'WFH'),
(1218, 18, 10, '2026-05-22', 'Office'),
(1219, 20, 10, '2026-05-22', 'WFH'),
(1220, 21, 10, '2026-05-22', 'WFH'),
(1221, 27, 10, '2026-05-22', 'Office'),
(1222, 28, 10, '2026-05-22', 'WFH'),
(1223, 29, 10, '2026-05-22', 'WFH'),
(1224, 12, 10, '2026-05-25', 'Office'),
(1225, 13, 10, '2026-05-25', 'Office'),
(1226, 16, 10, '2026-05-25', 'Office'),
(1227, 18, 10, '2026-05-25', 'WFH'),
(1228, 20, 10, '2026-05-25', 'Office'),
(1229, 21, 10, '2026-05-25', 'Office'),
(1230, 27, 10, '2026-05-25', 'Office'),
(1231, 28, 10, '2026-05-25', 'WFH'),
(1232, 29, 10, '2026-05-25', 'WFH'),
(1233, 12, 10, '2026-05-26', 'WFH'),
(1234, 13, 10, '2026-05-26', 'Office'),
(1235, 16, 10, '2026-05-26', 'WFH'),
(1236, 18, 10, '2026-05-26', 'Office'),
(1237, 20, 10, '2026-05-26', 'Office'),
(1238, 21, 10, '2026-05-26', 'WFH'),
(1239, 27, 10, '2026-05-26', 'WFH'),
(1240, 28, 10, '2026-05-26', 'WFH'),
(1241, 29, 10, '2026-05-26', 'Office'),
(1242, 12, 10, '2026-05-27', 'WFH'),
(1243, 13, 10, '2026-05-27', 'WFH'),
(1244, 16, 10, '2026-05-27', 'Office'),
(1245, 18, 10, '2026-05-27', 'WFH'),
(1246, 20, 10, '2026-05-27', 'Office'),
(1247, 21, 10, '2026-05-27', 'Office'),
(1248, 27, 10, '2026-05-27', 'Office'),
(1249, 28, 10, '2026-05-27', 'Office'),
(1250, 29, 10, '2026-05-27', 'WFH'),
(1251, 12, 10, '2026-05-28', 'Office'),
(1252, 13, 10, '2026-05-28', 'WFH'),
(1253, 16, 10, '2026-05-28', 'WFH'),
(1254, 18, 10, '2026-05-28', 'Office'),
(1255, 20, 10, '2026-05-28', 'WFH'),
(1256, 21, 10, '2026-05-28', 'WFH'),
(1257, 27, 10, '2026-05-28', 'WFH'),
(1258, 28, 10, '2026-05-28', 'WFH'),
(1259, 29, 10, '2026-05-28', 'WFH'),
(1260, 12, 10, '2026-05-29', 'Office'),
(1261, 13, 10, '2026-05-29', 'WFH'),
(1262, 16, 10, '2026-05-29', 'Office'),
(1263, 18, 10, '2026-05-29', 'Office'),
(1264, 20, 10, '2026-05-29', 'Office'),
(1265, 21, 10, '2026-05-29', 'Office'),
(1266, 27, 10, '2026-05-29', 'WFH'),
(1267, 28, 10, '2026-05-29', 'Office'),
(1268, 29, 10, '2026-05-29', 'WFH');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `announcements`
--
ALTER TABLE `announcements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `announcement_replies`
--
ALTER TABLE `announcement_replies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `announcement_id` (`announcement_id`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_date` (`user_id`,`attendance_date`);

--
-- Indexes for table `daily_reports`
--
ALTER TABLE `daily_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `leave_requests`
--
ALTER TABLE `leave_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `request_id` (`request_id`);

--
-- Indexes for table `overtime_requests`
--
ALTER TABLE `overtime_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `member_id` (`member_id`);

--
-- Indexes for table `progress_history`
--
ALTER TABLE `progress_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `report_categories`
--
ALTER TABLE `report_categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_id` (`project_id`);

--
-- Indexes for table `teams`
--
ALTER TABLE `teams`
  ADD PRIMARY KEY (`team_id`),
  ADD UNIQUE KEY `team_name` (`team_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `employee_id` (`employee_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `team_id` (`team_id`),
  ADD KEY `idx_user_emp` (`employee_id`),
  ADD KEY `idx_user_team` (`team_id`);

--
-- Indexes for table `wfh_schedules`
--
ALTER TABLE `wfh_schedules`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_schedule` (`user_id`,`schedule_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `announcements`
--
ALTER TABLE `announcements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `announcement_replies`
--
ALTER TABLE `announcement_replies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT for table `daily_reports`
--
ALTER TABLE `daily_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `leave_requests`
--
ALTER TABLE `leave_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=442;

--
-- AUTO_INCREMENT for table `overtime_requests`
--
ALTER TABLE `overtime_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `progress_history`
--
ALTER TABLE `progress_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `report_categories`
--
ALTER TABLE `report_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `teams`
--
ALTER TABLE `teams`
  MODIFY `team_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `wfh_schedules`
--
ALTER TABLE `wfh_schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1269;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `announcement_replies`
--
ALTER TABLE `announcement_replies`
  ADD CONSTRAINT `announcement_replies_ibfk_1` FOREIGN KEY (`announcement_id`) REFERENCES `announcements` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `daily_reports`
--
ALTER TABLE `daily_reports`
  ADD CONSTRAINT `daily_reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `leave_requests`
--
ALTER TABLE `leave_requests`
  ADD CONSTRAINT `leave_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`request_id`) REFERENCES `leave_requests` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `overtime_requests`
--
ALTER TABLE `overtime_requests`
  ADD CONSTRAINT `overtime_requests_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  ADD CONSTRAINT `overtime_requests_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL;

--
-- Constraints for table `wfh_schedules`
--
ALTER TABLE `wfh_schedules`
  ADD CONSTRAINT `wfh_schedules_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
