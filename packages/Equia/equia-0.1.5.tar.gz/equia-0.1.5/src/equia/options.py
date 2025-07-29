""" `options`
"""

from enum import Enum

class FlashType(str, Enum):
    """Allowable flash calculation specifications."""
    FixedTemperaturePressure    = "FixedTemperaturePressure"
    FixedPressureEnthalpy       = "FixedPressureEnthalpy"
    FixedPressureEntropy        = "FixedPressureEntropy"
    FixedTemperatureVolume      = "FixedTemperatureVolume"

class CloudPointType(str, Enum):
    """Allowable cloud point calculation specifications."""
    FixedTemperature    = "FixedTemperature"
    FixedPressure       = "FixedPressure"

class SlePointType(str, Enum):
    """Allowable SLE point calculation specifications."""
    FixedPressure       = "FixedPressure"
    FixedTemperaturePressure    = "FixedTemperaturePressure"
