import sqlite3

class Database:
    def __init__(self, name = "Database.db"):
        self.connection = sqlite3.connect(name)
    
    def execute(self, sql, parameters = None):
        cursor = self.connection.cursor()
        if parameters is None:
            cursor.execute(sql)
            fetch = cursor.fetchall()
        else:
            cursor.execute(sql, parameters)
            fetch = cursor.fetchall()
        
        self.connection.commit()
        return fetch
