-- Creates a database called "UMS_DB"
CREATE DATABASE ums_db;

-- Uses the "UMS_DB" database
USE ums_db;

-- Creates tables
CREATE TABLE department(
	depId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    depName varchar(50) NOT NULL
);

CREATE TABLE course(
	crsId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    crsName varchar(100) NOT NULL,
    credit int
);

CREATE TABLE program(
	prgId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    prgName varchar(50) NOT NULL,
    depId int NOT NULL,
    degree varchar(50) NOT NULL,
    
    FOREIGN KEY (depId) REFERENCES department(depId)
);

CREATE TABLE staff(
	staId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    depId int NOT NULL,
    `name` varchar(100) NOT NULL,
    position varchar(50),
    DOB date NOT NULL,
    gender char(1),
    phoneNo varchar(20),
    
    FOREIGN KEY (depId) REFERENCES department(depId)
);

CREATE TABLE class(
	clsId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	staId int NOT NULL,
    crsId int NOT NULL,
    
    FOREIGN KEY (staId) REFERENCES staff(staId),
    FOREIGN KEY (crsId) REFERENCES course(crsId)
);

CREATE TABLE student(
	stuId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    gender char(1) NOT NULL,
    prgId int,
    DOB date NOT NULL,
    entryDate date NOT NULL,
    phoneNo varchar(20),
    email varchar(320),
    
    FOREIGN KEY (prgId) REFERENCES program(prgId)
);

CREATE TABLE enrollment(
	enrId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    clsId int NOT NULL,
    stuId int NOT NULL,
    enrDate date NOT NULL,
    grade int,
    
    FOREIGN KEY (clsId) REFERENCES class(clsId),
    FOREIGN KEY (stuId) REFERENCES student(stuId)
);

CREATE TABLE `schedule`(
	schId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    enrId int NOT NULL,
    `day` varchar(20) NOT NULL,
    `time` time NOT NULL,
    
    FOREIGN KEY (enrId) REFERENCES enrollment(enrId)
);

