# File: /splang/src/splang/__init__.py
from .interpreter import SplangInterpreter
from .utils import get_last_second, get_first_second, process_ms, get_first_ascii_character
from .opcodes import OPCODES
from .errors import SplangError, SplangWarning, InvalidOpcodeWarning

__version__ = "1.0.9"
__author__ = "Naman Satish"
__all__ = [
    "SplangInterpreter",
    "get_last_second",
    "get_first_second",
    "process_ms",
    "get_first_ascii_character",
    "OPCODES",
    "SplangError",
    "SplangWarning",
    "InvalidOpcodeWarning"
]