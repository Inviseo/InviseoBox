import asyncio
from pymodbus.client import AsyncModbusSerialClient
import json
import requests
import sqlite3
import os

if os.path.exists('data.db'):
    os.remove('data.db')
    
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS mesures (id INTEGER PRIMARY KEY AUTOINCREMENT, capteur_id INTEGER, valeur REAL, date TEXT)")
conn.commit()

# Lire le fichier datasource.json
with open('datasource.json') as f:
    data = json.load(f)

# Format du JSON :

# {
#     "capteurs": [
#         {
#             "id": "1",
#             "type": "Modbus",
#             "protocol": "RTU",
#             "serial_port": "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",
#             "configuration": {
#                 "stopbits": 1,
#                 "bytesize": 8,
#                 "parity": "N",
#                 "baudrate": 9600
#             },
#             "adresse": 12,
#             "slave": 2,
#             "count": 1
#         },
#         {
#             "id": "2",
#             "type": "WebService",
#             "url": "http://192.168.3.16/",
#                 "response_format": {
#                     "temp": "float",
#                     "hum": "float",
#                     "CO2": "int"
#             }
#         }
#     ]
# }

list_capteurs = data["capteurs"]

for capteur in list_capteurs:
    if capteur["type"] == "Modbus":
        if capteur["protocol"] == "RTU over RS-485":
            serial_port = capteur["serial_port"]
            stopbits=capteur["configuration"]["stopbits"]
            bytesize=capteur["configuration"]["bytesize"]
            parity=capteur["configuration"]["parity"]
            baudrate=capteur["configuration"]["baudrate"]
            async def run():
                client = AsyncModbusSerialClient(method='rtu', port=serial_port, stopbits=stopbits, bytesize=bytesize, parity=parity, baudrate=baudrate, timeout=1)
                await client.connect()
                print("Connexion au dispositif Modbus établie")
                response = await client.read_input_registers(address=capteur["adresse"], slave=capteur["slave"], count=capteur["count"])
                if response.isError():
                    print("Erreur lors de la lecture des données:", response)
                else:
                    response = response.registers[0]
                    c.execute("INSERT INTO mesures (capteur_id, valeur, date) VALUES (?, ?, datetime('now'))", (capteur["id"], response))
                    conn.commit()
                client.close()
                print("Connexion au dispositif Modbus fermée")
            asyncio.run(run())

    elif capteur["type"] == "WebService":
        url = capteur["url"]
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
            data = response.json()  # Convertit la réponse en JSON
            keys = capteur["response_format"].keys()
            for key in keys:
                c.execute("INSERT INTO mesures (capteur_id, valeur, date) VALUES (?, ?, datetime('now'))", (capteur["id"], data[key]))
                conn.commit()
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion:", e)
            print(response.text)

    else:
        print("Type de capteur non reconnu")