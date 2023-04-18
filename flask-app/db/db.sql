DROP TABLE IF EXISTS Students, Faculty, Admins, Courses, Classes;

CREATE TABLE Students
(
  StudentID INT NOT NULL AUTO_INCREMENT,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL,
  Address TEXT NOT NULL,
  Phone_Number NUMERIC(10) NOT NULL,
  Email TEXT NOT NULL,
  PRIMARY KEY (StudentID)
);

CREATE TABLE Faculty
(
  FacultyID INT NOT NULL AUTO_INCREMENT,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL,
  Address TEXT NOT NULL,
  Phone_Number NUMERIC(10) NOT NULL,
  Email TEXT NOT NULL,
  PRIMARY KEY (FacultyID)
);

CREATE TABLE Admins
(
  AdminID INT NOT NULL AUTO_INCREMENT,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL,
  PRIMARY KEY (AdminID)
);

CREATE TABLE Courses
(
  CourseID INT NOT NULL AUTO_INCREMENT,
  Code Text NOT NULL,
  Major TEXT NOT NULL,
  Title TEXT NOT NULL,
  Semester TEXT NOT NULL,
  Prerequisites INT,
  PRIMARY KEY (CourseID),
  FOREIGN KEY (Prerequisites) REFERENCES Courses(CourseID)
);

CREATE TABLE Classes
(
  ClassID INT NOT NULL AUTO_INCREMENT,
  CourseID INT NOT NULL,
  SeatsAvailable INT NOT NULL,
  PRIMARY KEY (ClassID),
  FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);