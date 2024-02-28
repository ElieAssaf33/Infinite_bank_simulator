INSERT INTO Balance(id,Balance) 
    VALUES(1,1000000);

CREATE TABLE IF NOT EXISTS Balance(
id INTEGER PRIMARY KEY AUTOINCREMENT, 
Balance INTEGER DEFAULT 0 CHECK(Balance >= 0))

DROP TABLE Loans



CREATE TABLE Test(test DECIMAL(10,3);

INSERT INTO Test(test)
VALUES(1388.4444)

CREATE TABLE mytable ( id INT, amount DECIMAL(4,2) ); 

INSERT INTO mytable(id, amount)
VALUES(1, 333.3323333)

DELETE FROM Loans

CREATE TABLE IF NOT EXISTS Loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Loan TEXT UNIQUE,
        Amount INTEGER,
        Monthly INTEGER,
        Period INTEGER,
        Interest INTEGER,
        Period_left INTEGER,
        Amount_left INTEGER CHECK(Amount_left >=0),
        Created_at DATE);

CREATE TABLE IF NOT EXISTS Transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
Name TEXT,
Action TEXT ,
Amount INTEGER,
Cash INTEGER,
Current INTEGER,
Date DATE);

UPDATE Transactions SET Cash  = "-" WHERE Cash IS NULL

SELECT Monthly from Loans where Loan = 'Another'
DROP TABLE Loans
CREATE TABLE IF NOT EXISTS Loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Loan TEXT UNIQUE,
        Amount INTEGER,
        Monthly INTEGER,
        Period INTEGER,
        Interest INTEGER,
        Period_left INTEGER,
        Amount_left INTEGER CHECK(Amount_left >0),
        Created_at DATE

);