# SpectraSoft

SpectraSoft is a PyQt6 desktop application for configuring and operating an
emission spectral analysis workflow. It stores analytical-group configuration
in SQLite, communicates with the MCU through a CH340 USB-UART adapter, runs
calibration and correction calculations, and presents the operator workflow in
the same broad sequence as the QC-E1 instruction manual.

The source tree is intentionally organized by responsibility. New developers
should start with the navigation below, then open the relevant package instead
of searching the whole repository for a page or hardware command.

## Application navigation

This is the product navigation currently represented by the application. It is
based on the operating areas described in `Manual.md` and can be extended as
new screens are implemented.

```text
Application
│
├── Analytical Information
│   │
│   ├── Analytical Group Name
│   │   ├── AG-No.
│   │   └── Group name
│   │
│   ├── Analytical Condition
│   │   ├── Purge
│   │   ├── SEQ1 source/preburn/integration
│   │   ├── SEQ2 source/preburn/integration
│   │   ├── SEQ3 source/preburn/integration
│   │   └── CLEAN source/time
│   │
│   ├── Analytical Channel and Internal Standard
│   │   ├── AR-No.
│   │   ├── ITG
│   │   ├── ELE
│   │   ├── NAME
│   │   ├── SEQ
│   │   └── ISE Ref
│   │
│   ├── ATT Settings
│   │   └── ATT per selected analytical channel
│   │
│   ├── Drift Correction Information
│   ├── Working Curve Information
│   ├── Matrix Correction Information
│   ├── Master Curve Information
│   └── Result and calculation settings
│
├── Attenuator Adjustment
│   └── Operation that determines production ATT

├── Settings
│   └── Instrument Configuration
│       └── Installed emission unit: HPSG-300 or HVS
│
├── Regression Calculation
│   └── Operations that calculate curves and coefficients
│
├── Analysis
│   └── Jobs 2, 3, 4, 5, 6, 7, 8, X and Y
│
├── Report
│   └── Stored result reporting and statistics
│
└── Maintenance
    ├── Waste Discharge
    ├── Manual Scanning
    ├── Lamp Test
    └── Maintenance information
```

### Manual-to-code map

| Manual area | Current code location |
| --- | --- |
| Chapter 2 — system configuration and startup | `main.py`, `core/persistence/`, `ui/main_window.py` |
| Chapter 4 — master menu | `ui/main_window.py` |
| Chapter 5 — analytical information | `ui/anainf/` and `core/persistence/models.py` |
| Chapter 6 — attenuator sensitivity | `core/hardware/attenuator_programmer.py`, `ui/anainf/page_02_attenuator.py` |
| Chapter 7 — regression calculation | `ui/regression/` and `core/analysis/correction_engine.py` |
| Chapters 8–9 — analysis operations | `ui/analysis/`, `core/analysis/analysis_worker.py`, `core/hardware/sequence_engine.py` |
| Chapter 10 — report-oriented output | Existing export/report actions in analysis pages; more report screens can be added under `ui/report/` |
| Chapter 11 — maintenance and hardware support | `core/hardware/` and the maintenance pages as they are implemented |
| Instrument configuration and ATT adjustment | `core/persistence/configuration.py`, `ui/settings/instrument_configuration_page.py`, `ui/adjustment/` |

`Manual.md` is the source reference for instrument terminology, sequence
timing, correction formulas, environmental requirements, and operator safety.
It is not a substitute for the provider's hardware and maintenance manuals.

## Repository structure

```text
.
├── main.py                         # Thin desktop application entry point
├── core/
│   ├── hardware/                   # Transport-independent instrument control
│   │   ├── interfaces/             # Hardware controller and transport contracts
│   │   ├── protocols/              # MCU/protocol-specific implementations
│   │   ├── transports/             # UART and future connection transports
│   │   ├── factory.py              # Selects the configured hardware backend
│   │   ├── sequence_engine.py      # Protocol-independent burn orchestration
│   │   └── attenuator_programmer.py
│   ├── analysis/                   # Background jobs and result corrections
│   │   ├── analysis_worker.py
│   │   └── correction_engine.py
│   └── persistence/                # SQLite setup and SQLAlchemy models
│       ├── database.py
│       └── models.py
├── ui/
│   ├── main_window.py              # Menu and page orchestration
│   ├── anainf/                     # Analytical Information pages 1–9
│   ├── analysis/                   # Jobs 2, 3, 4, 5, 6, 7, 8, X and Y
│   ├── regression/                 # Standards, working curves, matrix work
│   └── settings/                   # Master elements and source-code tables
├── tools/
│   ├── check_hardware_connection.py # Safe connection/standby check
│   └── profile/                    # Stand-alone ADC/ATT profiling tools
│       ├── profile_task.py
│       └── profile_gui.py
├── import_data/
│   └── constants.py                # Shared domain and hardware constants
├── tests/                          # Fast, hardware-free regression tests
├── Manual.md                       # QC-E1 domain and operator reference
├── requirements.txt
└── README.md
```

## Refactoring completed

The codebase was reorganized without changing the existing application entry
points or the database schema.

All shared limits and hardware settings now have one developer-facing home in
`import_data/constants.py`. This includes analytical capacities, channel and
source-code counts, attenuator limits, ADC limits, UART settings, protocol
timings, and source-selection values. Change those values there rather than
duplicating them inside UI, analysis, or hardware modules.

The bundled `import_data/master_elements.json` and
`import_data/source_codes.json` files are validated and used to initialize
empty or blank placeholder tables at database startup. Existing nonblank
configuration is preserved. The Settings pages continue to support editing,
JSON import, and JSON export of both tables.

### 1. Core modules are grouped by responsibility

The former flat `core/` directory mixed persistence, hardware communication,
analysis orchestration, and correction logic. The modules now live in focused
packages:

- `core/hardware/` owns hardware interfaces, protocol implementations,
  transports, attenuator programming, and the complete burn sequence.
- `core/analysis/` owns the Qt worker used by analysis jobs and the analytical
  correction pipeline.
- `core/persistence/` owns SQLite path resolution, SQLAlchemy setup, and the
  `AnalyticalGroup`, `SourceCode`, and `MasterElement` models.

Imports in the UI and application entry point were updated to use these new
locations. The package `__init__.py` files are deliberately lightweight so
importing a submodule does not start Qt, open a serial port, or initialize the
database as a side effect. There are no compatibility import modules: all
application code now uses the grouped package paths directly.

### 2. Hardware control is transport- and protocol-independent

The ATmega sketch currently defines a line-oriented UART protocol at **115200
baud**:

- `O,<port>,<value>` writes a digital output and returns `K`.
- `I` reads the twelve input pins and returns `D,<value>`.
- `T,<ms>` starts a non-blocking controller delay and returns `K`.
- Lines beginning with `#` are diagnostic messages.

That contract is implemented in `core/hardware/protocols/uart_protocol.py`,
while serial-port operations are isolated in
`core/hardware/transports/uart_transport.py`. Application services depend on
the semantic `SpectrometerController` interface instead of sending `O,A,...`
commands directly.

To add another hardware option:

1. Implement `CommandTransport` if the new option still uses line commands.
2. Implement `SpectrometerController` if its command protocol differs from
   the ATmega protocol.
3. Register the implementation in `core/hardware/factory.py`.
4. Leave `SequenceEngine`, `AttenuatorProgrammer`, analysis jobs, and UI pages
   unchanged.

The selected backend can be configured with:

```bash
SPECTRASOFT_HARDWARE_TRANSPORT=uart
SPECTRASOFT_HARDWARE_PROTOCOL=uart
```

The default remains the current UART/ATmega implementation.

### 3. Profiling utilities are separated from the desktop application

The stand-alone Task 5 profiling implementation and its Tk GUI now live under
`tools/profile/`. The root files `task5_profile.py` and
`task5_profile_gui.py` remain small compatibility launchers, so existing local
commands continue to work while the implementation has a clear home.

The profiling GUI now uses the configured `CommandTransport` factory when it
needs to open hardware itself. The previous reference to the missing
`task1_usb_init` module was removed.

### 4. Regression checks were added

`tests/test_correction_engine.py` covers the correction chain and Page 8 display
ordering using hardware-free inputs. These checks protect the most important
calculation boundary while the UI and hardware layers continue to evolve.

### 5. Documentation now explains the architecture

This README records the navigation, manual-to-code mapping, package ownership,
compatibility launchers, and developer workflow. When a new screen is added,
update both the relevant navigation branch and the manual-to-code table.

## Getting started

### Install dependencies

Use a virtual environment for development:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

### Start the desktop application

```bash
python main.py
```

### Check the MCU connection

Before running a hardware analysis job, use the connection check. It opens the
configured controller, waits for the ATmega startup output, sends the standby
commands, and verifies their `K` acknowledgements before closing the connection:

```bash
python -m tools.check_hardware_connection
```

The CH340 adapter is auto-detected by VID/PID. To select a specific port, set:

```bash
SPECTRASOFT_UART_PORT=/dev/ttyUSB0 python -m tools.check_hardware_connection
```

On Windows, use a port such as `COM4`. The MCU sketch and the application must
both use **115200 baud**.

At startup the application creates `data.db` next to the project when running
from source. A packaged executable stores it beside the executable. The
database is intentionally created with `create_all` and is not reset by
starting the application.

### Run the optional profiling tool

```bash
python task5_profile_gui.py
```

The profiling tool is hardware-facing. Do not run it against an instrument
unless the serial adapter, power state, and instrument operating conditions
have been checked according to the provider documentation.

## Development conventions

- Keep instrument protocol code in `core/hardware/`; UI pages should call a
  service instead of assembling UART commands themselves.
- Keep calculations independent of Qt and serial I/O whenever possible. This
  makes them testable with ordinary Python inputs.
- Keep SQLAlchemy models and session setup in `core/persistence/`.
- Keep one functional area per UI package. Analytical Information pages belong
  in `ui/anainf/`, analysis jobs in `ui/analysis/`, and calibration/regression
  screens in `ui/regression/`.
- Add a focused test under `tests/` when changing a calculation, a saved data
  shape, or a hardware command boundary.
- Do not commit `data.db`, logs, generated CSV files, or other runtime output.

## Checks

The repository currently uses Python's import/compile check and pytest:

```bash
python3 -m compileall -q .
python3 -m pytest -q
```

The test suite is designed to run without a connected spectrometer. Hardware
flows should additionally be verified with a safe test fixture or simulator
before connecting to production equipment.

## Known follow-up areas

The repository contains UI pages for much of the analytical workflow, while
report and maintenance navigation is still being expanded. The next additions
should preserve the package boundaries above rather than adding new large
modules to the repository root.
