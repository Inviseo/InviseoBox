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

async def fetchDataFromModbusDevice(client, instrument):
    measurements=instrument["measurements"]
    
    for measurement in measurements:
        # Récupération du nom de la mesure
        measurement_id = measurement["id"]
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
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("INSERT INTO measurements (measurement_id, measurement, value, date) VALUES (?, ?, ?, datetime('now'))", (instrument["id"], measurement_id, decoded_response))
            conn.commit()

async def run(instrument):
    configuration = instrument["communication"]["configuration"]
    
    serial_port = configuration["serial_port"]
    stopbits=configuration["stopbits"]
    bytesize=configuration["bytesize"]
    parity=configuration["parity"]
    baudrate=configuration["baudrate"]

    # Initier la connexion avec le dispositif Modbus
    client = AsyncModbusSerialClient(method='rtu', port=serial_port, stopbits=stopbits, bytesize=bytesize, parity=parity, baudrate=baudrate, timeout=1)
    await client.connect()

    # Appeler fetchData pour chaque instrument
    await fetchDataFromModbusDevice(client, instrument)

    client.close()

def fetchDataFromWebService(instrument):
    url = instrument["communication"]["configuration"]["url"]
    # Faire la requête HTTP
    response = requests.get(url)
    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
    for measurement in instrument["measurements"]:
        measurement_id = measurement["id"]
        measurement_configuration = measurement["configuration"]
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO measurements (measurement_id, measurement, value, date) VALUES (?, ?, ?, datetime('now'))", (instrument["id"], measurement_id, response.json()[measurement_configuration["parameters"]["key"]]))
        conn.commit()
        

def sendMeasurementToAPI(instrument):
    for measurement in instrument["measurements"]:
        measurement_id = measurement["id"]
        measurement_configuration = measurement["configuration"]
        if "min" in measurement_configuration["response_format"]:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            min_value = c.execute("SELECT MIN(value) FROM measurements WHERE measurement = ?", (measurement_id,)).fetchone()[0]
            # Sera à remplacer par une requête HTTP POST
            print(f"La valeur minimale de la mesure {measurement_id} est {min_value}")
            # L'écrire dans un  fichier txt
            with open("./outputsInTxt/min_values.txt", "a") as f:
                f.write(f"La valeur minimale de la mesure {measurement_id} est {min_value}\n")
            
        if "max" in measurement_configuration["response_format"]:
            max_value = c.execute("SELECT MAX(value) FROM measurements WHERE measurement = ?", (measurement_id,)).fetchone()[0]
            # Sera à remplacer par une requête HTTP POST
            print(f"La valeur maximale de la mesure {measurement_id} est {max_value}")
            with open("./outputsInTxt/max_values.txt", "a") as f:
                f.write(f"La valeur maximale de la mesure {measurement_id} est {max_value}\n")
                
            
        if "avg" in measurement_configuration["response_format"]:
            avg_value = c.execute("SELECT AVG(value) FROM measurements WHERE measurement = ?", (measurement_id,)).fetchone()[0]
            # Sera à remplacer par une requête HTTP POST
            print(f"La valeur moyenne de la mesure {measurement_id} est {avg_value}")
            with open("./outputsInTxt/avg_values.txt", "a") as f:
                f.write(f"La valeur moyenne de la mesure {measurement_id} est {avg_value}\n")
                
        if "diff" in measurement_configuration["response_format"]:
            first_value = c.execute("SELECT value FROM measurements WHERE measurement = ? ORDER BY date ASC LIMIT 1", (measurement_id,)).fetchone()[0]
            last_value = c.execute("SELECT value FROM measurements WHERE measurement = ? ORDER BY date DESC LIMIT 1", (measurement_id,)).fetchone()[0]
            diff_value = last_value - first_value
            # Sera à remplacer par une requête HTTP POST
            print(f"La différence entre la première et la dernière valeur de la mesure {measurement_id} est {diff_value}")
            
            with open("./outputsInTxt/diff_values.txt", "a") as f:
                f.write(f"La différence entre la première et la dernière valeur de la mesure {measurement_id} est {diff_value}\n")
                

# Fonction pour exécuter une tâche en boucle pendant 30 minutes
def run_for_30_minutes():
    
    if os.path.exists('data.db'):
        os.remove('data.db')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS measurements (id INTEGER PRIMARY KEY AUTOINCREMENT, measurement_id INTEGER, measurement TEXT, value REAL, date TEXT)")
    conn.commit()

    with open('./datasource.json') as f:
        data = json.load(f)

    instruments = data["instruments"]
    start_time = time.time()
    while time.time() - start_time < 60 :  # Boucle pendant 30 minutes
        # Récupération des données depuis les instruments
        for instrument in instruments:
            if instrument["communication"]["protocol"] == "Modbus" and instrument["communication"]["mode"] == "RTU" and instrument["communication"]["type"] == "RS-485":
                asyncio.run(run(instrument))
            elif instrument["communication"]["protocol"] == "WebService":
                fetchDataFromWebService(instrument)
        time.sleep(1)  # Attente d'une seconde pour éviter une utilisation excessive du processeur
        
    # Envoi des données à l'API
    for instrument in instruments:
        sendMeasurementToAPI(instrument)

    conn.close()

if __name__ == '__main__':


    # Planification de l'exécution du programme toutes les 10 secondes
    schedule.every(1).minutes.do(run_for_30_minutes)

    # Exécution de la première partie du programme
    run_for_30_minutes()

    # Exécution du programme planifié
    while True:
        schedule.run_pending()
        time.sleep(1)