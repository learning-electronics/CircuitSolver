CREATE DATABASE CIRCUITDB;
CREATE USER ele;
GRANT ALL ON CIRCUITDB.* TO 'ele'@'localhost' IDENTIFIED BY 'Itsucks2022!';

USE CIRCUITDB;

CREATE TABLE CHAPTER(
	ID INTEGER,
	Name VARCHAR(40),
	PRIMARY KEY(ID));

CREATE TABLE SUBCHAPTER(
	SubChapID INTEGER,
	ChapID INTEGER,
	Name VARCHAR(40),
	PRIMARY KEY(SubChapID,ChapID),
	FOREIGN KEY(ChapID) REFERENCES CHAPTER(ID));

CREATE TABLE CIRCUIT(
	ID INTEGER,
	SpicePath VARCHAR(100),
	ImagePath VARCHAR(100),
	BaseRes VARCHAR(10000),
	BaseEnu VARCHAR(1000),
	PRIMARY KEY(ID));

CREATE TABLE EXERCISE(
	ID INTEGER,
	CircuitID INTEGER,
	Type CHAR,
	CompName VARCHAR(10),
	CorrectSol VARCHAR(100),
	WrongAns1 VARCHAR(100),
	WrongAns2 VARCHAR(100),
	WrongAns3 VARCHAR(100),
	SpecificRes VARCHAR(5000),
	SubChapID INTEGER,
	ChapID INTEGER,
	PRIMARY KEY(ID),
	FOREIGN KEY(CircuitID) REFERENCES CIRCUIT(ID),
	FOREIGN KEY(SubChapID) REFERENCES SUBCHAPTER(SubChapID),
	FOREIGN KEY(ChapID) REFERENCES SUBCHAPTER(ChapID));

delimiter //
CREATE PROCEDURE sp_CreateExercise(
	IN cid INTEGER,
	IN type CHAR,
	IN cn VARCHAR(10),
	IN cs VARCHAR(100),
	IN wa1 VARCHAR(100),	
	IN wa2 VARCHAR(100),	
	IN wa3 VARCHAR(100),	
	IN sr VARCHAR(5000))
BEGIN
	DECLARE nextId INTEGER;
	START TRANSACTION;
	SET @nextId = (SELECT ID 
					FROM EXERCISE 
					ORDER BY ID DESC 
					LIMIT 1);	

	SET @nextid = IF(@nextid IS NULL,0,@nextid + 1);

	INSERT INTO EXERCISE(ID,CircuitID,Type,CompName,CorrectSol,WrongAns1,WrongAns2,WrongAns3,SpecificRes) VALUES(@nextID,cid,type,cn,cs,wa1,wa2,wa3,sr);
	COMMIT;

	SELECT @nextId;
END //

delimiter //
CREATE PROCEDURE sp_CreateCircuit( 
	IN sp VARCHAR(100), 
	IN ip VARCHAR(100), 
	IN br VARCHAR(10000), 
	IN be VARCHAR(100))
BEGIN
	DECLARE nextId INTEGER;
	START TRANSACTION;
	SET @nextId = (SELECT ID 
					FROM CIRCUIT 
					ORDER BY ID DESC
					LIMIT 1);	

	SET @nextid = IF(@nextid IS NULL,0,@nextid + 1);
	
	INSERT INTO CIRCUIT(ID,SpicePath,ImagePath,BaseRes,BaseEnu) VALUES(@nextID,sp,ip,br,be);
	COMMIT;

	SELECT @nextId;
END //

delimiter ; //
