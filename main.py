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


# Tableau qui servira à stocker toutes les états des appareils, si jamais on arrive pas à les renvoyer à l'API
devices_status_to_send = []

# Tableau qui servira à stocker toutes les champs (fields) à envoyer à l'API
fields_to_send = []

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

    # Récupération des appareils
    try:
        devices = api.get_devices()
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
    
    while time.time() - start_time < 10:
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
                        database.insert_device(device["_id"], "dead")
                        time.sleep(1)
                    try:
                        await modbus_device.disconnect()
                    except Exception as e:
                        logger.error(f"[main.py] - Une erreur s'est produite lors de la déconnexion de l'appareil Modbus: {e}")
            if device["communication"]["protocol"] == "WebService":
                web_service_device = WebServiceDevice(device["communication"]["configuration"]["url"])
                try:
                    # Afficher l'URL du service Web
                    # print(device["communication"]["configuration"]["url"])
                    data = web_service_device.getData()
                    # print(data)
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
                except Exception as e:

                    logger.warning(f"[main.py] - Une erreur s'est produite lors de la récupération des données du service Web: {e}")
                    database.insert_device(device["_id"], "dead")
                    time.sleep(1)
                    
    devices_status = {"devices": []}

    for device in devices:
        device_id = device["_id"]
        
        device_status_list = database.execute(f"SELECT status FROM devices WHERE _id = '{device_id}'")
        device_status_list = [status[0] for status in device_status_list]
        # S'il n'y a QUE des "ok", alors le statut de l'appareil est "ok"
        if all(status == "ok" for status in device_status_list):
            device_status = "ok"
        # S'il n'y a QUE des "dead", alors le statut de l'appareil est "dead"
        elif all(status == "dead" for status in device_status_list):
            device_status = "dead"
        # S'il y a au moins un "ok" et un "dead", alors le statut de l'appareil est "partial"
        else:
            device_status = "partial"

        measurements_status = []
        for measurement in device["measurements"]:
            measurement_id = measurement["_id"]
            measurements_status_list = database.execute(f"SELECT status FROM measurements WHERE _id = '{measurement_id}'")
            measurements_status_list = [status[0] for status in measurements_status_list]
            # S'il n'y a QUE des "ok", alors le statut de la mesure est "ok"
            if all(status == "ok" for status in measurements_status_list):
                measurement_status = "ok"
            # S'il n'y a QUE des "dead", alors le statut de la mesure est "dead"
            elif all(status == "dead" for status in measurements_status_list):
                measurement_status = "dead"
            # S'il y a au moins un "ok" et un "dead", alors le statut de la mesure est "partial"
            else:
                measurement_status = "partial"
            measurements_status.append({"_id": measurement_id, "status": measurement_status})
        devices_status["devices"].append({"_id": device_id, "status": device_status, "measurements": measurements_status})

    # Envoi de l'état des appareils et mesures (devices) à l'API
    devices_status_to_send.append(devices_status)
    print(devices_status_to_send)
    try:
        for status in devices_status_to_send:
            api.send_devices_status(status)
            devices_status_to_send.remove(status)
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'envoi de l'état des appareils: {e}")

    # Envoi des champs (fields) à l'API
    fields = {"fields": []}

    for device in devices:
        for measurement in device["measurements"]:
            measurement_id = measurement["_id"]
            measurement_configuration = measurement["configuration"]
            response = {}

            if "min" in measurement_configuration["response_format"]:
                try:
                    min_value = database.execute(f"SELECT MIN(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["min"] = min_value
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la valeur minimale: {e}")

            if "max" in measurement_configuration["response_format"]:
                try:
                    max_value = database.execute(f"SELECT MAX(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["max"] = max_value
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la valeur maximale: {e}")

            if "avg" in measurement_configuration["response_format"]:
                try:
                    avg_value = database.execute(f"SELECT AVG(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["avg"] = avg_value
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la valeur moyenne: {e}")

            if "diff" in measurement_configuration["response_format"]:
                try:
                    first_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY timestamp ASC LIMIT 1")[0][0]
                    last_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY timestamp DESC LIMIT 1")[0][0]
                    diff_value = last_value - first_value
                    response["diff"] = diff_value
                except Exception as e:
                    logger.error(f"[main.py] - Une erreur s'est produite lors de la récupération de la différence de valeur: {e}")

            # Ici, si la valeur de la mesure est un nombre, on peut ajouter la mesure à la liste des champs à envoyer à l'API
            # Sinon, on ne l'ajoute pas
            if "min" in response:
                if response["min"] is not None:
                    # "timestamp" au format ISO 8601
                    fields["fields"].append({"measurement": measurement_id, "value": response, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")})
            if "diff" in response:
                if response["diff"] is not None:
                    fields["fields"].append({"measurement": measurement_id, "value": response, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")})

    fields_to_send.append(fields)
    # print(fields_to_send)
    try:
        for field in fields_to_send:
            api.send_fields(field)
            fields_to_send.remove(field)
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
