import asyncio
from ModbusDevice import SerialRTUModbusDevice

async def main():
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
