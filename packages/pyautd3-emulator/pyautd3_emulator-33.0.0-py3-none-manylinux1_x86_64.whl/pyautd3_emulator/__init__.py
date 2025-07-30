import pyautd3

from pyautd3_emulator.native_methods.autd3capi_emulator import NativeMethods as Emu

from .emulator import Emulator
from .instant import InstantRecordOption
from .range import RangeXYZ
from .recorder import Recorder
from .rms import RmsRecordOption

pyautd3._ext_tracing_init.append(lambda: Emu().emulator_tracing_init())


__all__ = [
    "Emulator",
    "InstantRecordOption",
    "RangeXYZ",
    "Recorder",
    "RmsRecordOption",
]


__version__ = "33.0.0"
