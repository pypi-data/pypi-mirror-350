"""Peripherals module.

This module contains embedded peripherals and standards enums.
"""

from ..utils.enums import IntEnumMember


class Peripheral(IntEnumMember):
    """Base peripherals enum class."""


class EmbedPeripherals(Peripheral):
    """Embedded peripherals enum."""

    COORDINATOR = 0
    NODE = 1
    OS = 2
    EEPROM = 3
    EEEPROM = 4
    RAM = 5
    LEDR = 6
    LEDG = 7
    IO = 9
    THERMOMETER = 10
    UART = 12
    FRC = 13
    EXPLORATION = 255


class Standards(Peripheral):
    """Standards peripherals enum."""

    DALI = 74
    BINARY_OUTPUT = 75
    SENSOR = 94
    LIGHT = 113
