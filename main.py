import asyncio
from pymodbus.client import AsyncModbusSerialClient

####
# Chemin du port série
serial_port = "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"

async def run():
    client = AsyncModbusSerialClient(method='rtu', port=serial_port, stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=1)
    await client.connect()
    print("Connexion au dispositif Modbus établie")
    response = await client.read_input_registers(address=12, slave=2, count=1)
    if response.isError():
        print("Erreur lors de la lecture des données:", response)
    else:
        response = response.registers[0]
        print("Données lues depuis le dispositif Modbus:")
        print(response)
            
    client.close()
    print("Connexion au dispositif Modbus fermée")
asyncio.run(run())
