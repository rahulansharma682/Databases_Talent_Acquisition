use final_project;
CREATE TABLE Job_Audit (
    AuditID INT AUTO_INCREMENT PRIMARY KEY,
    JobID INT,
    ActionType VARCHAR(10),
    OldSalaryRange VARCHAR(50),
    NewSalaryRange VARCHAR(50),
    ModifiedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DELIMITER //

CREATE TRIGGER after_job_update
AFTER UPDATE ON Job
FOR EACH ROW
BEGIN
    INSERT INTO Job_Audit (JobID, ActionType, OldSalaryRange, NewSalaryRange)
    VALUES (OLD.JobID, 'UPDATE', OLD.SalaryRange, NEW.SalaryRange);
END;
//

DELIMITER ;

UPDATE Job
SET SalaryRange = '120000-150000'
WHERE JobID = 1;
select * from job_audit;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,  -- Store hashed passwords
    Role ENUM('admin', 'recruiter') NOT NULL
);

SELECT r.ContactPerson, COUNT(DISTINCT j.JobID) AS TotalJobsPosted
FROM Recruiter r
LEFT JOIN Job j ON r.ContactPerson = j.ContactPerson
GROUP BY r.ContactPerson
ORDER BY TotalJobsPosted DESC;


SELECT CandidateID, EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills
FROM Candidate
WHERE Skills LIKE '%s'
AND EdLevel = '%s'
AND YearsCoded >= '%s';

SELECT CandidateID, EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills
FROM Candidate
WHERE Skills LIKE '%Python%'
AND EdLevel = 'Master'
AND YearsCoded >= 3;


SELECT SalaryRange
FROM Job
WHERE Skills LIKE '%Python%';

DESCRIBE Job_Audit;

                    SELECT r.ContactPerson, COUNT(c.CandidateID) AS CandidatesHired
                    FROM Recruiter r
                    JOIN Job j ON r.ContactPerson = j.ContactPerson
                    JOIN Candidate c ON j.JobID = c.JobID
                    GROUP BY r.ContactPerson
                    ORDER BY CandidatesHired DESC;
                    
                    

SELECT *
FROM Job
JOIN Candidate ON Job.JobID = Candidate.JobID;

    
