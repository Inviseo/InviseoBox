from SQLiteDatabase import SQLiteDatabase
from ModbusDevice import SerialRTUModbusDevice
from WebServiceDevice import WebServiceDevice

# Variables d'environnement
from dotenv import load_dotenv
import os

# Scheduler
import time
import asyncio

# Requêtes HTTP
import requests


def get_token(url, email, password):
    try:
        payload = {"email": email, "password": password}
        response = requests.post(f"{url}/auth/login", json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    data = response.json()
    if "token" in data:
        return data["token"]
    else:
        raise SystemExit("Token non trouvé dans la réponse")


def get_devices(url, token, worker_id):
    try:
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        devices = requests.get(f"{url}/workers/devices?id={worker_id}", headers=headers)
        devices.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return devices.json()


def send_data(url, token, fields_data):
    try:
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        response = requests.post(f"{url}/fields/bulk", headers=headers, json=fields_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response.json()

async def scheduled_main_loop(url, email, password, worker_id):
    print("Début de l'exécution du programme")
    start_time = time.time()
    
    # Récupération du token d'authentification
    token = get_token(url, email, password)

    # Création de la base de données
    database = SQLiteDatabase("data.db")

    # Récupération des appareils
    devices = get_devices(url, token, worker_id)

    
    while time.time() - start_time < 9:
        for device in devices:
            if device["communication"]["protocol"] == "Modbus":
                if device["communication"]["mode"] == "RTU":
                    modbus_device = SerialRTUModbusDevice(**device["communication"]["configuration"])
                    await modbus_device.connect()

                    for measurement in device["measurements"]:
                        value = await modbus_device.read(**measurement["configuration"]["parameters"])
                        database.insert_data(measurement["_id"], value)

                    await modbus_device.disconnect()
            if device["communication"]["protocol"] == "WebService":
                web_service_device = WebServiceDevice(device["communication"]["configuration"]["url"])
                try:
                    data = web_service_device.getData()
                    for measurement in device["measurements"]:
                        value = data[measurement["configuration"]["parameters"]["key"]]
                        database.insert_data(measurement["_id"], value)
                except Exception as e:
                    # On ne veut pas que le programme s'arrête si une erreur se produit
                    print(f"Une erreur s'est produite lors de la récupération des données: {e}")
                    
    # Envoi des données à l'API
    fields_data = {"fields": []}

    for device in devices:
        for measurement in device["measurements"]:
            measurement_id = measurement["_id"]
            measurement_configuration = measurement["configuration"]
            response = {}

            if "min" in measurement_configuration["response_format"]:
                min_value = database.execute(f"SELECT MIN(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                response["min"] = str(min_value)

            if "max" in measurement_configuration["response_format"]:
                max_value = database.execute(f"SELECT MAX(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                response["max"] = str(max_value)

            if "avg" in measurement_configuration["response_format"]:
                avg_value = database.execute(f"SELECT AVG(value) FROM fields WHERE measurement = '{measurement_id}'")[0][0]
                response["avg"] = str(avg_value)

            if "diff" in measurement_configuration["response_format"]:
                first_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY date ASC LIMIT 1")[0][0]
                last_value = database.execute(f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY date DESC LIMIT 1")[0][0]
                diff_value = last_value - first_value
                response["diff"] = str(diff_value)

            fields_data["fields"].append({"measurement": measurement_id, "value": response})
    send_data(url, token, fields_data)
    
async def main_execution_thread():
    try:
        load_dotenv()
        url = os.getenv("url_dev")
        email = os.getenv("email")
        password = os.getenv("password")
        worker_id = os.getenv("worker_id")

        while True:
            await scheduled_main_loop(url, email, password, worker_id)
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'exécution du programme: {e}")

if __name__ == "__main__":
    asyncio.run(main_execution_thread())
