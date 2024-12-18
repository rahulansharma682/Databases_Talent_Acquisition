CREATE DATABASE Final_Project;
USE Final_Project;
#DROP DATABASE final_project;
SHOW TABLES;

CREATE TABLE Recruiter(
   ContactPerson  VARCHAR(23) NOT NULL PRIMARY KEY
  ,Contact        VARCHAR(22) NOT NULL
  ,Company        VARCHAR(49) NOT NULL
  ,CompanyProfile VARCHAR(232)
);

CREATE TABLE IF NOT EXISTS Job (
            JobId INT PRIMARY KEY AUTO_INCREMENT,
            Location VARCHAR(255),
            Date VARCHAR(255),
            Experience VARCHAR(255),
            Skills TEXT,
            Title VARCHAR(255),
            ContactPerson VARCHAR(255),
            SalaryRange VARCHAR(255),
            FOREIGN KEY (ContactPerson) REFERENCES Recruiter(ContactPerson)
        );
        
CREATE TABLE IF NOT EXISTS Candidate (
            CandidateId INT PRIMARY KEY AUTO_INCREMENT,
            EdLevel VARCHAR(255),
            Gender VARCHAR(255),
            YearsCoded INT,
            Country VARCHAR(255),
            PreviousSalary INT,
            Skills TEXT
        );

SELECT * FROM Recruiter WHERE ContactPerson = 'Rahul Chemitiganti';