import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, db_name):
        if os.path.exists(db_name):
            os.remove(db_name)

        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()