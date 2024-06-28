from pymodbus import client
from struct import pack, unpack
from Logger import Logger
import time

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


def decodeValue(byte_order, value_class, value):
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


class SerialRTUModbusDevice:
    def __init__(self, port, baudrate, stopbits, bytesize, parity, logger=Logger()):
        self.client = client.AsyncModbusSerialClient(
            method="rtu",
            port=port,
            stopbits=stopbits,
            bytesize=bytesize,
            parity=parity,
            baudrate=baudrate,
            timeout=1,
        )
        self.logger = logger

    async def connect(self):
        try:
            await self.client.connect()
            seconds = 0
            while not self.client.connected:
                time.sleep(1)
                seconds += 1
                if seconds > 3:
                    self.logger.error("[ModbusDevice.py] Le client Modbus a pris trop de temps pour se connecter")
                    raise Exception("[ModbusDevice.py] Le client Modbus a pris trop de temps pour se connecter")
        except Exception as e:
            self.logger.error(f"[ModbusDevice.py] Une erreur s'est produite lors de la connexion du client Modbus: {e}")
    
    async def disconnect(self):
        try:
            self.client.close()
        except Exception as e:
            self.logger.error(f"[ModbusDevice.py] Une erreur s'est produite lors de la déconnexion du client Modbus: {e}")

    async def read(self, register, address, count, slave, byte_order, value_class):
        if not self.client.connected:
            self.logger.error("[ModbusDevice.py] Le client Modbus n'est pas connecté")
        try:
            if register == "0x01":
                value = await self.client.read_coils(address, count, slave)
            elif register == "0x02":
                value = await self.client.read_discrete_inputs(address, count, slave)
            elif register == "0x03":
                value = await self.client.read_holding_registers(address, count, slave)
            elif register == "0x04":
                value = await self.client.read_input_registers(address, count, slave)
            else:
                self.logger.error(f"[ModbusDevice.py] Le registre {register} n'est pas supporté")
            seconds = 0
            while not value:
                time.sleep(1)
                seconds += 1
                if seconds > 3:
                    self.logger.error("[ModbusDevice.py] Le client Modbus a pris trop de temps pour lire les registres")
        except Exception as e:
            self.logger.error(f"[ModbusDevice.py] Une erreur s'est produite lors de la lecture des registres Modbus: {e}")
        try:
            decodedValue = decodeValue(byte_order, value_class, value.registers)
        except Exception as e:
            self.logger.error(f"[ModbusDevice.py] Une erreur s'est produite lors du décodage de la valeur: {e}")

        return decodedValue