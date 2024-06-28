import os
import time
import json
import asyncio
import re
from dotenv import load_dotenv
from SQLiteDatabase import SQLiteDatabase
from ModbusDevice import SerialRTUModbusDevice
from WebServiceDevice import WebServiceDevice
from Logger import Logger
from API import API

logger = Logger()

# JSON file utilities
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

def check_input_data():
    token = os.getenv('token')
    if token is None:
        raise Exception("Le token n'est pas défini.")
    if not re.match(r'^[0-9a-f]{64}$', token):
        raise Exception("Le token doit contenir 32 caractères hexadécimaux.")
    
    interval = os.getenv('interval')
    if interval is None:
        raise Exception("L'intervalle n'est pas défini.")
    if not interval.isdigit() or int(interval) <= 0:
        raise Exception("L'intervalle doit être un entier positif.")

    # Url must be defined and valid
    url = os.getenv('url')
    if url is None:
        raise Exception("L'url n'est pas définie.")
    if not re.match(r'^https?://', url):
        raise Exception("L'url doit commencer par http:// ou https://")


# Initialisation des fichiers de JSON
devices_status_file = 'device_status_to_send.json'
fields_file = 'fields_to_send.json'
devices_status_to_send = load_json_file(devices_status_file)
fields_to_send = load_json_file(fields_file)

async def handle_modbus_device(device, database):
    modbus_device = SerialRTUModbusDevice(**device["communication"]["configuration"], logger=logger)
    try:
        await modbus_device.connect()
        database.insert_device(device["_id"], "ok")
        for measurement in device["measurements"]:
            try:
                value = await modbus_device.read(**measurement["configuration"]["parameters"])
                database.insert_data(measurement["_id"], value)
                database.insert_measurement(measurement["_id"], "ok")
            except Exception as e:
                logger.warning(f"[main.py] - Erreur de récupération des données Modbus: {e}")
                database.insert_data(measurement["_id"], None)
                database.insert_measurement(measurement["_id"], "dead")
                time.sleep(1)
    except Exception as e:
        logger.warning(f"[main.py] - Erreur de communication Modbus: {e}")
        for measurement in device["measurements"]:
            database.insert_data(measurement["_id"], None)
            database.insert_measurement(measurement["_id"], "dead")
        database.insert_device(device["_id"], "dead")
        time.sleep(1)
    finally:
        try:
            await modbus_device.disconnect()
        except Exception as e:
            logger.error(f"[main.py] - Erreur de déconnexion Modbus: {e}")

async def handle_web_service_device(device, database):
    web_service_device = WebServiceDevice(device["communication"]["configuration"]["url"], logger=logger)
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
                    logger.warning(f"[main.py] - Erreur de récupération des données du service web: {e}")
                    database.insert_data(measurement["_id"], None)
                    database.insert_measurement(measurement["_id"], "dead")
                    time.sleep(1)
        else:
            raise Exception("Failed to get data")
    except Exception as e:
        logger.warning(f"[main.py] - Erreur de communication avec le service web: {e}")
        for measurement in device["measurements"]:
            database.insert_data(measurement["_id"], None)
            database.insert_measurement(measurement["_id"], "dead")
        database.insert_device(device["_id"], "dead")
        time.sleep(1)

def determine_device_status(database, device):
    device_id = device["_id"]
    device_status_list = database.execute(f"SELECT status FROM devices WHERE _id = '{device_id}'")
    device_status_list = [status[0] for status in device_status_list]
    if all(status == "ok" for status in device_status_list):
        return "ok"
    elif all(status == "dead" for status in device_status_list):
        return "dead"
    return "partial"

def determine_measurement_status(database, measurement):
    measurement_id = measurement["_id"]
    measurements_status_list = database.execute(f"SELECT status FROM measurements WHERE _id = '{measurement_id}'")
    measurements_status_list = [status[0] for status in measurements_status_list]
    if all(status == "ok" for status in measurements_status_list):
        return "ok"
    elif all(status == "dead" for status in measurements_status_list):
        return "dead"
    return "partial"

def build_devices_status(database, devices):
    devices_status = {"devices": []}
    for device in devices:
        device_status = determine_device_status(database, device)
        measurements_status = [
            {"_id": m["_id"], "status": determine_measurement_status(database, m)}
            for m in device["measurements"]
        ]
        devices_status["devices"].append({"_id": device["_id"], "status": device_status, "measurements": measurements_status})
    return devices_status

def build_fields(database, devices):
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
                    logger.error(f"[main.py] - Erreur de récupération de la valeur minimale: {e}")

            if "max" in measurement_configuration["response_format"]:
                try:
                    max_value = database.execute(f"SELECT MAX(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["max"] = str(max_value)
                except Exception as e:
                    logger.error(f"[main.py] - Erreur de récupération de la valeur maximale: {e}")

            if "avg" in measurement_configuration["response_format"]:
                try:
                    avg_value = database.execute(f"SELECT AVG(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                    response["avg"] = str(avg_value)
                except Exception as e:
                    logger.error(f"[main.py] - Erreur de récupération de la valeur moyenne: {e}")

            if "diff" in measurement_configuration["response_format"]:
                try:
                    first_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY timestamp ASC LIMIT 1")[0][0]
                    last_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY timestamp DESC LIMIT 1")[0][0]
                    if isinstance(first_value, (int, float)) and isinstance(last_value, (int, float)):
                        response["diff"] = str(last_value - first_value)
                    else:
                        response["diff"] = str(None)
                except Exception as e:
                    logger.error(f"[main.py] - Erreur de récupération de la différence: {e}")

            # Ajouter les valeurs à envoyer
            fields["fields"].append({"measurement": measurement_id, "value": response, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")})
    return fields

async def scheduled_main_loop(api, interval=1800):
    logger.info("[main.py] - Début de la boucle principale")
    start_time = time.time()
    database = SQLiteDatabase("data.db", logger=logger)

    # Mettre à jour les devices
    devices = api.get_devices()

    while time.time() - start_time < interval:
        for device in devices:
            if device["communication"]["protocol"] == "Modbus" and device["communication"]["mode"] == "RTU":
                await handle_modbus_device(device, database)
            elif device["communication"]["protocol"] == "WebService":
                await handle_web_service_device(device, database)

    devices_status = build_devices_status(database, devices)
    devices_status_to_send.append(devices_status)
    append_to_json_file(devices_status_file, devices_status)
    try:
        for status in devices_status_to_send:
            if api.send_devices_status(status):
                devices_status_to_send.remove(status)
                remove_from_json_file(devices_status_file, status)
    except Exception as e:
        logger.error(f"[main.py] - Erreur d'envoi du statut des appareils: {e}")

    fields = build_fields(database, devices)
    fields_to_send.append(fields)
    append_to_json_file(fields_file, fields)
    try:
        for field in fields_to_send:
            if api.send_fields(field):
                fields_to_send.remove(field)
                remove_from_json_file(fields_file, field)
    except Exception as e:
        logger.error(f"[main.py] - Erreur d'envoi des données: {e}")

    await scheduled_main_loop(api, interval)

async def main_execution_thread():
    try:
        load_dotenv()
        check_input_data()
        interval = int(os.getenv("interval"))
        api = API(os.getenv("url"), os.getenv("token"), logger=logger)
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'initialisation: {e}")
        time.sleep(5)
        await main_execution_thread()
    
    try:
        await scheduled_main_loop(api, interval)
    except Exception as e:
        logger.error(f"[main.py] - Une erreur s'est produite lors de l'exécution de la boucle principale: {e}")

if __name__ == "__main__":
    asyncio.run(main_execution_thread())
