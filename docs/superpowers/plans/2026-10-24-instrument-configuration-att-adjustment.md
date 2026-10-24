# Instrument Configuration and Attenuator Adjustment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a persisted instrument-level HPSG-300/HVS setting and a native, group-aware Attenuator Adjustment operation with live graphing and explicit ATT persistence.

**Architecture:** Store one `InstrumentConfiguration` row in SQLite. Keep HPSG/HVS guidance in shared constants and pure adjustment services, while the PyQt page loads the selected group/channel and runs hardware through the existing `SpectrometerController` protocol in a worker thread. Accepted ATT values continue to use `AnalyticalGroup.page_02_attenuator` only.

**Tech Stack:** Python 3, PyQt6, SQLAlchemy/SQLite, existing semantic spectrometer controller, unittest/pytest.

**Spec:** `docs/superpowers/specs/2026-10-24-instrument-configuration-att-adjustment-design.md`

## Global Constraints

- Use `.venv` for every check; do not run system Python test commands.
- Keep HPSG-300/HVS as a system-level value, never duplicate it in Analytical Group ATT rows.
- Keep ATT values in the inclusive range `0` through `63`.
- Use the existing semantic hardware interface; do not assemble UART commands in UI code.
- Do not add a plotting dependency; use a native PyQt graph widget.
- Do not automatically accept an ATT value; the operator must press Accept.

## Review Focus

- Existing database startup with a missing singleton configuration row; test default creation without overwriting a saved selection in Task 1.
- Invalid emission-unit and ATT values; test rejection at the pure service boundary in Tasks 1 and 2.
- Stale or incomplete selected-channel data; test that adjustment cannot start without a valid selected ITG/SEQ in Task 3.
- Controller failure during a measurement cycle; test that failure produces no accepted ATT and cleanup occurs in Task 2.
- ATT history containing multiple ATT values and readings outside the target band; test graph data/markers and target guidance in Task 2.

---

### Task 1: Instrument Configuration and Shared Presets

**Files:**
- Modify: `import_data/constants.py`
- Modify: `core/persistence/models.py`
- Create: `core/persistence/configuration.py`
- Test: `tests/test_instrument_configuration.py`

**Interfaces:**
- Produces `InstrumentConfiguration` with `id` and `emission_unit_type`.
- Produces `get_or_create_instrument_configuration(session) -> InstrumentConfiguration`.
- Produces `set_emission_unit_type(session, emission_unit_type) -> InstrumentConfiguration`.
- Produces `AdjustmentPreset`/`get_adjustment_preset(emission_unit_type)` from `core.adjustment.service` for later tasks.

- [ ] **Step 1: Write failing tests** for the two emission-unit constants, exact preset values, singleton default creation, saved-value preservation, and invalid-value rejection.
- [ ] **Step 2: Run the focused tests through `.venv`** and confirm they fail because the configuration model/service is absent.
- [ ] **Step 3: Add constants and the `InstrumentConfiguration` model**, using a stable singleton row id and a string emission-unit field.
- [ ] **Step 4: Implement configuration helpers** that create row id `1` with default `HPSG_300`, validate choices, and commit changes without overwriting an existing selection.
- [ ] **Step 5: Implement pure preset metadata** with HPSG-300 `(scale 2, graduation 6-7, integration 4000 ms, target 0.5-0.6)` and HVS `(scale 5, graduation 4-5, integration 15000 ms, target 0.5-0.6)`.
- [ ] **Step 6: Run the focused tests, then the full `.venv` suite.**

### Task 2: Adjustment Service and Persistence Boundary

**Files:**
- Create: `core/adjustment/__init__.py`
- Create: `core/adjustment/service.py`
- Modify: `core/persistence/models.py` only if a helper needs a model-level field adjustment
- Test: `tests/test_attenuator_adjustment_service.py`

**Interfaces:**
- `AdjustmentReading(timestamp: float, itg_no: int, att_value: int, intensity: float)`.
- `AdjustmentHistory.add(timestamp, att_value, intensity)` and `.readings`, `.att_markers`.
- `validate_adjustment_channel(channel: dict) -> tuple[bool, str]`.
- `update_group_att_rows(page_data: dict, element: dict, att_value: int) -> dict`.
- `save_group_att(session, group_id: int, element: dict, att_value: int) -> None`.
- `AttenuatorAdjustmentRunner.measure_once(group_condition: dict, channel: dict, preset: AdjustmentPreset, att_value: int) -> AdjustmentReading`.

- [ ] **Step 1: Write failing tests** for channel validation, ATT range validation, preservation/replacement of group ATT rows, target-band checks, history markers, and one semantic-controller measurement cycle.
- [ ] **Step 2: Run the focused service tests through `.venv`** and confirm the expected missing-module failures.
- [ ] **Step 3: Implement the pure history and persistence helpers**, preserving unrelated ATT rows and replacing only the selected ITG row.
- [ ] **Step 4: Implement `AttenuatorAdjustmentRunner.measure_once`** using `set_attenuator`, `reset`, `argon_purge`, `prespark`, and `integrate`; parse the configured source selection through `SequenceEngine._source_code_from_selection`; return the selected channel intensity.
- [ ] **Step 5: Add cleanup behavior** so the runner shuts down when a cycle fails or the worker stops, while never persisting an ATT by itself.
- [ ] **Step 6: Run the focused service tests, then the full `.venv` suite.**

### Task 3: Instrument Configuration Screen

**Files:**
- Create: `ui/settings/instrument_configuration_page.py`
- Modify: `ui/main_window.py`
- Test: `tests/test_instrument_configuration_ui.py`

**Interfaces:**
- `InstrumentConfigurationPage(main_window)` loads the singleton setting and exposes a combo with `HPSG-300` and `HVS`.
- `MainWindow._open_instrument_configuration()` opens the settings page without requiring an Analytical Group.

- [ ] **Step 1: Write failing UI/navigation tests** for the two choices, loading the saved value, saving HVS, and opening the page from the Settings menu.
- [ ] **Step 2: Run the focused UI tests through `.venv`** with `QT_QPA_PLATFORM=offscreen` and confirm they fail because the page/action is absent.
- [ ] **Step 3: Implement the native PyQt configuration page** using the existing application styling and the persistence helper.
- [ ] **Step 4: Add a Settings menu and action** in `MainWindow`, keeping the left Analytical Group panel visible for this page.
- [ ] **Step 5: Run the focused UI tests and full `.venv` suite.**

### Task 4: Attenuator Adjustment Service Worker and Native Graph

**Files:**
- Create: `ui/adjustment/__init__.py`
- Create: `ui/adjustment/adjustment_graph.py`
- Create: `ui/adjustment/attenuator_adjustment_page.py`
- Modify: `ui/main_window.py`
- Test: `tests/test_attenuator_adjustment_ui.py`

**Interfaces:**
- `AdjustmentGraphWidget.set_target_band(low: float, high: float)` and `.set_history(history)`.
- `AttenuatorAdjustmentPage(main_window)` loads the current group, selected ITGs, current ATT, sequence/source, and system preset.
- `MainWindow._open_attenuator_adjustment()` requires a selected Analytical Group and opens the page.

- [ ] **Step 1: Write failing UI tests** for group/channel loading, invalid/no-channel blocking, HPSG/HVS guidance display, graph target band, and Accept writing the selected ATT.
- [ ] **Step 2: Run the focused UI tests through `.venv`** and confirm the page/action is absent.
- [ ] **Step 3: Implement the native `QPainter` graph** with axes, intensity points, target band, and ATT-change markers; keep history data testable without pixel assertions.
- [ ] **Step 4: Implement the page layout** with group/channel selectors, emission-unit guidance, current ATT input, sequence details, Start/Stop, Accept ATT, live intensity/status, graph, and readings table.
- [ ] **Step 5: Implement the `QThread` worker** that creates/connects the configured controller, runs repeated `measure_once` cycles, emits readings, and stops/shuts down/closes safely.
- [ ] **Step 6: Add the Adjustment menu/action** and no-group warning path in `MainWindow`.
- [ ] **Step 7: Run focused UI tests and full `.venv` suite.**

### Task 5: Documentation, Smoke Checks, and Final Verification

**Files:**
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-10-24-instrument-configuration-att-adjustment-design.md` only if implementation decisions require clarification
- Test: existing suite plus a short offscreen startup smoke command

- [ ] **Step 1: Update README navigation and manual-to-code mapping** for Instrument Configuration and native Attenuator Adjustment.
- [ ] **Step 2: Run `.venv/bin/python -m py_compile` on all changed Python files.**
- [ ] **Step 3: Run `QT_QPA_PLATFORM=offscreen .venv/bin/pytest -q`.**
- [ ] **Step 4: Run the offscreen Qt startup smoke check and inspect `git diff --check`.**
- [ ] **Step 5: Review the final diff and report exact changed files, checks, and any hardware-only limitation.**
