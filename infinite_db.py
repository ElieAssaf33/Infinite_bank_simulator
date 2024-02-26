import sqlite3

connection = sqlite3.connect('infinite.db')
cursor = connection.cursor()


def create_tables(
        connection: sqlite3.Connection = connection, 
        cursor: sqlite3.Cursor = cursor,
):

    queries = [
        '''
    CREATE TABLE IF NOT EXISTS Investments(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Investment TEXT UNIQUE, 
        Ammount INTEGER DEFAULT 0, 
        Cash INTEGER DEFAULT 0,
        Current INTEGER DEFAULT 0
);
''',
        '''
    CREATE TABLE IF NOT EXISTS Balance(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Balance INTEGER
);      
''',
        '''
    CREATE TABLE IF NOT EXISTS Loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Loan TEXT UNIQUE,
        Ammount Integer,
        Monthly Integer,
        Period Integer,
        Interest Integer,
        Period_left Integer,
        Ammount_left Integer,
        Created_at DATE

);
''',
'INSERT INTO Investments(Investment) VALUES("Bitcoin"), ("Ethereum"), ("Dogecoin");'

    ]
    with connection:
        for query in queries:
            cursor.execute(query)

if __name__ == '__main__':
    create_tables()