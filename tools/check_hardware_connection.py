"""Verify the configured hardware controller can connect and enter standby."""

import sys

from core.hardware.factory import create_spectrometer_controller


def main() -> int:
    controller = create_spectrometer_controller()
    try:
        print("Connecting to the configured spectrometer controller...")
        if not controller.connect():
            print("Connection failed.")
            return 1
        print("Connection successful; standby commands were acknowledged.")
        return 0
    except Exception as exc:
        print(f"Connection check failed: {exc}")
        return 1
    finally:
        controller.close()


if __name__ == "__main__":
    sys.exit(main())
