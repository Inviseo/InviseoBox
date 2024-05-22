from SQLiteDatabase import SQLiteDatabase
from ModbusDevice import SerialRTUModbusDevice
from WebServiceDevice import WebServiceDevice

# Variables d'environnement
from dotenv import load_dotenv
import os

# Scheduler
import time
import asyncio

# Logs
from Logger import Logger
logger = Logger()

# API
from API import API

# Gestions des fichiers JSON
import json

# Ajouter ces fonctions pour lire et écrire les fichiers JSON
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def append_to_json_file(file_path, data):
    current_data = load_json_file(file_path)
    current_data.append(data)
    save_json_file(file_path, current_data)

def remove_from_json_file(file_path, data):
    current_data = load_json_file(file_path)
    if data in current_data:
        current_data.remove(data)
        save_json_file(file_path, current_data)

# Initialiser les fichiers JSON
devices_status_file = 'device_status_to_send.json'
fields_file = 'fields_to_send.json'

# Charger les données depuis les fichiers JSON
devices_status_to_send = load_json_file(devices_status_file)
fields_to_send = load_json_file(fields_file)

async def scheduled_main_loop(api, devices):
    logger.info("[main.py] - Début de la boucle principale")
    start_time = time.time()
    # Récupération du token d'authentification
    try:
        api.get_token()
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération du token d'authentification: {e}")
    
    # Création de la base de données
    database = SQLiteDatabase("data.db")

    try:
        devices = api.get_devices()
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
    
    while time.time() - start_time < 1800:
        for device in devices:
            if device["communication"]["protocol"] == "Modbus":
                if device["communication"]["mode"] == "RTU":
                    try:
                        modbus_device = SerialRTUModbusDevice(**device["communication"]["configuration"])
                        await modbus_device.connect()
                        database.insert_device(device["_id"], "ok")
                        for measurement in device["measurements"]:
                            try:
                                value = await modbus_device.read(**measurement["configuration"]["parameters"])
                                database.insert_data(measurement["_id"], value)
                                database.insert_measurement(measurement["_id"], "ok")
                            except Exception as e:
                                logger.warning(f"[main.py] - Une erreur s'est produite lors de la lecture des données Modbus: {e}")
                                database.insert_data(measurement["_id"], None)
                                database.insert_measurement(measurement["_id"], "dead")
                                time.sleep(1)
                    except Exception as e:
                        logger.warning(f"[main.py] - Une erreur s'est produite lors de la connexion de l'appareil Modbus: {e}")
                        for measurement in device["measurements"]:
                            database.insert_data(measurement["_id"], None)
                            database.insert_measurement(measurement["_id"], "dead")
                        database.insert_device(device["_id"], "dead")
                        time.sleep(1)
                    try:
                        await modbus_device.disconnect()
                    except Exception as e:
                        logger.error(f"[main.py] - Une erreur s'est produite lors de la déconnexion de l'appareil Modbus: {e}")
            if device["communication"]["protocol"] == "WebService":
                web_service_device = WebServiceDevice(device["communication"]["configuration"]["url"])
                try:
                    success, data = web_service_device.getData()
                    if success:
                        database.insert_device(device["_id"], "ok")
                        for measurement in device["measurements"]:
                            try:
                                value = data[measurement["configuration"]["parameters"]["key"]]
                                database.insert_data(measurement["_id"], value)
                                database.insert_measurement(measurement["_id"], "ok")
                            except Exception as e:  
                                logger.warning(f"[main.py] - Une erreur s'est produite lors de la récupération des données du service Web: {e}")
                                database.insert_data(measurement["_id"], None)
                                database.insert_measurement(measurement["_id"], "dead")
                                time.sleep(1)
                    else:
                        database.insert_device(device["_id"], "dead")
                        for measurement in device["measurements"]:
                            database.insert_data(measurement["_id"], None)
                            database.insert_measurement(measurement["_id"], "dead")
                        logger.warning(f"[main.py] - Une erreur s'est produite lors de la récupération des données du service Web")
                except Exception as e:
                    logger.warning(f"[main.py] - Une erreur s'est produite lors de la récupération des données du service Web: {e}")
                    for measurement in device["measurements"]:
                        database.insert_data(measurement["_id"], None)
                        database.insert_measurement(measurement["_id"], "dead")
                    database.insert_device(device["_id"], "dead")
                    time.sleep(1)

    devices_status = {"devices": []}

    for device in devices:
        device_id = device["_id"]
        
        device_status_list = database.execute(f"SELECT status FROM devices WHERE _id = '{device_id}'")
        device_status_list = [status[0] for status in device_status_list]
        # S'il n'y a que des "ok" dans la liste des status, alors le status de l'appareil est "ok"
        if all(status == "ok" for status in device_status_list):
            device_status = "ok"
        # S'il n'y a que des "dead" dans la liste des status, alors le status de l'appareil est "dead"
        elif all(status == "dead" for status in device_status_list):
            device_status = "dead"
        # Sinon, le status de l'appareil est "partial"
        else:
            device_status = "partial"

        measurements_status = []
        for measurement in device["measurements"]:
            measurement_id = measurement["_id"]
            measurements_status_list = database.execute(f"SELECT status FROM measurements WHERE _id = '{measurement_id}'")
            measurements_status_list = [status[0] for status in measurements_status_list]
            # S'il n'y a que des "ok" dans la liste des status, alors le status de la mesure est "ok"
            if all(status == "ok" for status in measurements_status_list):
                measurement_status = "ok"
            # S'il n'y a que des "dead" dans la liste des status, alors le status de la mesure est "dead"
            elif all(status == "dead" for status in measurements_status_list):
                measurement_status = "dead"
            # Sinon, le status de la mesure est "partial"
            else:
                measurement_status = "partial"
            measurements_status.append({"_id": measurement_id, "status": measurement_status})
        devices_status["devices"].append({"_id": device_id, "status": device_status, "measurements": measurements_status})

    # Envoi des statuts des appareils
    devices_status_to_send.append(devices_status)
    append_to_json_file(devices_status_file, devices_status)
    try:
        for status in devices_status_to_send:
            api.send_devices_status(status)
            devices_status_to_send.remove(status)
            remove_from_json_file(devices_status_file, status)
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'envoi de l'état des appareils: {e}")

    fields = {"fields": []}

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
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la valeur minimale: {e}")

            if "max" in measurement_configuration["response_format"]:
                try:
                    max_value = database.execute(f"SELECT MAX(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["max"] = str(max_value)
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la valeur maximale: {e}")

            if "avg" in measurement_configuration["response_format"]:
                try:
                    avg_value = database.execute(f"SELECT AVG(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["avg"] = str(avg_value)
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la valeur moyenne: {e}")

            if "diff" in measurement_configuration["response_format"]:
                try:
                    first_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY timestamp ASC LIMIT 1")[0][0]
                    last_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY timestamp DESC LIMIT 1")[0][0]                    # Si last_value et first_value sont des nombres, on peut calculer la différence
                    # Si last_value et first_value sont des nombres, on peut calculer la différence
                    if not isinstance(first_value, (int, float)) or not isinstance(last_value, (int, float)):
                        response["diff"] = None
                    diff_value = last_value - first_value
                    response["diff"] = str(diff_value)
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la différence de valeur: {e}")

            # Ajouter les valeurs à envoyer
            if "min" in response:
                if response["min"]:
                    fields["fields"].append({"measurement": measurement_id, "value": response, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")})
            if "diff" in response:
                if response["diff"]:
                    fields["fields"].append({"measurement": measurement_id, "value": response, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")})

    fields_to_send.append(fields)
    append_to_json_file(fields_file, fields)
    try:
        for field in fields_to_send:
            api.send_fields(field)
            fields_to_send.remove(field)
            remove_from_json_file(fields_file, field)
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'envoi des champs: {e}")

    await scheduled_main_loop(api, devices)

async def main_execution_thread():
    try:
        load_dotenv()
        api = API(os.getenv("url"), os.getenv("email"), os.getenv("password"), os.getenv("worker_id"), logger)
        api.get_token()
        devices = api.get_devices()
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'initialisation de l'API: {e}")
        time.sleep(5)
        await main_execution_thread()
    
    try:
        await scheduled_main_loop(api, devices)
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'exécution de la boucle principale: {e}")

if __name__ == "__main__":
    asyncio.run(main_execution_thread())
