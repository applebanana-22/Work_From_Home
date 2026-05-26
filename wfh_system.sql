-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 26, 2026 at 04:05 AM
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
(1, 'Official WFH Protocol Reminder', 'All employees must maintain their mouse and keyboard tracking state as active during working hours.', 'admin', 'Admin One', '2026-05-22 10:50:00', 1),
(2, 'Quarterly Performance Review Schedule', 'The template for the quarterly self-evaluation is now available. Please submit your reviews by next Monday.', 'admin', 'Admin One', '2026-05-22 10:50:00', 1),
(3, 'New Security Patch Guidelines', 'Please update your local desktop clients to version 2.4.1 to fix the background sync connectivity issue.', 'admin', 'Admin One', '2026-05-22 10:50:00', 1),
(4, 'System Update: Auto-Checkout Enabled', 'Starting tomorrow, the system will automatically log you out if no activity is detected after 7:00 PM.', 'admin', 'Admin Two', '2026-05-22 10:50:00', 2),
(5, 'Server Maintenance Window', 'The production database will be offline for optimization this Sunday from 2:00 AM to 4:00 AM.', 'admin', 'Admin Two', '2026-05-22 10:50:00', 2),
(6, 'HR Policy: Leave Submission Rules', 'All leave requests must be submitted through the portal at least 3 days in advance for proper team coverage.', 'admin', 'Admin Two', '2026-05-22 10:50:00', 2),
(7, 'Internet Link Failover Test', 'We are testing our secondary ISP link today at 4:30 PM. Expect a minor 30-second drop in connections.', 'admin', 'Admin Three', '2026-05-22 10:50:00', 3),
(8, 'Office Attendance Log Fix', 'The check-in issue affecting users on the local office Wi-Fi network has been successfully patched.', 'admin', 'Admin Three', '2026-05-22 10:50:00', 3),
(9, 'Holiday Announcement', 'Please note that the office will be closed next Monday in observance of the upcoming public holiday.', 'admin', 'Admin Three', '2026-05-22 10:50:00', 3),
(10, 'Team 1: Core Framework Architecture Update', 'We are moving our base models to a new framework layer. Please pull the latest main branch before starting work.', 'leader', 'Leader One', '2026-05-22 10:50:00', 4),
(11, 'Team 1: Standup Meeting Time Shift', 'Starting tomorrow, our daily sync meeting will move from 9:30 AM to 10:00 AM to accommodate ongoing code reviews.', 'leader', 'Leader One', '2026-05-22 10:50:00', 4),
(12, 'Team 1: Genexus Project Milestones', 'The client loved the initial portal design! Let\'s focus on connecting the backend endpoints this week.', 'leader', 'Leader One', '2026-05-22 10:50:00', 4),
(13, 'Team 1: Python WFH System Tasks', 'Please update the progress bar on your assigned sub-tasks today. We need a clear view of the sprint status.', 'leader', 'Leader Two', '2026-05-22 10:50:00', 5),
(14, 'Team 1: Peer Code Review Assignments', 'I have updated the peer review matrix document. Check who you are reviewing for this week\'s merge requests.', 'leader', 'Leader Two', '2026-05-22 10:50:00', 5),
(15, 'Team 1: Bug Squashing Session', 'We have 12 open tickets remaining on the payroll module. Let\'s clear them out by Thursday evening.', 'leader', 'Leader Two', '2026-05-22 10:50:00', 5),
(16, 'Team 2: UX Guidelines for Redesign', 'Please review Figma file v3.2 before styling the new dashboard interface components.', 'leader', 'Leader Three', '2026-05-22 10:50:00', 6),
(17, 'Team 2: Asset Delivery Deadline', 'All iconography and finalized vector graphics must be pushed to the asset repository by noon tomorrow.', 'leader', 'Leader Three', '2026-05-22 10:50:00', 6),
(18, 'Team 2: Mobile Prototyping Review', 'We will host a walkthrough session of the user flow interactions on Friday at 3:00 PM.', 'leader', 'Leader Three', '2026-05-22 10:50:00', 6),
(19, 'Team 2: Client Feedback on Landing Pages', 'The client requested less whitespace on the headers. Let\'s adjust the CSS layout parameters accordingly.', 'leader', 'Leader Four', '2026-05-22 10:50:00', 7),
(20, 'Team 2: CSS Component Library Release', 'The custom design token library is live. Stop using hardcoded hex values in your component styles.', 'leader', 'Leader Four', '2026-05-22 10:50:00', 7),
(21, 'Team 2: Frontend Optimization Task', 'Our initial loading speed is a bit slow. Please optimize all banner images and use lazy loading.', 'leader', 'Leader Four', '2026-05-22 10:50:00', 7),
(22, 'Team 3: API Gateway Schema Finalized', 'The route schemas are locked. Backend engineers can now safely start writing the controllers.', 'leader', 'Leader Five', '2026-05-22 10:50:00', 8),
(23, 'Team 3: Database Indexing Priority', 'We are experiencing slow queries on the legacy tables. Please look into adding missing compound indexes.', 'leader', 'Leader Five', '2026-05-22 10:50:00', 8),
(24, 'Team 3: Cloud Storage Integration Sync', 'Please verify your API access tokens for AWS S3 environments. Staging keys have been rotated.', 'leader', 'Leader Five', '2026-05-22 10:50:00', 8),
(25, 'Team 3: Data Warehouse Architecture Note', 'We are enforcing strict schemas on incoming JSON payloads. Ensure your validation pipeline handles errors gracefully.', 'leader', 'Leader Six', '2026-05-22 10:50:00', 9),
(26, 'Team 3: Third-Party Webhook Testing', 'Payment gateway webhooks will be tested in our sandbox environment this afternoon. Ignore unexpected log entries.', 'leader', 'Leader Six', '2026-05-22 10:50:00', 9),
(27, 'Team 3: Backend Sprint Planning', 'The new task allocations for the middleware endpoints are ready on the scrum board. Pick your items.', 'leader', 'Leader Six', '2026-05-22 10:50:00', 9),
(28, 'Team 4: Test Automation Coverage Goal', 'Our current unit test coverage is at 68%. Let\'s aim to bring it up to 80% before the stable build launch.', 'leader', 'Leader Seven', '2026-05-22 10:50:00', 10),
(29, 'Team 4: Desktop Tracker Automation Test', 'We are initializing automated stress tests on the desktop app client. Alert the team if memory spikes occur.', 'leader', 'Leader Seven', '2026-05-22 10:50:00', 10),
(30, 'Team 4: Selenium Script Maintenance', 'A few login DOM selectors changed in the main app. We need to update our end-to-end testing scripts.', 'leader', 'Leader Seven', '2026-05-22 10:50:00', 10),
(31, 'Team 4: Excel Bot Exception Handling', 'The generator bot crashes when it encounters blank cells. Please implement null checks on data parsers.', 'leader', 'Leader Eight', '2026-05-22 10:50:00', 11),
(32, 'Team 4: System Health Monitoring Setup', 'We need to deploy Prometheus agents to the target nodes today. Follow the setup guide in the repo.', 'leader', 'Leader Eight', '2026-05-22 10:50:00', 11),
(33, 'Team 4: QA Bug Documentation Format', 'When logging issues, please attach the full stack trace alongside replication steps to speed up fixes.', 'leader', 'Leader Eight', '2026-05-22 10:50:00', 11);

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
(12, 10, 'hh', 'Member 1', '2026-05-25 04:01:46', 12),
(13, 10, 'kk', 'Member 1', '2026-05-25 04:02:08', 12),
(14, 1, 'ff', 'Leader One', '2026-05-25 04:30:50', 4),
(15, 1, 'gg', 'Leader One', '2026-05-25 04:31:13', 4),
(16, 1, 'hh', 'Leader One', '2026-05-25 04:31:20', 4);

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
(871, 12, '2026-05-24', '07:45:00', '16:30:00', 'Office', '2026-05-25 01:32:34', 'Office'),
(872, 12, '2026-05-23', '07:45:00', '19:30:00', 'Office', '2026-05-25 01:33:30', 'Office'),
(874, 12, '2026-05-25', '07:46:00', '20:30:00', 'Office', '2026-05-26 01:31:56', 'Office'),
(875, 12, '2026-05-22', '07:45:00', NULL, 'Office', '2026-05-26 01:43:07', 'Office');

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
(1, 12, '2026-05-01', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(2, 12, '2026-05-04', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(3, 12, '2026-05-05', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(4, 12, '2026-05-07', 'Wrote unit tests.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(5, 12, '2026-05-08', 'Attended sprint planning.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(6, 12, '2026-05-11', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(7, 12, '2026-05-12', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(8, 12, '2026-05-13', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(9, 12, '2026-05-14', 'Attended sprint planning.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(10, 12, '2026-05-18', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(11, 12, '2026-05-20', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(12, 12, '2026-05-21', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(13, 12, '2026-05-22', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(14, 13, '2026-05-01', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(15, 13, '2026-05-04', 'Fixed minor bugs.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(16, 13, '2026-05-05', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(17, 13, '2026-05-06', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(18, 13, '2026-05-08', 'Developed frontend feature.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(19, 13, '2026-05-11', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(20, 13, '2026-05-13', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(21, 13, '2026-05-14', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(22, 13, '2026-05-15', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(23, 13, '2026-05-18', 'Integrated API.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(24, 13, '2026-05-19', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(25, 13, '2026-05-20', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(26, 13, '2026-05-21', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(27, 13, '2026-05-22', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(28, 14, '2026-05-01', 'Fixed minor bugs.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(29, 14, '2026-05-04', 'Integrated API.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(30, 14, '2026-05-05', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(31, 14, '2026-05-06', 'Integrated API.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(32, 14, '2026-05-11', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(33, 14, '2026-05-13', 'Wrote unit tests.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(34, 14, '2026-05-14', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(35, 14, '2026-05-15', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(36, 14, '2026-05-18', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(37, 14, '2026-05-19', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(38, 14, '2026-05-20', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(39, 14, '2026-05-21', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(40, 14, '2026-05-22', 'Attended sprint planning.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(41, 15, '2026-05-01', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(42, 15, '2026-05-04', 'Wrote unit tests.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(43, 15, '2026-05-06', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(44, 15, '2026-05-08', 'Refactored legacy code.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(45, 15, '2026-05-11', 'Developed frontend feature.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(46, 15, '2026-05-12', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(47, 15, '2026-05-13', 'Fixed minor bugs.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(48, 15, '2026-05-14', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(49, 15, '2026-05-15', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(50, 15, '2026-05-18', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(51, 15, '2026-05-19', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(52, 15, '2026-05-20', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(53, 15, '2026-05-21', 'Developed frontend feature.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(54, 15, '2026-05-22', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(55, 16, '2026-05-01', 'Wrote unit tests.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(56, 16, '2026-05-04', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(57, 16, '2026-05-05', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(58, 16, '2026-05-06', 'Integrated API.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(59, 16, '2026-05-07', 'Developed frontend feature.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(60, 16, '2026-05-08', 'Integrated API.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(61, 16, '2026-05-11', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(62, 16, '2026-05-12', 'Attended sprint planning.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(63, 16, '2026-05-13', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(64, 16, '2026-05-14', 'Developed frontend feature.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(65, 16, '2026-05-15', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(66, 16, '2026-05-18', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(67, 16, '2026-05-19', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(68, 16, '2026-05-20', 'Integrated API.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(69, 16, '2026-05-21', 'Developed frontend feature.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(70, 16, '2026-05-22', 'Integrated API.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(71, 17, '2026-05-01', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(72, 17, '2026-05-04', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(73, 17, '2026-05-05', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(74, 17, '2026-05-06', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(75, 17, '2026-05-07', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(76, 17, '2026-05-08', 'Wrote unit tests.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(77, 17, '2026-05-11', 'Developed frontend feature.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(78, 17, '2026-05-12', 'Fixed minor bugs.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(79, 17, '2026-05-13', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(80, 17, '2026-05-14', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(81, 17, '2026-05-15', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(82, 17, '2026-05-18', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(83, 17, '2026-05-19', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(84, 17, '2026-05-20', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(85, 17, '2026-05-21', 'Wrote unit tests.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(86, 17, '2026-05-22', 'Fixed minor bugs.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(87, 18, '2026-05-01', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(88, 18, '2026-05-04', 'Developed frontend feature.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(89, 18, '2026-05-05', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(90, 18, '2026-05-06', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(91, 18, '2026-05-07', 'Fixed minor bugs.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(92, 18, '2026-05-08', 'Wrote unit tests.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(93, 18, '2026-05-11', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(94, 18, '2026-05-12', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(95, 18, '2026-05-13', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(96, 18, '2026-05-14', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(97, 18, '2026-05-15', 'Fixed minor bugs.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(98, 18, '2026-05-18', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(99, 18, '2026-05-19', 'Refactored legacy code.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(100, 18, '2026-05-20', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(101, 18, '2026-05-21', 'Wrote unit tests.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(102, 18, '2026-05-22', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(103, 19, '2026-05-01', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(104, 19, '2026-05-04', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(105, 19, '2026-05-05', 'Refactored legacy code.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(106, 19, '2026-05-07', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(107, 19, '2026-05-08', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(108, 19, '2026-05-11', 'Developed frontend feature.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(109, 19, '2026-05-12', 'Refactored legacy code.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(110, 19, '2026-05-14', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(111, 19, '2026-05-15', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(112, 19, '2026-05-18', 'Attended sprint planning.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(113, 19, '2026-05-19', 'Integrated API.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(114, 19, '2026-05-20', 'Developed frontend feature.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(115, 19, '2026-05-21', 'Fixed minor bugs.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(116, 20, '2026-05-04', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(117, 20, '2026-05-05', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(118, 20, '2026-05-06', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(119, 20, '2026-05-07', 'Wrote unit tests.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(120, 20, '2026-05-08', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(121, 20, '2026-05-11', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(122, 20, '2026-05-12', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(123, 20, '2026-05-13', 'Developed frontend feature.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(124, 20, '2026-05-14', 'Wrote unit tests.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(125, 20, '2026-05-18', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(126, 20, '2026-05-19', 'Integrated API.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(127, 20, '2026-05-20', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(128, 20, '2026-05-22', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(129, 21, '2026-05-01', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(130, 21, '2026-05-04', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(131, 21, '2026-05-05', 'Integrated API.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(132, 21, '2026-05-06', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(133, 21, '2026-05-07', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(134, 21, '2026-05-08', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(135, 21, '2026-05-11', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(136, 21, '2026-05-12', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(137, 21, '2026-05-13', 'Attended sprint planning.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(138, 21, '2026-05-14', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(139, 21, '2026-05-15', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(140, 21, '2026-05-18', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(141, 21, '2026-05-19', 'Developed frontend feature.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(142, 21, '2026-05-20', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(143, 21, '2026-05-21', 'Fixed minor bugs.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(144, 21, '2026-05-22', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(145, 22, '2026-05-01', 'Integrated API.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(146, 22, '2026-05-04', 'Integrated API.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(147, 22, '2026-05-05', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(148, 22, '2026-05-06', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(149, 22, '2026-05-07', 'Developed frontend feature.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(150, 22, '2026-05-08', 'Integrated API.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(151, 22, '2026-05-11', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(152, 22, '2026-05-14', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(153, 22, '2026-05-15', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(154, 22, '2026-05-18', 'Wrote unit tests.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(155, 22, '2026-05-19', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(156, 22, '2026-05-21', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(157, 22, '2026-05-22', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(158, 23, '2026-05-01', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(159, 23, '2026-05-04', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(160, 23, '2026-05-05', 'Developed frontend feature.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(161, 23, '2026-05-06', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(162, 23, '2026-05-07', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(163, 23, '2026-05-08', 'Fixed minor bugs.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(164, 23, '2026-05-11', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(165, 23, '2026-05-12', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(166, 23, '2026-05-13', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(167, 23, '2026-05-15', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(168, 23, '2026-05-18', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(169, 23, '2026-05-19', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(170, 23, '2026-05-22', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(171, 24, '2026-05-01', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(172, 24, '2026-05-04', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(173, 24, '2026-05-05', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(174, 24, '2026-05-06', 'Refactored legacy code.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(175, 24, '2026-05-07', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(176, 24, '2026-05-08', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(177, 24, '2026-05-11', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(178, 24, '2026-05-14', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(179, 24, '2026-05-15', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(180, 24, '2026-05-19', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(181, 24, '2026-05-20', 'Developed frontend feature.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(182, 24, '2026-05-21', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(183, 24, '2026-05-22', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(184, 25, '2026-05-01', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(185, 25, '2026-05-04', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(186, 25, '2026-05-05', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(187, 25, '2026-05-06', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(188, 25, '2026-05-07', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(189, 25, '2026-05-08', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(190, 25, '2026-05-11', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(191, 25, '2026-05-12', 'Attended sprint planning.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(192, 25, '2026-05-13', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(193, 25, '2026-05-14', 'Wrote unit tests.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(194, 25, '2026-05-15', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(195, 25, '2026-05-18', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(196, 25, '2026-05-19', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(197, 25, '2026-05-20', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(198, 25, '2026-05-21', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(199, 25, '2026-05-22', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(200, 26, '2026-05-01', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(201, 26, '2026-05-04', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(202, 26, '2026-05-05', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(203, 26, '2026-05-06', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(204, 26, '2026-05-07', 'Fixed minor bugs.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(205, 26, '2026-05-08', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(206, 26, '2026-05-11', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(207, 26, '2026-05-12', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(208, 26, '2026-05-13', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(209, 26, '2026-05-14', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(210, 26, '2026-05-15', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(211, 26, '2026-05-18', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(212, 26, '2026-05-19', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(213, 26, '2026-05-20', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(214, 26, '2026-05-21', 'Developed frontend feature.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(215, 26, '2026-05-22', 'Fixed minor bugs.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(216, 27, '2026-05-01', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(217, 27, '2026-05-04', 'Fixed minor bugs.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(218, 27, '2026-05-05', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(219, 27, '2026-05-06', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(220, 27, '2026-05-07', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(221, 27, '2026-05-08', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(222, 27, '2026-05-11', 'Wrote unit tests.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(223, 27, '2026-05-12', 'Integrated API.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(224, 27, '2026-05-13', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(225, 27, '2026-05-14', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(226, 27, '2026-05-15', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(227, 27, '2026-05-18', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(228, 27, '2026-05-19', 'Refactored legacy code.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(229, 27, '2026-05-20', 'Wrote unit tests.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(230, 27, '2026-05-21', 'Refactored legacy code.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(231, 27, '2026-05-22', 'Refactored legacy code.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(232, 28, '2026-05-04', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(233, 28, '2026-05-06', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(234, 28, '2026-05-07', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(235, 28, '2026-05-08', 'Refactored legacy code.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(236, 28, '2026-05-11', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(237, 28, '2026-05-12', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(238, 28, '2026-05-13', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(239, 28, '2026-05-14', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(240, 28, '2026-05-18', 'Integrated API.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(241, 28, '2026-05-19', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(242, 28, '2026-05-20', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(243, 28, '2026-05-21', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(244, 28, '2026-05-22', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(245, 29, '2026-05-01', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(246, 29, '2026-05-05', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(247, 29, '2026-05-06', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(248, 29, '2026-05-07', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(249, 29, '2026-05-08', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(250, 29, '2026-05-12', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(251, 29, '2026-05-13', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(252, 29, '2026-05-14', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(253, 29, '2026-05-15', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(254, 29, '2026-05-18', 'Developed frontend feature.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(255, 29, '2026-05-19', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(256, 29, '2026-05-20', 'Fixed minor bugs.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(257, 29, '2026-05-21', 'Developed frontend feature.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(258, 29, '2026-05-22', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(259, 30, '2026-05-01', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(260, 30, '2026-05-05', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(261, 30, '2026-05-07', 'Refactored legacy code.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(262, 30, '2026-05-08', 'Fixed minor bugs.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(263, 30, '2026-05-11', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(264, 30, '2026-05-12', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(265, 30, '2026-05-13', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(266, 30, '2026-05-14', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(267, 30, '2026-05-15', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(268, 30, '2026-05-18', 'Refactored legacy code.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(269, 30, '2026-05-19', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(270, 30, '2026-05-20', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(271, 30, '2026-05-21', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(272, 30, '2026-05-22', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(273, 31, '2026-05-01', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(274, 31, '2026-05-04', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(275, 31, '2026-05-05', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(276, 31, '2026-05-06', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(277, 31, '2026-05-07', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(278, 31, '2026-05-08', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(279, 31, '2026-05-11', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(280, 31, '2026-05-12', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(281, 31, '2026-05-13', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(282, 31, '2026-05-14', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(283, 31, '2026-05-15', 'Integrated API.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(284, 31, '2026-05-18', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(285, 31, '2026-05-19', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(286, 31, '2026-05-20', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(287, 31, '2026-05-21', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(288, 31, '2026-05-22', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(289, 32, '2026-05-01', 'Integrated API.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(290, 32, '2026-05-04', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(291, 32, '2026-05-05', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(292, 32, '2026-05-06', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(293, 32, '2026-05-07', 'Refactored legacy code.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(294, 32, '2026-05-08', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(295, 32, '2026-05-13', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(296, 32, '2026-05-14', 'Fixed minor bugs.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(297, 32, '2026-05-15', 'Attended sprint planning.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(298, 32, '2026-05-18', 'Wrote unit tests.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(299, 32, '2026-05-19', 'Attended sprint planning.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(300, 32, '2026-05-20', 'Attended sprint planning.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(301, 32, '2026-05-21', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(302, 32, '2026-05-22', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(303, 33, '2026-05-01', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(304, 33, '2026-05-04', 'Fixed minor bugs.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(305, 33, '2026-05-05', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(306, 33, '2026-05-06', 'Integrated API.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(307, 33, '2026-05-07', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(308, 33, '2026-05-08', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(309, 33, '2026-05-11', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(310, 33, '2026-05-12', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(311, 33, '2026-05-13', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(312, 33, '2026-05-14', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(313, 33, '2026-05-15', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(314, 33, '2026-05-18', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(315, 33, '2026-05-19', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(316, 33, '2026-05-20', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(317, 33, '2026-05-21', 'Integrated API.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(318, 33, '2026-05-22', 'Wrote unit tests.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(319, 34, '2026-05-01', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(320, 34, '2026-05-04', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(321, 34, '2026-05-06', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(322, 34, '2026-05-08', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(323, 34, '2026-05-11', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(324, 34, '2026-05-12', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(325, 34, '2026-05-13', 'Wrote unit tests.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(326, 34, '2026-05-14', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(327, 34, '2026-05-15', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(328, 34, '2026-05-19', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(329, 34, '2026-05-20', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(330, 34, '2026-05-21', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(331, 34, '2026-05-22', 'Attended sprint planning.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(332, 35, '2026-05-01', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(333, 35, '2026-05-04', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(334, 35, '2026-05-05', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(335, 35, '2026-05-06', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(336, 35, '2026-05-07', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(337, 35, '2026-05-08', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(338, 35, '2026-05-11', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(339, 35, '2026-05-12', 'Wrote unit tests.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(340, 35, '2026-05-15', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(341, 35, '2026-05-18', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(342, 35, '2026-05-19', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(343, 35, '2026-05-20', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(344, 35, '2026-05-21', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(345, 35, '2026-05-22', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(346, 36, '2026-05-01', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(347, 36, '2026-05-04', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(348, 36, '2026-05-05', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(349, 36, '2026-05-06', 'Attended sprint planning.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(350, 36, '2026-05-07', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(351, 36, '2026-05-08', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(352, 36, '2026-05-11', 'Integrated API.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(353, 36, '2026-05-12', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(354, 36, '2026-05-13', 'Attended sprint planning.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(355, 36, '2026-05-14', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(356, 36, '2026-05-15', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(357, 36, '2026-05-18', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(358, 36, '2026-05-19', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(359, 36, '2026-05-20', 'Attended sprint planning.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(360, 36, '2026-05-21', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(361, 36, '2026-05-22', 'Refactored legacy code.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(362, 37, '2026-05-01', 'Wrote unit tests.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(363, 37, '2026-05-04', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(364, 37, '2026-05-05', 'Refactored legacy code.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(365, 37, '2026-05-06', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(366, 37, '2026-05-07', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(367, 37, '2026-05-08', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(368, 37, '2026-05-11', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(369, 37, '2026-05-12', 'Refactored legacy code.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(370, 37, '2026-05-13', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(371, 37, '2026-05-14', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(372, 37, '2026-05-15', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(373, 37, '2026-05-18', 'Refactored legacy code.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(374, 37, '2026-05-19', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(375, 37, '2026-05-20', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(376, 37, '2026-05-21', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(377, 37, '2026-05-22', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(378, 38, '2026-05-01', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(379, 38, '2026-05-04', 'Fixed minor bugs.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(380, 38, '2026-05-05', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(381, 38, '2026-05-07', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(382, 38, '2026-05-08', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(383, 38, '2026-05-11', 'Integrated API.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(384, 38, '2026-05-12', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(385, 38, '2026-05-13', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(386, 38, '2026-05-18', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(387, 38, '2026-05-19', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(388, 38, '2026-05-20', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(389, 38, '2026-05-21', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(390, 38, '2026-05-22', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(391, 39, '2026-05-01', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(392, 39, '2026-05-04', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(393, 39, '2026-05-05', 'Wrote unit tests.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(394, 39, '2026-05-06', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(395, 39, '2026-05-07', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(396, 39, '2026-05-11', 'Fixed minor bugs.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(397, 39, '2026-05-12', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(398, 39, '2026-05-13', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(399, 39, '2026-05-14', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(400, 39, '2026-05-15', 'Refactored legacy code.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(401, 39, '2026-05-18', 'Attended sprint planning.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(402, 39, '2026-05-20', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(403, 39, '2026-05-21', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(404, 39, '2026-05-22', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(405, 40, '2026-05-01', 'Refactored legacy code.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(406, 40, '2026-05-04', 'Attended sprint planning.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(407, 40, '2026-05-05', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(408, 40, '2026-05-06', 'Wrote unit tests.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(409, 40, '2026-05-07', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(410, 40, '2026-05-08', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(411, 40, '2026-05-11', 'Wrote unit tests.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(412, 40, '2026-05-12', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(413, 40, '2026-05-13', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(414, 40, '2026-05-14', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(415, 40, '2026-05-15', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(416, 40, '2026-05-18', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(417, 40, '2026-05-19', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(418, 40, '2026-05-20', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(419, 40, '2026-05-21', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(420, 40, '2026-05-22', 'Wrote unit tests.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(421, 41, '2026-05-01', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(422, 41, '2026-05-04', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(423, 41, '2026-05-05', 'Wrote unit tests.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(424, 41, '2026-05-06', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(425, 41, '2026-05-07', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(426, 41, '2026-05-08', 'Attended sprint planning.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(427, 41, '2026-05-11', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(428, 41, '2026-05-12', 'Refactored legacy code.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(429, 41, '2026-05-13', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(430, 41, '2026-05-14', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(431, 41, '2026-05-15', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(432, 41, '2026-05-18', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(433, 41, '2026-05-19', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(434, 41, '2026-05-20', 'Wrote unit tests.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(435, 41, '2026-05-21', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(436, 41, '2026-05-22', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(437, 42, '2026-05-01', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16');
INSERT INTO `daily_reports` (`id`, `user_id`, `report_date`, `today_work`, `tomorrow_work`, `problems_issues`, `shared_matters`, `created_at`) VALUES
(438, 42, '2026-05-04', 'Integrated API.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(439, 42, '2026-05-05', 'Wrote unit tests.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(440, 42, '2026-05-06', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(441, 42, '2026-05-07', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(442, 42, '2026-05-08', 'Developed frontend feature.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(443, 42, '2026-05-11', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(444, 42, '2026-05-12', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(445, 42, '2026-05-13', 'Attended sprint planning.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(446, 42, '2026-05-14', 'Developed frontend feature.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(447, 42, '2026-05-15', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(448, 42, '2026-05-18', 'Integrated API.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(449, 42, '2026-05-19', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(450, 42, '2026-05-20', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(451, 42, '2026-05-21', 'Fixed minor bugs.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(452, 42, '2026-05-22', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(453, 43, '2026-05-04', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(454, 43, '2026-05-05', 'Integrated API.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(455, 43, '2026-05-06', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(456, 43, '2026-05-07', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(457, 43, '2026-05-08', 'Fixed minor bugs.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(458, 43, '2026-05-11', 'Wrote unit tests.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(459, 43, '2026-05-12', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(460, 43, '2026-05-13', 'Refactored legacy code.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(461, 43, '2026-05-14', 'Developed frontend feature.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(462, 43, '2026-05-15', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(463, 43, '2026-05-18', 'Developed frontend feature.', 'Deploy to staging.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(464, 43, '2026-05-19', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(465, 43, '2026-05-20', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(466, 43, '2026-05-21', 'Refactored legacy code.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(467, 44, '2026-05-01', 'Attended sprint planning.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(468, 44, '2026-05-04', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(469, 44, '2026-05-05', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(470, 44, '2026-05-06', 'Developed frontend feature.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(471, 44, '2026-05-07', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(472, 44, '2026-05-08', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(473, 44, '2026-05-11', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(474, 44, '2026-05-12', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(475, 44, '2026-05-13', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(476, 44, '2026-05-14', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(477, 44, '2026-05-15', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(478, 44, '2026-05-18', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(479, 44, '2026-05-19', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(480, 44, '2026-05-20', 'Refactored legacy code.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(481, 44, '2026-05-21', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(482, 44, '2026-05-22', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(483, 45, '2026-05-01', 'Integrated API.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(484, 45, '2026-05-04', 'Wrote unit tests.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(485, 45, '2026-05-05', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(486, 45, '2026-05-06', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(487, 45, '2026-05-07', 'Developed frontend feature.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(488, 45, '2026-05-08', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(489, 45, '2026-05-11', 'Attended sprint planning.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(490, 45, '2026-05-12', 'Wrote unit tests.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(491, 45, '2026-05-13', 'Integrated API.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(492, 45, '2026-05-14', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(493, 45, '2026-05-15', 'Fixed minor bugs.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(494, 45, '2026-05-18', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(495, 45, '2026-05-19', 'Attended sprint planning.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(496, 45, '2026-05-20', 'Wrote unit tests.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(497, 45, '2026-05-21', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(498, 45, '2026-05-22', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(499, 46, '2026-05-01', 'Refactored legacy code.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(500, 46, '2026-05-04', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(501, 46, '2026-05-06', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(502, 46, '2026-05-07', 'Refactored legacy code.', 'Deploy to staging.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(503, 46, '2026-05-08', 'Attended sprint planning.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(504, 46, '2026-05-12', 'Attended sprint planning.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(505, 46, '2026-05-13', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(506, 46, '2026-05-14', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(507, 46, '2026-05-15', 'Developed frontend feature.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(508, 46, '2026-05-18', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(509, 46, '2026-05-19', 'Integrated API.', 'Optimize queries.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(510, 46, '2026-05-20', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(511, 46, '2026-05-21', 'Wrote unit tests.', 'Start next ticket.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(512, 46, '2026-05-22', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(513, 47, '2026-05-01', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(514, 47, '2026-05-04', 'Attended sprint planning.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(515, 47, '2026-05-05', 'Fixed minor bugs.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(516, 47, '2026-05-06', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(517, 47, '2026-05-07', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(518, 47, '2026-05-08', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(519, 47, '2026-05-11', 'Fixed minor bugs.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(520, 47, '2026-05-12', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(521, 47, '2026-05-13', 'Attended sprint planning.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(522, 47, '2026-05-14', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(523, 47, '2026-05-15', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(524, 47, '2026-05-18', 'Integrated API.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(525, 47, '2026-05-19', 'Integrated API.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(526, 47, '2026-05-20', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(527, 47, '2026-05-21', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(528, 47, '2026-05-22', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(529, 48, '2026-05-01', 'Developed frontend feature.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(530, 48, '2026-05-04', 'Fixed minor bugs.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(531, 48, '2026-05-05', 'Refactored legacy code.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(532, 48, '2026-05-06', 'Fixed minor bugs.', 'Continue feature development.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(533, 48, '2026-05-07', 'Fixed minor bugs.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(534, 48, '2026-05-08', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(535, 48, '2026-05-11', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(536, 48, '2026-05-12', 'Refactored legacy code.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(537, 48, '2026-05-13', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(538, 48, '2026-05-14', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(539, 48, '2026-05-15', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(540, 48, '2026-05-18', 'Fixed minor bugs.', 'Fix QA bugs.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(541, 48, '2026-05-19', 'Attended sprint planning.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(542, 48, '2026-05-20', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(543, 48, '2026-05-21', 'Refactored legacy code.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(544, 48, '2026-05-22', 'Refactored legacy code.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(545, 49, '2026-05-01', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(546, 49, '2026-05-04', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(547, 49, '2026-05-05', 'Integrated API.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(548, 49, '2026-05-06', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(549, 49, '2026-05-07', 'Fixed minor bugs.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(550, 49, '2026-05-08', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(551, 49, '2026-05-11', 'Attended sprint planning.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(552, 49, '2026-05-12', 'Developed frontend feature.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(553, 49, '2026-05-13', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(554, 49, '2026-05-14', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(555, 49, '2026-05-15', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(556, 49, '2026-05-18', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(557, 49, '2026-05-19', 'Integrated API.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(558, 49, '2026-05-20', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(559, 49, '2026-05-21', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(560, 49, '2026-05-22', 'Wrote unit tests.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(561, 50, '2026-05-01', 'Refactored legacy code.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(562, 50, '2026-05-04', 'Attended sprint planning.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(563, 50, '2026-05-05', 'Wrote unit tests.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(564, 50, '2026-05-06', 'Integrated API.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(565, 50, '2026-05-07', 'Integrated API.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(566, 50, '2026-05-08', 'Fixed minor bugs.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(567, 50, '2026-05-11', 'Wrote unit tests.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(568, 50, '2026-05-12', 'Developed frontend feature.', 'Continue feature development.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(569, 50, '2026-05-13', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(570, 50, '2026-05-14', 'Developed frontend feature.', 'Optimize queries.', 'None', 'N/A', '2026-05-22 11:52:16'),
(571, 50, '2026-05-15', 'Fixed minor bugs.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(572, 50, '2026-05-18', 'Attended sprint planning.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(573, 50, '2026-05-19', 'Wrote unit tests.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(574, 50, '2026-05-20', 'Integrated API.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(575, 50, '2026-05-21', 'Refactored legacy code.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(576, 50, '2026-05-22', 'Developed frontend feature.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(577, 51, '2026-05-01', 'Attended sprint planning.', 'Continue feature development.', 'None', 'N/A', '2026-05-22 11:52:16'),
(578, 51, '2026-05-04', 'Developed frontend feature.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(579, 51, '2026-05-05', 'Attended sprint planning.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(580, 51, '2026-05-06', 'Wrote unit tests.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16'),
(581, 51, '2026-05-07', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(582, 51, '2026-05-08', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(583, 51, '2026-05-11', 'Refactored legacy code.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(584, 51, '2026-05-12', 'Developed frontend feature.', 'Fix QA bugs.', 'None', 'N/A', '2026-05-22 11:52:16'),
(585, 51, '2026-05-13', 'Wrote unit tests.', 'Deploy to staging.', 'None', 'N/A', '2026-05-22 11:52:16'),
(586, 51, '2026-05-19', 'Wrote unit tests.', 'Fix QA bugs.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(587, 51, '2026-05-20', 'Wrote unit tests.', 'Optimize queries.', 'Environment setup issues.', 'N/A', '2026-05-22 11:52:16'),
(588, 51, '2026-05-21', 'Wrote unit tests.', 'Start next ticket.', 'API rate limits.', 'N/A', '2026-05-22 11:52:16'),
(589, 51, '2026-05-22', 'Refactored legacy code.', 'Start next ticket.', 'None', 'N/A', '2026-05-22 11:52:16');

-- --------------------------------------------------------

--
-- Table structure for table `leave_details`
--

CREATE TABLE `leave_details` (
  `id` int(11) NOT NULL,
  `request_id` int(11) NOT NULL,
  `leave_date` date NOT NULL,
  `shift_status` varchar(50) DEFAULT 'Full Day'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_details`
--

INSERT INTO `leave_details` (`id`, `request_id`, `leave_date`, `shift_status`) VALUES
(8, 3, '2026-05-25', 'Full Day'),
(9, 4, '2026-05-26', 'Full Day');

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
  `leader_reason` text DEFAULT NULL,
  `total_days` decimal(4,1) NOT NULL,
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_requests`
--

INSERT INTO `leave_requests` (`id`, `user_id`, `leave_type`, `start_shift`, `end_shift`, `start_date`, `end_date`, `reason`, `leader_reason`, `total_days`, `status`, `created_at`, `updated_at`) VALUES
(3, 12, 'Casual Leave', 'Full Day', 'Full Day', '2026-05-25', '2026-05-25', 'qq', '', 1.0, 'Approved', '2026-05-23 18:16:50', '2026-05-23 18:17:53'),
(4, 12, 'Vacation', 'Full Day', 'Full Day', '2026-05-26', '2026-05-26', 'ss', NULL, 1.0, 'Pending', '2026-05-23 18:24:01', '2026-05-23 18:24:01');

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
(102, 4, 3, '📅 Member 1 requested 1.0 day leave.', 'System', 1, '2026-05-23 18:16:50'),
(103, 5, 3, '📅 Member 1 requested 1.0 day leave.', 'System', 0, '2026-05-23 18:16:50'),
(105, 12, NULL, '✅ Your Casual Leave request has been Approved by Team Leader.', 'System', 1, '2026-05-23 18:17:53'),
(106, 5, NULL, '✅ Your Casual Leave request has been Approved by Team Leader.', 'System', 0, '2026-05-23 18:17:53'),
(107, 4, 4, '📅 Member 1 requested 1.0 day leave.', 'System', 1, '2026-05-23 18:24:01'),
(108, 5, 4, '📅 Member 1 requested 1.0 day leave.', 'System', 0, '2026-05-23 18:24:01'),
(110, 4, NULL, 'overtime request submitted by Member 1.', 'System', 1, '2026-05-24 12:45:11'),
(111, 12, NULL, 'Your overtime request for 2026-05-24 has been Accepted.', 'System', 1, '2026-05-24 12:45:36'),
(442, 4, NULL, 'overtime request submitted by Member 1.', 'System', 1, '2026-05-25 02:06:02'),
(443, 12, NULL, 'New Overtime Request for 2026-05-25.', 'System', 1, '2026-05-25 02:35:58'),
(444, 4, NULL, 'overtime request submitted by Member 1.', 'System', 1, '2026-05-25 04:29:17'),
(445, 12, NULL, 'Your overtime request for 2026-05-26 has been Accepted.', 'System', 1, '2026-05-25 04:29:59'),
(446, 12, NULL, 'Your overtime request for 2026-05-25 has been Rejected. Reason: no nedd', 'System', 1, '2026-05-25 04:30:05');

-- --------------------------------------------------------

--
-- Table structure for table `overtime_requests`
--

CREATE TABLE `overtime_requests` (
  `id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `ot_date` date DEFAULT NULL,
  `hours` decimal(4,2) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('Pending','Accepted','Rejected','Cancelled') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `rejected_reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `overtime_requests`
--

INSERT INTO `overtime_requests` (`id`, `member_id`, `created_by`, `project_id`, `ot_date`, `hours`, `reason`, `status`, `created_at`, `rejected_reason`) VALUES
(87, 12, 12, 1, '2026-05-25', 2.00, 'dd', 'Rejected', '2026-05-25 02:06:02', 'no nedd'),
(88, 12, 4, 2, '2026-05-25', 2.00, 'dd', 'Cancelled', '2026-05-25 02:35:58', NULL),
(89, 12, 12, 5, '2026-05-26', 2.00, 'ddd', 'Accepted', '2026-05-25 04:29:17', NULL),
(90, 12, 12, 1, '2026-05-25', 2.50, 'Urgent hotfix deployment for the frontend.', 'Accepted', '2026-05-26 01:32:39', NULL),
(92, 12, 12, 1, '2026-05-22', 3.00, 'Urgent hotfix deployment for the frontend.', 'Accepted', '2026-05-26 01:44:29', NULL);

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
(1, 1, 1, 'Member 3', 25, '2026-05-10', 'Initial repository initialized and basic setup complete.'),
(2, 2, 1, 'Member 7', 50, '2026-05-12', 'Database schema migration scripts written and tested.'),
(3, 3, 1, 'Member 1', 75, '2026-05-15', 'Designed the landing view UI layout using responsive grids.'),
(4, 4, 1, 'Member 9', 0, '2026-05-10', 'Awaiting core modules to be finished before starting test cases.'),
(5, 5, 1, 'Member 4', 100, '2026-05-18', 'Documentation generated and deployment scripts verified successfully.'),
(6, 6, 2, 'Member 2', 50, '2026-05-11', 'Collected all feature requirements from team leads.'),
(7, 7, 2, 'Member 8', 25, '2026-05-13', 'Configured base tables and relationships.'),
(8, 8, 2, 'Member 5', 80, '2026-05-16', 'Created most CRUD endpoints, handling validation routines.'),
(9, 9, 2, 'Member 10', 40, '2026-05-14', 'Connected user login panels to backend testing server.'),
(10, 10, 2, 'Member 6', 100, '2026-05-19', 'Conducted final code walkthrough; merged to dev branch.'),
(11, 11, 3, 'Member 4', 100, '2026-05-10', 'Kickoff meeting complete, technical constraints documented.'),
(12, 12, 3, 'Member 1', 65, '2026-05-14', 'JWT Token generation and role checking logic implemented.'),
(13, 13, 3, 'Member 8', 35, '2026-05-12', 'Extracted initial mock datasets for graphing components.'),
(14, 14, 3, 'Member 2', 20, '2026-05-15', 'Identified potential package vulnerabilities in dependency tree.'),
(15, 15, 3, 'Member 9', 90, '2026-05-20', 'Production build successfully staged on local testing box.'),
(16, 16, 4, 'Member 7', 45, '2026-05-11', 'Drafted system sequence and component block diagrams.'),
(17, 17, 4, 'Member 3', 70, '2026-05-16', 'Parsed old production records into flat JSON files.'),
(18, 18, 4, 'Member 6', 15, '2026-05-13', 'Began connection interface setup for payment engine.'),
(19, 19, 4, 'Member 10', 50, '2026-05-17', 'Conducted first internal pass of dashboard functionality.'),
(20, 20, 4, 'Member 5', 100, '2026-05-21', 'Handover materials packaged into markdown files in repo.'),
(21, 26, 6, 'Member 14', 30, '2026-05-10', 'Drafted rough wires for home layouts.'),
(22, 27, 6, 'Member 18', 60, '2026-05-13', 'Refactored backend routes to serve static views quickly.'),
(23, 28, 6, 'Member 12', 45, '2026-05-14', 'Hooked up form bindings to event handlers.'),
(24, 29, 6, 'Member 20', 10, '2026-05-12', 'Configuring test suite parameters for component coverage.'),
(25, 30, 6, 'Member 15', 100, '2026-05-20', 'Pushed stable distribution assets to deployment bucket.'),
(26, 31, 7, 'Member 13', 75, '2026-05-11', 'Collected interactive prototypes and feedback logs.'),
(27, 32, 7, 'Member 19', 40, '2026-05-15', 'Adjusted secondary indices to scale up query lookups.'),
(28, 33, 7, 'Member 16', 90, '2026-05-18', 'Finished REST controller methods for dynamic fetching.'),
(29, 34, 7, 'Member 11', 25, '2026-05-12', 'Setup base templates using utility CSS selectors.'),
(30, 35, 7, 'Member 17', 100, '2026-05-21', 'Final layout approved by design leader.'),
(31, 36, 8, 'Member 15', 100, '2026-05-10', 'Environment configuration keys generated and saved.'),
(32, 37, 8, 'Member 12', 55, '2026-05-14', 'Implemented cookie session store handling mechanisms.'),
(33, 38, 8, 'Member 19', 30, '2026-05-13', 'Integrated chart elements into main tracking card view.'),
(34, 39, 8, 'Member 13', 85, '2026-05-19', 'Ran load testing runs on data ingestion modules.'),
(35, 40, 8, 'Member 20', 100, '2026-05-22', 'Merged everything up to production branch without errors.'),
(36, 51, 11, 'Member 25', 50, '2026-05-11', 'Mapping reverse proxy gateway routes to downstream endpoints.'),
(37, 52, 11, 'Member 29', 80, '2026-05-15', 'Optimized raw storage queries reducing execution time by half.'),
(38, 53, 11, 'Member 23', 20, '2026-05-12', 'Scaffolding view controllers for data synchronization lists.'),
(39, 54, 11, 'Member 21', 100, '2026-05-18', 'Validated request headers against malicious injection profiles.'),
(40, 55, 11, 'Member 26', 100, '2026-05-20', 'Readme files containing API usage endpoints completed.'),
(41, 56, 12, 'Member 24', 95, '2026-05-12', 'Documented structural data rules for incoming sync streams.'),
(42, 57, 12, 'Member 30', 40, '2026-05-14', 'Re-indexing transaction logs to clean up redundant spaces.'),
(43, 58, 12, 'Member 27', 60, '2026-05-16', 'Exposed health statistics endpoints via lightweight routes.'),
(44, 59, 12, 'Member 22', 15, '2026-05-13', 'Began styling configuration control dashboard view.'),
(45, 60, 12, 'Member 28', 100, '2026-05-21', 'Obtained engineering approval on processing throughput metrics.'),
(46, 76, 16, 'Member 36', 40, '2026-05-11', 'Setup Selenium Grid config properties on staging nodes.'),
(47, 77, 16, 'Member 40', 70, '2026-05-15', 'Wrote mock input data parsers to drive functional suites.'),
(48, 78, 16, 'Member 34', 85, '2026-05-17', 'Configured continuous reporting output hooks to Slack.'),
(49, 79, 16, 'Member 32', 100, '2026-05-19', 'Integrated parallel script runner inside CI pipelines.'),
(50, 80, 16, 'Member 37', 100, '2026-05-22', 'Bundled target logs into centralized storage mount targets.'),
(51, 81, 17, 'Member 35', 60, '2026-05-12', 'Drafted test scripts checking boundaries of text inputs.'),
(52, 82, 17, 'Member 31', 30, '2026-05-14', 'Investigating background loop resource overhead behaviors.'),
(53, 83, 17, 'Member 38', 50, '2026-05-16', 'Completed structural test cases focusing on error triggers.'),
(54, 84, 17, 'Member 33', 100, '2026-05-20', 'Resolved race conditions during multiple parallel run tasks.'),
(55, 85, 17, 'Member 39', 100, '2026-05-22', 'Final verification criteria reports exported successfully.');

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
(1, 'Genexus Employee Portal', 'Leader One', 1, 'In Progress', '2026-05-22 10:45:46'),
(2, 'Java Home Management', 'Leader One', 1, 'Pending', '2026-05-22 10:45:46'),
(3, 'Python WFH System', 'Leader Two', 1, 'In Progress', '2026-05-22 10:45:46'),
(4, 'Internal Payroll System', 'Leader Two', 1, 'Pending', '2026-05-22 10:45:46'),
(5, 'Inventory Tracking Module', 'Leader One', 1, 'In Progress (0%)', '2026-05-22 10:45:46'),
(6, 'Main Website Redesign', 'Leader Three', 2, 'In Progress', '2026-05-22 10:45:46'),
(7, 'Mobile App Prototyping', 'Leader Four', 2, 'Pending', '2026-05-22 10:45:46'),
(8, 'Dashboard UI Overhaul', 'Leader Three', 2, 'Pending', '2026-05-22 10:45:46'),
(9, 'Client Landing Pages', 'Leader Four', 2, 'Pending', '2026-05-22 10:45:46'),
(10, 'Company Design System', 'Leader Three', 2, 'In Progress', '2026-05-22 10:45:46'),
(11, 'API Gateway Migration', 'Leader Five', 3, 'In Progress', '2026-05-22 10:45:46'),
(12, 'Legacy Database Optimization', 'Leader Six', 3, 'Pending', '2026-05-22 10:45:46'),
(13, 'Cloud Storage Sync', 'Leader Five', 3, 'Pending', '2026-05-22 10:45:46'),
(14, 'Real-time Data Warehouse', 'Leader Six', 3, 'Pending', '2026-05-22 10:45:46'),
(15, 'Third-party Payment Integration', 'Leader Five', 3, 'In Progress (0%)', '2026-05-22 10:45:46'),
(16, 'Automated Testing Suite', 'Leader Seven', 4, 'In Progress', '2026-05-22 10:45:46'),
(17, 'Excel Report Generator Bot', 'Leader Eight', 4, 'Pending', '2026-05-22 10:45:46'),
(18, 'Desktop Activity Tracker', 'Leader Seven', 4, 'In Progress', '2026-05-22 10:45:46'),
(19, 'Selenium Scraping Tool', 'Leader Eight', 4, 'Pending', '2026-05-22 10:45:46'),
(20, 'System Health Monitor', 'Leader Seven', 4, 'Pending', '2026-05-22 10:45:46');

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
-- Table structure for table `sec_notifications`
--

CREATE TABLE `sec_notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `request_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `notif_type` enum('New_Request','Status_Update','System') DEFAULT 'System',
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sec_notifications`
--

INSERT INTO `sec_notifications` (`id`, `user_id`, `request_id`, `message`, `notif_type`, `is_read`, `created_at`) VALUES
(21, 5, NULL, '✅ Your Casual Leave request has been Approved by Team Leader.', 'System', 0, '2026-05-23 18:08:29'),
(22, 4, NULL, 'overtime request submitted by Member 1.', 'System', 1, '2026-05-24 12:45:11'),
(23, 12, NULL, 'Your overtime request for 2026-05-24 has been Accepted.', 'System', 1, '2026-05-24 12:45:36'),
(24, 4, NULL, 'overtime request submitted by Member 1.', 'System', 1, '2026-05-25 02:06:02'),
(25, 4, NULL, 'overtime request submitted by Member 1.', 'System', 1, '2026-05-25 04:29:17'),
(26, 12, NULL, 'Your overtime request for 2026-05-26 has been Accepted.', 'System', 1, '2026-05-25 04:29:59'),
(27, 12, NULL, 'Your overtime request for 2026-05-25 has been Rejected. Reason: no nedd', 'System', 1, '2026-05-25 04:30:05');

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
(1, 1, 'Initial Planning & Architecture', 'Member 3', '2026-06-05', 0, 'Todo'),
(2, 1, 'Core Backend Development', 'Member 7', '2026-06-15', 0, 'Todo'),
(3, 1, 'Frontend UI Integration', 'Member 1', '2026-06-20', 0, 'Todo'),
(4, 1, 'Quality Assurance & Testing', 'Member 9', '2026-06-25', 0, 'Todo'),
(5, 1, 'Documentation & Deployment', 'Member 4', '2026-06-30', 0, 'Todo'),
(6, 2, 'Requirement Gathering', 'Member 2', '2026-06-05', 0, 'Todo'),
(7, 2, 'Database Schema Setup', 'Member 8', '2026-06-15', 0, 'Todo'),
(8, 2, 'API Endpoint Creation', 'Member 5', '2026-06-20', 0, 'Todo'),
(9, 2, 'Client-Side Implementation', 'Member 10', '2026-06-25', 0, 'Todo'),
(10, 2, 'Final Review', 'Member 6', '2026-06-30', 0, 'Todo'),
(11, 3, 'Project Kickoff & Setup', 'Member 4', '2026-06-05', 0, 'Todo'),
(12, 3, 'Authentication Module', 'Member 1', '2026-06-15', 0, 'Todo'),
(13, 3, 'Dashboard Analytics', 'Member 8', '2026-06-20', 0, 'Todo'),
(14, 3, 'Security Auditing', 'Member 2', '2026-06-25', 0, 'Todo'),
(15, 3, 'Production Release', 'Member 9', '2026-06-30', 0, 'Todo'),
(16, 4, 'System Blueprint Creation', 'Member 7', '2026-06-05', 0, 'Todo'),
(17, 4, 'Data Migration', 'Member 3', '2026-06-15', 0, 'Todo'),
(18, 4, 'Third-party Integrations', 'Member 6', '2026-06-20', 0, 'Todo'),
(19, 4, 'User Acceptance Testing', 'Member 10', '2026-06-25', 0, 'Todo'),
(20, 4, 'Handover Preparation', 'Member 5', '2026-06-30', 0, 'Todo'),
(21, 5, 'Scope Definition', 'Member 9', '2026-06-05', 0, 'Todo'),
(22, 5, 'Microservices Architecture', 'Member 2', '2026-06-15', 0, 'Todo'),
(23, 5, 'State Management', 'Member 4', '2026-06-20', 0, 'Todo'),
(24, 5, 'Bug Fixing Phase', 'Member 1', '2026-06-25', 0, 'Todo'),
(25, 5, 'Post-Launch Support Plan', 'Member 8', '2026-06-30', 0, 'Todo'),
(26, 6, 'Initial Planning & Architecture', 'Member 14', '2026-06-05', 0, 'Todo'),
(27, 6, 'Core Backend Development', 'Member 18', '2026-06-15', 0, 'Todo'),
(28, 6, 'Frontend UI Integration', 'Member 12', '2026-06-20', 0, 'Todo'),
(29, 6, 'Quality Assurance & Testing', 'Member 20', '2026-06-25', 0, 'Todo'),
(30, 6, 'Documentation & Deployment', 'Member 15', '2026-06-30', 0, 'Todo'),
(31, 7, 'Requirement Gathering', 'Member 13', '2026-06-05', 0, 'Todo'),
(32, 7, 'Database Schema Setup', 'Member 19', '2026-06-15', 0, 'Todo'),
(33, 7, 'API Endpoint Creation', 'Member 16', '2026-06-20', 0, 'Todo'),
(34, 7, 'Client-Side Implementation', 'Member 11', '2026-06-25', 0, 'Todo'),
(35, 7, 'Final Review', 'Member 17', '2026-06-30', 0, 'Todo'),
(36, 8, 'Project Kickoff & Setup', 'Member 15', '2026-06-05', 0, 'Todo'),
(37, 8, 'Authentication Module', 'Member 12', '2026-06-15', 0, 'Todo'),
(38, 8, 'Dashboard Analytics', 'Member 19', '2026-06-20', 0, 'Todo'),
(39, 8, 'Security Auditing', 'Member 13', '2026-06-25', 0, 'Todo'),
(40, 8, 'Production Release', 'Member 20', '2026-06-30', 0, 'Todo'),
(41, 9, 'System Blueprint Creation', 'Member 18', '2026-06-05', 0, 'Todo'),
(42, 9, 'Data Migration', 'Member 14', '2026-06-15', 0, 'Todo'),
(43, 9, 'Third-party Integrations', 'Member 17', '2026-06-20', 0, 'Todo'),
(44, 9, 'User Acceptance Testing', 'Member 11', '2026-06-25', 0, 'Todo'),
(45, 9, 'Handover Preparation', 'Member 16', '2026-06-30', 0, 'Todo'),
(46, 10, 'Scope Definition', 'Member 20', '2026-06-05', 0, 'Todo'),
(47, 10, 'Microservices Architecture', 'Member 13', '2026-06-15', 0, 'Todo'),
(48, 10, 'State Management', 'Member 15', '2026-06-20', 0, 'Todo'),
(49, 10, 'Bug Fixing Phase', 'Member 12', '2026-06-25', 0, 'Todo'),
(50, 10, 'Post-Launch Support Plan', 'Member 19', '2026-06-30', 0, 'Todo'),
(51, 11, 'Initial Planning & Architecture', 'Member 25', '2026-06-05', 0, 'Todo'),
(52, 11, 'Core Backend Development', 'Member 29', '2026-06-15', 0, 'Todo'),
(53, 11, 'Frontend UI Integration', 'Member 23', '2026-06-20', 0, 'Todo'),
(54, 11, 'Quality Assurance & Testing', 'Member 21', '2026-06-25', 0, 'Todo'),
(55, 11, 'Documentation & Deployment', 'Member 26', '2026-06-30', 0, 'Todo'),
(56, 12, 'Requirement Gathering', 'Member 24', '2026-06-05', 0, 'Todo'),
(57, 12, 'Database Schema Setup', 'Member 30', '2026-06-15', 0, 'Todo'),
(58, 12, 'API Endpoint Creation', 'Member 27', '2026-06-20', 0, 'Todo'),
(59, 12, 'Client-Side Implementation', 'Member 22', '2026-06-25', 0, 'Todo'),
(60, 12, 'Final Review', 'Member 28', '2026-06-30', 0, 'Todo'),
(61, 13, 'Project Kickoff & Setup', 'Member 26', '2026-06-05', 0, 'Todo'),
(62, 13, 'Authentication Module', 'Member 23', '2026-06-15', 0, 'Todo'),
(63, 13, 'Dashboard Analytics', 'Member 30', '2026-06-20', 0, 'Todo'),
(64, 13, 'Security Auditing', 'Member 24', '2026-06-25', 0, 'Todo'),
(65, 13, 'Production Release', 'Member 21', '2026-06-30', 0, 'Todo'),
(66, 14, 'System Blueprint Creation', 'Member 29', '2026-06-05', 0, 'Todo'),
(67, 14, 'Data Migration', 'Member 25', '2026-06-15', 0, 'Todo'),
(68, 14, 'Third-party Integrations', 'Member 28', '2026-06-20', 0, 'Todo'),
(69, 14, 'User Acceptance Testing', 'Member 22', '2026-06-25', 0, 'Todo'),
(70, 14, 'Handover Preparation', 'Member 27', '2026-06-30', 0, 'Todo'),
(71, 15, 'Scope Definition', 'Member 21', '2026-06-05', 0, 'Todo'),
(72, 15, 'Microservices Architecture', 'Member 24', '2026-06-15', 0, 'Todo'),
(73, 15, 'State Management', 'Member 26', '2026-06-20', 0, 'Todo'),
(74, 15, 'Bug Fixing Phase', 'Member 23', '2026-06-25', 0, 'Todo'),
(75, 15, 'Post-Launch Support Plan', 'Member 30', '2026-06-30', 0, 'Todo'),
(76, 16, 'Initial Planning & Architecture', 'Member 36', '2026-06-05', 0, 'Todo'),
(77, 16, 'Core Backend Development', 'Member 40', '2026-06-15', 0, 'Todo'),
(78, 16, 'Frontend UI Integration', 'Member 34', '2026-06-20', 0, 'Todo'),
(79, 16, 'Quality Assurance & Testing', 'Member 32', '2026-06-25', 0, 'Todo'),
(80, 16, 'Documentation & Deployment', 'Member 37', '2026-06-30', 0, 'Todo'),
(81, 17, 'Requirement Gathering', 'Member 35', '2026-06-05', 0, 'Todo'),
(82, 17, 'Database Schema Setup', 'Member 31', '2026-06-15', 0, 'Todo'),
(83, 17, 'API Endpoint Creation', 'Member 38', '2026-06-20', 0, 'Todo'),
(84, 17, 'Client-Side Implementation', 'Member 33', '2026-06-25', 0, 'Todo'),
(85, 17, 'Final Review', 'Member 39', '2026-06-30', 0, 'Todo'),
(86, 18, 'Project Kickoff & Setup', 'Member 37', '2026-06-05', 0, 'Todo'),
(87, 18, 'Authentication Module', 'Member 34', '2026-06-15', 0, 'Todo'),
(88, 18, 'Dashboard Analytics', 'Member 31', '2026-06-20', 0, 'Todo'),
(89, 18, 'Security Auditing', 'Member 35', '2026-06-25', 0, 'Todo'),
(90, 18, 'Production Release', 'Member 32', '2026-06-30', 0, 'Todo'),
(91, 19, 'System Blueprint Creation', 'Member 40', '2026-06-05', 0, 'Todo'),
(92, 19, 'Data Migration', 'Member 36', '2026-06-15', 0, 'Todo'),
(93, 19, 'Third-party Integrations', 'Member 39', '2026-06-20', 0, 'Todo'),
(94, 19, 'User Acceptance Testing', 'Member 33', '2026-06-25', 0, 'Todo'),
(95, 19, 'Handover Preparation', 'Member 38', '2026-06-30', 0, 'Todo'),
(96, 20, 'Scope Definition', 'Member 32', '2026-06-05', 0, 'Todo'),
(97, 20, 'Microservices Architecture', 'Member 35', '2026-06-15', 0, 'Todo'),
(98, 20, 'State Management', 'Member 37', '2026-06-20', 0, 'Todo'),
(99, 20, 'Bug Fixing Phase', 'Member 34', '2026-06-25', 0, 'Todo'),
(100, 20, 'Post-Launch Support Plan', 'Member 31', '2026-06-30', 0, 'Todo');

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
(1, 'Team - 1', '2026-05-22 17:13:44', 'Core Full-Stack and Framework Development Team'),
(2, 'Team - 2', '2026-05-22 17:13:44', 'UI/UX Design and Frontend Implementation Team'),
(3, 'Team - 3', '2026-05-22 17:13:44', 'Data Integration and Backend Systems Team'),
(4, 'Team - 4', '2026-05-22 17:13:44', 'Quality Assurance and Desktop Automation Team');

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
(1, '10000', 'Admin One', 'admin1', 'Admin1', 'admin', NULL, '2026-05-22 10:44:02', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(2, '10001', 'Admin Two', 'admin2', 'Admin2', 'admin', NULL, '2026-05-22 10:44:02', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(3, '10002', 'Admin Three', 'admin3', 'Admin3', 'admin', NULL, '2026-05-22 10:44:02', 'Office', NULL, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(4, '10003', 'Leader One', 'leader1', 'Leader1', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(5, '10004', 'Leader Two', 'leader2', 'Leader2', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(6, '10005', 'Leader Three', 'leader3', 'Leader3', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(7, '10006', 'Leader Four', 'leader4', 'Leader4', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(8, '10007', 'Leader Five', 'leader5', 'Leader5', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(9, '10008', 'Leader Six', 'leader6', 'Leader6', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(10, '10009', 'Leader Seven', 'leader7', 'Leader7', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(11, '10010', 'Leader Eight', 'leader8', 'Leader8', 'leader', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(12, '10011', 'Member 1', 'member1', 'Member1', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(13, '10012', 'Member 2', 'member2', 'Member2', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(14, '10013', 'Member 3', 'member3', 'Member3', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(15, '10014', 'Member 4', 'member4', 'Member4', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(16, '10015', 'Member 5', 'member5', 'Member5', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(17, '10016', 'Member 6', 'member6', 'Member6', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(18, '10017', 'Member 7', 'member7', 'Member7', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(19, '10018', 'Member 8', 'member8', 'Member8', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(20, '10019', 'Member 9', 'member9', 'Member9', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(21, '10020', 'Member 10', 'member10', 'Member10', 'member', NULL, '2026-05-22 10:44:02', 'Office', 1, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(22, '10021', 'Member 11', 'member11', 'Member11', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(23, '10022', 'Member 12', 'member12', 'Member12', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(24, '10023', 'Member 13', 'member13', 'Member13', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(25, '10024', 'Member 14', 'member14', 'Member14', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(26, '10025', 'Member 15', 'member15', 'Member15', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(27, '10026', 'Member 16', 'member16', 'Member16', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(28, '10027', 'Member 17', 'member17', 'Member17', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(29, '10028', 'Member 18', 'member18', 'Member18', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(30, '10029', 'Member 19', 'member19', 'Member19', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(31, '10030', 'Member 20', 'member20', 'Member20', 'member', NULL, '2026-05-22 10:44:02', 'Office', 2, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(32, '10031', 'Member 21', 'member21', 'Member21', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(33, '10032', 'Member 22', 'member22', 'Member22', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(34, '10033', 'Member 23', 'member23', 'Member23', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(35, '10034', 'Member 24', 'member24', 'Member24', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(36, '10035', 'Member 25', 'member25', 'Member25', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(37, '10036', 'Member 26', 'member26', 'Member26', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(38, '10037', 'Member 27', 'member27', 'Member27', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(39, '10038', 'Member 28', 'member28', 'Member28', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(40, '10039', 'Member 29', 'member29', 'Member29', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(41, '10040', 'Member 30', 'member30', 'Member30', 'member', NULL, '2026-05-22 10:44:02', 'Office', 3, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(42, '10041', 'Member 31', 'member31', 'Member31', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(43, '10042', 'Member 32', 'member32', 'Member32', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(44, '10043', 'Member 33', 'member33', 'Member33', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(45, '10044', 'Member 34', 'member34', 'Member34', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(46, '10045', 'Member 35', 'member35', 'Member35', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(47, '10046', 'Member 36', 'member36', 'Member36', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(48, '10047', 'Member 37', 'member37', 'Member37', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(49, '10048', 'Member 38', 'member38', 'Member38', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(50, '10049', 'Member 39', 'member39', 'Member39', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL),
(51, '10050', 'Member 40', 'member40', 'Member40', 'member', NULL, '2026-05-22 10:44:02', 'Office', 4, 'offline', NULL, 0, 0, 0, 'Office', NULL);

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
(1, 12, 4, '2026-05-01', 'Office'),
(2, 13, 4, '2026-05-01', 'WFH'),
(3, 14, 4, '2026-05-01', 'Office'),
(4, 15, 4, '2026-05-01', 'WFH'),
(5, 16, 4, '2026-05-01', 'Office'),
(6, 17, 4, '2026-05-01', 'Office'),
(7, 18, 4, '2026-05-01', 'WFH'),
(8, 19, 4, '2026-05-01', 'Office'),
(9, 20, 4, '2026-05-01', 'Office'),
(10, 21, 4, '2026-05-01', 'WFH'),
(11, 12, 4, '2026-05-04', 'Office'),
(12, 13, 4, '2026-05-04', 'Office'),
(13, 14, 4, '2026-05-04', 'Office'),
(14, 15, 4, '2026-05-04', 'WFH'),
(15, 16, 4, '2026-05-04', 'Office'),
(16, 17, 4, '2026-05-04', 'WFH'),
(17, 18, 4, '2026-05-04', 'WFH'),
(18, 19, 4, '2026-05-04', 'WFH'),
(19, 20, 4, '2026-05-04', 'Office'),
(20, 21, 4, '2026-05-04', 'WFH'),
(21, 12, 4, '2026-05-05', 'WFH'),
(22, 13, 4, '2026-05-05', 'WFH'),
(23, 14, 4, '2026-05-05', 'WFH'),
(24, 15, 4, '2026-05-05', 'Office'),
(25, 16, 4, '2026-05-05', 'WFH'),
(26, 17, 4, '2026-05-05', 'WFH'),
(27, 18, 4, '2026-05-05', 'Office'),
(28, 19, 4, '2026-05-05', 'WFH'),
(29, 20, 4, '2026-05-05', 'Office'),
(30, 21, 4, '2026-05-05', 'WFH'),
(31, 12, 4, '2026-05-06', 'Office'),
(32, 13, 4, '2026-05-06', 'WFH'),
(33, 14, 4, '2026-05-06', 'WFH'),
(34, 15, 4, '2026-05-06', 'Office'),
(35, 16, 4, '2026-05-06', 'WFH'),
(36, 17, 4, '2026-05-06', 'WFH'),
(37, 18, 4, '2026-05-06', 'Office'),
(38, 19, 4, '2026-05-06', 'Office'),
(39, 20, 4, '2026-05-06', 'WFH'),
(40, 21, 4, '2026-05-06', 'Office'),
(41, 12, 4, '2026-05-07', 'Office'),
(42, 13, 4, '2026-05-07', 'Office'),
(43, 14, 4, '2026-05-07', 'Office'),
(44, 15, 4, '2026-05-07', 'Office'),
(45, 16, 4, '2026-05-07', 'WFH'),
(46, 17, 4, '2026-05-07', 'Office'),
(47, 18, 4, '2026-05-07', 'WFH'),
(48, 19, 4, '2026-05-07', 'Office'),
(49, 20, 4, '2026-05-07', 'WFH'),
(50, 21, 4, '2026-05-07', 'WFH'),
(51, 12, 4, '2026-05-08', 'Office'),
(52, 13, 4, '2026-05-08', 'Office'),
(53, 14, 4, '2026-05-08', 'Office'),
(54, 15, 4, '2026-05-08', 'WFH'),
(55, 16, 4, '2026-05-08', 'WFH'),
(56, 17, 4, '2026-05-08', 'WFH'),
(57, 18, 4, '2026-05-08', 'Office'),
(58, 19, 4, '2026-05-08', 'Office'),
(59, 20, 4, '2026-05-08', 'Office'),
(60, 21, 4, '2026-05-08', 'WFH'),
(61, 12, 4, '2026-05-11', 'Office'),
(62, 13, 4, '2026-05-11', 'WFH'),
(63, 14, 4, '2026-05-11', 'WFH'),
(64, 15, 4, '2026-05-11', 'WFH'),
(65, 16, 4, '2026-05-11', 'WFH'),
(66, 17, 4, '2026-05-11', 'Office'),
(67, 18, 4, '2026-05-11', 'Office'),
(68, 19, 4, '2026-05-11', 'Office'),
(69, 20, 4, '2026-05-11', 'Office'),
(70, 21, 4, '2026-05-11', 'WFH'),
(71, 12, 4, '2026-05-12', 'Office'),
(72, 13, 4, '2026-05-12', 'Office'),
(73, 14, 4, '2026-05-12', 'Office'),
(74, 15, 4, '2026-05-12', 'WFH'),
(75, 16, 4, '2026-05-12', 'WFH'),
(76, 17, 4, '2026-05-12', 'Office'),
(77, 18, 4, '2026-05-12', 'Office'),
(78, 19, 4, '2026-05-12', 'WFH'),
(79, 20, 4, '2026-05-12', 'Office'),
(80, 21, 4, '2026-05-12', 'Office'),
(81, 12, 4, '2026-05-13', 'Office'),
(82, 13, 4, '2026-05-13', 'WFH'),
(83, 14, 4, '2026-05-13', 'WFH'),
(84, 15, 4, '2026-05-13', 'WFH'),
(85, 16, 4, '2026-05-13', 'WFH'),
(86, 17, 4, '2026-05-13', 'Office'),
(87, 18, 4, '2026-05-13', 'WFH'),
(88, 19, 4, '2026-05-13', 'Office'),
(89, 20, 4, '2026-05-13', 'Office'),
(90, 21, 4, '2026-05-13', 'WFH'),
(91, 12, 4, '2026-05-14', 'Office'),
(92, 13, 4, '2026-05-14', 'Office'),
(93, 14, 4, '2026-05-14', 'WFH'),
(94, 15, 4, '2026-05-14', 'WFH'),
(95, 16, 4, '2026-05-14', 'WFH'),
(96, 17, 4, '2026-05-14', 'Office'),
(97, 18, 4, '2026-05-14', 'Office'),
(98, 19, 4, '2026-05-14', 'WFH'),
(99, 20, 4, '2026-05-14', 'Office'),
(100, 21, 4, '2026-05-14', 'WFH'),
(101, 12, 4, '2026-05-15', 'Office'),
(102, 13, 4, '2026-05-15', 'Office'),
(103, 14, 4, '2026-05-15', 'Office'),
(104, 15, 4, '2026-05-15', 'WFH'),
(105, 16, 4, '2026-05-15', 'WFH'),
(106, 17, 4, '2026-05-15', 'Office'),
(107, 18, 4, '2026-05-15', 'Office'),
(108, 19, 4, '2026-05-15', 'WFH'),
(109, 20, 4, '2026-05-15', 'WFH'),
(110, 21, 4, '2026-05-15', 'Office'),
(111, 12, 4, '2026-05-18', 'WFH'),
(112, 13, 4, '2026-05-18', 'WFH'),
(113, 14, 4, '2026-05-18', 'Office'),
(114, 15, 4, '2026-05-18', 'Office'),
(115, 16, 4, '2026-05-18', 'WFH'),
(116, 17, 4, '2026-05-18', 'Office'),
(117, 18, 4, '2026-05-18', 'Office'),
(118, 19, 4, '2026-05-18', 'WFH'),
(119, 20, 4, '2026-05-18', 'Office'),
(120, 21, 4, '2026-05-18', 'WFH'),
(121, 12, 4, '2026-05-19', 'Office'),
(122, 13, 4, '2026-05-19', 'WFH'),
(123, 14, 4, '2026-05-19', 'Office'),
(124, 15, 4, '2026-05-19', 'WFH'),
(125, 16, 4, '2026-05-19', 'Office'),
(126, 17, 4, '2026-05-19', 'WFH'),
(127, 18, 4, '2026-05-19', 'Office'),
(128, 19, 4, '2026-05-19', 'Office'),
(129, 20, 4, '2026-05-19', 'Office'),
(130, 21, 4, '2026-05-19', 'WFH'),
(131, 12, 4, '2026-05-20', 'WFH'),
(132, 13, 4, '2026-05-20', 'WFH'),
(133, 14, 4, '2026-05-20', 'Office'),
(134, 15, 4, '2026-05-20', 'Office'),
(135, 16, 4, '2026-05-20', 'Office'),
(136, 17, 4, '2026-05-20', 'Office'),
(137, 18, 4, '2026-05-20', 'Office'),
(138, 19, 4, '2026-05-20', 'Office'),
(139, 20, 4, '2026-05-20', 'Office'),
(140, 21, 4, '2026-05-20', 'Office'),
(141, 12, 4, '2026-05-21', 'WFH'),
(142, 13, 4, '2026-05-21', 'WFH'),
(143, 14, 4, '2026-05-21', 'WFH'),
(144, 15, 4, '2026-05-21', 'WFH'),
(145, 16, 4, '2026-05-21', 'WFH'),
(146, 17, 4, '2026-05-21', 'Office'),
(147, 18, 4, '2026-05-21', 'WFH'),
(148, 19, 4, '2026-05-21', 'Office'),
(149, 20, 4, '2026-05-21', 'WFH'),
(150, 21, 4, '2026-05-21', 'WFH'),
(151, 12, 4, '2026-05-22', 'WFH'),
(152, 13, 4, '2026-05-22', 'Office'),
(153, 14, 4, '2026-05-22', 'Office'),
(154, 15, 4, '2026-05-22', 'WFH'),
(155, 16, 4, '2026-05-22', 'Office'),
(156, 17, 4, '2026-05-22', 'WFH'),
(157, 18, 4, '2026-05-22', 'Office'),
(158, 19, 4, '2026-05-22', 'Office'),
(159, 20, 4, '2026-05-22', 'WFH'),
(160, 21, 4, '2026-05-22', 'WFH'),
(161, 12, 4, '2026-05-25', 'Office'),
(162, 13, 4, '2026-05-25', 'WFH'),
(163, 14, 4, '2026-05-25', 'Office'),
(164, 15, 4, '2026-05-25', 'WFH'),
(165, 16, 4, '2026-05-25', 'Office'),
(166, 17, 4, '2026-05-25', 'Office'),
(167, 18, 4, '2026-05-25', 'WFH'),
(168, 19, 4, '2026-05-25', 'Office'),
(169, 20, 4, '2026-05-25', 'Office'),
(170, 21, 4, '2026-05-25', 'Office'),
(171, 12, 4, '2026-05-26', 'Office'),
(172, 13, 4, '2026-05-26', 'Office'),
(173, 14, 4, '2026-05-26', 'WFH'),
(174, 15, 4, '2026-05-26', 'WFH'),
(175, 16, 4, '2026-05-26', 'WFH'),
(176, 17, 4, '2026-05-26', 'Office'),
(177, 18, 4, '2026-05-26', 'Office'),
(178, 19, 4, '2026-05-26', 'Office'),
(179, 20, 4, '2026-05-26', 'Office'),
(180, 21, 4, '2026-05-26', 'WFH'),
(181, 12, 4, '2026-05-27', 'WFH'),
(182, 13, 4, '2026-05-27', 'Office'),
(183, 14, 4, '2026-05-27', 'WFH'),
(184, 15, 4, '2026-05-27', 'Office'),
(185, 16, 4, '2026-05-27', 'WFH'),
(186, 17, 4, '2026-05-27', 'WFH'),
(187, 18, 4, '2026-05-27', 'Office'),
(188, 19, 4, '2026-05-27', 'Office'),
(189, 20, 4, '2026-05-27', 'WFH'),
(190, 21, 4, '2026-05-27', 'Office'),
(191, 12, 4, '2026-05-28', 'Office'),
(192, 13, 4, '2026-05-28', 'Office'),
(193, 14, 4, '2026-05-28', 'WFH'),
(194, 15, 4, '2026-05-28', 'WFH'),
(195, 16, 4, '2026-05-28', 'WFH'),
(196, 17, 4, '2026-05-28', 'Office'),
(197, 18, 4, '2026-05-28', 'Office'),
(198, 19, 4, '2026-05-28', 'WFH'),
(199, 20, 4, '2026-05-28', 'Office'),
(200, 21, 4, '2026-05-28', 'Office'),
(201, 12, 4, '2026-05-29', 'WFH'),
(202, 13, 4, '2026-05-29', 'WFH'),
(203, 14, 4, '2026-05-29', 'Office'),
(204, 15, 4, '2026-05-29', 'WFH'),
(205, 16, 4, '2026-05-29', 'WFH'),
(206, 17, 4, '2026-05-29', 'Office'),
(207, 18, 4, '2026-05-29', 'WFH'),
(208, 19, 4, '2026-05-29', 'Office'),
(209, 20, 4, '2026-05-29', 'WFH'),
(210, 21, 4, '2026-05-29', 'WFH'),
(211, 22, 6, '2026-05-01', 'WFH'),
(212, 23, 6, '2026-05-01', 'WFH'),
(213, 24, 6, '2026-05-01', 'WFH'),
(214, 25, 6, '2026-05-01', 'Office'),
(215, 26, 6, '2026-05-01', 'WFH'),
(216, 27, 6, '2026-05-01', 'WFH'),
(217, 28, 6, '2026-05-01', 'Office'),
(218, 29, 6, '2026-05-01', 'WFH'),
(219, 30, 6, '2026-05-01', 'WFH'),
(220, 31, 6, '2026-05-01', 'WFH'),
(221, 22, 6, '2026-05-04', 'Office'),
(222, 23, 6, '2026-05-04', 'Office'),
(223, 24, 6, '2026-05-04', 'WFH'),
(224, 25, 6, '2026-05-04', 'Office'),
(225, 26, 6, '2026-05-04', 'Office'),
(226, 27, 6, '2026-05-04', 'Office'),
(227, 28, 6, '2026-05-04', 'Office'),
(228, 29, 6, '2026-05-04', 'WFH'),
(229, 30, 6, '2026-05-04', 'Office'),
(230, 31, 6, '2026-05-04', 'WFH'),
(231, 22, 6, '2026-05-05', 'Office'),
(232, 23, 6, '2026-05-05', 'Office'),
(233, 24, 6, '2026-05-05', 'Office'),
(234, 25, 6, '2026-05-05', 'Office'),
(235, 26, 6, '2026-05-05', 'Office'),
(236, 27, 6, '2026-05-05', 'Office'),
(237, 28, 6, '2026-05-05', 'Office'),
(238, 29, 6, '2026-05-05', 'WFH'),
(239, 30, 6, '2026-05-05', 'Office'),
(240, 31, 6, '2026-05-05', 'WFH'),
(241, 22, 6, '2026-05-06', 'WFH'),
(242, 23, 6, '2026-05-06', 'Office'),
(243, 24, 6, '2026-05-06', 'WFH'),
(244, 25, 6, '2026-05-06', 'Office'),
(245, 26, 6, '2026-05-06', 'WFH'),
(246, 27, 6, '2026-05-06', 'WFH'),
(247, 28, 6, '2026-05-06', 'Office'),
(248, 29, 6, '2026-05-06', 'WFH'),
(249, 30, 6, '2026-05-06', 'Office'),
(250, 31, 6, '2026-05-06', 'Office'),
(251, 22, 6, '2026-05-07', 'WFH'),
(252, 23, 6, '2026-05-07', 'WFH'),
(253, 24, 6, '2026-05-07', 'Office'),
(254, 25, 6, '2026-05-07', 'WFH'),
(255, 26, 6, '2026-05-07', 'WFH'),
(256, 27, 6, '2026-05-07', 'WFH'),
(257, 28, 6, '2026-05-07', 'Office'),
(258, 29, 6, '2026-05-07', 'WFH'),
(259, 30, 6, '2026-05-07', 'WFH'),
(260, 31, 6, '2026-05-07', 'Office'),
(261, 22, 6, '2026-05-08', 'WFH'),
(262, 23, 6, '2026-05-08', 'WFH'),
(263, 24, 6, '2026-05-08', 'Office'),
(264, 25, 6, '2026-05-08', 'WFH'),
(265, 26, 6, '2026-05-08', 'WFH'),
(266, 27, 6, '2026-05-08', 'Office'),
(267, 28, 6, '2026-05-08', 'Office'),
(268, 29, 6, '2026-05-08', 'Office'),
(269, 30, 6, '2026-05-08', 'Office'),
(270, 31, 6, '2026-05-08', 'WFH'),
(271, 22, 6, '2026-05-11', 'WFH'),
(272, 23, 6, '2026-05-11', 'WFH'),
(273, 24, 6, '2026-05-11', 'Office'),
(274, 25, 6, '2026-05-11', 'WFH'),
(275, 26, 6, '2026-05-11', 'WFH'),
(276, 27, 6, '2026-05-11', 'Office'),
(277, 28, 6, '2026-05-11', 'Office'),
(278, 29, 6, '2026-05-11', 'WFH'),
(279, 30, 6, '2026-05-11', 'Office'),
(280, 31, 6, '2026-05-11', 'Office'),
(281, 22, 6, '2026-05-12', 'WFH'),
(282, 23, 6, '2026-05-12', 'Office'),
(283, 24, 6, '2026-05-12', 'WFH'),
(284, 25, 6, '2026-05-12', 'WFH'),
(285, 26, 6, '2026-05-12', 'Office'),
(286, 27, 6, '2026-05-12', 'WFH'),
(287, 28, 6, '2026-05-12', 'WFH'),
(288, 29, 6, '2026-05-12', 'WFH'),
(289, 30, 6, '2026-05-12', 'Office'),
(290, 31, 6, '2026-05-12', 'Office'),
(291, 22, 6, '2026-05-13', 'WFH'),
(292, 23, 6, '2026-05-13', 'Office'),
(293, 24, 6, '2026-05-13', 'Office'),
(294, 25, 6, '2026-05-13', 'Office'),
(295, 26, 6, '2026-05-13', 'WFH'),
(296, 27, 6, '2026-05-13', 'WFH'),
(297, 28, 6, '2026-05-13', 'WFH'),
(298, 29, 6, '2026-05-13', 'WFH'),
(299, 30, 6, '2026-05-13', 'WFH'),
(300, 31, 6, '2026-05-13', 'WFH'),
(301, 22, 6, '2026-05-14', 'WFH'),
(302, 23, 6, '2026-05-14', 'Office'),
(303, 24, 6, '2026-05-14', 'Office'),
(304, 25, 6, '2026-05-14', 'WFH'),
(305, 26, 6, '2026-05-14', 'Office'),
(306, 27, 6, '2026-05-14', 'WFH'),
(307, 28, 6, '2026-05-14', 'Office'),
(308, 29, 6, '2026-05-14', 'Office'),
(309, 30, 6, '2026-05-14', 'Office'),
(310, 31, 6, '2026-05-14', 'Office'),
(311, 22, 6, '2026-05-15', 'Office'),
(312, 23, 6, '2026-05-15', 'Office'),
(313, 24, 6, '2026-05-15', 'WFH'),
(314, 25, 6, '2026-05-15', 'WFH'),
(315, 26, 6, '2026-05-15', 'Office'),
(316, 27, 6, '2026-05-15', 'WFH'),
(317, 28, 6, '2026-05-15', 'Office'),
(318, 29, 6, '2026-05-15', 'WFH'),
(319, 30, 6, '2026-05-15', 'Office'),
(320, 31, 6, '2026-05-15', 'Office'),
(321, 22, 6, '2026-05-18', 'WFH'),
(322, 23, 6, '2026-05-18', 'Office'),
(323, 24, 6, '2026-05-18', 'WFH'),
(324, 25, 6, '2026-05-18', 'Office'),
(325, 26, 6, '2026-05-18', 'WFH'),
(326, 27, 6, '2026-05-18', 'WFH'),
(327, 28, 6, '2026-05-18', 'WFH'),
(328, 29, 6, '2026-05-18', 'WFH'),
(329, 30, 6, '2026-05-18', 'WFH'),
(330, 31, 6, '2026-05-18', 'Office'),
(331, 22, 6, '2026-05-19', 'Office'),
(332, 23, 6, '2026-05-19', 'WFH'),
(333, 24, 6, '2026-05-19', 'Office'),
(334, 25, 6, '2026-05-19', 'Office'),
(335, 26, 6, '2026-05-19', 'Office'),
(336, 27, 6, '2026-05-19', 'WFH'),
(337, 28, 6, '2026-05-19', 'WFH'),
(338, 29, 6, '2026-05-19', 'WFH'),
(339, 30, 6, '2026-05-19', 'WFH'),
(340, 31, 6, '2026-05-19', 'Office'),
(341, 22, 6, '2026-05-20', 'Office'),
(342, 23, 6, '2026-05-20', 'Office'),
(343, 24, 6, '2026-05-20', 'Office'),
(344, 25, 6, '2026-05-20', 'WFH'),
(345, 26, 6, '2026-05-20', 'WFH'),
(346, 27, 6, '2026-05-20', 'Office'),
(347, 28, 6, '2026-05-20', 'WFH'),
(348, 29, 6, '2026-05-20', 'WFH'),
(349, 30, 6, '2026-05-20', 'Office'),
(350, 31, 6, '2026-05-20', 'WFH'),
(351, 22, 6, '2026-05-21', 'Office'),
(352, 23, 6, '2026-05-21', 'Office'),
(353, 24, 6, '2026-05-21', 'WFH'),
(354, 25, 6, '2026-05-21', 'WFH'),
(355, 26, 6, '2026-05-21', 'WFH'),
(356, 27, 6, '2026-05-21', 'WFH'),
(357, 28, 6, '2026-05-21', 'WFH'),
(358, 29, 6, '2026-05-21', 'WFH'),
(359, 30, 6, '2026-05-21', 'WFH'),
(360, 31, 6, '2026-05-21', 'Office'),
(361, 22, 6, '2026-05-22', 'Office'),
(362, 23, 6, '2026-05-22', 'Office'),
(363, 24, 6, '2026-05-22', 'Office'),
(364, 25, 6, '2026-05-22', 'Office'),
(365, 26, 6, '2026-05-22', 'WFH'),
(366, 27, 6, '2026-05-22', 'WFH'),
(367, 28, 6, '2026-05-22', 'Office'),
(368, 29, 6, '2026-05-22', 'Office'),
(369, 30, 6, '2026-05-22', 'WFH'),
(370, 31, 6, '2026-05-22', 'Office'),
(371, 22, 6, '2026-05-25', 'Office'),
(372, 23, 6, '2026-05-25', 'Office'),
(373, 24, 6, '2026-05-25', 'WFH'),
(374, 25, 6, '2026-05-25', 'Office'),
(375, 26, 6, '2026-05-25', 'WFH'),
(376, 27, 6, '2026-05-25', 'Office'),
(377, 28, 6, '2026-05-25', 'WFH'),
(378, 29, 6, '2026-05-25', 'Office'),
(379, 30, 6, '2026-05-25', 'Office'),
(380, 31, 6, '2026-05-25', 'Office'),
(381, 22, 6, '2026-05-26', 'Office'),
(382, 23, 6, '2026-05-26', 'Office'),
(383, 24, 6, '2026-05-26', 'WFH'),
(384, 25, 6, '2026-05-26', 'Office'),
(385, 26, 6, '2026-05-26', 'WFH'),
(386, 27, 6, '2026-05-26', 'WFH'),
(387, 28, 6, '2026-05-26', 'Office'),
(388, 29, 6, '2026-05-26', 'Office'),
(389, 30, 6, '2026-05-26', 'WFH'),
(390, 31, 6, '2026-05-26', 'Office'),
(391, 22, 6, '2026-05-27', 'WFH'),
(392, 23, 6, '2026-05-27', 'Office'),
(393, 24, 6, '2026-05-27', 'WFH'),
(394, 25, 6, '2026-05-27', 'Office'),
(395, 26, 6, '2026-05-27', 'Office'),
(396, 27, 6, '2026-05-27', 'Office'),
(397, 28, 6, '2026-05-27', 'WFH'),
(398, 29, 6, '2026-05-27', 'WFH'),
(399, 30, 6, '2026-05-27', 'WFH'),
(400, 31, 6, '2026-05-27', 'Office'),
(401, 22, 6, '2026-05-28', 'Office'),
(402, 23, 6, '2026-05-28', 'Office'),
(403, 24, 6, '2026-05-28', 'Office'),
(404, 25, 6, '2026-05-28', 'Office'),
(405, 26, 6, '2026-05-28', 'Office'),
(406, 27, 6, '2026-05-28', 'WFH'),
(407, 28, 6, '2026-05-28', 'WFH'),
(408, 29, 6, '2026-05-28', 'WFH'),
(409, 30, 6, '2026-05-28', 'WFH'),
(410, 31, 6, '2026-05-28', 'WFH'),
(411, 22, 6, '2026-05-29', 'WFH'),
(412, 23, 6, '2026-05-29', 'WFH'),
(413, 24, 6, '2026-05-29', 'WFH'),
(414, 25, 6, '2026-05-29', 'WFH'),
(415, 26, 6, '2026-05-29', 'Office'),
(416, 27, 6, '2026-05-29', 'WFH'),
(417, 28, 6, '2026-05-29', 'Office'),
(418, 29, 6, '2026-05-29', 'WFH'),
(419, 30, 6, '2026-05-29', 'Office'),
(420, 31, 6, '2026-05-29', 'Office'),
(421, 32, 8, '2026-05-01', 'Office'),
(422, 33, 8, '2026-05-01', 'Office'),
(423, 34, 8, '2026-05-01', 'WFH'),
(424, 35, 8, '2026-05-01', 'Office'),
(425, 36, 8, '2026-05-01', 'WFH'),
(426, 37, 8, '2026-05-01', 'WFH'),
(427, 38, 8, '2026-05-01', 'WFH'),
(428, 39, 8, '2026-05-01', 'WFH'),
(429, 40, 8, '2026-05-01', 'WFH'),
(430, 41, 8, '2026-05-01', 'WFH'),
(431, 32, 8, '2026-05-04', 'Office'),
(432, 33, 8, '2026-05-04', 'WFH'),
(433, 34, 8, '2026-05-04', 'Office'),
(434, 35, 8, '2026-05-04', 'Office'),
(435, 36, 8, '2026-05-04', 'Office'),
(436, 37, 8, '2026-05-04', 'WFH'),
(437, 38, 8, '2026-05-04', 'WFH'),
(438, 39, 8, '2026-05-04', 'WFH'),
(439, 40, 8, '2026-05-04', 'WFH'),
(440, 41, 8, '2026-05-04', 'WFH'),
(441, 32, 8, '2026-05-05', 'Office'),
(442, 33, 8, '2026-05-05', 'WFH'),
(443, 34, 8, '2026-05-05', 'Office'),
(444, 35, 8, '2026-05-05', 'WFH'),
(445, 36, 8, '2026-05-05', 'Office'),
(446, 37, 8, '2026-05-05', 'WFH'),
(447, 38, 8, '2026-05-05', 'Office'),
(448, 39, 8, '2026-05-05', 'Office'),
(449, 40, 8, '2026-05-05', 'Office'),
(450, 41, 8, '2026-05-05', 'WFH'),
(451, 32, 8, '2026-05-06', 'Office'),
(452, 33, 8, '2026-05-06', 'Office'),
(453, 34, 8, '2026-05-06', 'WFH'),
(454, 35, 8, '2026-05-06', 'WFH'),
(455, 36, 8, '2026-05-06', 'WFH'),
(456, 37, 8, '2026-05-06', 'Office'),
(457, 38, 8, '2026-05-06', 'Office'),
(458, 39, 8, '2026-05-06', 'Office'),
(459, 40, 8, '2026-05-06', 'WFH'),
(460, 41, 8, '2026-05-06', 'Office'),
(461, 32, 8, '2026-05-07', 'WFH'),
(462, 33, 8, '2026-05-07', 'WFH'),
(463, 34, 8, '2026-05-07', 'WFH'),
(464, 35, 8, '2026-05-07', 'WFH'),
(465, 36, 8, '2026-05-07', 'WFH'),
(466, 37, 8, '2026-05-07', 'Office'),
(467, 38, 8, '2026-05-07', 'WFH'),
(468, 39, 8, '2026-05-07', 'Office'),
(469, 40, 8, '2026-05-07', 'Office'),
(470, 41, 8, '2026-05-07', 'WFH'),
(471, 32, 8, '2026-05-08', 'Office'),
(472, 33, 8, '2026-05-08', 'WFH'),
(473, 34, 8, '2026-05-08', 'Office'),
(474, 35, 8, '2026-05-08', 'Office'),
(475, 36, 8, '2026-05-08', 'WFH'),
(476, 37, 8, '2026-05-08', 'Office'),
(477, 38, 8, '2026-05-08', 'Office'),
(478, 39, 8, '2026-05-08', 'WFH'),
(479, 40, 8, '2026-05-08', 'Office'),
(480, 41, 8, '2026-05-08', 'WFH'),
(481, 32, 8, '2026-05-11', 'Office'),
(482, 33, 8, '2026-05-11', 'WFH'),
(483, 34, 8, '2026-05-11', 'WFH'),
(484, 35, 8, '2026-05-11', 'WFH'),
(485, 36, 8, '2026-05-11', 'Office'),
(486, 37, 8, '2026-05-11', 'WFH'),
(487, 38, 8, '2026-05-11', 'WFH'),
(488, 39, 8, '2026-05-11', 'Office'),
(489, 40, 8, '2026-05-11', 'Office'),
(490, 41, 8, '2026-05-11', 'WFH'),
(491, 32, 8, '2026-05-12', 'WFH'),
(492, 33, 8, '2026-05-12', 'Office'),
(493, 34, 8, '2026-05-12', 'WFH'),
(494, 35, 8, '2026-05-12', 'Office'),
(495, 36, 8, '2026-05-12', 'Office'),
(496, 37, 8, '2026-05-12', 'WFH'),
(497, 38, 8, '2026-05-12', 'Office'),
(498, 39, 8, '2026-05-12', 'Office'),
(499, 40, 8, '2026-05-12', 'Office'),
(500, 41, 8, '2026-05-12', 'WFH'),
(501, 32, 8, '2026-05-13', 'WFH'),
(502, 33, 8, '2026-05-13', 'Office'),
(503, 34, 8, '2026-05-13', 'WFH'),
(504, 35, 8, '2026-05-13', 'WFH'),
(505, 36, 8, '2026-05-13', 'WFH'),
(506, 37, 8, '2026-05-13', 'Office'),
(507, 38, 8, '2026-05-13', 'WFH'),
(508, 39, 8, '2026-05-13', 'Office'),
(509, 40, 8, '2026-05-13', 'WFH'),
(510, 41, 8, '2026-05-13', 'Office'),
(511, 32, 8, '2026-05-14', 'WFH'),
(512, 33, 8, '2026-05-14', 'WFH'),
(513, 34, 8, '2026-05-14', 'Office'),
(514, 35, 8, '2026-05-14', 'WFH'),
(515, 36, 8, '2026-05-14', 'Office'),
(516, 37, 8, '2026-05-14', 'WFH'),
(517, 38, 8, '2026-05-14', 'WFH'),
(518, 39, 8, '2026-05-14', 'Office'),
(519, 40, 8, '2026-05-14', 'Office'),
(520, 41, 8, '2026-05-14', 'Office'),
(521, 32, 8, '2026-05-15', 'WFH'),
(522, 33, 8, '2026-05-15', 'Office'),
(523, 34, 8, '2026-05-15', 'WFH'),
(524, 35, 8, '2026-05-15', 'WFH'),
(525, 36, 8, '2026-05-15', 'WFH'),
(526, 37, 8, '2026-05-15', 'Office'),
(527, 38, 8, '2026-05-15', 'Office'),
(528, 39, 8, '2026-05-15', 'Office'),
(529, 40, 8, '2026-05-15', 'Office'),
(530, 41, 8, '2026-05-15', 'Office'),
(531, 32, 8, '2026-05-18', 'Office'),
(532, 33, 8, '2026-05-18', 'Office'),
(533, 34, 8, '2026-05-18', 'WFH'),
(534, 35, 8, '2026-05-18', 'WFH'),
(535, 36, 8, '2026-05-18', 'Office'),
(536, 37, 8, '2026-05-18', 'Office'),
(537, 38, 8, '2026-05-18', 'WFH'),
(538, 39, 8, '2026-05-18', 'Office'),
(539, 40, 8, '2026-05-18', 'WFH'),
(540, 41, 8, '2026-05-18', 'WFH'),
(541, 32, 8, '2026-05-19', 'WFH'),
(542, 33, 8, '2026-05-19', 'Office'),
(543, 34, 8, '2026-05-19', 'WFH'),
(544, 35, 8, '2026-05-19', 'Office'),
(545, 36, 8, '2026-05-19', 'Office'),
(546, 37, 8, '2026-05-19', 'WFH'),
(547, 38, 8, '2026-05-19', 'WFH'),
(548, 39, 8, '2026-05-19', 'Office'),
(549, 40, 8, '2026-05-19', 'WFH'),
(550, 41, 8, '2026-05-19', 'WFH'),
(551, 32, 8, '2026-05-20', 'Office'),
(552, 33, 8, '2026-05-20', 'WFH'),
(553, 34, 8, '2026-05-20', 'Office'),
(554, 35, 8, '2026-05-20', 'WFH'),
(555, 36, 8, '2026-05-20', 'Office'),
(556, 37, 8, '2026-05-20', 'WFH'),
(557, 38, 8, '2026-05-20', 'Office'),
(558, 39, 8, '2026-05-20', 'Office'),
(559, 40, 8, '2026-05-20', 'Office'),
(560, 41, 8, '2026-05-20', 'Office'),
(561, 32, 8, '2026-05-21', 'Office'),
(562, 33, 8, '2026-05-21', 'Office'),
(563, 34, 8, '2026-05-21', 'WFH'),
(564, 35, 8, '2026-05-21', 'Office'),
(565, 36, 8, '2026-05-21', 'WFH'),
(566, 37, 8, '2026-05-21', 'WFH'),
(567, 38, 8, '2026-05-21', 'Office'),
(568, 39, 8, '2026-05-21', 'WFH'),
(569, 40, 8, '2026-05-21', 'Office'),
(570, 41, 8, '2026-05-21', 'WFH'),
(571, 32, 8, '2026-05-22', 'Office'),
(572, 33, 8, '2026-05-22', 'WFH'),
(573, 34, 8, '2026-05-22', 'WFH'),
(574, 35, 8, '2026-05-22', 'WFH'),
(575, 36, 8, '2026-05-22', 'WFH'),
(576, 37, 8, '2026-05-22', 'Office'),
(577, 38, 8, '2026-05-22', 'WFH'),
(578, 39, 8, '2026-05-22', 'WFH'),
(579, 40, 8, '2026-05-22', 'Office'),
(580, 41, 8, '2026-05-22', 'Office'),
(581, 32, 8, '2026-05-25', 'WFH'),
(582, 33, 8, '2026-05-25', 'WFH'),
(583, 34, 8, '2026-05-25', 'WFH'),
(584, 35, 8, '2026-05-25', 'WFH'),
(585, 36, 8, '2026-05-25', 'WFH'),
(586, 37, 8, '2026-05-25', 'WFH'),
(587, 38, 8, '2026-05-25', 'Office'),
(588, 39, 8, '2026-05-25', 'WFH'),
(589, 40, 8, '2026-05-25', 'Office'),
(590, 41, 8, '2026-05-25', 'Office'),
(591, 32, 8, '2026-05-26', 'Office'),
(592, 33, 8, '2026-05-26', 'WFH'),
(593, 34, 8, '2026-05-26', 'Office'),
(594, 35, 8, '2026-05-26', 'Office'),
(595, 36, 8, '2026-05-26', 'Office'),
(596, 37, 8, '2026-05-26', 'Office'),
(597, 38, 8, '2026-05-26', 'WFH'),
(598, 39, 8, '2026-05-26', 'Office'),
(599, 40, 8, '2026-05-26', 'Office'),
(600, 41, 8, '2026-05-26', 'WFH'),
(601, 32, 8, '2026-05-27', 'Office'),
(602, 33, 8, '2026-05-27', 'Office'),
(603, 34, 8, '2026-05-27', 'WFH'),
(604, 35, 8, '2026-05-27', 'Office'),
(605, 36, 8, '2026-05-27', 'Office'),
(606, 37, 8, '2026-05-27', 'WFH'),
(607, 38, 8, '2026-05-27', 'WFH'),
(608, 39, 8, '2026-05-27', 'WFH'),
(609, 40, 8, '2026-05-27', 'Office'),
(610, 41, 8, '2026-05-27', 'WFH'),
(611, 32, 8, '2026-05-28', 'Office'),
(612, 33, 8, '2026-05-28', 'Office'),
(613, 34, 8, '2026-05-28', 'WFH'),
(614, 35, 8, '2026-05-28', 'WFH'),
(615, 36, 8, '2026-05-28', 'Office'),
(616, 37, 8, '2026-05-28', 'Office'),
(617, 38, 8, '2026-05-28', 'Office'),
(618, 39, 8, '2026-05-28', 'WFH'),
(619, 40, 8, '2026-05-28', 'Office'),
(620, 41, 8, '2026-05-28', 'Office'),
(621, 32, 8, '2026-05-29', 'Office'),
(622, 33, 8, '2026-05-29', 'Office'),
(623, 34, 8, '2026-05-29', 'WFH'),
(624, 35, 8, '2026-05-29', 'Office'),
(625, 36, 8, '2026-05-29', 'WFH'),
(626, 37, 8, '2026-05-29', 'WFH'),
(627, 38, 8, '2026-05-29', 'WFH'),
(628, 39, 8, '2026-05-29', 'Office'),
(629, 40, 8, '2026-05-29', 'WFH'),
(630, 41, 8, '2026-05-29', 'Office'),
(631, 42, 10, '2026-05-01', 'WFH'),
(632, 43, 10, '2026-05-01', 'WFH'),
(633, 44, 10, '2026-05-01', 'Office'),
(634, 45, 10, '2026-05-01', 'WFH'),
(635, 46, 10, '2026-05-01', 'Office'),
(636, 47, 10, '2026-05-01', 'Office'),
(637, 48, 10, '2026-05-01', 'Office'),
(638, 49, 10, '2026-05-01', 'Office'),
(639, 50, 10, '2026-05-01', 'Office'),
(640, 51, 10, '2026-05-01', 'Office'),
(641, 42, 10, '2026-05-04', 'WFH'),
(642, 43, 10, '2026-05-04', 'WFH'),
(643, 44, 10, '2026-05-04', 'WFH'),
(644, 45, 10, '2026-05-04', 'Office'),
(645, 46, 10, '2026-05-04', 'Office'),
(646, 47, 10, '2026-05-04', 'Office'),
(647, 48, 10, '2026-05-04', 'WFH'),
(648, 49, 10, '2026-05-04', 'Office'),
(649, 50, 10, '2026-05-04', 'WFH'),
(650, 51, 10, '2026-05-04', 'Office'),
(651, 42, 10, '2026-05-05', 'Office'),
(652, 43, 10, '2026-05-05', 'WFH'),
(653, 44, 10, '2026-05-05', 'WFH'),
(654, 45, 10, '2026-05-05', 'WFH'),
(655, 46, 10, '2026-05-05', 'Office'),
(656, 47, 10, '2026-05-05', 'WFH'),
(657, 48, 10, '2026-05-05', 'Office'),
(658, 49, 10, '2026-05-05', 'WFH'),
(659, 50, 10, '2026-05-05', 'Office'),
(660, 51, 10, '2026-05-05', 'WFH'),
(661, 42, 10, '2026-05-06', 'WFH'),
(662, 43, 10, '2026-05-06', 'Office'),
(663, 44, 10, '2026-05-06', 'Office'),
(664, 45, 10, '2026-05-06', 'Office'),
(665, 46, 10, '2026-05-06', 'Office'),
(666, 47, 10, '2026-05-06', 'Office'),
(667, 48, 10, '2026-05-06', 'WFH'),
(668, 49, 10, '2026-05-06', 'Office'),
(669, 50, 10, '2026-05-06', 'Office'),
(670, 51, 10, '2026-05-06', 'WFH'),
(671, 42, 10, '2026-05-07', 'Office'),
(672, 43, 10, '2026-05-07', 'WFH'),
(673, 44, 10, '2026-05-07', 'Office'),
(674, 45, 10, '2026-05-07', 'WFH'),
(675, 46, 10, '2026-05-07', 'Office'),
(676, 47, 10, '2026-05-07', 'WFH'),
(677, 48, 10, '2026-05-07', 'WFH'),
(678, 49, 10, '2026-05-07', 'WFH'),
(679, 50, 10, '2026-05-07', 'WFH'),
(680, 51, 10, '2026-05-07', 'WFH'),
(681, 42, 10, '2026-05-08', 'Office'),
(682, 43, 10, '2026-05-08', 'Office'),
(683, 44, 10, '2026-05-08', 'WFH'),
(684, 45, 10, '2026-05-08', 'Office'),
(685, 46, 10, '2026-05-08', 'Office'),
(686, 47, 10, '2026-05-08', 'Office'),
(687, 48, 10, '2026-05-08', 'WFH'),
(688, 49, 10, '2026-05-08', 'WFH'),
(689, 50, 10, '2026-05-08', 'WFH'),
(690, 51, 10, '2026-05-08', 'Office'),
(691, 42, 10, '2026-05-11', 'WFH'),
(692, 43, 10, '2026-05-11', 'WFH'),
(693, 44, 10, '2026-05-11', 'Office'),
(694, 45, 10, '2026-05-11', 'Office'),
(695, 46, 10, '2026-05-11', 'WFH'),
(696, 47, 10, '2026-05-11', 'WFH'),
(697, 48, 10, '2026-05-11', 'Office'),
(698, 49, 10, '2026-05-11', 'Office'),
(699, 50, 10, '2026-05-11', 'WFH'),
(700, 51, 10, '2026-05-11', 'Office'),
(701, 42, 10, '2026-05-12', 'Office'),
(702, 43, 10, '2026-05-12', 'WFH'),
(703, 44, 10, '2026-05-12', 'WFH'),
(704, 45, 10, '2026-05-12', 'WFH'),
(705, 46, 10, '2026-05-12', 'WFH'),
(706, 47, 10, '2026-05-12', 'Office'),
(707, 48, 10, '2026-05-12', 'WFH'),
(708, 49, 10, '2026-05-12', 'Office'),
(709, 50, 10, '2026-05-12', 'WFH'),
(710, 51, 10, '2026-05-12', 'Office'),
(711, 42, 10, '2026-05-13', 'Office'),
(712, 43, 10, '2026-05-13', 'Office'),
(713, 44, 10, '2026-05-13', 'WFH'),
(714, 45, 10, '2026-05-13', 'Office'),
(715, 46, 10, '2026-05-13', 'Office'),
(716, 47, 10, '2026-05-13', 'Office'),
(717, 48, 10, '2026-05-13', 'Office'),
(718, 49, 10, '2026-05-13', 'Office'),
(719, 50, 10, '2026-05-13', 'Office'),
(720, 51, 10, '2026-05-13', 'Office'),
(721, 42, 10, '2026-05-14', 'WFH'),
(722, 43, 10, '2026-05-14', 'Office'),
(723, 44, 10, '2026-05-14', 'WFH'),
(724, 45, 10, '2026-05-14', 'WFH'),
(725, 46, 10, '2026-05-14', 'WFH'),
(726, 47, 10, '2026-05-14', 'WFH'),
(727, 48, 10, '2026-05-14', 'WFH'),
(728, 49, 10, '2026-05-14', 'Office'),
(729, 50, 10, '2026-05-14', 'Office'),
(730, 51, 10, '2026-05-14', 'Office'),
(731, 42, 10, '2026-05-15', 'Office'),
(732, 43, 10, '2026-05-15', 'WFH'),
(733, 44, 10, '2026-05-15', 'Office'),
(734, 45, 10, '2026-05-15', 'Office'),
(735, 46, 10, '2026-05-15', 'WFH'),
(736, 47, 10, '2026-05-15', 'Office'),
(737, 48, 10, '2026-05-15', 'Office'),
(738, 49, 10, '2026-05-15', 'Office'),
(739, 50, 10, '2026-05-15', 'WFH'),
(740, 51, 10, '2026-05-15', 'WFH'),
(741, 42, 10, '2026-05-18', 'Office'),
(742, 43, 10, '2026-05-18', 'WFH'),
(743, 44, 10, '2026-05-18', 'Office'),
(744, 45, 10, '2026-05-18', 'Office'),
(745, 46, 10, '2026-05-18', 'WFH'),
(746, 47, 10, '2026-05-18', 'Office'),
(747, 48, 10, '2026-05-18', 'WFH'),
(748, 49, 10, '2026-05-18', 'WFH'),
(749, 50, 10, '2026-05-18', 'Office'),
(750, 51, 10, '2026-05-18', 'WFH'),
(751, 42, 10, '2026-05-19', 'WFH'),
(752, 43, 10, '2026-05-19', 'Office'),
(753, 44, 10, '2026-05-19', 'WFH'),
(754, 45, 10, '2026-05-19', 'WFH'),
(755, 46, 10, '2026-05-19', 'WFH'),
(756, 47, 10, '2026-05-19', 'WFH'),
(757, 48, 10, '2026-05-19', 'Office'),
(758, 49, 10, '2026-05-19', 'WFH'),
(759, 50, 10, '2026-05-19', 'WFH'),
(760, 51, 10, '2026-05-19', 'Office'),
(761, 42, 10, '2026-05-20', 'WFH'),
(762, 43, 10, '2026-05-20', 'WFH'),
(763, 44, 10, '2026-05-20', 'WFH'),
(764, 45, 10, '2026-05-20', 'Office'),
(765, 46, 10, '2026-05-20', 'WFH'),
(766, 47, 10, '2026-05-20', 'Office'),
(767, 48, 10, '2026-05-20', 'Office'),
(768, 49, 10, '2026-05-20', 'Office'),
(769, 50, 10, '2026-05-20', 'WFH'),
(770, 51, 10, '2026-05-20', 'Office'),
(771, 42, 10, '2026-05-21', 'WFH'),
(772, 43, 10, '2026-05-21', 'WFH'),
(773, 44, 10, '2026-05-21', 'WFH'),
(774, 45, 10, '2026-05-21', 'Office'),
(775, 46, 10, '2026-05-21', 'Office'),
(776, 47, 10, '2026-05-21', 'Office'),
(777, 48, 10, '2026-05-21', 'Office'),
(778, 49, 10, '2026-05-21', 'Office'),
(779, 50, 10, '2026-05-21', 'Office'),
(780, 51, 10, '2026-05-21', 'WFH'),
(781, 42, 10, '2026-05-22', 'WFH'),
(782, 43, 10, '2026-05-22', 'WFH'),
(783, 44, 10, '2026-05-22', 'Office'),
(784, 45, 10, '2026-05-22', 'Office'),
(785, 46, 10, '2026-05-22', 'WFH'),
(786, 47, 10, '2026-05-22', 'WFH'),
(787, 48, 10, '2026-05-22', 'Office'),
(788, 49, 10, '2026-05-22', 'WFH'),
(789, 50, 10, '2026-05-22', 'WFH'),
(790, 51, 10, '2026-05-22', 'Office'),
(791, 42, 10, '2026-05-25', 'Office'),
(792, 43, 10, '2026-05-25', 'WFH'),
(793, 44, 10, '2026-05-25', 'WFH'),
(794, 45, 10, '2026-05-25', 'Office'),
(795, 46, 10, '2026-05-25', 'WFH'),
(796, 47, 10, '2026-05-25', 'WFH'),
(797, 48, 10, '2026-05-25', 'Office'),
(798, 49, 10, '2026-05-25', 'Office'),
(799, 50, 10, '2026-05-25', 'WFH'),
(800, 51, 10, '2026-05-25', 'WFH'),
(801, 42, 10, '2026-05-26', 'WFH'),
(802, 43, 10, '2026-05-26', 'Office'),
(803, 44, 10, '2026-05-26', 'Office'),
(804, 45, 10, '2026-05-26', 'Office'),
(805, 46, 10, '2026-05-26', 'Office'),
(806, 47, 10, '2026-05-26', 'Office'),
(807, 48, 10, '2026-05-26', 'WFH'),
(808, 49, 10, '2026-05-26', 'WFH'),
(809, 50, 10, '2026-05-26', 'WFH'),
(810, 51, 10, '2026-05-26', 'Office'),
(811, 42, 10, '2026-05-27', 'WFH'),
(812, 43, 10, '2026-05-27', 'Office'),
(813, 44, 10, '2026-05-27', 'WFH'),
(814, 45, 10, '2026-05-27', 'Office'),
(815, 46, 10, '2026-05-27', 'Office'),
(816, 47, 10, '2026-05-27', 'Office'),
(817, 48, 10, '2026-05-27', 'Office'),
(818, 49, 10, '2026-05-27', 'Office'),
(819, 50, 10, '2026-05-27', 'WFH'),
(820, 51, 10, '2026-05-27', 'Office'),
(821, 42, 10, '2026-05-28', 'Office'),
(822, 43, 10, '2026-05-28', 'WFH'),
(823, 44, 10, '2026-05-28', 'WFH'),
(824, 45, 10, '2026-05-28', 'WFH'),
(825, 46, 10, '2026-05-28', 'Office'),
(826, 47, 10, '2026-05-28', 'Office'),
(827, 48, 10, '2026-05-28', 'Office'),
(828, 49, 10, '2026-05-28', 'WFH'),
(829, 50, 10, '2026-05-28', 'WFH'),
(830, 51, 10, '2026-05-28', 'WFH'),
(831, 42, 10, '2026-05-29', 'Office'),
(832, 43, 10, '2026-05-29', 'WFH'),
(833, 44, 10, '2026-05-29', 'WFH'),
(834, 45, 10, '2026-05-29', 'WFH'),
(835, 46, 10, '2026-05-29', 'WFH'),
(836, 47, 10, '2026-05-29', 'WFH'),
(837, 48, 10, '2026-05-29', 'Office'),
(838, 49, 10, '2026-05-29', 'Office'),
(839, 50, 10, '2026-05-29', 'Office'),
(840, 51, 10, '2026-05-29', 'WFH'),
(841, 5, 5, '2026-05-25', 'Office');

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
-- Indexes for table `leave_details`
--
ALTER TABLE `leave_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `request_id` (`request_id`);

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
  ADD KEY `member_id` (`member_id`),
  ADD KEY `created_by` (`created_by`);

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
-- Indexes for table `sec_notifications`
--
ALTER TABLE `sec_notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `request_id` (`request_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `announcement_replies`
--
ALTER TABLE `announcement_replies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=876;

--
-- AUTO_INCREMENT for table `daily_reports`
--
ALTER TABLE `daily_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=590;

--
-- AUTO_INCREMENT for table `leave_details`
--
ALTER TABLE `leave_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `leave_requests`
--
ALTER TABLE `leave_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=447;

--
-- AUTO_INCREMENT for table `overtime_requests`
--
ALTER TABLE `overtime_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `progress_history`
--
ALTER TABLE `progress_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `report_categories`
--
ALTER TABLE `report_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `sec_notifications`
--
ALTER TABLE `sec_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `teams`
--
ALTER TABLE `teams`
  MODIFY `team_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `wfh_schedules`
--
ALTER TABLE `wfh_schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=842;

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
-- Constraints for table `leave_details`
--
ALTER TABLE `leave_details`
  ADD CONSTRAINT `leave_details_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `leave_requests` (`id`) ON DELETE CASCADE;

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
  ADD CONSTRAINT `overtime_requests_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `overtime_requests_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

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
