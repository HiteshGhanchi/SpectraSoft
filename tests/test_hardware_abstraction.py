import unittest

from core.hardware.attenuator_programmer import AttenuatorProgrammer
from import_data.constants import ELEMENT_CHANNEL_COUNT, UART_BAUD_RATE
from core.hardware.interfaces.spectrometer import SpectrometerController
from core.hardware.protocols.uart_protocol import UARTSpectrometerController
from core.hardware.sequence_engine import SequenceEngine
from core.hardware.transports.uart_transport import UARTTransport


class FakeController:
    def __init__(self):
        self.calls = []

    def connect(self):
        self.calls.append(("connect",))
        return True

    def reset(self):
        self.calls.append(("reset",))
        return True

    def argon_purge(self, purge_sec):
        self.calls.append(("argon_purge", purge_sec))
        return True

    def prespark(self, source_code, preburn_ms):
        self.calls.append(("prespark", source_code, preburn_ms))
        return True

    def integrate(self, integ_ms, elements):
        self.calls.append(("integrate", integ_ms, elements))
        return {element["ele"]: 123 for element in elements}

    def clean(self, clean_ms):
        self.calls.append(("clean", clean_ms))
        return True

    def shutdown(self):
        self.calls.append(("shutdown",))
        return True

    def set_attenuator(self, itg_no, att_value):
        self.calls.append(("set_attenuator", itg_no, att_value))
        return True

    def close(self):
        self.calls.append(("close",))


class FakeTransport:
    def __init__(self):
        self.commands = []
        self.connected = False

    def connect(self, endpoint=None):
        self.connected = True
        return True

    def write_line(self, command):
        self.commands.append(command)
        return True

    def read_line(self, timeout=1.0):
        return "K"

    def clear_buffers(self):
        pass

    def close(self):
        self.connected = False


class ADCTransport(FakeTransport):
    def read_line(self, timeout=1.0):
        if self.commands and self.commands[-1] == "I":
            return "D,123"
        return "K"


class HardwareAbstractionTests(unittest.TestCase):
    def test_sequence_engine_uses_semantic_controller_operations(self):
        controller = FakeController()
        engine = SequenceEngine(controller)

        result = engine.execute_integration(
            25,
            [{"seq": "1", "itg": 1, "ele": "Fe"}],
        )

        self.assertEqual(result, {"Fe": 123})
        self.assertEqual(controller.calls[0][0], "integrate")

    def test_attenuator_programmer_does_not_know_protocol_commands(self):
        controller = FakeController()
        programmer = AttenuatorProgrammer(controller)

        count = programmer.program_all([{"itg_no": 1, "att_value": 7}])

        self.assertEqual(count, ELEMENT_CHANNEL_COUNT)
        self.assertEqual(controller.calls[0], ("set_attenuator", 1, 7))
        self.assertEqual(controller.calls[1], ("set_attenuator", 2, 0))

    def test_uart_protocol_translates_mcu_operations(self):
        transport = FakeTransport()
        controller = UARTSpectrometerController(transport)

        self.assertTrue(controller.connect())
        self.assertTrue(controller.set_attenuator(1, 7))

        self.assertEqual(
            transport.commands[:4],
            ["O,A,C2", "O,A,9E", "O,A,00", "O,B,16"],
        )
        self.assertEqual(transport.commands[-4:], ["O,A,00", "T,100", "O,A,47", "O,A,47"])

    def test_uart_protocol_keeps_same_element_rows_separate_by_ar_number(self):
        transport = ADCTransport()
        controller = UARTSpectrometerController(transport)

        results = controller.integrate(
            25,
            [
                {"ar_no": 1, "itg": 3, "ele": "FE"},
                {"ar_no": 2, "itg": 8, "ele": "FE"},
            ],
        )

        self.assertEqual(results, {"AR:1": 123, "AR:2": 123})

    def test_uart_protocol_uses_frontend_source_code_directly(self):
        transport = FakeTransport()
        controller = UARTSpectrometerController(transport)

        self.assertTrue(controller.prespark(0xB, 10))

        self.assertEqual(transport.commands, ["O,A,C9", "O,B,5A", "T,10"])

    def test_sequence_engine_parses_hex_source_selection(self):
        self.assertEqual(SequenceEngine._source_code_from_selection("B: Custom"), 0xB)
        self.assertEqual(SequenceEngine._source_code_from_selection("F: Custom"), 0xF)

    def test_uart_transport_matches_mcu_baud_rate(self):
        self.assertEqual(UARTTransport().baud_rate, UART_BAUD_RATE)


if __name__ == "__main__":
    unittest.main()
