-- MySQL Dump for Student Management System
CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

SET FOREIGN_KEY_CHECKS = 0;

-- Table structure for user
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255),
  `email` VARCHAR(255) NOT NULL,
  `role` VARCHAR(255),
  `password_hash` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for user
INSERT INTO `user` VALUES ('u1', 'Super Admin', 'admin@elitesms.com', 'admin', 'scrypt:32768:8:1$tCzHxYmiQSxovGHv$d35d0e69f25d2b62acd9161a2671bbb43f3b49d7b02d07ebae2fa8b2db0c3cf8c6fd494bb43bae1f785c2d4273e994a1d1805aea7740e721be048c98ed179e8c');
INSERT INTO `user` VALUES ('u2', 'Dr. Smith', 'professor@elitesms.com', 'professor', 'scrypt:32768:8:1$FDjS9BglcEJG6jkb$3b1465450610e1a61c2332debf8166bed7023439d91807adf33931dcd788161263060b3d39cf74c5317a3081191bbc7723dc04e3fae3cc49d4f467f94d7f60ef');
INSERT INTO `user` VALUES ('u3', 'Jane Doe', 'student1@elitesms.com', 'student', 'scrypt:32768:8:1$C3s42BridH2eZE4l$6b7078ab59c33e19b24f488af3a080bc3ca65950c2000eae8b01b141e79bc3b51c09bf4adc677be543b9473a0d6b89d6dc41b6e4503a6b5ec5c906ba38bcf896');
INSERT INTO `user` VALUES ('u4', 'Student Beta', 'student2@elitesms.com', 'student', 'scrypt:32768:8:1$x4Fh1Z0vKgNu297R$d3a1e311acd208a9adc4a85d9b52b6190170999e45e2936c9ffe34872bd4c50f066b7183b70a3f3c180bb455b2857db1c921e73141eefc13f6c993346bff11c1');
INSERT INTO `user` VALUES ('u5', 'Dr. Jones', 'professor2@elitesms.com', 'professor', 'scrypt:32768:8:1$sLJ6NgsuNn8nKC7m$29bf329cb5ac7bafc9f2295c932a0b7a0dc9359dd7f772d2fdf1766489be37e485068a1e2f05cb340f0343a925c9f5a66ded3d405e6ceaf481ccf3a4b1c0f44a');

-- Table structure for student
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `student_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255),
  `age` INTEGER,
  `email` VARCHAR(255),
  `enrollment_date` VARCHAR(255),
  `enrolled_subjects` JSON,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for student
INSERT INTO `student` VALUES ('d8a27c62-f2c4-4601-aaac-0cbc37274804', 'Jane Doe', 20, 'student@elitesms.com', '2026-01-15', '["Algorithms", "Data Structures", "Database Systems", "Machine Learning"]');
INSERT INTO `student` VALUES ('b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', 'John Stiles', 21, 'john@elitesms.com', '2026-01-18', '["Algorithms", "Machine Learning"]');
INSERT INTO `student` VALUES ('a6cbcc95-df21-4bf9-a3c2-4ce9b552bed1', 'Alice Johnson', 19, 'alice@elitesms.com', '2026-02-10', '["Data Structures", "Machine Learning"]');
INSERT INTO `student` VALUES ('3873c441-a653-49c1-8626-2d166505b82d', 'Test Student', 21, 'test@example.com', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('00a1061f-62c9-4d29-bffe-6c022d776753', 'Leanne Graham', 20, 'Sincere@april.biz', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('ff71eab1-370f-4a21-8a95-30ad6689f5da', 'Ervin Howell', 20, 'Shanna@melissa.tv', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('e6ac18f1-4029-49cf-9206-181887979bb3', 'Clementine Bauch', 20, 'Nathan@yesenia.net', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('58ec4325-10b7-42b9-99fe-23c6a2f255a2', 'Patricia Lebsack', 20, 'Julianne.OConner@kory.org', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('65817d8c-26a9-43ea-b7e2-4584471415a3', 'Chelsey Dietrich', 20, 'Lucio_Hettinger@annie.ca', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('04af940c-7c2e-4d81-b915-32e5cd6256c0', 'Mrs. Dennis Schulist', 20, 'Karley_Dach@jasper.info', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('547443bf-bb0e-4e26-9355-71e12d0cc116', 'Kurtis Weissnat', 20, 'Telly.Hoeger@billy.biz', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('07413431-e93c-4b89-ba5e-b205c5aa7cc3', 'Nicholas Runolfsdottir V', 20, 'Sherwood@rosamond.me', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('80f536b1-a310-451c-9376-2fb040f1c7c9', 'Glenna Reichert', 20, 'Chaim_McDermott@dana.io', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('5c15f955-d138-49dc-947d-a7bef917e632', 'Clementina DuBuque', 20, 'Rey.Padberg@karina.biz', '2026-04-24', '[]');
INSERT INTO `student` VALUES ('u3', 'Jane Doe', 20, 'student1@elitesms.com', '2024-01-01', '["Mathematics", "Physics"]');
INSERT INTO `student` VALUES ('u4', 'Student Beta', 21, 'student2@elitesms.com', '2024-01-02', '["Algorithms", "Data Structures"]');

-- Table structure for grade
DROP TABLE IF EXISTS `grade`;
CREATE TABLE `grade` (
  `grade_id` VARCHAR(255) NOT NULL,
  `student_id` VARCHAR(255),
  `subject` VARCHAR(255),
  `score` FLOAT,
  PRIMARY KEY (`grade_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for grade
INSERT INTO `grade` VALUES ('85fd9a68-9035-4b11-8122-a6a1b8dac051', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'Algorithms', 92.0);
INSERT INTO `grade` VALUES ('5ee04550-1452-4858-b3f4-e65f61e7bb4c', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'Data Structures', 88.0);
INSERT INTO `grade` VALUES ('7b20cbc7-929b-4705-99b8-7a8c8ab2e582', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', 'Algorithms', 75.0);
INSERT INTO `grade` VALUES ('f607b0b4-ec4f-49ea-9904-17090aa2f0f5', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', 'Machine Learning', 45.0);
INSERT INTO `grade` VALUES ('8b3c26ee-074c-4cc5-b480-04a4015b0a3c', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'Data Structures', 95.0);
INSERT INTO `grade` VALUES ('g1', 'u3', 'Mathematics', 85.0);
INSERT INTO `grade` VALUES ('g2', 'u3', 'Physics', 78.0);
INSERT INTO `grade` VALUES ('a16e861e-7d7d-46be-8efb-5929a7622b55', 'u4', 'Computer Science', 85.0);

-- Table structure for attendance
DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `attendance_id` VARCHAR(255) NOT NULL,
  `student_id` VARCHAR(255),
  `date` VARCHAR(255),
  `status` VARCHAR(255),
  PRIMARY KEY (`attendance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for attendance
INSERT INTO `attendance` VALUES ('e062d73e-3156-43c9-8c32-f8b78230af5b', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-20', 'Present');
INSERT INTO `attendance` VALUES ('993f0ab2-0fca-4a02-b6a2-2c74c8b2cd77', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('6ffabdd9-495a-45b5-88fd-8c76f3efe18f', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-20', 'Absent');
INSERT INTO `attendance` VALUES ('79066ba7-e165-430c-a0b1-4323f2dfbd31', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('bfc2da6b-e560-4de8-8f60-e82bc6bf5b38', 'a6cbcc95-df21-4bf9-a3c2-4ce9b552bed1', '2026-04-22', 'Present');
INSERT INTO `attendance` VALUES ('541106de-2f1c-4c85-bf79-7da86faff595', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-22', 'Present');
INSERT INTO `attendance` VALUES ('44920b81-7ee1-471b-b9aa-cff1c0b16011', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-22', 'Absent');
INSERT INTO `attendance` VALUES ('a2b0d96a-b6ca-4760-97cf-f5a925d7fd99', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-23', 'Present');
INSERT INTO `attendance` VALUES ('682d9dcd-ea05-4a09-a00e-bafa1266399a', 'a6cbcc95-df21-4bf9-a3c2-4ce9b552bed1', '2026-04-24', 'Present');
INSERT INTO `attendance` VALUES ('6cf34193-7207-49f7-a893-4b0f6a62b31f', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-20', 'Present');
INSERT INTO `attendance` VALUES ('128b7c75-5c07-4944-92bd-4a6f156ea7a9', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('894a9b6e-6dbb-4d0f-a3db-f1b0881cae83', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-20', 'Absent');
INSERT INTO `attendance` VALUES ('18f903f2-6545-497c-a173-e028c6197706', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('fedf7319-6b66-4d70-b35c-c4517af44788', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-24', 'Present');
INSERT INTO `attendance` VALUES ('78354dac-d38a-4ebb-bad0-8309d6399f8d', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-20', 'Present');
INSERT INTO `attendance` VALUES ('bf73a2c7-88c4-4983-af81-7233e9726843', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('ed7d192e-a541-4cf6-b93f-ccc90ed46b9b', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-20', 'Absent');
INSERT INTO `attendance` VALUES ('2ccfcd02-a894-466e-92d4-e7d7a8e8fcaa', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('d1e2c609-27a2-4b08-ae4b-85cca1721c70', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-20', 'Present');
INSERT INTO `attendance` VALUES ('ced588a7-cf44-446b-a562-ed542d164ba9', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('43106eb6-14cd-4d97-bcff-2be79bc4a8cf', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-20', 'Absent');
INSERT INTO `attendance` VALUES ('8228a1bb-61b4-4e2b-b3af-44da4c10b7d5', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', '2026-04-21', 'Present');
INSERT INTO `attendance` VALUES ('51d3751e-5f5b-467d-bb21-8c8cf79afda9', '5c15f955-d138-49dc-947d-a7bef917e632', '2026-04-24', 'Present');
INSERT INTO `attendance` VALUES ('d98e483f-f3eb-4a4e-8b19-928ed1a348de', '07413431-e93c-4b89-ba5e-b205c5aa7cc3', '2026-04-24', 'Present');
INSERT INTO `attendance` VALUES ('a08b9681-7e35-4a9a-a6d5-14144ba828c6', '547443bf-bb0e-4e26-9355-71e12d0cc116', '2026-04-24', 'Absent');
INSERT INTO `attendance` VALUES ('a22a01da-52bb-4319-8700-18267b8e2e83', '04af940c-7c2e-4d81-b915-32e5cd6256c0', '2026-04-24', 'Absent');
INSERT INTO `attendance` VALUES ('a0', 'u3', '2024-04-18', 'Present');
INSERT INTO `attendance` VALUES ('a1', 'u3', '2024-04-19', 'Present');
INSERT INTO `attendance` VALUES ('a2', 'u3', '2024-04-20', 'Absent');
INSERT INTO `attendance` VALUES ('a3', 'u3', '2024-04-21', 'Present');
INSERT INTO `attendance` VALUES ('a4', 'u3', '2024-04-22', 'Present');
INSERT INTO `attendance` VALUES ('a5', 'u3', '2024-04-23', 'Present');
INSERT INTO `attendance` VALUES ('a6', 'u3', '2024-04-24', 'Present');
INSERT INTO `attendance` VALUES ('6319418a-adee-4a82-ac39-6f81f88e9c8a', 'u3', '2026-04-24', 'Present');
INSERT INTO `attendance` VALUES ('6d2c8780-df36-48fa-8881-44d54b140a20', 'u4', '2026-04-25', 'Present');
INSERT INTO `attendance` VALUES ('4c05775c-ee75-49b2-b7a6-0348246a4f5e', 'u4', '2026-04-17', 'Present');
INSERT INTO `attendance` VALUES ('101a7b6d-7d9d-4c24-a513-97da0e873105', 'u4', '2026-04-18', 'Present');
INSERT INTO `attendance` VALUES ('70c944ca-4643-4139-961e-e1bd6b719546', 'u4', '2026-04-19', 'Present');
INSERT INTO `attendance` VALUES ('4a974583-2f6f-4a69-8458-6eae5f543329', 'u4', '2026-04-20', 'Absent');
INSERT INTO `attendance` VALUES ('9a46f336-f51a-4d84-8a25-800568f17e30', 'u4', '2026-04-21', 'Absent');
INSERT INTO `attendance` VALUES ('530cf6f7-0bdb-4d2e-ac23-6ebedffc1f60', 'u4', '2026-04-22', 'Present');
INSERT INTO `attendance` VALUES ('8e3bde2a-2bf7-41e1-bf3d-c3713c5081b9', 'u4', '2026-04-23', 'Present');
INSERT INTO `attendance` VALUES ('2a61e7d9-070c-47f5-a445-fedd6f09adae', 'u4', '2026-04-24', 'Absent');

-- Table structure for notice
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice` (
  `notice_id` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255),
  `content` TEXT,
  `date_posted` VARCHAR(255),
  `posted_by` VARCHAR(255),
  `target_roles` JSON,
  PRIMARY KEY (`notice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for notice
INSERT INTO `notice` VALUES ('0851a41c-8b1d-4c6d-b62a-beffa77382dd', 'Prof Only Notice', 'Only professors should see this', '2026-04-23 08:38:57', 'Super Admin', '["admin", "professor", "student"]');
INSERT INTO `notice` VALUES ('867fa73b-9c58-4b1f-b3bf-ff0b2d1b2a42', 'Assignment submission due', 'Assignment submission last due date is 22.04.2026.', '2026-04-22 23:51:15', 'Prof. Smith', '["student"]');
INSERT INTO `notice` VALUES ('30084f53-6168-4e6c-9345-ab48fc89959d', 'Holiday announcement', 'Sunday', '2026-04-22 23:45:36', 'Super Admin', '["professor"]');
INSERT INTO `notice` VALUES ('76e8dffe-7c40-4c9b-8a98-9fa748e8b455', 'Test Notice', 'This is a test notice with an author.', '2026-04-22 11:11:46', 'System Administrator', '[]');
INSERT INTO `notice` VALUES ('a3ed6023-e75c-41b8-9f89-93efd424f3a6', 'Final Exams Approaching', 'Make sure all assignments are turned in before 2026-05-01.', '2026-04-22 00:11:19', NULL, '[]');
INSERT INTO `notice` VALUES ('9927f728-dbcc-414f-ac26-f81e27ffcbf2', 'System Outage', 'The library tracker will be undergoing maintenance on Saturday.', '2026-04-22 00:11:19', NULL, '[]');

-- Table structure for staff
DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff` (
  `staff_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255),
  `email` VARCHAR(255),
  `role` VARCHAR(255),
  `department` VARCHAR(255),
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for staff
INSERT INTO `staff` VALUES ('668abc38-6a08-4b37-8c27-63014a8620dc', 'Prof. Smith', 'professor@elitesms.com', 'Teacher', 'Computer Science');
INSERT INTO `staff` VALUES ('228eac11-6e56-468f-8613-f11bedf162de', 'Dr. Miller', 'miller@elitesms.com', 'Head of Department', 'Engineering');
INSERT INTO `staff` VALUES ('1d42b40b-1b7d-4a6d-b6b3-e1daf7c71cf2', 'Sam Support', 'sam@elitesms.com', 'Administrator', 'IT Support');
INSERT INTO `staff` VALUES ('u2', 'Dr. Smith', 'professor@elitesms.com', 'Teacher', 'Mathematics');
INSERT INTO `staff` VALUES ('u5', 'Dr. Jones', 'professor2@elitesms.com', 'Teacher', 'Physics');

-- Table structure for subject
DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `subject_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255),
  `description` VARCHAR(255),
  `department` TEXT,
  PRIMARY KEY (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for subject
INSERT INTO `subject` VALUES ('33e7ea51-15e5-4b2b-8153-d5a98dd15e56', 'Algorithms', 'Core CS Concepts.', 'Computer Science');
INSERT INTO `subject` VALUES ('91588aba-fdc5-4f66-a07a-82608f290770', 'Data Structures', 'Advanced trees and graphs.', 'Computer Science');
INSERT INTO `subject` VALUES ('676d522c-ec1b-4997-b84c-2331e7a8164b', 'Database Systems', 'SQL and Relational logic.', 'Computer Science');
INSERT INTO `subject` VALUES ('e8e9a85c-cb21-4d45-9357-698ff1218619', 'Machine Learning', 'AI modelling.', 'Computer Science');
INSERT INTO `subject` VALUES ('4a4f87ee-90d7-499a-b9bf-70bb969d3b4e', 'Computer Science', 'computer science', 'Physics');

-- Table structure for library_record
DROP TABLE IF EXISTS `library_record`;
CREATE TABLE `library_record` (
  `record_id` VARCHAR(255) NOT NULL,
  `student_id` VARCHAR(255),
  `book_title` VARCHAR(255),
  `checkout_date` VARCHAR(255),
  `status` VARCHAR(255),
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for library_record
INSERT INTO `library_record` VALUES ('e88d21cb-2c59-40a5-af01-407699c5cd12', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'Introduction to Algorithms', '2026-04-05', 'Returned');
INSERT INTO `library_record` VALUES ('31501fe1-4f3c-48a3-b7c0-1a339cd85782', 'b5ad4c4f-8cd9-4557-a821-19fcdd57ee9b', 'Artificial Intelligence: A Modern Approach', '2026-03-20', 'Returned');
INSERT INTO `library_record` VALUES ('5826b0f3-b786-4c97-845b-fd26ea81f4cc', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'Clean Code', '2026-04-22', 'Returned');
INSERT INTO `library_record` VALUES ('bb006fc6-6123-4c4f-ac34-ef723c62ed34', 'u3', 'Python Crash Course', '2026-04-25', 'Borrowed');

-- Table structure for assignment
DROP TABLE IF EXISTS `assignment`;
CREATE TABLE `assignment` (
  `id` VARCHAR(255) NOT NULL,
  `prof_id` VARCHAR(255),
  `subject` VARCHAR(255),
  `title` VARCHAR(255),
  `description` TEXT,
  `deadline` VARCHAR(255),
  `created_at` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for assignment
INSERT INTO `assignment` VALUES ('55937282-f3ab-41be-be6f-418a96e92109', '668abc38-6a08-4b37-8c27-63014a8620dc', 'Algorithms', 'Sorting Implementation', 'Implement QuickSort in Python.', '2026-04-25', '2026-04-22T00:11:19.166751');
INSERT INTO `assignment` VALUES ('315633fb-7d3b-49a6-be4f-0aef89791f23', '668abc38-6a08-4b37-8c27-63014a8620dc', 'Database Systems', 'SQL Join Queries', 'Complete exercises 1 to 5.', '2026-04-28', '2026-04-22T00:11:19.166785');
INSERT INTO `assignment` VALUES ('85bfeed5-a4cd-4ba5-98c7-c32a595cfff6', '668abc38-6a08-4b37-8c27-63014a8620dc', 'Algorithms', 'Algorithms ', 'make notes of Algorithm', '2026-04-30', '2026-04-23T09:49:28.860547');
INSERT INTO `assignment` VALUES ('6dbdffd5-e357-4b5e-9e4d-2e2c75b0a594', '668abc38-6a08-4b37-8c27-63014a8620dc', 'Data Structures', 'Data structure', 'how many data structure and describe in details', '2026-05-23', '2026-04-23T11:05:05.204191');
INSERT INTO `assignment` VALUES ('as1', 'u2', 'Mathematics', 'Algebra Fundamentals', 'Complete all exercises in Chapter 1.', '2024-04-25', '2024-04-10T10:00:00');
INSERT INTO `assignment` VALUES ('as2', 'u2', 'Mathematics', 'Geometry Basics', 'Draw and label 5 geometric shapes.', '2024-04-28', '2024-04-12T11:00:00');
INSERT INTO `assignment` VALUES ('77f73d3a-0f3b-427f-b3cf-de9e401226e0', 'u5', 'Computer Science', 'java programming', 'programming language', '2026-04-30', '2026-04-26T00:15:02.135771');

-- Table structure for submission
DROP TABLE IF EXISTS `submission`;
CREATE TABLE `submission` (
  `id` VARCHAR(255) NOT NULL,
  `assignment_id` VARCHAR(255),
  `student_id` VARCHAR(255),
  `content` TEXT,
  `submitted_at` VARCHAR(255),
  `status` VARCHAR(255),
  `score` FLOAT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for submission
INSERT INTO `submission` VALUES ('3a5be731-7dcc-416c-9f50-a64ca5393880', '55937282-f3ab-41be-be6f-418a96e92109', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'Sorting algorithms rearrange arrays into ascending or descending order, with implementations varying by efficiency (e.g., 




 vs 



), stability, and data size. Common methods include bubble sort (simple, 



), insertion sort (efficient for small data), and merge sort (fast divide-and-conquer). Python typically uses Timsort, while C++ often uses IntroSort. 
GeeksforGeeks
GeeksforGeeks
 +6
Common Sorting Algorithm Implementations
Bubble Sort (Python): Compares adjacent elements and swaps them if they are in the wrong order.
python
def bubbleSort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
Insertion Sort (Conceptual): Builds the final sorted array one item at a time.
Iterate from i = 1 to n-1.
Store current element as key.
Compare key with previous elements, shifting them if they are larger.
Merge Sort (C++): A divide-and-conquer algorithm that splits the array in half, sorts them, and merges.
Divide: mid = left + (right - left) / 2
Conquer: Recursive calls mergeSort(arr, left, mid) and mergeSort(arr, mid + 1, right).
Merge: merge(arr, left, mid, right) to combine sorted halves. 
W3Schools
W3Schools
 +5
Key Considerations
Time Complexity: Quicksort/Merge Sort are ideal for large datasets (




), while Bubble Sort is generally inefficient (



).
Stability: Stable sorts maintain the relative order of equal elements (e.g., Merge Sort).
Best Use Cases:
Small datasets: Insertion Sort.
Large datasets: Merge Sort or Quick Sort.
Nearly sorted data: Insertion Sort. 
GeeksforGeeks
GeeksforGeeks
 +4
Standard Library Implementations
Python: list.sort() or sorted(list).
C++: std::sort().
JavaScript: Array.prototype.sort(). ', '2026-04-23T11:25:35.105594', 'Graded', NULL);
INSERT INTO `submission` VALUES ('ada37f4a-8498-499e-bb3b-2b6c2c5488cb', '315633fb-7d3b-49a6-be4f-0aef89791f23', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', '# RandomUser API

# Get Method

# get_cell()                      get_login_md5()
# get_city()                      get_login_salt()
# get_dob()                       get_login_sha1()
# get_email()                     get_login_sha256()
# get_first_name()                get_nat()
# get_full_name()                 get_password()
# get_gender()                    get_phone()
# get_id()                        get_picture()
# get_id_number()                 get_postcode()
# get_id_type()                   get_registered()
# get_info()                      get_state()
# get_last_name()                 get_street()
# get_username()                  get_zipcode()


from randomuser import RandomUser
import pandas as pd
import json

import requests

r = RandomUser()
# print("r", r)
some_list = r.generate_users(10) 
# print(some_list)

# The "Get Methods" functions mentioned at the beginning of this notebook,
#  can generate the required parameters to construct a dataset.
name = r.get_full_name()

# Let''s say we only need 10 users with full names and their email addresses.
#  We can write a "for-loop" to print these 10 users.

for user in some_list:
    # print (user.get_full_name()," ",user.get_email())

# Exercise 1 /////////////////////////////////////////////////////

# In this Exercise, generate photos of the random 10 users.
 for user in some_list:
    # print(user.get_picture())

    def get_users():
        users =[]
        for user in r.generate_users(10):
            users.append({"Name":user.get_full_name(),
                      "Gender":user.get_gender(),
                      "City":user.get_city(),
                      "State":user.get_state(),
                      "Email":user.get_email(),
                      "DOB":user.get_dob(),
                      "Picture":user.get_picture()})
        print("users", pd.DataFrame(users))
        return pd.DataFrame(users) 
    get_users()
    # df1 = pd.DataFrame(get_users())               

# Example 2: Fruityvice API //////////////////////////////////

# We will obtain the fruityvice API data using requests.get("url") function. The data is in a json format.
data = requests.get("https://web.archive.org/web/20240929211114/https://fruityvice.com/api/fruit/all")

# We will retrieve results using json.loads() function.
results = json.loads(data.text)

# We will convert our json data into pandas data frame.
pd.DataFrame(results)

# The result is in a nested json format. The ''nutrition'' column contains multiple subcolumns, so the data needs to be ''flattened'' or normalized.
df2 = pd.json_normalize(results)

# Let''s see if we can extract some information from this dataframe. Perhaps, we need to know the family and genus of a cherry.
cherry = df2.loc[df2["name"] == ''Cherry'']
(cherry.iloc[0][''family'']) , (cherry.iloc[0][''genus''])

# In this Exercise, find out how many calories are contained in a banana.

# Write your code here
cal_banana = df2.loc[df2["name"] == ''banana'']
cal_banana.iloc[0][''nutritions.calories'']

# Exercise 3 ////////////////////////////////////////

# Using requests.get("url") function, load the data from the URL.
data = requests.get("https://official-joke-api.appspot.com/jokes/ten")

# Retrieve results using json.loads() function.
# Write your code here
result = json.loads(data.text)

# Convert json data into pandas data frame. Drop the type and id columns.

df3 = df2.DataFrame(result)
df3.drop(columns=["type","id"],implace=True)
df3', '2026-04-23T08:45:58.360519', 'Graded', 80.0);
INSERT INTO `submission` VALUES ('11d2b3c4-0253-4dbe-8eee-e4e7e9a123bf', '55937282-f3ab-41be-be6f-418a96e92109', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'https://example.com
', '2026-04-23T09:06:21.710675', 'Graded', NULL);
INSERT INTO `submission` VALUES ('f5e7675b-c48f-45be-9922-d5533d342bae', '85bfeed5-a4cd-4ba5-98c7-c32a595cfff6', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 'https://www.google.com/search?q=algoeithm+of+python&rlz=1C1CHBF_enIN1048IN1048&oq=algoeithm+of+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIJCAEQABgNGIAEMgkIAhAAGA0YgAQyCAgDEAAYFhgeMggIBBAAGBYYHjIICAUQABgWGB4yCAgGEAAYFhgeMggIBxAAGBYYHjIICAgQABgWGB4yCAgJEAAYFhge0gEKMTM4MDhqMGoxNagCCLACAfEF_uIpka6cdag&sourceid=chrome&ie=UTF-8&sei=953paZeQNOilvr0Ppqi5gQY

Core Characteristics of a Python Algorithm
For a set of instructions to be considered a proper algorithm, it generally must meet these six criteria:
Unambiguous: Each step and its inputs/outputs must be clear and lead to only one meaning.
Well-defined Inputs: It must specify exactly what data is required (e.g., a list of integers).
Defined Outputs: It must have at least one intended result.
Finiteness: The algorithm must terminate after a finite number of steps; it cannot run forever.
Feasibility: It must be executable using available resources like memory and processing power.
Language Independence: The logic should be definable as pseudocode before being translated into Python code. ', '2026-04-23T09:50:46.312559', 'Submitted', NULL);
INSERT INTO `submission` VALUES ('sub1', 'as1', 'u3', 'I have completed the algebra work.', '2024-04-20', 'Graded', 90.0);
INSERT INTO `submission` VALUES ('sub2', 'as2', 'u3', 'Geometry submission', '2024-04-22', 'Pending', NULL);
INSERT INTO `submission` VALUES ('51b3e195-63f7-48c2-87c5-7588750da47a', '55937282-f3ab-41be-be6f-418a96e92109', 'u3', 'Test Submitted.', '2026-04-26T00:11:14.244975', 'Submitted', NULL);
INSERT INTO `submission` VALUES ('512e5230-8bcb-413a-918f-c9f003dd1968', '77f73d3a-0f3b-427f-b3cf-de9e401226e0', 'u4', 'testing', '2026-04-26T00:15:52.178803', 'Graded', 85.0);

-- Table structure for quiz
DROP TABLE IF EXISTS `quiz`;
CREATE TABLE `quiz` (
  `id` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `subject` VARCHAR(255) NOT NULL,
  `prof_id` VARCHAR(255) NOT NULL,
  `created_at` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for quiz
INSERT INTO `quiz` VALUES ('ea4432cb-477d-475e-b382-966a625d137d', 'software developer', 'data science', 'u2', '2026-04-25 00:38');
INSERT INTO `quiz` VALUES ('q1', 'Final Math Exam', 'Mathematics', 'u2', '2024-04-20 10:00');
INSERT INTO `quiz` VALUES ('q2', 'Physics Fundamentals', 'Physics', 'u5', '2024-04-21 11:00');
INSERT INTO `quiz` VALUES ('b5d47e1b-b7b1-46e0-90f3-a4caeea6a268', 'software developer', 'Web developmet', 'u5', '2026-04-25 11:03');
INSERT INTO `quiz` VALUES ('16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'Python', 'Algorithms', '668abc38-6a08-4b37-8c27-63014a8620dc', '2026-04-25 11:35');

-- Table structure for quiz_question
DROP TABLE IF EXISTS `quiz_question`;
CREATE TABLE `quiz_question` (
  `id` VARCHAR(255) NOT NULL,
  `quiz_id` VARCHAR(255) NOT NULL,
  `question_text` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for quiz_question
INSERT INTO `quiz_question` VALUES ('f7ebf779-2dac-41e0-9e97-13a4f3d7e17c', 'ea4432cb-477d-475e-b382-966a625d137d', 'what is software developer?');
INSERT INTO `quiz_question` VALUES ('bde7eac8-ea7a-4438-a51f-72227ad63347', 'ea4432cb-477d-475e-b382-966a625d137d', 'why you want to learn data science?');
INSERT INTO `quiz_question` VALUES ('q1_q0', 'q1', 'What is 5 + 7?');
INSERT INTO `quiz_question` VALUES ('q1_q1', 'q1', 'Solve for x: 2x = 10');
INSERT INTO `quiz_question` VALUES ('q1_q2', 'q1', 'Area of a square with side 4?');
INSERT INTO `quiz_question` VALUES ('q1_q3', 'q1', 'Value of Pi (approx)?');
INSERT INTO `quiz_question` VALUES ('q2_q0', 'q2', 'Unit of Force?');
INSERT INTO `quiz_question` VALUES ('q2_q1', 'q2', 'Speed of light is approx?');
INSERT INTO `quiz_question` VALUES ('q2_q2', 'q2', 'Force = Mass x ?');
INSERT INTO `quiz_question` VALUES ('q2_q3', 'q2', 'Gravity on Earth approx?');
INSERT INTO `quiz_question` VALUES ('374a36ef-6887-488e-8cd8-9933add3cfde', 'b5d47e1b-b7b1-46e0-90f3-a4caeea6a268', 'Test ');
INSERT INTO `quiz_question` VALUES ('a4bfcda2-c841-4290-aae3-a7d50d7cfd81', 'b5d47e1b-b7b1-46e0-90f3-a4caeea6a268', 'Test');
INSERT INTO `quiz_question` VALUES ('0d24f52b-97c3-418c-8b10-2d9655ceaa97', 'b5d47e1b-b7b1-46e0-90f3-a4caeea6a268', 'Test');
INSERT INTO `quiz_question` VALUES ('948cd8f9-562c-41e2-821c-5cf251d369bf', 'b5d47e1b-b7b1-46e0-90f3-a4caeea6a268', 'test');
INSERT INTO `quiz_question` VALUES ('3d39d924-37bf-4768-a861-1fbb0c94db98', '16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'test ');
INSERT INTO `quiz_question` VALUES ('5afa58a4-0a3d-4e8b-8d1d-953178b83b66', '16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'test');
INSERT INTO `quiz_question` VALUES ('5cdf494d-9763-4bc3-b903-abfde1a0a2e1', '16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'test ');
INSERT INTO `quiz_question` VALUES ('6cb9f2d5-1c98-4b54-9ac6-292516057cdd', '16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'test ');

-- Table structure for quiz_result
DROP TABLE IF EXISTS `quiz_result`;
CREATE TABLE `quiz_result` (
  `id` VARCHAR(255) NOT NULL,
  `quiz_id` VARCHAR(255) NOT NULL,
  `student_id` VARCHAR(255) NOT NULL,
  `score` INTEGER NOT NULL,
  `total_questions` INTEGER NOT NULL,
  `completed_at` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for quiz_result
INSERT INTO `quiz_result` VALUES ('4b61edeb-db5a-43a6-b006-d9ac619769c6', 'ea4432cb-477d-475e-b382-966a625d137d', 'd8a27c62-f2c4-4601-aaac-0cbc37274804', 1, 2, '2026-04-25 00:39');
INSERT INTO `quiz_result` VALUES ('f9103b35-ca05-4d3a-8847-4651684b94c5', 'ea4432cb-477d-475e-b382-966a625d137d', 'u3', 0, 2, '2026-04-25 01:12');
INSERT INTO `quiz_result` VALUES ('f2935f4a-eb53-4333-a329-076286a3cdd4', 'ea4432cb-477d-475e-b382-966a625d137d', 'u4', 0, 2, '2026-04-25 01:24');
INSERT INTO `quiz_result` VALUES ('48a9249c-4dba-402f-8430-0286d02b38ac', 'b5d47e1b-b7b1-46e0-90f3-a4caeea6a268', 'u3', 2, 4, '2026-04-25 18:02');
INSERT INTO `quiz_result` VALUES ('56d67640-3188-48f0-b188-e5c0abafa919', '16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'u3', 1, 4, '2026-04-25 18:06');
INSERT INTO `quiz_result` VALUES ('6f07a9ca-00ff-4b13-8668-9e60e01520b4', '16ed9d31-6c6f-4dca-a253-f6b9168ed991', 'u4', 4, 4, '2026-04-25 18:11');
INSERT INTO `quiz_result` VALUES ('d52550ff-bef9-44f1-943d-8e0c30daf675', 'q1', 'u3', 4, 4, '2026-04-25 21:27');
INSERT INTO `quiz_result` VALUES ('3103327c-1b5e-48e2-b39d-e9cf359dd301', 'q2', 'u3', 4, 4, '2026-04-25 21:27');

-- Table structure for quiz_option
DROP TABLE IF EXISTS `quiz_option`;
CREATE TABLE `quiz_option` (
  `id` VARCHAR(255) NOT NULL,
  `question_id` VARCHAR(255) NOT NULL,
  `option_text` VARCHAR(255) NOT NULL,
  `is_correct` TINYINT(1),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for quiz_option
INSERT INTO `quiz_option` VALUES ('68dd6020-ea8b-467e-a3f9-9b27517a4cae', 'f7ebf779-2dac-41e0-9e97-13a4f3d7e17c', 'test1', 1);
INSERT INTO `quiz_option` VALUES ('128e5e6c-d4dd-49a6-a39b-262e5adde681', 'f7ebf779-2dac-41e0-9e97-13a4f3d7e17c', 'test2', 0);
INSERT INTO `quiz_option` VALUES ('aa16a2d8-ccbb-441a-9680-2bbe9d3770a0', 'f7ebf779-2dac-41e0-9e97-13a4f3d7e17c', 'test3', 0);
INSERT INTO `quiz_option` VALUES ('2f9f4493-237b-48be-8275-45b20b452186', 'f7ebf779-2dac-41e0-9e97-13a4f3d7e17c', 'test4', 0);
INSERT INTO `quiz_option` VALUES ('c969f9a4-f51d-46f6-9110-86d5758c8c6a', 'bde7eac8-ea7a-4438-a51f-72227ad63347', 'test1', 0);
INSERT INTO `quiz_option` VALUES ('85ea04de-28f2-41b5-9d48-5a20458cee6d', 'bde7eac8-ea7a-4438-a51f-72227ad63347', 'test2', 1);
INSERT INTO `quiz_option` VALUES ('3667c70a-4a5e-45a9-9ccf-10b007e8a494', 'bde7eac8-ea7a-4438-a51f-72227ad63347', 'test3', 0);
INSERT INTO `quiz_option` VALUES ('e6e47bd8-403d-46e7-aadb-938e782652c9', 'bde7eac8-ea7a-4438-a51f-72227ad63347', 'test4', 0);
INSERT INTO `quiz_option` VALUES ('1ab5bcf2-fe58-4c9c-b105-5e3abacf41a8', 'q1_q0', '12', 1);
INSERT INTO `quiz_option` VALUES ('aef497b4-b3ab-4d6c-93a5-d73986fa286b', 'q1_q0', '10', 0);
INSERT INTO `quiz_option` VALUES ('469b2b0d-70b6-426a-ae83-5b6507fccf23', 'q1_q0', '15', 0);
INSERT INTO `quiz_option` VALUES ('0bf421b4-7e8a-47d6-b4ce-4586614132e1', 'q1_q0', '11', 0);
INSERT INTO `quiz_option` VALUES ('b00067cd-e612-442c-9042-e0c10b4a3923', 'q1_q1', '5', 1);
INSERT INTO `quiz_option` VALUES ('956953e0-ce91-47c6-a618-1bb52fe25e6b', 'q1_q1', '2', 0);
INSERT INTO `quiz_option` VALUES ('ca29f91e-dd38-4450-aa4a-c952f016b65b', 'q1_q1', '10', 0);
INSERT INTO `quiz_option` VALUES ('f90ea062-b2de-4ab7-b5ec-ae237ec16ba5', 'q1_q1', '4', 0);
INSERT INTO `quiz_option` VALUES ('72fd937d-cc38-4eca-a380-e0667e5e9a4d', 'q1_q2', '16', 1);
INSERT INTO `quiz_option` VALUES ('07625924-cd81-406b-bb97-4bee8d864252', 'q1_q2', '8', 0);
INSERT INTO `quiz_option` VALUES ('a025449d-e9a0-45d0-aaf6-3ffe35975987', 'q1_q2', '4', 0);
INSERT INTO `quiz_option` VALUES ('33244dfb-7a0b-4f00-bddb-ae19d3b09a17', 'q1_q2', '20', 0);
INSERT INTO `quiz_option` VALUES ('3d2fac1a-603e-4bd4-b4f5-4ef4d2556515', 'q1_q3', '3.14', 1);
INSERT INTO `quiz_option` VALUES ('06a98aa7-ff70-474e-b23b-d59c7156e382', 'q1_q3', '2.14', 0);
INSERT INTO `quiz_option` VALUES ('1830b161-a23f-4ba7-9152-274cc1b2a86c', 'q1_q3', '4.14', 0);
INSERT INTO `quiz_option` VALUES ('b0b151b2-6422-45c1-9474-6c7db0c3cf0d', 'q1_q3', '1.14', 0);
INSERT INTO `quiz_option` VALUES ('75ff84c3-c64d-4cb4-afe5-8a3e400e39fc', 'q2_q0', 'Newton', 1);
INSERT INTO `quiz_option` VALUES ('786ef421-46ee-42aa-80ef-3fc71023e30f', 'q2_q0', 'Joule', 0);
INSERT INTO `quiz_option` VALUES ('aebaad44-602b-4eae-a184-8a13e48dff49', 'q2_q0', 'Watt', 0);
INSERT INTO `quiz_option` VALUES ('5807d8fd-c096-4236-bbfb-d04d326a7e8b', 'q2_q0', 'Volt', 0);
INSERT INTO `quiz_option` VALUES ('1c649d6d-06cd-48c2-ba25-d57a702de79c', 'q2_q1', '3x10^8 m/s', 1);
INSERT INTO `quiz_option` VALUES ('3f675b72-b6d7-451e-a252-0679908eea20', 'q2_q1', '2x10^8 m/s', 0);
INSERT INTO `quiz_option` VALUES ('946799d1-f6ae-4df1-871d-60c0fec0a0e7', 'q2_q1', '1x10^8 m/s', 0);
INSERT INTO `quiz_option` VALUES ('6b8f1305-07f0-4f66-b963-e2831e2f2496', 'q2_q1', '4x10^8 m/s', 0);
INSERT INTO `quiz_option` VALUES ('79b0ef4a-b346-4354-be21-f948e292513d', 'q2_q2', 'Acceleration', 1);
INSERT INTO `quiz_option` VALUES ('849a28e5-998f-4a2f-99b4-11c93c9d6def', 'q2_q2', 'Velocity', 0);
INSERT INTO `quiz_option` VALUES ('91873630-c770-4a51-96a4-b4239b96b5c6', 'q2_q2', 'Distance', 0);
INSERT INTO `quiz_option` VALUES ('84bae36f-dd48-40fa-a478-914e4b3f1c9e', 'q2_q2', 'Time', 0);
INSERT INTO `quiz_option` VALUES ('c5da4d80-8234-45a9-a9ba-16a345886de2', 'q2_q3', '9.8 m/s^2', 1);
INSERT INTO `quiz_option` VALUES ('36cf85a7-6993-4050-82e6-ceb825cb6690', 'q2_q3', '8.8 m/s^2', 0);
INSERT INTO `quiz_option` VALUES ('3f5172c9-75e4-432f-a903-5a6aa5716b96', 'q2_q3', '10.8 m/s^2', 0);
INSERT INTO `quiz_option` VALUES ('b73ff590-e0e2-430d-b513-2928d471fd82', 'q2_q3', '7.8 m/s^2', 0);
INSERT INTO `quiz_option` VALUES ('576cdb1a-7797-451f-af84-f547cff1dc87', '374a36ef-6887-488e-8cd8-9933add3cfde', 'test 1', 1);
INSERT INTO `quiz_option` VALUES ('ad87a726-380a-460d-873e-c1adfc40f5b3', '374a36ef-6887-488e-8cd8-9933add3cfde', 'test 2', 0);
INSERT INTO `quiz_option` VALUES ('fe6163d2-32d5-40ec-98e0-1f984de316d8', '374a36ef-6887-488e-8cd8-9933add3cfde', 'test3', 0);
INSERT INTO `quiz_option` VALUES ('387755e6-3ba4-46a3-8380-72389673777a', '374a36ef-6887-488e-8cd8-9933add3cfde', 'test4', 0);
INSERT INTO `quiz_option` VALUES ('7269988c-9d2a-4ea7-9b80-6dc3a500be68', 'a4bfcda2-c841-4290-aae3-a7d50d7cfd81', 'test 1', 0);
INSERT INTO `quiz_option` VALUES ('d329ca40-2af8-40ca-b668-0d14fa50c4bb', 'a4bfcda2-c841-4290-aae3-a7d50d7cfd81', 'test 2', 1);
INSERT INTO `quiz_option` VALUES ('4ad25f20-c6de-4eb4-9524-c2bdffbd78d7', 'a4bfcda2-c841-4290-aae3-a7d50d7cfd81', 'test 3', 0);
INSERT INTO `quiz_option` VALUES ('33081ac0-aaa6-498b-b4e7-df7f0d4b1cfd', 'a4bfcda2-c841-4290-aae3-a7d50d7cfd81', 'test 4', 0);
INSERT INTO `quiz_option` VALUES ('b5dbd8da-efcb-4ace-9051-b58ec8da856b', '0d24f52b-97c3-418c-8b10-2d9655ceaa97', 'test 1', 0);
INSERT INTO `quiz_option` VALUES ('fb409479-2a9a-44dc-977e-928516be871c', '0d24f52b-97c3-418c-8b10-2d9655ceaa97', 'test 2', 0);
INSERT INTO `quiz_option` VALUES ('95f0bb42-64bb-4586-8d79-96df0d80d906', '0d24f52b-97c3-418c-8b10-2d9655ceaa97', 'test 3', 1);
INSERT INTO `quiz_option` VALUES ('936777ca-f87c-4eba-b279-6acb1252ca23', '0d24f52b-97c3-418c-8b10-2d9655ceaa97', 'test 4', 0);
INSERT INTO `quiz_option` VALUES ('5d183643-07b2-4039-8171-85a0be777b9f', '948cd8f9-562c-41e2-821c-5cf251d369bf', 'test 1', 0);
INSERT INTO `quiz_option` VALUES ('65bcd4a0-3a3d-49dd-97e4-a90efc7ee943', '948cd8f9-562c-41e2-821c-5cf251d369bf', 'test 2', 0);
INSERT INTO `quiz_option` VALUES ('5f31d454-67ff-4f14-876e-8c686cad646a', '948cd8f9-562c-41e2-821c-5cf251d369bf', 'test 3', 0);
INSERT INTO `quiz_option` VALUES ('bf531376-cb74-46b7-8a51-fbf93c768595', '948cd8f9-562c-41e2-821c-5cf251d369bf', 'test 4', 1);
INSERT INTO `quiz_option` VALUES ('867c8f5a-d4b5-4f94-be96-cf2eaf7a61fc', '3d39d924-37bf-4768-a861-1fbb0c94db98', 'test 1', 1);
INSERT INTO `quiz_option` VALUES ('4fcbf224-26ce-41fa-973f-3435239ec892', '3d39d924-37bf-4768-a861-1fbb0c94db98', 'test 2', 0);
INSERT INTO `quiz_option` VALUES ('5efbec7c-8e95-4a4e-bfb8-179f7e051ad6', '3d39d924-37bf-4768-a861-1fbb0c94db98', 'test 3', 0);
INSERT INTO `quiz_option` VALUES ('19fd4619-53be-4420-b182-2eaa84c3d22d', '3d39d924-37bf-4768-a861-1fbb0c94db98', 'test 4', 0);
INSERT INTO `quiz_option` VALUES ('ec2e28b8-e435-4109-97e5-85a6a7148579', '5afa58a4-0a3d-4e8b-8d1d-953178b83b66', 'test 1', 0);
INSERT INTO `quiz_option` VALUES ('183c750c-9e09-4f5d-b3c6-702330532473', '5afa58a4-0a3d-4e8b-8d1d-953178b83b66', 'test 2', 1);
INSERT INTO `quiz_option` VALUES ('013f3255-f073-42a9-8ed2-7ce484712b85', '5afa58a4-0a3d-4e8b-8d1d-953178b83b66', 'test 3 ', 0);
INSERT INTO `quiz_option` VALUES ('7ecd7dcf-d89b-4867-bb8a-ffa9a8b5c1b8', '5afa58a4-0a3d-4e8b-8d1d-953178b83b66', 'test 4', 0);
INSERT INTO `quiz_option` VALUES ('e5bd49fc-1ea7-4e2e-bf9a-3bbc53ed8d7b', '5cdf494d-9763-4bc3-b903-abfde1a0a2e1', 'test 1', 0);
INSERT INTO `quiz_option` VALUES ('2e7087e9-97ee-48e7-adb4-51bd89369fce', '5cdf494d-9763-4bc3-b903-abfde1a0a2e1', 'test 2', 0);
INSERT INTO `quiz_option` VALUES ('6411e2d4-f03d-4fbb-bc49-64673a71b0b1', '5cdf494d-9763-4bc3-b903-abfde1a0a2e1', 'test 3', 1);
INSERT INTO `quiz_option` VALUES ('c3b68130-2675-40f0-b2f4-083092d5707a', '5cdf494d-9763-4bc3-b903-abfde1a0a2e1', 'test 4', 0);
INSERT INTO `quiz_option` VALUES ('4f979a14-7fc3-4e6d-8bfe-7016eeb3975f', '6cb9f2d5-1c98-4b54-9ac6-292516057cdd', 'test 1', 0);
INSERT INTO `quiz_option` VALUES ('1af642de-c19b-43d5-b232-f6380074a268', '6cb9f2d5-1c98-4b54-9ac6-292516057cdd', 'test 2', 0);
INSERT INTO `quiz_option` VALUES ('e73935a2-463b-4117-8032-5b201e38764d', '6cb9f2d5-1c98-4b54-9ac6-292516057cdd', 'test 3', 0);
INSERT INTO `quiz_option` VALUES ('e8ed0463-d087-4ba6-8f65-6b82169d9a0b', '6cb9f2d5-1c98-4b54-9ac6-292516057cdd', 'test 4', 1);

SET FOREIGN_KEY_CHECKS = 1;
