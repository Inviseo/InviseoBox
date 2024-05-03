import sqlite3
import os
from Logger import Logger
import time

class SQLiteDatabase:
    def __init__(self, db_name, logger=Logger()):
        self.logger = logger
        if os.path.exists(db_name):
            os.remove(db_name)
        self.db_name = db_name

        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            # TABLE devices
            # _id: UUID de l'appareil (issue de MongoDB)
            # status: Statut de l'appareil (ok, dead)
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS devices (_id TEXT, status TEXT)"
            )
            # TABLE measurements
            # id: UUID de la mesure (issue de MongoDB)
            # status: Statut de la mesure (ok, dead)
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS measurements (_id TEXT, status TEXT)"
            )
            # TABLE fields
            # measurement: ID de la mesure (issue de MongoDB)
            # value: Valeur de la mesure
            # date: Date de la mesure, gérée par SQLite
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS fields (measurement TEXT, value REAL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )

            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.log_error(f"[SQLiteDatabase.py] - Une erreur s'est produite lors de la connexion à la base de données: {e}")

    def __del__(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            self.logger.log_error(f"[SQLiteDatabase.py] - Une erreur s'est produite lors de la fermeture de la base de données: {e}")

    def insert_device(self, device_id, status):
        try:
            self.cursor.execute("INSERT INTO devices (_id, status) VALUES (?, ?)", (device_id, status))
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.log_error(f"[SQLiteDatabase.py] - Une erreur s'est produite lors de l'insertion ou de la mise à jour de l'appareil: {e}")
    
    def insert_measurement(self, measurement_id, status):
        try:
            self.cursor.execute("INSERT INTO measurements (_id, status) VALUES (?, ?)", (measurement_id, status))
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.log_error(f"[SQLiteDatabase.py] - Une erreur s'est produite lors de l'insertion ou de la mise à jour de la mesure: {e}")

    def insert_data(self, measurement, value):
        try:
            self.cursor.execute("INSERT INTO fields (measurement, value) VALUES (?, ?)", (measurement, value))
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.log_error(f"[SQLiteDatabase.py] - Une erreur s'est produite lors de l'insertion des données: {e}")

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.log_error(f"[SQLiteDatabase.py] - Une erreur s'est produite lors de l'exécution de la requête: {e}")
            return None