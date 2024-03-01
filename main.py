import asyncio
from pymodbus.client import AsyncModbusSerialClient
import json
import requests
import sqlite3
import os

async def fetchDataFromModbusDevice(client, instrument):
    measurements=instrument["measurements"]
    
    for measurement in measurements:
        # Récupération du nom de la mesure
        measurement_name, measurement_details = next(iter(measurement.items()))
        parameters = measurement_details["parameters"]
        
        # Lecture des données en fonction du registre spécifié
        register = parameters["register"]
        address = parameters["address"]
        count = parameters["count"]
        slave = parameters["slave"]
        
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
            response = response.registers[0]
            c.execute("INSERT INTO mesures (capteur_id, mesure, valeur, date) VALUES (?, ?, ?, datetime('now'))", (instrument["id"], measurement_name, response))
            conn.commit()

async def run(instrument):
    configuration = instrument["configuration"]
    
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
    url = instrument["configuration"]["url"]
    # Faire la requête HTTP
    response = requests.get(url)
    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
    for measurement in instrument["measurements"]:
        measurement_name, measurement_details = next(iter(measurement.items()))
        c.execute("INSERT INTO mesures (capteur_id, mesure, valeur, date) VALUES (?, ?, ?, datetime('now'))", (instrument["id"], measurement_name, response.json()[measurement_name]))
        conn.commit()
        
        
def sendMeasurementToAPI(instrument):
    for measurement in instrument["measurements"]:
        measurement_name, measurement_details = next(iter(measurement.items()))
        if "min" in measurement_details["response_format"]:
            min_value = c.execute("SELECT MIN(valeur) FROM mesures WHERE mesure = ?", (measurement_name,)).fetchone()[0]
            # Sera à remplacer par une requête HTTP POST
            print(f"La valeur minimale de la mesure {measurement_name} est {min_value}")
            
        if "max" in measurement_details["response_format"]:
            max_value = c.execute("SELECT MAX(valeur) FROM mesures WHERE mesure = ?", (measurement_name,)).fetchone()[0]
            # Sera à remplacer par une requête HTTP POST
            print(f"La valeur maximale de la mesure {measurement_name} est {max_value}")
            
        if "avg" in measurement_details["response_format"]:
            avg_value = c.execute("SELECT AVG(valeur) FROM mesures WHERE mesure = ?", (measurement_name,)).fetchone()[0]
            # Sera à remplacer par une requête HTTP POST
            print(f"La valeur moyenne de la mesure {measurement_name} est {avg_value}")
        
        if "diff" in measurement_details["response_format"]:
            first_value = c.execute("SELECT valeur FROM mesures WHERE mesure = ? ORDER BY date ASC LIMIT 1", (measurement_name,)).fetchone()[0]
            last_value = c.execute("SELECT valeur FROM mesures WHERE mesure = ? ORDER BY date DESC LIMIT 1", (measurement_name,)).fetchone()[0]
            diff_value = last_value - first_value
            # Sera à remplacer par une requête HTTP POST
            print(f"La différence entre la première et la dernière valeur de la mesure {measurement_name} est {diff_value}")
                
if __name__ == '__main__':
    
    if os.path.exists('data.db'):
        os.remove('data.db')
        
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS mesures (id INTEGER PRIMARY KEY AUTOINCREMENT, capteur_id INTEGER, mesure TEXT, valeur REAL, date TEXT)")
    conn.commit()

    # A remplacer par la lecture des données depuis l'API
    with open('datasource.json') as f:
        data = json.load(f)

    instruments = data["instruments"]

    # Récupération des données depuis les instruments
    for instrument in instruments:
        if instrument["protocol"]=="Modbus":
            if instrument["mode"]=="RTU":
                if instrument["type"]=="RS-485":
                    asyncio.run(run(instrument))
        if instrument["protocol"]=="WebService":
            fetchDataFromWebService(instrument)
            
    # Envoi des données à l'API
    for instrument in instruments:
        sendMeasurementToAPI(instrument)
        
    conn.close()