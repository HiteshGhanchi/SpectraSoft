# Analytical Information Page Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Analytical Information flow through Analytical Condition → Order/ISE → selected-channel ATT, and prevent ATT navigation until at least one channel is configured.

**Architecture:** Keep the existing `SourceConditionPage`, `ChannelPage`, and `AttenuatorPage` widgets and the existing `AnalyticalGroup` JSON columns. Navigation changes stay in the page classes; small pure helper functions will make selected-channel extraction and validation testable without starting Qt.

**Tech Stack:** Python 3, PyQt6, SQLAlchemy/SQLite, unittest/pytest.

**Spec:** `docs/superpowers/specs/2026-10-24-analytical-information-page-flow-design.md`

## Global Constraints

- Use the existing page JSON fields; do not add database tables.
- ATT values remain integers from `0` through `63`.
- Page 3 supports up to 32 analytical positions.
- ELE and wavelength must come from the selected ITG's `MasterElement` record.
- Do not change MCU commands or scientific calculations.

## Review Focus

- No Page 3 ITG selected: Next must be blocked with a clear warning rather than opening ATT.
- Selected ITG without SEQ 1/2/3: Next must remain blocked.
- Page 2 with selected ITGs: only those ITGs appear, in Page 3 order, with saved ATT values preserved.
- Page 2 with stale/empty selection: it must not show all master channels accidentally; it should render empty state.
- Existing saved Page 3/Page 2 JSON: loading and navigating must preserve valid rows and values.

---

### Task 1: Make channel-selection rules testable

**Files:**
- Modify: `ui/anainf/page_03_channel.py`
- Test: `tests/test_analytical_information_flow.py`

**Interfaces:**
- Produces `validate_channel_data(data: list[dict]) -> tuple[bool, str]` for pure validation of selected ITGs and SEQ values.
- Produces `selected_itg_numbers(data: list[dict]) -> list[int]` for ordered selected ITG extraction.

- [ ] **Step 1: Write failing tests** for zero selections, missing/invalid SEQ, repeated ITGs for channel skip, valid ordered selections, and malformed/stale ITG values.
- [ ] **Step 2: Run the focused tests** with `pytest tests/test_analytical_information_flow.py -q`; verify they fail because the helpers do not exist.
- [ ] **Step 3: Implement the pure helpers** in `page_03_channel.py`, allowing repeated physical ITGs for channel skip while retaining the SEQ rules and required at-least-one-selection rule for navigation.
- [ ] **Step 4: Update `ChannelPage._validate_rows`** to use the helper and show the returned warning text.
- [ ] **Step 5: Run the focused tests** again and verify they pass.

### Task 2: Reorder the three pages and filter ATT by selection

**Files:**
- Modify: `ui/anainf/page_01_source.py`
- Modify: `ui/anainf/page_02_attenuator.py`
- Modify: `ui/anainf/page_03_channel.py`
- Test: `tests/test_analytical_information_flow.py`

**Interfaces:**
- Consumes `selected_itg_numbers` from Task 1.
- `AttenuatorPage` loads selected ITGs from `AnalyticalGroup.page_03_channel` and renders only matching `MasterElement` rows.

- [ ] **Step 1: Add failing tests** proving Page 1's Next target is Page 3, Page 3's Next target is Page 2 after valid selection, Page 3's Previous target is Page 1, and ATT row preparation preserves Page 3 order while excluding unselected master elements.
- [ ] **Step 2: Run the focused tests** and verify the current implementation fails the page-order and selected-only expectations.
- [ ] **Step 3: Change Page 1 navigation** so `_on_next` saves and opens `ChannelPage`.
- [ ] **Step 4: Change Page 3 navigation** so `_on_next` validates/saves and opens `AttenuatorPage`, while `_on_pre` validates/saves and opens `SourceConditionPage`.
- [ ] **Step 5: Change Page 2 loading** to read the active group's Page 3 JSON, resolve only selected ITGs through `MasterElement`, preserve Page 3 ordering, and split the result across the existing two tables.
- [ ] **Step 6: Render a clear empty state** when there are no valid selected ITGs, without falling back to the full master-element list; keep ATT defaults at `0` for newly selected rows and preserve saved values by ITG.
- [ ] **Step 7: Update Page 2 Previous/Cancel navigation** to return to Page 3 and update user-facing text/title comments to reflect the new sequence.
- [ ] **Step 8: Run the focused tests** and verify they pass.

### Task 3: Verify the complete project behavior

**Files:**
- Modify: `README.md` only if the navigation table needs correction after implementation.
- Test: `tests/test_analytical_information_flow.py`

- [ ] **Step 1: Run the complete test suite** with `pytest -q`.
- [ ] **Step 2: Run Python compilation/import checks** for the changed page modules and test module.
- [ ] **Step 3: Inspect the final diff** to confirm only the requested page flow, selected-channel ATT behavior, tests, and design/plan documentation changed.
- [ ] **Step 4: If the environment supports Qt display startup, launch the app or a minimal offscreen page smoke test** and verify the three page transitions; otherwise report the limitation without claiming a GUI smoke test passed.
