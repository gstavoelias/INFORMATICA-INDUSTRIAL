from enum import Enum

class Units(Enum):
    TEMPERATURE = "°C"
    PRESSURE = "psi"
    SPEED = "m/s"
    FLOW = "m³/h"
    TORQUE = "N.m"
    ROTATION = "RPM"
    VOLTAGE = "V"
    CURRENT = "A"
    POWER = "W"

class ModbusType(Enum):
    FP = "FP"
    HOLDING_REGISTER = "4x"
