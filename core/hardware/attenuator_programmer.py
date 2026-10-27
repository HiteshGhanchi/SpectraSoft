"""Program attenuators through the selected spectrometer controller."""

from typing import Dict, List

from import_data.constants import ELEMENT_CHANNEL_COUNT
from core.hardware.interfaces.spectrometer import SpectrometerController


class AttenuatorProgrammer:
    """Programs attenuator values for all 45 master ITG lines."""

    def __init__(self, controller: SpectrometerController):
        self.controller = controller

    def program_all(self, att_rows: List[Dict]) -> int:
        """Program every channel and return the number accepted by the controller."""
        success_count = 0
        att_map = {
            row.get("itg_no", 0): row.get("att_value", 0)
            for row in att_rows
        }

        for itg_no in range(1, ELEMENT_CHANNEL_COUNT + 1):
            att_value = att_map.get(itg_no, 0)
            print(f"  ele{itg_no}: att={att_value}")

            if self.controller.set_attenuator(itg_no, att_value):
                success_count += 1

        return success_count
