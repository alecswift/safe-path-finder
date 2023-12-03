import sqlite3

def make_database():
    conn = sqlite3.connect('database.sqlite')
    conn.execute('CREATE TABLE database (source TEXT, destination TEXT, path TEXT)')   
    conn.close()

make_database()
