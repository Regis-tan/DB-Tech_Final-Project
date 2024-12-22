-- Creates a database called "UMS_DB"
CREATE DATABASE ums_db;

-- Uses the "UMS_DB" database
USE ums_db;

-- Creates tables
CREATE TABLE department(
	departmentId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    departmentName varchar(50) NOT NULL
);

CREATE TABLE course(
	courseId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    courseName varchar(100) NOT NULL,
    credit int
);

CREATE TABLE program(
	programId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    programName varchar(50) NOT NULL,
    departmentId int NOT NULL,
    degree varchar(50) NOT NULL,
    
    FOREIGN KEY (departmentId) REFERENCES department(departmentId)
);

CREATE TABLE staff(
	staffId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    departmentId int NOT NULL,
    staffName varchar(100) NOT NULL,
    position varchar(50),
    DOB date NOT NULL,
    gender char(1),
    phoneNo varchar(20),
    
    FOREIGN KEY (departmentId) REFERENCES department(departmentId)
);

CREATE TABLE class(
	classId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	staffId int NOT NULL,
    courseId int NOT NULL,
    
    FOREIGN KEY (staffId) REFERENCES staff(staffId),
    FOREIGN KEY (courseId) REFERENCES course(courseId)
);

CREATE TABLE student(
	studentId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    studentName varchar(100) NOT NULL,
    gender char(1) NOT NULL,
    programId int,
    DOB date NOT NULL,
    entryDate date NOT NULL,
    phoneNo varchar(20),
    email varchar(320),
    gpa double,
    
    FOREIGN KEY (programId) REFERENCES program(programId)
);

CREATE TABLE enrollment(
	enrollId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    classId int NOT NULL,
    studentId int NOT NULL,
    enrollDate date NOT NULL,
    enrollAvailable date NOT NULL,
    
    FOREIGN KEY (classId) REFERENCES class(classId),
    FOREIGN KEY (studentId) REFERENCES student(studentId)
);

CREATE TABLE `schedule`(
	scheduleId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    enrollId int NOT NULL,
    `day` varchar(20) NOT NULL,
    `time` time NOT NULL,
    
    FOREIGN KEY (enrollId) REFERENCES enrollment(enrollId)
);
