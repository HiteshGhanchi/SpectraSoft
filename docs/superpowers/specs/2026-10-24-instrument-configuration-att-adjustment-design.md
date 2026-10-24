# Instrument Configuration and Attenuator Adjustment Design

## Intent

Add the instrument-level emission-unit setting and the separate Attenuator
Adjustment operation described by the QC-E1 workflow. The installed emission
unit is a property of the physical spectrometer; accepted ATT values remain
properties of an Analytical Group and selected ITG/channel.

## Goals

- Persist one instrument configuration record with an emission-unit type:
  `HPSG_300` or `HVS`.
- Provide a native PyQt screen for changing and saving that system setting.
- Add a separate native Attenuator Adjustment screen reachable from the main
  application menu.
- Require an Analytical Group and one of its configured analytical channels.
- Read the selected group's analytical condition, channel sequence, source,
  integration time, and current ATT.
- Use the installed emission-unit type to show the manual-defined adjustment
  guidance:
  - HPSG-300: scale x2, graduation 6-7, integration 4 seconds.
  - HVS: scale x5, graduation 4-5, integration 15 seconds.
  - Both: target intensity 0.5-0.6.
- Allow live ATT changes from 0 through 63 during measurement.
- Show a live intensity-over-time graph with the target band and ATT-change
  markers, plus a compact readings table for exact values.
- Save an explicitly accepted ATT value back into the selected group's existing
  `page_02_attenuator` row without duplicating HPSG/HVS in group data.
- Keep the adjustment workflow hardware-independent at the service boundary by
  using `SpectrometerController` and `SequenceEngine` abstractions.

## Non-goals

- Automatically deciding or accepting an ATT value without operator action.
- Applying HPSG/HVS-specific behavior to routine analysis jobs unless another
  verified manual or hardware requirement defines it.
- Changing the existing ATT JSON shape for Analytical Groups.
- Replacing the standalone legacy profile tool in this change.
- Adding a plotting dependency; the graph will use a small native PyQt widget.

## Acceptance criteria

1. A fresh database creates the instrument configuration storage and defaults to
   HPSG-300 without overwriting a saved selection.
2. The instrument configuration UI can load, change, and persist HPSG-300/HVS.
3. The main menu exposes Instrument Configuration and Attenuator Adjustment.
4. Attenuator Adjustment refuses to start without a group, selected channel, or
   valid analytical sequence.
5. Starting adjustment programs the selected ATT, executes the selected source
   and integration sequence through semantic controller methods, and emits
   readings for the selected channel.
6. Changing ATT validates 0-63, updates the controller, and records an ATT
   marker in the live history.
7. The graph displays intensity history and the 0.5-0.6 target band without
   making the acceptance decision.
8. Accepting a value persists it under the selected group's ITG row and it is
   visible again when the group ATT Settings page is reopened.
9. Stop/failure paths leave the controller in shutdown/closed state and do not
   overwrite the stored ATT unless the operator accepts it.

## Approach

Use the existing SQLAlchemy database and PyQt navigation:

- Add `InstrumentConfiguration` to `core/persistence/models.py`, with a
  singleton row identified by a stable key rather than a group relationship.
- Add constants and preset metadata to `import_data/constants.py` and a small
  pure-Python adjustment service for validation, guidance, history, and ATT
  persistence.
- Add the instrument configuration page under `ui/settings/`.
- Add the adjustment page under `ui/adjustment/` with a worker thread, native
  graph widget, target-band guidance, readings table, and explicit Accept ATT
  action.
- Keep the page's worker dependent on the semantic controller protocol and
  inject a controller in tests.

## Graph decision

The graph is preferred over a table-only screen because ATT adjustment is a
time-based tuning operation. Intensity over time lets the operator see whether
the signal is stable, drifting, saturating, or responding to an ATT change.
The target band and ATT markers make the relationship visible without turning
the software into an automatic scientific decision-maker. The exact readings
table remains available for auditability and troubleshooting.

## Verification

Add hardware-free tests first for constants/guidance, singleton persistence,
ATT validation and persistence, controller sequencing, graph history, and UI
navigation. Run all checks only through the repository virtual environment:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/pytest -q
.venv/bin/python -m py_compile ...
```
