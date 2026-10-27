"""Shared domain and hardware constants.

Keep configurable instrument limits here instead of repeating them in UI,
analysis, and hardware modules. UI styling dimensions and algorithm-local
values should remain close to the code that owns them.
"""

# ---------------------------------------------------------------------------
# Analytical-system capacities from the QC-E1 manual
# ---------------------------------------------------------------------------
ELEMENT_CHANNEL_COUNT = 45
ANALYTICAL_CHANNEL_COUNT = 32
SOURCE_CODE_COUNT = 16
SOURCE_CODE_MIN = 0x0
SOURCE_CODE_MAX = SOURCE_CODE_COUNT - 1
DEFAULT_SOURCE_CODE = 0x1
ANALYTICAL_CONDITION_GROUP_COUNT = 20
ANALYTICAL_GROUP_COUNT = 100
WORKING_CURVE_GROUP_COUNT = 5
STANDARD_GROUP_COUNT = 500
ANALYTICAL_SEQUENCE_COUNT = 3
MAX_ANALYSIS_BURNS = 3
MATRIX_CORRECTION_LIMIT = 8
REPRODUCIBILITY_MAX_MEASUREMENTS = 21

# ---------------------------------------------------------------------------
# Persisted field sizes
# ---------------------------------------------------------------------------
ANALYTICAL_GROUP_NAME_MAX_LENGTH = 100
SOURCE_CODE_NAME_MAX_LENGTH = 100
ELEMENT_NAME_MAX_LENGTH = 20
WAVELENGTH_MAX_LENGTH = 20

# ---------------------------------------------------------------------------
# Instrument value ranges
# ---------------------------------------------------------------------------
ATTENUATOR_MIN_VALUE = 0
ATTENUATOR_MAX_VALUE = 63
ATTENUATOR_COMMAND_OFFSET = 0x40
ADC_BIT_COUNT = 12
ADC_MAX_VALUE = (1 << ADC_BIT_COUNT) - 1
ADC_OVERFLOW_RATIO = 0.8
PERCENT_SCALE = 100.0
PURITY_TOTAL_PERCENT = 100.0

# ---------------------------------------------------------------------------
# Installed emission-unit configuration and ATT adjustment guidance
# ---------------------------------------------------------------------------
EMISSION_UNIT_HPSG_300 = "HPSG_300"
EMISSION_UNIT_HVS = "HVS"
DEFAULT_EMISSION_UNIT_TYPE = EMISSION_UNIT_HPSG_300
EMISSION_UNIT_TYPES = (EMISSION_UNIT_HPSG_300, EMISSION_UNIT_HVS)
ATT_ADJUSTMENT_TARGET_MIN = 0.5
ATT_ADJUSTMENT_TARGET_MAX = 0.6
HPSG_300_ADJUSTMENT_SCALE = 2
HPSG_300_ADJUSTMENT_GRADUATION_MIN = 6
HPSG_300_ADJUSTMENT_GRADUATION_MAX = 7
HPSG_300_ADJUSTMENT_INTEGRATION_MS = 4000
HVS_ADJUSTMENT_SCALE = 5
HVS_ADJUSTMENT_GRADUATION_MIN = 4
HVS_ADJUSTMENT_GRADUATION_MAX = 5
HVS_ADJUSTMENT_INTEGRATION_MS = 15000

# ---------------------------------------------------------------------------
# ATmega/CH340 connection settings
# ---------------------------------------------------------------------------
UART_BAUD_RATE = 9600
CH340_VENDOR_ID = 0x1A86
CH340_PRODUCT_ID = 0x7523
DEFAULT_UART_PORT = "COM3"

# ---------------------------------------------------------------------------
# ATmega UART protocol timing
# ---------------------------------------------------------------------------
ELEMENT_SELECT_DELAY_SECONDS = 0.100
ADC_INTER_DELAY_SECONDS = 0.010
ADC_SETTLE_DELAY_SECONDS = 0.100
RESET_HOLD_SECONDS = 0.5
ATTENUATOR_ELEMENT_DELAY_SECONDS = 0.100

# Fixed Port-B control bits appended to the frontend-selected source code.
SOURCE_PORT_CONTROL_BITS = 0b010
