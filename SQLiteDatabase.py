import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, db_name):
        try:
            if os.path.exists(db_name):
                os.remove(db_name)

            self.db_name = db_name
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS fields (id INTEGER PRIMARY KEY AUTOINCREMENT, measurement TEXT, value REAL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print("Erreur lors de la connexion à la base de données:", e)

    def __del__(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print("Erreur lors de la fermeture de la connexion à la base de données:", e)

    def insert_data(self, measurement, value):
        try:
            self.cursor.execute("INSERT INTO fields (measurement, value) VALUES (?, ?)", (measurement, value))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Erreur lors de l'insertion des données:", e)

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Erreur lors de l'exécution de la requête:", e)