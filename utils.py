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
    ACTIVE_POWER = "W"
    APPARENT_POWER = "VA"
    REACTIVE_POWER = "VAr"


class ModbusType(Enum):
    FP = "FP"
    HOLDING_REGISTER = "4x"
    INT_16 = "INT16"
