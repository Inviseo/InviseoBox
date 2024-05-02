from SQLiteDatabase import SQLiteDatabase
from ModbusDevice import SerialRTUModbusDevice
from WebServiceDevice import WebServiceDevice
from Logger import Logger  # Importe la classe Logger

# Variables d'environnement
from dotenv import load_dotenv
import os

# Scheduler
import time
import asyncio

# Requêtes HTTP
import requests

# Crée une instance de la classe Logger
logger = Logger()

def get_token(url, email, password):
    try:
        payload = {"email": email, "password": password}
        response = requests.post(f"{url}/auth/login", json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.log_error(f"Une erreur HTTP s'est produite lors de la récupération du token: {err}")
        return None
    except Exception as e:
        logger.log_error(f"Une erreur s'est produite lors de la récupération du token: {e}")
        return None
    data = response.json()
    if "token" in data:
        return data["token"]
    else:
        logger.log_error("Token non trouvé dans la réponse")
        return None

def get_devices(url, token, worker_id):
    try:
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        devices = requests.get(f"{url}/workers/devices?id={worker_id}", headers=headers)
        devices.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.log_error(f"Une erreur HTTP s'est produite lors de la récupération des appareils: {err}")
        return None
    except Exception as e:
        logger.log_error(f"Une erreur s'est produite lors de la récupération des appareils: {e}")
        return None
    return devices.json()

def send_data(url, token, fields_data):
    try:
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        response = requests.post(f"{url}/fields/bulk", headers=headers, json=fields_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.log_error(f"Une erreur HTTP s'est produite lors de l'envoi des données: {err}")
    except Exception as e:
        logger.log_error(f"Une erreur s'est produite lors de l'envoi des données: {e}")

async def scheduled_main_loop(url, email, password, worker_id):
    logger.log_info("Démarrage du programme")
    start_time = time.time()
    
    # Récupération du token d'authentification
    token = get_token(url, email, password)
    if token is None:
        return

    # Création de la base de données
    database = SQLiteDatabase("data.db")

    # Récupération des appareils
    devices = get_devices(url, token, worker_id)
    if devices is None:
        return
    
    while time.time() - start_time < 1800:
        for device in devices:
            if device["communication"]["protocol"] == "Modbus":
                if device["communication"]["mode"] == "RTU":
                    try:
                        modbus_device = SerialRTUModbusDevice(**device["communication"]["configuration"])
                        await modbus_device.connect()

                        for measurement in device["measurements"]:
                            try:
                                value = await modbus_device.read(**measurement["configuration"]["parameters"])
                                database.insert_data(measurement["_id"], value)
                            except Exception as e:
                                logger.log_error(f"Une erreur s'est produite lors de la lecture des données Modbus: {e}")
                    except Exception as e:
                        logger.log_error(f"Une erreur s'est produite lors de la connexion à l'appareil Modbus: {e}")

                    try:
                        await modbus_device.disconnect()
                    except Exception as e:
                        logger.log_error(f"Une erreur s'est produite lors de la déconnexion de l'appareil Modbus: {e}")
            if device["communication"]["protocol"] == "WebService":
                web_service_device = WebServiceDevice(device["communication"]["configuration"]["url"])
                try:
                    data = web_service_device.getData()
                    for measurement in device["measurements"]:
                        try:
                            value = data[measurement["configuration"]["parameters"]["key"]]
                            database.insert_data(measurement["_id"], value)
                        except Exception as e:
                            logger.log_error(f"Une erreur s'est produite lors de la récupération des données du service Web: {e}")
                except Exception as e:
                    logger.log_error(f"Une erreur s'est produite lors de la connexion au service Web: {e}")
                    
    # Envoi des données à l'API
    fields_data = {"fields": []}

    for device in devices:
        for measurement in device["measurements"]:
            measurement_id = measurement["_id"]
            measurement_configuration = measurement["configuration"]
            response = {}

            if "min" in measurement_configuration["response_format"]:
                try:
                    min_value = database.execute(f"SELECT MIN(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["min"] = str(min_value)
                except Exception as e:
                    logger.log_error(f"Une erreur s'est produite lors de la récupération de la valeur minimale: {e}")

            if "max" in measurement_configuration["response_format"]:
                try:
                    max_value = database.execute(f"SELECT MAX(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["max"] = str(max_value)
                except Exception as e:
                    logger.log_error(f"Une erreur s'est produite lors de la récupération de la valeur maximale: {e}")

            if "avg" in measurement_configuration["response_format"]:
                try:
                    avg_value = database.execute(f"SELECT AVG(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["avg"] = str(avg_value)
                except Exception as e:
                    logger.log_error(f"Une erreur s'est produite lors de la récupération de la valeur moyenne: {e}")

            if "diff" in measurement_configuration["response_format"]:
                try:
                    first_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY date ASC LIMIT 1")[0][0]
                    last_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY date DESC LIMIT 1")[0][0]
                    diff_value = last_value - first_value
                    response["diff"] = str(diff_value)
                except Exception as e:
                    logger.log_error(f"Une erreur s'est produite lors de la récupération de la différence de valeur: {e}")

            fields_data["fields"].append({"measurement": measurement_id, "value": response})
    send_data(url, token, fields_data)

async def main_execution_thread():
    try:
        load_dotenv()
        url = os.getenv("url")
        email = os.getenv("email")
        password = os.getenv("password")
        worker_id = os.getenv("worker_id")

        while True:
            await scheduled_main_loop(url, email, password, worker_id)
    except Exception as e:
        logger.log_error(f"Une erreur s'est produite lors de l'exécution du programme: {e}")

if __name__ == "__main__":
    asyncio.run(main_execution_thread())
