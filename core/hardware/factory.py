"""Factories for selecting hardware transports and controllers."""

from __future__ import annotations

import os
from typing import Callable, Dict, Optional

from core.hardware.interfaces.spectrometer import SpectrometerController
from core.hardware.interfaces.transport import CommandTransport
from core.hardware.protocols.uart_protocol import UARTSpectrometerController
from core.hardware.transports.uart_transport import UARTTransport


TransportFactory = Callable[[], CommandTransport]
ControllerFactory = Callable[[], SpectrometerController]


_TRANSPORT_FACTORIES: Dict[str, TransportFactory] = {
    "uart": UARTTransport,
}
_CONTROLLER_FACTORIES: Dict[str, ControllerFactory] = {
    "uart": UARTSpectrometerController,
}


def create_command_transport(kind: Optional[str] = None) -> CommandTransport:
    """Create a configured connection transport.

    ``SPECTRASOFT_HARDWARE_TRANSPORT`` can select a registered transport. New
    connection types can be added by registering another factory here without
    changing analysis or UI code.
    """
    selected = (kind or os.getenv("SPECTRASOFT_HARDWARE_TRANSPORT", "uart")).lower()
    try:
        return _TRANSPORT_FACTORIES[selected]()
    except KeyError as exc:
        supported = ", ".join(sorted(_TRANSPORT_FACTORIES))
        raise ValueError(
            f"Unsupported hardware transport '{selected}'. Supported: {supported}"
        ) from exc


def create_spectrometer_controller(kind: Optional[str] = None) -> SpectrometerController:
    """Create a semantic instrument controller for the selected protocol."""
    selected = (kind or os.getenv("SPECTRASOFT_HARDWARE_PROTOCOL", "uart")).lower()
    if selected == "uart":
        return UARTSpectrometerController(create_command_transport())

    try:
        return _CONTROLLER_FACTORIES[selected]()
    except KeyError as exc:
        supported = ", ".join(sorted(_CONTROLLER_FACTORIES))
        raise ValueError(
            f"Unsupported hardware protocol '{selected}'. Supported: {supported}"
        ) from exc
