import asyncio
from pymodbus.client import AsyncModbusSerialClient
import json
import requests
import sqlite3
import os
import time
import schedule
from struct import pack, unpack


format_map = {
    "FLOAT32": ("f", "2H"),
    "SINGLE": ("f", "2H"),
    "REAL": ("f", "2H"),
    "UNIXTIMEF32": ("f", "2H"),
    "UINT32": ("I", "2H"),
    "DWORD": ("I", "2H"),
    "UNIXTIMEI32": ("I", "2H"),
    "INT32": ("i", "2H"),
    "FLOAT48": ("f", "3H"),
    "INT48": ("q", "3H"),
    "FLOAT64": ("d", "4H"),
    "DOUBLE": ("d", "4H"),
    "FLOAT": ("d", "4H"),
    "LREAL": ("d", "4H"),
    "UNIXTIMEF64": ("d", "4H"),
    "UINT64": ("Q", "4H"),
    "INT64": ("q", "4H"),
    "UNIXTIMEI64": ("q", "4H"),
    "INT16": ("h", "2H"),
    "INT": ("h", "2H"),
    "BCD32": ("f", "2H"),
    "BCD24": ("f", "2H"),
    "BCD16": ("f", "2H"),
}


def decode_value(byte_order, value_class, value):
    value_class_upper = value_class.upper()
    if value_class_upper in format_map:
        target_format, source_format = format_map[value_class_upper]
        if source_format == "2H":
            value = value[0], value[1]
        elif source_format == "3H":
            value = 0, value[0], value[1], value[2]

        if byte_order == "1-0-3-2":
            return unpack(target_format, pack(source_format, *value))[0]
        elif byte_order == "3-2-1-0":
            return unpack(target_format, pack(source_format, *reversed(value)))[0]
        elif byte_order == "0-1-2-3":
            value = [unpack(">H", pack("<H", v))[0] for v in value]
            return unpack(target_format, pack(source_format, *value))[0]
        elif byte_order == "2-3-0-1":
            value = [unpack(">H", pack("<H", v))[0] for v in reversed(value)]
            return unpack(target_format, pack(source_format, *value))[0]

    elif value_class_upper in ["INT16", "INT"]:
        if byte_order in ["1-0-3-2", "3-2-1-0"]:
            return unpack("h", pack("H", value[0]))[0]
        else:
            return unpack(">h", pack("<H", value[0]))[0]
    else:
        return value[0]


def authenticate(email, password):
    url = "http://192.168.3.40:3000/api/auth/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    data = response.json()
    if "token" in data:
        return data["token"]
    else:
        return None


import requests

def getDevicesByWorkerId(token, worker_id):
    url = f"http://192.168.3.40:3000/api/workers/devices?id={worker_id}"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    devices = requests.get(url, headers=headers)
    return devices.json()


async def fetchDataFromModbusDevice(client, device):
    measurements = device["measurements"]

    for measurement in measurements:
        # Récupération du nom de la mesure
        measurement_id = measurement["_id"]
        measurement_configuration = measurement["configuration"]
        parameters = measurement_configuration["parameters"]
        # Lecture des données en fonction du registre spécifié
        register = parameters["register"]
        address = parameters["address"]
        count = parameters["count"]
        slave = parameters["slave"]
        byte_order = parameters["byte_order"]
        value_class = parameters["value_class"]

        match register:
            case "0x01":
                response = await client.read_coils(address, count, slave)
            case "0x02":
                response = await client.read_discrete_inputs(address, count, slave)
            case "0x03":
                response = await client.read_holding_registers(address, count, slave)
            case "0x04":
                response = await client.read_input_registers(address, count, slave)
            case _:
                raise ValueError("Code de registre non reconnu")
        if response.isError():
            raise ValueError("Erreur lors de la lecture des données:", response)
        else:
            decoded_response = decode_value(byte_order, value_class, response.registers)
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO fields (measurement, value) VALUES (?, ?)",
                (measurement_id, decoded_response),
            )
            conn.commit()


async def run(device):
    configuration = device["communication"]["configuration"]

    serial_port = configuration["serial_port"]
    stopbits = configuration["stopbits"]
    bytesize = configuration["bytesize"]
    parity = configuration["parity"]
    baudrate = configuration["baudrate"]

    # Initier la connexion avec le dispositif Modbus
    client = AsyncModbusSerialClient(
        method="rtu",
        port=serial_port,
        stopbits=stopbits,
        bytesize=bytesize,
        parity=parity,
        baudrate=baudrate,
        timeout=1,
    )
    await client.connect()

    # Appeler fetchData pour chaque instrument
    await fetchDataFromModbusDevice(client, device)

    client.close()


def fetchDataFromWebService(device):
    url = device["communication"]["configuration"]["url"]

    # Faire la requête HTTP
    response = requests.get(url)
    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
    for measurement in device["measurements"]:
        measurement_id = measurement["_id"]
        measurement_configuration = measurement["configuration"]
        print(response.json())
        print(measurement_configuration)
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO fields (measurement, value) VALUES (?, ?)",
            (
                measurement_id,
                response.json()[measurement_configuration["parameters"]["key"]],
            ),
        )
        conn.commit()


def sendMeasurementToAPI(token, instruments):
    fields_data = {"fields": []}
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    for instrument in instruments:
        for measurement in instrument["measurements"]:
            measurement_id = measurement["_id"]
            measurement_configuration = measurement["configuration"]
            response = {}

            if "min" in measurement_configuration["response_format"]:
                min_value = c.execute(
                    f"SELECT MIN(value) FROM fields WHERE measurement = '{measurement_id}'"
                ).fetchone()[0]
                response["min"] = str(min_value)

            if "max" in measurement_configuration["response_format"]:
                max_value = c.execute(
                    f"SELECT MAX(value) FROM fields WHERE measurement = '{measurement_id}'"
                ).fetchone()[0]
                response["max"] = str(max_value)

            if "avg" in measurement_configuration["response_format"]:
                avg_value = c.execute(
                    f"SELECT AVG(value) FROM fields WHERE measurement = '{measurement_id}'"
                ).fetchone()[0]
                response["avg"] = str(avg_value)

            if "diff" in measurement_configuration["response_format"]:
                first_value = c.execute(
                    f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY date ASC LIMIT 1"
                ).fetchone()[0]
                last_value = c.execute(
                    f"SELECT value FROM fields WHERE measurement = '{measurement_id}' ORDER BY date DESC LIMIT 1"
                ).fetchone()[0]
                diff_value = last_value - first_value
                response["diff"] = str(diff_value)

            fields_data["fields"].append(
                {"measurement": measurement_id, "value": response}
            )

    url = "http://192.168.3.40:3000/api/fields/bulk"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    print("Envoi des données à l'API...")
    print(json.dumps(fields_data, indent=4))
    response = requests.post(url, headers=headers, json=fields_data)

    conn.close()


# Fonction pour exécuter une tâche en boucle pendant 30 minutes
def run_for_30_minutes():

    if os.path.exists("data.db"):
        # créer le dossier data
        os.remove("data.db")
        
        
        

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS fields (id INTEGER PRIMARY KEY AUTOINCREMENT, measurement TEXT, value REAL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()

    email = "vincent@inviseo.fr"
    password = "runf86lq"
    worker_id = "6616a5167b05eb8969bc7ba8"

    # Authentification et récupération du token
    token = authenticate(email, password)
    if token:
        # Utilisation du token pour obtenir les appareils
        devices = getDevicesByWorkerId(token, worker_id)
    else:
        print("Échec de l'authentification.")

    # print data formaté en JSON
    print("Données récupérées depuis l'API :")
    print(json.dumps(devices, indent=4))

    start_time = time.time()
    while time.time() - start_time < 60:  # Boucle pendant 30 minutes
        # Récupération des données depuis les instruments
        for device in devices:
            if (
                device["communication"]["protocol"] == "Modbus"
                and device["communication"]["mode"] == "RTU"
                and device["communication"]["type"] == "RS-485"
            ):
                asyncio.run(run(device))
            # elif device["communication"]["protocol"] == "WebService":
            #     fetchDataFromWebService(device)
        time.sleep(
            1
        )  # Attente d'une seconde pour éviter une utilisation excessive du processeur

    # Envoi des données à l'API
    sendMeasurementToAPI(token, devices)

    conn.close()


if __name__ == "__main__":

    # Planification de l'exécution du programme toutes les 10 secondes
    schedule.every(1).minutes.do(run_for_30_minutes)

    # Exécution de la première partie du programme
    run_for_30_minutes()

    # Exécution du programme planifié
    while True:
        schedule.run_pending()
        time.sleep(1)
