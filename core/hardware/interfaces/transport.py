"""Connection-level interface used by hardware protocol implementations."""

from __future__ import annotations

from typing import Optional, Protocol


class CommandTransport(Protocol):
    """Minimal line transport needed by a hardware protocol."""

    def connect(self, endpoint: Optional[str] = None) -> bool:
        """Open the transport endpoint."""
        ...

    def write_line(self, command: str) -> bool:
        """Write one command line."""
        ...

    def read_line(self, timeout: float = 1.0) -> Optional[str]:
        """Read one response line or return ``None`` on timeout."""
        ...

    def clear_buffers(self) -> None:
        """Discard pending input and output."""
        ...

    def close(self) -> None:
        """Close the transport endpoint."""
        ...
