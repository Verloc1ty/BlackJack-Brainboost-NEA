-- CREATE TABLE Subject(
--     SubjectID INT PRIMARY KEY AUTO_INCREMENT,
--     SubjectName VARCHAR(50) NOT NULL,
--     Level VARCHAR(25) NOT NULL
-- );

-- CREATE TABLE Units(
--     UnitID INT PRIMARY KEY,
--     UnitName VARCHAR(50) NOT NULL,
--     SubjectID INT NOT NULL,
--     FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID)
-- );

-- CREATE TABLE Topics(
--     TopicID INT PRIMARY KEY,
--     TopicName VARCHAR(50) NOT NULL,
--     UnitID INT NOT NULL,
--     FOREIGN KEY (UnitID) REFERENCES Units(UnitID)
-- );

-- Create TABLE QUIZ(
--     QuizID INT PRIMARY KEY,
--     QuizName VARCHAR(50) NOT NULL,
--     TopicID INT NOT NULL,
--     FOREIGN KEY (TopicID) REFERENCES Topics(TopicID)
-- );

-- CREATE TABLE Questions(
--     QuestionID INT PRIMARY KEY,
--     Question VARCHAR(255) NOT NULL,
--     Answer1 VARCHAR(255) NOT NULL,
--     Answer2 VARCHAR(255) NOT NULL,
--     Answer3 VARCHAR(255) NOT NULL,
--     Answer4 VARCHAR(255) NOT NULL,
--     QuizID INT NOT NULL,
--     FOREIGN KEY (QuizID) REFERENCES QUIZ(QuizID)
-- );


INSERT INTO Units VALUES (1, 'Unit 1: Measurements and Errors', 1);
INSERT INTO Units VALUES (2, 'Unit 2: Particles & Radiation', 1);
INSERT INTO Units VALUES (3, 'Unit 3: Waves', 1);
INSERT INTO Units VALUES (4, 'Unit 4: Mechanics', 1);
INSERT INTO Units VALUES (5, 'Unit 5: Electricity', 1);
INSERT INTO Units VALUES (6, 'Unit 6: Further Mechanics & Thermal Physics', 1);
INSERT INTO Units VALUES (7, 'Unit 7: Fields & Their Consequences', 1);
INSERT INTO Units VALUES (8, 'Unit 8: Nuclear Physics', 1);