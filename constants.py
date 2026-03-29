"""
SpectraSoft — Constants
=======================
Two sections:
  1. UI Constants     — confirmed from old software screenshots. Do not change.
  2. Hardware Constants — placeholders. Vivaan fills these from the Excel sheet.
"""

# =============================================================================
# SECTION 1: UI CONSTANTS
# Confirmed from PDAWin old software screenshots. All values verified.
# =============================================================================

APP_NAME = "SpectraSoft"
APP_VERSION = "1.0.0"
DB_FILE = "data.db"  # SQLite file, created next to the .exe automatically

# Window sizes
MAIN_WINDOW_WIDTH = 1100
MAIN_WINDOW_HEIGHT = 700
PAGE_WINDOW_WIDTH = 900
PAGE_WINDOW_HEIGHT = 650

# --- Analytical Condition (Page 1) ---

ANALYTICAL_METHOD_OPTIONS = [
    "P:PDA+Integ. Mode",
    "I:Integration Mode",
]
ANALYTICAL_METHOD_DEFAULT = "P:PDA+Integ. Mode"

# Source dropdown — same list applies to SEQ1, SEQ2, SEQ3, and Clean
SOURCE_OPTIONS = [
    "3 Peak Spark",
    "Normal Spark",
    "Combined Spark",
    "Arclike Spark",
    "Cleaning",
    "High Voltage Spark",
    "AD OFFSET",
    "ITG OFFSET",
    "SH OFFSET",
    "NOISE TEST",
]
SOURCE_DEFAULT_SEQ1  = "3 Peak Spark"
SOURCE_DEFAULT_SEQ2  = "Normal Spark"
SOURCE_DEFAULT_SEQ3  = "Lamp"
SOURCE_DEFAULT_CLEAN = "Cleaning"

# Preburn / Integration clean unit
CLEAN_UNIT_OPTIONS = ["Pulse", "Time"]
CLEAN_UNIT_DEFAULT  = "Pulse"

# Number of sequences (always 3 + Clean)
NUM_SEQUENCES = 3

# Level Cut — H and L level columns (9 values: SEQ1/2/3 for each of 3 monitor elements)
LEVEL_CUT_NUM_VALUES = 9
LEVEL_CUT_DEFAULT    = "0"

# --- Measurement Mode (Page 5) ---

PI_MODE_OPTIONS = [
    "I:Integ.Mode",
    "P:PDA.Mode",
]
PI_MODE_DEFAULT = "P:PDA.Mode"

METHOD_OPTIONS = [
    "0:Integation",
    "2:Distribution",
    "6:Metarographic",
    "9:Interval integration",
    "A:To Get Sampling Count",
    "I:Input For DCA",
]
METHOD_DEFAULT = "9:Interval integration"

AREA_OPTIONS = [
    "S:Spark Area",
    "A:Arc Area",
    "T:Total Area",
]
AREA_DEFAULT = "T:Total Area"

MEASUREMENT_M_DEFAULT = "20"
MEASUREMENT_N_DEFAULT = "80"

# --- Analytical Mode (Page 12) ---

MAGN_OPTIONS = ["75", "100", "125", "150", "200"]
MAGN_DEFAULT  = "125"

ANALYSIS_METHOD_OPTIONS = ["Normal", "4-times analysis"]
ANALYSIS_METHOD_DEFAULT  = "4-times analysis"

RECAL_METHOD_OPTIONS = ["1point Recal.", "2point Recal."]
RECAL_METHOD_DEFAULT  = "2point Recal."

PRINT_MODE_OPTIONS = ["Auto", "Manu"]
PRINT_MODE_DEFAULT  = "Manu"

# --- Control Chart (Page 13) ---

SIGMA_LINE_OPTIONS = ["±1.0STD", "±1.5STD", "±2.0STD", "±3.0STD"]
SIGMA_LINE_DEFAULT  = "±2.0STD"

CENTER_LINE_OPTIONS = ["Average", "Median", "Target"]
CENTER_LINE_DEFAULT  = "Average"

DISPLAY_SCALE_OPTIONS = ["Auto", "Fixed"]
DISPLAY_SCALE_DEFAULT  = "Auto"

CONTROL_RANGE_OPTIONS = ["Standard Range", "Control Range"]
CONTROL_RANGE_DEFAULT  = "Standard Range"

# --- 100% Correction (Page 8) ---

CORRECTION_OPTIONS = ["Y", "N", "I", " "]  # Y=require, N=not require, I=base element
CORRECTION_DEFAULT  = "N"

# --- Master Element List ---
# The full set of elements the system supports.
# Users pick from this list — they cannot invent new element names.
# Each entry: (element_code, chemical_symbol, default_wavelength)
# Elements with multiple wavelengths appear multiple times.

MASTER_ELEMENTS = [
    ("FE",  "Fe",  "273.0"),
    ("C",   "C",   "193.0"),
    ("SI",  "Si",  "212.4"),
    ("MN",  "Mn",  "293.3"),
    ("P",   "P",   "178.3"),
    ("S",   "S",   "180.7"),
    ("V",   "V",   "311.0"),
    ("CR",  "Cr",  "267.7"),
    ("CR",  "Cr",  "298.9"),   # second channel for CR
    ("MO",  "Mo",  "202.0"),
    ("MO",  "Mo",  "277.5"),   # second channel for MO
    ("NI",  "Ni",  "231.6"),
    ("NI",  "Ni",  "227.7"),   # second channel for NI
    ("AL",  "Al",  "394.4"),
    ("CU",  "Cu",  "224.2"),
    ("TI",  "Ti",  "337.2"),
    ("W",   "W",   "220.4"),
    ("B",   "B",   "182.6"),
    ("NB",  "Nb",  "319.5"),
    ("CA",  "Ca",  "396.8"),
    ("CO",  "Co",  "258.0"),
    ("SN",  "Sn",  "189.9"),
    ("N",   "N",   "174.5*2"),
    ("PB",  "Pb",  "405.7"),
    ("RH",  "Rh",  "421.8"),
    ("CE",  "",    ""),        # placeholder element, no wavelength
]

# Unique element codes for pickers (no duplicates)
MASTER_ELEMENT_CODES = list(dict.fromkeys(e[0] for e in MASTER_ELEMENTS))

# Element code → wavelength mapping (primary wavelength per element)
ELEMENT_WAVELENGTH_MAP = {
    "FE": "273.0",  "C": "193.0",  "SI": "212.4",  "MN": "293.3",
    "P":  "178.3",  "S": "180.7",  "V":  "311.0",  "CR": "267.7",
    "MO": "202.0",  "NI": "231.6", "AL": "394.4",  "CU": "224.2",
    "TI": "337.2",  "W": "220.4",  "B":  "182.6",  "NB": "319.5",
    "CA": "396.8",  "CO": "258.0", "SN": "189.9",  "N":  "174.5*2",
    "PB": "405.7",  "RH": "421.8", "CE": "",
}

# Monitor element picker — "None" is always the first option
# Options are built dynamically from active elements but None is always present
MONITOR_ELEMENT_NONE = "None"

# Default group list (pre-loaded from old software data)
DEFAULT_GROUPS = [
    "LAS 2023", "SS 2023", "LA 2021", "SS - 2022", "FERR 2022",
    "TOLL STEEL2021", "FERR 2020", "SS 2021", "LA 2021 S",
    "GLOBAL CAL", "LA 2020", "LA-WITH HI MN", "SS WITH HI MN",
    "Cast", "LOW-ALLOY-HS", "NI 2017", "INCONEL 17", "MONEL 17",
    "TEST GROUP", "LA 2021 WITH CA", "TEST LAS", "26-11-22",
    "FERR 2023", "GHHaj",
]

# =============================================================================
# SECTION 2: HARDWARE CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
# ⚠️  ALL VALUES BELOW ARE PLACEHOLDERS.
# ⚠️  Vivaan must fill these from the hardware Excel sheet before the
# ⚠️  Analysis runner can communicate with real hardware.
# ⚠️  AnaInf (offline module) works perfectly without these.
# =============================================================================

SIMULATION_MODE = True  # Set to False when hardware constants are filled in

# UART settings
UART_BAUDRATE   = 9600
UART_TIMEOUT    = 2.0   # seconds to wait for a response
UART_BYTESIZE   = 8
UART_PARITY     = "N"   # N=None, E=Even, O=Odd
UART_STOPBITS   = 1
ADC_READ_TIMEOUT = 5.0  # seconds to wait for ADC response

# Port B — Spark source type codes (7-bit values for Port B)
# ⚠️  Replace 0x00 placeholders with real values from hardware Excel
SOURCE_7BIT_MAP = {
    "3 Peak Spark":      0x00,  # ⚠️ PLACEHOLDER
    "Normal Spark":      0x00,  # ⚠️ PLACEHOLDER
    "Combined Spark":    0x00,  # ⚠️ PLACEHOLDER
    "Arclike Spark":     0x00,  # ⚠️ PLACEHOLDER
    "Cleaning":          0x00,  # ⚠️ PLACEHOLDER
    "High Voltage Spark":0x00,  # ⚠️ PLACEHOLDER
    "AD OFFSET":         0x00,  # ⚠️ PLACEHOLDER
    "ITG OFFSET":        0x00,  # ⚠️ PLACEHOLDER
    "SH OFFSET":         0x00,  # ⚠️ PLACEHOLDER
    "NOISE TEST":        0x00,  # ⚠️ PLACEHOLDER
    "Lamp":              0x00,  # ⚠️ PLACEHOLDER
}

# Port A — Mode bits (top 2 bits of the 8-bit command byte)
# These are confirmed from hardware team documentation — do NOT change
MODE_ELEMENT_SELECT  = 0b00  # Select which element channel to use
MODE_ATTENUATOR_SET  = 0b01  # Set attenuator value for selected element
MODE_SENSOR_1        = 0b10  # Sensor 1 control
MODE_SENSOR_2        = 0b11  # Sensor 2 control

# Element to channel mapping
# Format: (element_code, wavelength): (serial_number, 6bit_channel_id)
# ⚠️  All channel IDs are placeholders. Vivaan fills from Excel sheet.
ELEMENT_CHANNEL_MAP = {
    ("FE",  "273.0"):   (1,  0x00),  # ⚠️ PLACEHOLDER
    ("C",   "193.0"):   (2,  0x00),  # ⚠️ PLACEHOLDER
    ("SI",  "212.4"):   (3,  0x00),  # ⚠️ PLACEHOLDER
    ("MN",  "293.3"):   (4,  0x00),  # ⚠️ PLACEHOLDER
    ("P",   "178.3"):   (5,  0x00),  # ⚠️ PLACEHOLDER
    ("S",   "180.7"):   (6,  0x00),  # ⚠️ PLACEHOLDER
    ("V",   "311.0"):   (7,  0x00),  # ⚠️ PLACEHOLDER
    ("CR",  "267.7"):   (8,  0x00),  # ⚠️ PLACEHOLDER
    ("CR",  "298.9"):   (9,  0x00),  # ⚠️ PLACEHOLDER
    ("MO",  "202.0"):   (10, 0x00),  # ⚠️ PLACEHOLDER
    ("MO",  "277.5"):   (11, 0x00),  # ⚠️ PLACEHOLDER
    ("NI",  "231.6"):   (12, 0x00),  # ⚠️ PLACEHOLDER
    ("NI",  "227.7"):   (13, 0x00),  # ⚠️ PLACEHOLDER
    ("AL",  "394.4"):   (14, 0x00),  # ⚠️ PLACEHOLDER
    ("CU",  "224.2"):   (15, 0x00),  # ⚠️ PLACEHOLDER
    ("TI",  "337.2"):   (16, 0x00),  # ⚠️ PLACEHOLDER
    ("W",   "220.4"):   (17, 0x00),  # ⚠️ PLACEHOLDER
    ("B",   "182.6"):   (18, 0x00),  # ⚠️ PLACEHOLDER
    ("NB",  "319.5"):   (19, 0x00),  # ⚠️ PLACEHOLDER
    ("CA",  "396.8"):   (20, 0x00),  # ⚠️ PLACEHOLDER
    ("CO",  "258.0"):   (21, 0x00),  # ⚠️ PLACEHOLDER
    ("SN",  "189.9"):   (22, 0x00),  # ⚠️ PLACEHOLDER
    ("N",   "174.5*2"): (23, 0x00),  # ⚠️ PLACEHOLDER
    ("PB",  "405.7"):   (24, 0x00),  # ⚠️ PLACEHOLDER
    ("RH",  "421.8"):   (25, 0x00),  # ⚠️ PLACEHOLDER
}

# Predefined 6-bit command codes for each phase of analysis
# ⚠️  All values below are placeholders. Vivaan fills from Excel sheet.

PURGE_CODE_SENSOR1_6BIT       = 0x00  # ⚠️ PLACEHOLDER — triggers argon purge
PURGE_CODE_SENSOR2_6BIT       = 0x00  # ⚠️ PLACEHOLDER

PREBURN_CODE_SENSOR1_6BIT     = 0x00  # ⚠️ PLACEHOLDER — starts pre-burn spark
PREBURN_CODE_SENSOR2_6BIT     = 0x00  # ⚠️ PLACEHOLDER

INTEGRATION_CODE_SENSOR1_6BIT = 0x00  # ⚠️ PLACEHOLDER — starts integration
INTEGRATION_CODE_SENSOR2_6BIT = 0x00  # ⚠️ PLACEHOLDER

OUTPUT_CODE_SENSOR1_6BIT      = 0x00  # ⚠️ PLACEHOLDER — output/measurement state
OUTPUT_CODE_SENSOR2_6BIT      = 0x00  # ⚠️ PLACEHOLDER

CLEAN_CODE_SENSOR1_6BIT       = 0x00  # ⚠️ PLACEHOLDER — cleaning sequence
CLEAN_CODE_SENSOR2_6BIT       = 0x00  # ⚠️ PLACEHOLDER

# Special input channels (not regular element channels)
# ⚠️  Confirm values with Vivaan
CHANNEL_TEMPERATURE   = 46  # temperature sensor
CHANNEL_VACUUM        = 47  # vacuum gauge
CHANNEL_AC_SUPPLY     = 48  # AC supply reading

# Attenuator value range
# ⚠️  Confirm exact max with Vivaan — screenshots show up to 98
ATTENUATOR_MIN = 0
ATTENUATOR_MAX = 127  # ⚠️ CONFIRM — likely 127 (7-bit) or 99

# Simulated ADC value returned when SIMULATION_MODE = True
SIMULATION_ADC_VALUE = 2048