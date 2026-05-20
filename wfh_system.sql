-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2026 at 05:11 PM
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
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `announcements`
--

INSERT INTO `announcements` (`id`, `title`, `message`, `sender_role`, `created_by`, `created_at`, `user_id`) VALUES
(28, 'Important', 'Hello', 'leader', 'Kyaw Hla', '2026-05-18 06:19:52', NULL),
(29, 'Morning ', 'Good Evening Guys', 'admin', 'Arthur Pendragon', '2026-05-20 10:35:17', 35),
(30, 'Evening', 'Good To See You', 'admin', 'Arthur Pendragon', '2026-05-20 12:56:58', 35);

-- --------------------------------------------------------

--
-- Table structure for table `announcement_replies`
--

CREATE TABLE `announcement_replies` (
  `id` int(11) NOT NULL,
  `announcement_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `announcement_replies`
--

INSERT INTO `announcement_replies` (`id`, `announcement_id`, `message`, `created_by`, `created_at`, `user_id`) VALUES
(18, 29, 'hello', 'Arthur Pendragon', '2026-05-20 10:35:26', 35),
(19, 29, 'your name is what', 'Arthur Pendragon', '2026-05-20 10:35:34', 35);

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
(98, 25, '2026-05-20', '15:42:14', NULL, 'Office', '2026-05-20 09:12:14', 'Office'),
(99, 38, '2026-05-20', '15:48:18', NULL, 'Office', '2026-05-20 09:18:18', 'Office'),
(100, 26, '2026-05-20', '19:13:15', '19:13:26', 'Office', '2026-05-20 12:43:15', 'Office'),
(101, 41, '2026-05-20', '19:14:29', NULL, 'Office', '2026-05-20 12:44:29', 'Office');

-- --------------------------------------------------------

--
-- Table structure for table `daily_reports`
--

CREATE TABLE `daily_reports` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `report_date` date NOT NULL,
  `today_work` text DEFAULT NULL,
  `tomorrow_work` text DEFAULT NULL,
  `problems_issues` text DEFAULT NULL,
  `shared_matters` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `daily_reports`
--

INSERT INTO `daily_reports` (`id`, `user_id`, `report_date`, `today_work`, `tomorrow_work`, `problems_issues`, `shared_matters`, `created_at`) VALUES
(0, 25, '2026-05-19', 'fff', 'ff', 'fff', 'ff', '2026-05-19 04:19:37'),
(0, 25, '2026-05-20', 'hi', 'hi', 'hi', '', '2026-05-20 07:35:06'),
(0, 27, '2026-05-20', 'gg', 'gg', 'gg', 'gg', '2026-05-20 07:43:59'),
(0, 38, '2026-05-20', 'ff', 'f', 'f', 'f', '2026-05-20 07:46:38');

-- --------------------------------------------------------

--
-- Table structure for table `leave_requests`
--

CREATE TABLE `leave_requests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `leave_type` enum('Sick Leave','Casual Leave','Vacation','Medical','Personal','Maternity/Paternity') DEFAULT 'Sick Leave',
  `start_shift` enum('Full Day','Morning','Evening') DEFAULT 'Full Day',
  `end_shift` enum('Full Day','Morning','Evening') DEFAULT 'Full Day',
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

INSERT INTO `leave_requests` (`id`, `user_id`, `leave_type`, `start_shift`, `end_shift`, `start_date`, `end_date`, `reason`, `total_days`, `status`, `created_at`, `updated_at`) VALUES
(57, 25, 'Casual Leave', 'Full Day', 'Full Day', '2026-05-18', '2026-05-18', 'e', 1.0, 'Approved', '2026-05-18 06:20:08', '2026-05-18 06:20:19');

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
(555, 29, NULL, 'New Overtime Request for 2026-05-18.', 'System', 1, '2026-05-18 01:42:51'),
(559, 29, NULL, 'New Overtime Request for 2026-05-22.', 'System', 1, '2026-05-18 04:45:20'),
(563, 29, NULL, 'New Overtime Request for 2026-05-20.', 'System', 1, '2026-05-18 04:57:42'),
(564, 25, NULL, 'New Overtime Request for 2026-05-18.', 'System', 1, '2026-05-18 06:19:27'),
(565, 25, NULL, 'New Team Announcement: Important', 'System', 1, '2026-05-18 06:19:52'),
(566, 26, NULL, 'New Team Announcement: Important', 'System', 1, '2026-05-18 06:19:52'),
(567, 27, NULL, 'New Team Announcement: Important', 'System', 0, '2026-05-18 06:19:52'),
(568, 28, NULL, 'New Team Announcement: Important', 'System', 0, '2026-05-18 06:19:52'),
(569, 29, NULL, 'New Team Announcement: Important', 'System', 1, '2026-05-18 06:19:52'),
(570, 30, NULL, 'New Team Announcement: Important', 'System', 0, '2026-05-18 06:19:52'),
(571, 31, NULL, 'New Team Announcement: Important', 'System', 0, '2026-05-18 06:19:52'),
(572, 32, NULL, 'New Team Announcement: Important', 'System', 0, '2026-05-18 06:19:52'),
(583, 25, NULL, 'Leave request Approved by Team Leader.', 'System', 1, '2026-05-18 06:20:19'),
(587, 29, NULL, 'New Overtime Request for 2026-05-21.', 'System', 1, '2026-05-18 09:10:07'),
(588, 26, NULL, 'New Overtime Request for 2026-05-19.', 'System', 0, '2026-05-19 01:23:46'),
(589, 29, NULL, 'Your overtime request for 2026-05-21 has been Accepted.', 'System', 0, '2026-05-20 10:11:53'),
(590, 25, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(591, 26, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(592, 27, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(593, 28, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(594, 29, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(595, 30, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(596, 31, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(597, 32, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(598, 40, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(599, 41, NULL, 'New Announcement: Morning ', 'System', 1, '2026-05-20 10:35:17'),
(600, 38, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(601, 39, NULL, 'New Announcement: Morning ', 'System', 0, '2026-05-20 10:35:17'),
(605, 42, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(606, 43, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(607, 25, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(608, 26, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(609, 27, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(610, 28, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(611, 29, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(612, 30, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(613, 31, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(614, 32, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(615, 40, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(616, 41, NULL, 'New Announcement: Evening', 'System', 1, '2026-05-20 12:56:58'),
(617, 38, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(618, 39, NULL, 'New Announcement: Evening', 'System', 0, '2026-05-20 12:56:58'),
(620, 25, NULL, 'New Overtime Request for 2026-05-20.', 'System', 1, '2026-05-20 12:59:17'),
(621, 40, NULL, 'Win Thu Zar Aung submitted a new overtime request.', 'System', 0, '2026-05-20 12:59:50'),
(622, 41, NULL, 'Win Thu Zar Aung submitted a new overtime request.', 'System', 1, '2026-05-20 12:59:50');

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
(92, 29, 16, '2026-05-18', 2.00, 'Login Fix', 'Accepted', '2026-05-18 01:42:51', NULL),
(93, 29, 18, '2026-05-22', 2.00, 'task still undone', 'Accepted', '2026-05-18 04:45:20', NULL),
(94, 29, 17, '2026-05-20', 1.00, 'undone', 'Pending', '2026-05-18 04:57:42', NULL),
(95, 25, 18, '2026-05-18', 2.00, 'ff', 'Accepted', '2026-05-18 06:19:27', NULL),
(96, 29, 16, '2026-05-21', 3.00, 'test', 'Accepted', '2026-05-18 09:10:07', NULL),
(97, 26, 17, '2026-05-19', 2.00, 'Hi', '', '2026-05-19 01:23:46', NULL),
(98, 25, 16, '2026-05-20', 2.00, 'ww', 'Accepted', '2026-05-20 12:59:17', NULL);

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
(16, 'Genexus Employee', 'Khaing Aye', 1, 'In Progress (0%)', '2026-05-18 01:41:13'),
(17, 'Java Home Manage', 'Khaing Aye', 1, 'In Progress (0%)', '2026-05-18 01:41:23'),
(18, 'Python WFH System', 'Khaing Aye', 1, 'In Progress (0%)', '2026-05-18 01:41:32');

-- --------------------------------------------------------

--
-- Table structure for table `report_categories`
--

CREATE TABLE `report_categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(23, 18, 'Login Part', 'Yin Yin Kyaw', '2026-05-29', 0, 'Todo'),
(24, 17, 'Logout', 'Yin Yin Kyaw', '2026-05-29', 0, 'Todo'),
(25, 16, 'Dashboard', 'Yin Yin Kyaw', '2026-05-29', 0, 'Todo');

-- --------------------------------------------------------

--
-- Table structure for table `teams`
--

CREATE TABLE `teams` (
  `team_id` int(11) NOT NULL,
  `team_name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teams`
--

INSERT INTO `teams` (`team_id`, `team_name`, `created_at`, `description`) VALUES
(1, 'Team - 1', '2026-05-15 13:15:52', NULL),
(2, 'Team - 2', '2026-05-15 13:16:04', NULL),
(3, 'Team - 3', '2026-05-15 13:16:09', NULL),
(4, 'Team - 4', '2026-05-15 13:16:16', NULL);

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
(25, '1003', 'Win Thu Zar Aung', 'member', 'member', 'member', NULL, '2026-05-18 01:21:51', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(26, '1004', 'Aung Thura Khant', 'member1', 'member1', 'member', NULL, '2026-05-18 01:21:51', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(27, '1005', 'Min Min Phyo', 'member2', 'member2', 'member', NULL, '2026-05-18 01:21:51', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(28, '1006', 'Kyi Nu5Aye Chan', 'member3', 'member3', 'member', NULL, '2026-05-18 01:21:51', 'WFH', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(29, '1007', 'Yin Yin Kyaw', 'member4', 'member4', 'member', NULL, '2026-05-18 01:21:51', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(30, '1008', 'Zin Moh Moh Win Swe', 'member5', 'member5', 'member', NULL, '2026-05-18 01:21:51', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(31, '1009', 'Shwe Zin May', 'member6', 'member6', 'member', NULL, '2026-05-18 01:21:51', 'WFH', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(32, '1010', 'Ei Khaing Moe', 'member7', 'member7', 'member', NULL, '2026-05-18 01:21:51', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(35, '2002', 'Arthur Pendragon', 'admin', 'admin', 'admin', NULL, '2026-05-18 06:39:53', 'Office', NULL, 'active', NULL, 0, 0, 0, 'Office', NULL),
(38, '2003', 'kokokoko', 'aaaaaa', 'Aung123', 'member', 'Batch 13', '2026-05-20 07:46:24', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(39, '2004', 'aaaaa', 'bbbbbb', 'Aung123', 'leader', 'N/A', '2026-05-20 07:48:47', 'WFH', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(40, '2005', 'aaaaa', 'aaaaaaaa', 'Aung1234', 'leader', 'N/A', '2026-05-20 09:56:44', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(41, '2006', 'kyaw myo', 'leader5', 'Leader5', 'leader', 'N/A', '2026-05-20 09:59:00', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(42, '2007', 'dfgd', 'fdgdf', 'WS3wt3q55', 'admin', 'N/A', '2026-05-20 10:41:31', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(43, '2008', 'stge', 'etwe', 'ASetw465w4', 'admin', 'N/A', '2026-05-20 10:41:46', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL);

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
(1437, 25, 24, '2026-05-01', 'WFH'),
(1438, 26, 24, '2026-05-01', 'Office'),
(1439, 27, 24, '2026-05-01', 'WFH'),
(1440, 28, 24, '2026-05-01', 'WFH'),
(1441, 29, 24, '2026-05-01', 'WFH'),
(1442, 30, 24, '2026-05-01', 'WFH'),
(1443, 31, 24, '2026-05-01', 'Office'),
(1444, 32, 24, '2026-05-01', 'Office'),
(1445, 25, 24, '2026-05-04', 'WFH'),
(1446, 26, 24, '2026-05-04', 'Office'),
(1447, 27, 24, '2026-05-04', 'WFH'),
(1448, 28, 24, '2026-05-04', 'Office'),
(1449, 29, 24, '2026-05-04', 'Office'),
(1450, 30, 24, '2026-05-04', 'WFH'),
(1451, 31, 24, '2026-05-04', 'WFH'),
(1452, 32, 24, '2026-05-04', 'WFH'),
(1453, 25, 24, '2026-05-05', 'WFH'),
(1454, 26, 24, '2026-05-05', 'WFH'),
(1455, 27, 24, '2026-05-05', 'WFH'),
(1456, 28, 24, '2026-05-05', 'WFH'),
(1457, 29, 24, '2026-05-05', 'WFH'),
(1458, 30, 24, '2026-05-05', 'WFH'),
(1459, 31, 24, '2026-05-05', 'Office'),
(1460, 32, 24, '2026-05-05', 'WFH'),
(1461, 25, 24, '2026-05-06', 'Office'),
(1462, 26, 24, '2026-05-06', 'WFH'),
(1463, 27, 24, '2026-05-06', 'Office'),
(1464, 28, 24, '2026-05-06', 'Office'),
(1465, 29, 24, '2026-05-06', 'Office'),
(1466, 30, 24, '2026-05-06', 'Office'),
(1467, 31, 24, '2026-05-06', 'WFH'),
(1468, 32, 24, '2026-05-06', 'Office'),
(1469, 25, 24, '2026-05-07', 'Office'),
(1470, 26, 24, '2026-05-07', 'Office'),
(1471, 27, 24, '2026-05-07', 'WFH'),
(1472, 28, 24, '2026-05-07', 'Office'),
(1473, 29, 24, '2026-05-07', 'Office'),
(1474, 30, 24, '2026-05-07', 'WFH'),
(1475, 31, 24, '2026-05-07', 'Office'),
(1476, 32, 24, '2026-05-07', 'Office'),
(1477, 25, 24, '2026-05-08', 'WFH'),
(1478, 26, 24, '2026-05-08', 'Office'),
(1479, 27, 24, '2026-05-08', 'Office'),
(1480, 28, 24, '2026-05-08', 'WFH'),
(1481, 29, 24, '2026-05-08', 'WFH'),
(1482, 30, 24, '2026-05-08', 'Office'),
(1483, 31, 24, '2026-05-08', 'WFH'),
(1484, 32, 24, '2026-05-08', 'WFH'),
(1485, 25, 24, '2026-05-11', 'Office'),
(1486, 26, 24, '2026-05-11', 'WFH'),
(1487, 27, 24, '2026-05-11', 'Office'),
(1488, 28, 24, '2026-05-11', 'Office'),
(1489, 29, 24, '2026-05-11', 'Office'),
(1490, 30, 24, '2026-05-11', 'WFH'),
(1491, 31, 24, '2026-05-11', 'WFH'),
(1492, 32, 24, '2026-05-11', 'Office'),
(1493, 25, 24, '2026-05-12', 'WFH'),
(1494, 26, 24, '2026-05-12', 'WFH'),
(1495, 27, 24, '2026-05-12', 'WFH'),
(1496, 28, 24, '2026-05-12', 'WFH'),
(1497, 29, 24, '2026-05-12', 'WFH'),
(1498, 30, 24, '2026-05-12', 'Office'),
(1499, 31, 24, '2026-05-12', 'Office'),
(1500, 32, 24, '2026-05-12', 'WFH'),
(1501, 25, 24, '2026-05-13', 'WFH'),
(1502, 26, 24, '2026-05-13', 'Office'),
(1503, 27, 24, '2026-05-13', 'Office'),
(1504, 28, 24, '2026-05-13', 'WFH'),
(1505, 29, 24, '2026-05-13', 'WFH'),
(1506, 30, 24, '2026-05-13', 'Office'),
(1507, 31, 24, '2026-05-13', 'WFH'),
(1508, 32, 24, '2026-05-13', 'WFH'),
(1509, 25, 24, '2026-05-14', 'Office'),
(1510, 26, 24, '2026-05-14', 'WFH'),
(1511, 27, 24, '2026-05-14', 'WFH'),
(1512, 28, 24, '2026-05-14', 'WFH'),
(1513, 29, 24, '2026-05-14', 'WFH'),
(1514, 30, 24, '2026-05-14', 'Office'),
(1515, 31, 24, '2026-05-14', 'Office'),
(1516, 32, 24, '2026-05-14', 'Office'),
(1517, 25, 24, '2026-05-15', 'Office'),
(1518, 26, 24, '2026-05-15', 'Office'),
(1519, 27, 24, '2026-05-15', 'WFH'),
(1520, 28, 24, '2026-05-15', 'WFH'),
(1521, 29, 24, '2026-05-15', 'WFH'),
(1522, 30, 24, '2026-05-15', 'WFH'),
(1523, 31, 24, '2026-05-15', 'Office'),
(1524, 32, 24, '2026-05-15', 'WFH'),
(1525, 25, 24, '2026-05-18', 'Office'),
(1526, 26, 24, '2026-05-18', 'WFH'),
(1527, 27, 24, '2026-05-18', 'WFH'),
(1528, 28, 24, '2026-05-18', 'Office'),
(1529, 29, 24, '2026-05-18', 'Office'),
(1530, 30, 24, '2026-05-18', 'Office'),
(1531, 31, 24, '2026-05-18', 'WFH'),
(1532, 32, 24, '2026-05-18', 'Office'),
(1533, 25, 24, '2026-05-19', 'Office'),
(1534, 26, 24, '2026-05-19', 'WFH'),
(1535, 27, 24, '2026-05-19', 'WFH'),
(1536, 28, 24, '2026-05-19', 'Office'),
(1537, 29, 24, '2026-05-19', 'WFH'),
(1538, 30, 24, '2026-05-19', 'WFH'),
(1539, 31, 24, '2026-05-19', 'WFH'),
(1540, 32, 24, '2026-05-19', 'Office'),
(1541, 25, 24, '2026-05-20', 'Office'),
(1542, 26, 24, '2026-05-20', 'Office'),
(1543, 27, 24, '2026-05-20', 'WFH'),
(1544, 28, 24, '2026-05-20', 'WFH'),
(1545, 29, 24, '2026-05-20', 'Office'),
(1546, 30, 24, '2026-05-20', 'WFH'),
(1547, 31, 24, '2026-05-20', 'Office'),
(1548, 32, 24, '2026-05-20', 'Office'),
(1549, 25, 24, '2026-05-21', 'Office'),
(1550, 26, 24, '2026-05-21', 'WFH'),
(1551, 27, 24, '2026-05-21', 'Office'),
(1552, 28, 24, '2026-05-21', 'Office'),
(1553, 29, 24, '2026-05-21', 'Office'),
(1554, 30, 24, '2026-05-21', 'Office'),
(1555, 31, 24, '2026-05-21', 'Office'),
(1556, 32, 24, '2026-05-21', 'Office'),
(1557, 25, 24, '2026-05-22', 'WFH'),
(1558, 26, 24, '2026-05-22', 'WFH'),
(1559, 27, 24, '2026-05-22', 'Office'),
(1560, 28, 24, '2026-05-22', 'Office'),
(1561, 29, 24, '2026-05-22', 'WFH'),
(1562, 30, 24, '2026-05-22', 'Office'),
(1563, 31, 24, '2026-05-22', 'Office'),
(1564, 32, 24, '2026-05-22', 'Office'),
(1565, 25, 24, '2026-05-25', 'WFH'),
(1566, 26, 24, '2026-05-25', 'WFH'),
(1567, 27, 24, '2026-05-25', 'Office'),
(1568, 28, 24, '2026-05-25', 'WFH'),
(1569, 29, 24, '2026-05-25', 'WFH'),
(1570, 30, 24, '2026-05-25', 'Office'),
(1571, 31, 24, '2026-05-25', 'Office'),
(1572, 32, 24, '2026-05-25', 'Office'),
(1573, 25, 24, '2026-05-26', 'Office'),
(1574, 26, 24, '2026-05-26', 'Office'),
(1575, 27, 24, '2026-05-26', 'WFH'),
(1576, 28, 24, '2026-05-26', 'Office'),
(1577, 29, 24, '2026-05-26', 'Office'),
(1578, 30, 24, '2026-05-26', 'Office'),
(1579, 31, 24, '2026-05-26', 'WFH'),
(1580, 32, 24, '2026-05-26', 'Office'),
(1581, 25, 24, '2026-05-27', 'WFH'),
(1582, 26, 24, '2026-05-27', 'Office'),
(1583, 27, 24, '2026-05-27', 'Office'),
(1584, 28, 24, '2026-05-27', 'Office'),
(1585, 29, 24, '2026-05-27', 'WFH'),
(1586, 30, 24, '2026-05-27', 'Office'),
(1587, 31, 24, '2026-05-27', 'WFH'),
(1588, 32, 24, '2026-05-27', 'WFH'),
(1589, 25, 24, '2026-05-28', 'WFH'),
(1590, 26, 24, '2026-05-28', 'Office'),
(1591, 27, 24, '2026-05-28', 'WFH'),
(1592, 28, 24, '2026-05-28', 'WFH'),
(1593, 29, 24, '2026-05-28', 'Office'),
(1594, 30, 24, '2026-05-28', 'Office'),
(1595, 31, 24, '2026-05-28', 'WFH'),
(1596, 32, 24, '2026-05-28', 'Office'),
(1597, 25, 24, '2026-05-29', 'Office'),
(1598, 26, 24, '2026-05-29', 'WFH'),
(1599, 27, 24, '2026-05-29', 'WFH'),
(1600, 28, 24, '2026-05-29', 'Office'),
(1601, 29, 24, '2026-05-29', 'Office'),
(1602, 30, 24, '2026-05-29', 'WFH'),
(1603, 31, 24, '2026-05-29', 'WFH'),
(1604, 32, 24, '2026-05-29', 'Office'),
(1608, 39, 39, '2026-05-20', 'WFH'),
(1609, 38, 38, '2026-05-20', 'Office'),
(1610, 35, 35, '2026-05-20', 'Office'),
(1611, 41, 41, '2026-05-20', 'Office');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `announcement_replies`
--
ALTER TABLE `announcement_replies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT for table `leave_requests`
--
ALTER TABLE `leave_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=624;

--
-- AUTO_INCREMENT for table `overtime_requests`
--
ALTER TABLE `overtime_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `progress_history`
--
ALTER TABLE `progress_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `report_categories`
--
ALTER TABLE `report_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `teams`
--
ALTER TABLE `teams`
  MODIFY `team_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `wfh_schedules`
--
ALTER TABLE `wfh_schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1612;

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
