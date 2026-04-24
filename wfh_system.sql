-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 24, 2026 at 03:40 AM
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
(12, 'project wfh', 'aung assign to login part', 'leader', 'Aye', '2026-04-08 05:07:14');

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
(46, 27, '2026-04-23', '14:04:45', '14:06:14', 'Office', '2026-04-23 07:34:44', 'Office');

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
(8, 12, '2026-04-08', 'ssssss', 'esf', 2.00, '2026-04-08 02:32:11'),
(9, 12, '2026-04-08', 'meeting', 'afe', 1.00, '2026-04-08 02:32:11'),
(10, 12, '2026-04-08', 'python', 'af', 3.00, '2026-04-08 02:32:11'),
(11, 12, '2026-04-08', 'genexus', 'fea', 1.50, '2026-04-08 02:32:11'),
(12, 12, '2026-04-08', 'apple', 'affaf', 0.50, '2026-04-08 02:32:11'),
(13, 12, '2026-04-08', 'Java', 'login', 2.00, '2026-04-08 05:12:10'),
(14, 12, '2026-04-08', 'meeting', 'ff', 4.00, '2026-04-08 05:12:10'),
(15, 12, '2026-04-08', 'python', 'ff', 2.00, '2026-04-08 05:12:10');

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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_requests`
--

INSERT INTO `leave_requests` (`id`, `user_id`, `leave_type`, `shift_type`, `start_date`, `end_date`, `reason`, `total_days`, `status`, `created_at`) VALUES
(1, 12, 'Casual Leave', '', '2026-04-23', '2026-04-23', 'fff', 1.0, 'Approved', '2026-04-23 09:33:32');

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
(1, 10, 1, 'aa requested 1.0 days leave.', 'System', 1, '2026-04-23 09:33:32'),
(2, 17, 1, 'aa requested 1.0 days leave.', 'System', 0, '2026-04-23 09:33:32'),
(4, 12, NULL, 'Your leave request has been Approved.', 'System', 0, '2026-04-23 09:34:02');

-- --------------------------------------------------------

--
-- Table structure for table `overtime`
--

CREATE TABLE `overtime` (
  `id` int(11) NOT NULL,
  `member_name` varchar(255) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `ot_date` date DEFAULT NULL,
  `hours` decimal(4,2) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('Pending','Accepted','Rejected','Approved') DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `overtime`
--

INSERT INTO `overtime` (`id`, `member_name`, `project_id`, `ot_date`, `hours`, `reason`, `status`, `created_at`) VALUES
(1, 'Aung Thura Khant', 3, '2026-04-07', 2.00, 'gg', 'Pending', '2026-04-07 01:25:44'),
(2, 'Aung Thura Khant', 7, '2026-04-07', 2.00, '3r', 'Pending', '2026-04-07 04:44:57'),
(3, 'aa', 7, '2026-04-07', 3.00, '33', 'Accepted', '2026-04-07 04:47:29'),
(4, 'aa', 7, '2026-04-07', 4.00, '44', 'Accepted', '2026-04-07 04:48:12'),
(5, 'aa', 7, '2026-04-07', 44.00, '444\n[Rejected Reason: ff]', 'Rejected', '2026-04-07 04:48:16'),
(6, 'HH', 7, '2026-04-07', 3.00, '233\n[Rejected Reason: i cant]', 'Rejected', '2026-04-07 07:43:59'),
(7, 'FF', NULL, '2026-04-07', 44.00, 'gg', 'Pending', '2026-04-07 08:03:24'),
(8, 'aa', 7, '2026-04-07', 3.00, 'fg', 'Accepted', '2026-04-07 08:36:49'),
(9, 'member123', 10, '2026-04-08', 2.00, 'logout \n[Rejected Reason: illness]', 'Rejected', '2026-04-08 02:38:20'),
(10, 'member123', 10, '2026-04-08', 2.00, 'f', 'Accepted', '2026-04-08 02:39:24'),
(11, 'member123', 11, '2026-04-08', 2.00, 'good\n[Rejected Reason: illness]', 'Rejected', '2026-04-08 05:17:36'),
(12, 'aa', 7, '2026-04-08', 3.00, 'ff', 'Pending', '2026-04-08 08:13:03');

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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `overtime_requests`
--

INSERT INTO `overtime_requests` (`id`, `member_id`, `project_id`, `ot_date`, `hours`, `reason`, `status`, `created_at`) VALUES
(2, 18, 7, '2026-04-23', 2.00, 'login', 'Pending', '2026-04-23 04:26:38');

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
(10, 'WFH project', 'Aye', 3, 'In Progress (75%)', '2026-04-08 02:33:40'),
(11, 'Genexus', 'Aye', 3, 'In Progress (23%)', '2026-04-08 05:13:16');

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
(16, 10, 'login', 'aa', '2026-04-30', 100, 'Todo'),
(17, 10, 'logout', 'member123', '2026-04-28', 50, 'Todo'),
(18, 11, 'login', 'aung', '2026-04-10', 45, 'Todo'),
(19, 11, 'logout', 'member123', '2026-04-10', 1, 'Todo');

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
(3, 'Team-1', '2026-04-02 08:27:09'),
(4, 'Team-2', '2026-04-02 08:27:15'),
(5, 'Team-3', '2026-04-02 08:28:14'),
(6, 'Team-4', '2026-04-02 08:28:23'),
(8, 'Team-5', '2026-04-08 11:39:06');

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
(1, 'ADM-001', 'Aung Thura Khant', 'admin', 'admin', 'admin', NULL, '2026-03-30 07:02:03', 'WFH', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(10, 'L-01', 'Aye', 'leader', 'leader', 'leader', 'N/A', '2026-04-02 06:18:12', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(11, 'L-002', 'Ko', 'leader1', 'leader1', 'leader', 'N/A', '2026-04-02 06:18:45', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(12, 'E1', 'aa', 'member', 'member', 'member', 'Batch 1', '2026-04-02 06:19:34', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(13, 'E2', 'HH', 'member1', 'member1', 'member', 'Batch 1', '2026-04-02 06:20:02', 'WFH', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(14, 'E3', 'FF', 'member2', 'member2', 'member', 'Batch 1', '2026-04-02 06:20:27', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(16, '1', '1', '11', '1', 'member', 'N/A', '2026-04-02 09:20:25', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(17, '100000', 'admin123', 'admin123', 'admin123', 'leader', 'N/A', '2026-04-08 02:20:26', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(18, '22222', 'member123', 'member123', 'member123', 'member', 'Batch 12', '2026-04-08 02:21:00', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(19, '111111', 'memeber22', 'memeber22', 'memeber22', 'member', 'Batch 13', '2026-04-08 02:21:36', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(20, '1234', 'aung', 'aung', 'aung', 'member', 'Batch 13', '2026-04-08 05:09:29', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(21, '111112', 'member20', 'member20', 'Member20', 'member', 'Batch 13', '2026-04-23 07:19:12', 'Office', 3, 'away', NULL, 0, 0, 0, 'Office', NULL),
(22, '111113', 'admin1', 'admin1', 'Admin1', 'admin', 'N/A', '2026-04-23 07:19:30', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(23, '111114', 'member21', 'member21', 'Member21', 'member', 'Batch 13', '2026-04-23 07:21:01', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(24, '111115', 'member22', 'member22', 'Member22', 'member', 'Batch 13', '2026-04-23 07:21:41', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(25, '111116', 'member23', 'member23', 'Member23', 'member', 'Batch 13', '2026-04-23 07:22:20', 'Office', 6, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(26, '111117', 'member24', 'member24', 'Member24', 'member', 'Batch 13', '2026-04-23 07:23:00', 'Office', 6, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(27, '111118', 'member25', 'member25', 'Member25', 'member', 'Batch 13', '2026-04-23 07:23:46', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(28, '111119', 'member26', 'member26', 'Member26', 'member', 'Batch 13', '2026-04-23 07:24:16', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(29, '111120', 'member27', 'member27', 'Member17', 'member', 'Batch 13', '2026-04-23 07:24:48', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL);

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
(1079, 29, 10, '2026-04-30', 'WFH');

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
-- Indexes for table `overtime`
--
ALTER TABLE `overtime`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_id` (`project_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `announcement_replies`
--
ALTER TABLE `announcement_replies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `daily_reports`
--
ALTER TABLE `daily_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `leave_requests`
--
ALTER TABLE `leave_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `overtime`
--
ALTER TABLE `overtime`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `overtime_requests`
--
ALTER TABLE `overtime_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `progress_history`
--
ALTER TABLE `progress_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `report_categories`
--
ALTER TABLE `report_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `teams`
--
ALTER TABLE `teams`
  MODIFY `team_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `wfh_schedules`
--
ALTER TABLE `wfh_schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1080;

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
-- Constraints for table `overtime`
--
ALTER TABLE `overtime`
  ADD CONSTRAINT `overtime_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

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
