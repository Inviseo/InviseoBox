from ModbusDevice import SerialRTUModbusDevice
from SQLiteDatabase import SQLiteDatabase

# Variables d'environnement
from dotenv import load_dotenv
import os

# Scheduler
import time
import asyncio
import schedule

# Requêtes HTTP
import json
import requests
import sqlite3


def getToken(url, email, password):
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
        return None



async def main():

    load_dotenv()
    url = os.getenv("url_dev")
    email = os.getenv("email")
    password = os.getenv("password")
    worker_id = os.getenv("worker_id")

    token = getToken(url, email, password)

    communication_config = {
        "port": "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",
        "stopbits": 1,
        "bytesize": 8,
        "parity": "N",
        "baudrate": 9600
    }
    measurement_config = {
        "register": "0x04",
        "address": 52,
        "slave": 1,
        "count": 2,
        "byte_order": "3-2-1-0",
        "value_class": "FLOAT32"
    }

    device = SerialRTUModbusDevice(**communication_config)
    await device.connect()

    while True:
        value = await device.read(**measurement_config)
        print("Valeur lue:", value)
        await asyncio.sleep(1)

if __name__ == "__main__":


    asyncio.run(main())
