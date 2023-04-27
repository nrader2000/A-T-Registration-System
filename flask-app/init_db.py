import sqlite3

#create db connection
connection = sqlite3.connect('database.db')

#add test data to the connection db
cur = connection.cursor()

#drop tables if they exist
cur.execute("DROP TABLE IF EXISTS Students")
cur.execute("DROP TABLE IF EXISTS Faculty")
cur.execute("DROP TABLE IF EXISTS Admins")
cur.execute("DROP TABLE IF EXISTS Courses")
cur.execute("DROP TABLE IF EXISTS Classes")

#create and insert data into students table
cur.executescript("""
CREATE TABLE Students
(
  StudentID INT PRIMARY KEY,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL,
  Address TEXT NOT NULL,
  Phone_Number NUMERIC(15) NOT NULL,
  Email TEXT NOT NULL
);

INSERT INTO Students VALUES
            (1,'narader','testpass12','Nick Rader','123 Fake Address Dr',3362831617,'narader@ncat.edu'),
            (2,'joorekunrin','testpass98','John Orekunrin','1235 Fake Address Ln',3367864785,'joorekunrin@ncat.edu'),
            (3,'lrachakonda','testpass54','Lakshmi Priya Rachakonda','9567 Fake Address St',3364559923,'lrachakonda@ncat.edu');

""")
#create and insert data into faculty table
cur.executescript("""
CREATE TABLE Faculty
(
  FacultyID INT PRIMARY KEY,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL,
  Address TEXT NOT NULL,
  Phone_Number NUMERIC(15) NOT NULL,
  Email TEXT NOT NULL
);

INSERT INTO Faculty VALUES (1,'kroy','testpass09','Kaushik Roy','48 Fake Address Ln',3367891234,'kroy@ncat.edu');
""")

#create and insert data into admins table
cur.executescript("""
CREATE TABLE Admins
(
  AdminID INT PRIMARY KEY,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL
);

INSERT INTO Admins VALUES (1,'tadmin091','testadminpass09','NCATRS Admin');
""")

#create and insert data into courses table
cur.executescript("""
CREATE TABLE Courses
(
  CourseID INT PRIMARY KEY,
  Code Text NOT NULL,
  Major TEXT NOT NULL,
  Title TEXT NOT NULL,
  Semester TEXT NOT NULL,
  Prerequisites Text
);

INSERT INTO Courses VALUES 
            (1,'COMP620','Computer Science','Information Privacy and Security','Fall2023',NULL),
            (2,'COMP651','Computer Science','Data Analysis Techniques','Fall2023',NULL),
            (3,'COMP710','Computer Science','Software Specification, Analysis, & Design','Spring2024',NULL),
            (4,'COMP725','Computer Science','Software Security Testing','Fall2023',NULL),
            (5,'COMP726','Computer Science','Network Security','Fall2023','COMP620'),
            (6,'COMP727','Computer Science','Secure Software Engineeering','Spring2024',NULL),
            (7,'COMP755','Computer Science','Advanced Operating Systems','Fall2023',NULL),
            (8,'COMP765','Computer Science','Data Mining','Summer2023',NULL),
            (9,'COMP775','Computer Science','Advanced Design and Analysis of Algorithms','Spring2024',NULL),
            (10,'COMP851','Computer Science','Big Data Analytics','Spring2024','COMP651'),
            (11,'ELEN602','Electrical Engineering','Semiconductor Theory & Devices','Fall2023',NULL),
            (12,'ELEN614','Electrical Engineering','Integrated Circuit Fabrication Methods','Summer2023',NULL),
            (13,'GEEN601','General Engineering','Industrial Automation','Summer2023',NULL),
            (14,'GEEN602','General Engineering','Advanced Manufacturing','Fall2023',NULL),
            (15,'MATH607','Mathematics','Theory of Numbers','Fall2023',NULL),
            (16,'MATH701','Mathematics','Theory of Functions of a Real Variable I','Summer2023',NULL),
            (17,'MATH702','Mathematics','Theory of Functions of a Real Variable II','Fall2023','MATH701');
""")

#create and insert data into classes table
cur.executescript("""
CREATE TABLE Classes
(
  ClassID INT PRIMARY KEY,
  CourseID INT NOT NULL,
  SeatsAvailable INT NOT NULL,
  FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

INSERT INTO Classes VALUES
            (1,1,24),(2,1,26),
            (3,2,20),(4,2,22),
            (5,3,30),
            (6,4,21),(7,4,19),
            (8,5,23),
            (9,6,30),
            (10,7,26),
            (11,8,17),(12,8,16),
            (13,9,0),(14,9,1),
            (15,10,30),
            (16,11,30),
            (17,12,18),
            (18,13,4),(19,13,6),
            (20,14,8),(21,14,10),
            (22,15,19),
            (23,16,2),(24,16,7),
            (25,17,21);
""")

#close the connection
connection.commit()
connection.close()
print("DB INITIATED!!!")