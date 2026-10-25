# SpectraSoft Application Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply one consistent light laboratory-dashboard theme with a navy/slate shell and deliberate color accents across all SpectraSoft laptop screens while preserving every existing workflow, signal, validation rule, data path, and hardware behavior.

**Architecture:** Add a centralized PyQt6 QSS theme module and apply it at the QApplication level. Refactor only visual shell/layout code: the main window becomes resizable, the left group/navigation panel becomes a navy/slate dashboard rail, and page-level legacy styles are migrated to shared object names and theme tokens. No domain or business logic changes are permitted.

**Tech Stack:** Python, PyQt6, QSS, pytest, existing `.venv` environment.

**Spec:** `docs/superpowers/specs/2026-10-25-application-theme-design.md`

## Global Constraints

- Do not change analytical calculations, database models, persistence, hardware protocols, worker behavior, signal connections, validation rules, or navigation destinations.
- The application is laptop-only; use the available screen width and remove the fixed `1100x680` restriction.
- Use a light cool-gray canvas with white content surfaces, a navy/slate shell, and colorful teal/blue/violet/amber/green accents; do not make every surface charcoal.
- Use Qt layout managers and stretch policies; do not add absolute-positioned UI.
- Keep the existing stack and add no third-party UI dependency.
- Run checks with `QT_QPA_PLATFORM=offscreen .venv/bin/python`.
- Preserve unrelated working-tree changes and do not commit unless explicitly requested.

## Review Focus

- A long analytical form or table must expand into the available central width instead of remaining trapped in a narrow fixed panel; test the main window and representative page size policies in Task 2 and Task 3.
- Page-specific inline styles must not restore legacy beige/blue/beveled controls; test representative widgets for the new palette and absence of legacy style markers in Task 3.
- Read-only cells, editable cells, selected rows, warnings, and errors must remain distinguishable in the dark palette; test table and message styles in Task 3.
- Dialogs and confirmation flows must remain readable and usable against the dark application palette; test a representative dialog in Task 4.
- Existing navigation and page construction must still work after stylesheet application; test offscreen startup and representative page creation in Task 5.

---

### Task 1: Central theme module and application-level stylesheet

**Files:**
- Create: `ui/theme.py`
- Modify: `main.py:16-35`
- Test: `tests/test_theme.py`

**Interfaces:**
- Produces `ui.theme.APPLICATION_STYLE`, a complete application-level QSS string.
- Produces `ui.theme.COLORS`, a stable mapping of named color tokens used by migrated UI code.
- Produces `ui.theme.apply_theme(app: QApplication) -> None`, which applies the QSS and platform-neutral font settings.
- Produces `ui.theme.primary_button_style()`, `secondary_button_style()`, and `page_header_style()` only if page code needs a small shared style helper; helpers must return QSS and contain no behavior.

- [ ] **Step 1: Write failing theme tests**

  Add tests that create a QApplication and assert:
- `APPLICATION_STYLE` contains the light canvas, white surface, navy/slate shell, teal accent, graph-friendly semantic colors, and non-beveled button rules.
  - `apply_theme(app)` installs a non-empty application stylesheet and a platform sans-serif font.
  - The stylesheet does not contain the legacy `#d4d0c8`, `outset`, or `inset` visual treatment.

- [ ] **Step 2: Run the focused tests and verify they fail**

  Run:

  ```bash
  QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q tests/test_theme.py
  ```

  Expected: FAIL because `ui.theme` does not exist yet.

- [ ] **Step 3: Implement `ui/theme.py`**

  Define the palette and QSS for `QMainWindow`, `QWidget`, `QMenuBar`, `QMenu`, `QStatusBar`, navigation widgets, cards/group boxes, labels, line edits, combo boxes, spin boxes, check boxes, push buttons, tables, list widgets, scroll areas, tabs, dialogs, message boxes, tooltips, and graph/chart elements. Use object names/classes for shell-specific variants instead of forcing one style onto every page element. Include named chart colors with sufficient contrast on the light canvas.

- [ ] **Step 4: Wire `main.py` to `apply_theme(app)`**

  Replace the current inline beige stylesheet and hard-coded Arial font with the centralized theme call. Do not change initialization order or application entry-point behavior.

- [ ] **Step 5: Run the focused tests and verify they pass**

  Run the same command from Step 2. Expected: PASS.

### Task 2: Resizable laptop shell and uniform navigation rail

**Files:**
- Modify: `ui/main_window.py:15-30, 36-62, 181-283`
- Modify: `ui/anainf/group_panel.py:14-124, 194-300`
- Test: `tests/test_main_window_theme.py`

**Interfaces:**
- Preserve all existing `MainWindow` navigation methods and action names.
- Preserve `GroupPanel._selected()`, `highlight()`, group loading, filtering, creation, deletion, and copy behavior.
- Add only visual object names/properties and layout configuration needed by the theme.

- [ ] **Step 1: Write failing shell tests**

  Add tests that instantiate `MainWindow` offscreen and assert:
  - The window is not fixed-size and has a minimum size suitable for laptop use.
  - The group rail has the theme object name and remains visible on the home view.
  - The right content widget has stretch and can expand beyond the old fixed width.
  - The menu/status bar are present and use the new shell object names.

- [ ] **Step 2: Run the focused shell tests and verify the expected failures**

  Run:

  ```bash
  QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q tests/test_main_window_theme.py
  ```

- [ ] **Step 3: Refactor `MainWindow` shell styling and sizing**

  Remove `setFixedSize(1100, 680)`, set a practical laptop minimum size, and allow normal resize/maximize behavior. Add a compact top-level shell structure using the existing menu/navigation/content/status components. Use object names such as `mainWindow`, `navigationRail`, `contentSurface`, and `statusBar` so QSS can style them consistently. Keep all existing action wiring and page replacement behavior unchanged.

- [ ] **Step 4: Migrate `GroupPanel` to the dark navigation rail**

  Remove palette-based dark-gray/beige styling and inline legacy button styling. Set object names for the rail, title, search field, list, active item, and navigation buttons. Keep all group database operations, search behavior, dialogs, and selection semantics unchanged.

- [ ] **Step 5: Run the focused shell tests and verify they pass**

  Run the command from Step 2. Expected: PASS.

### Task 3: Migrate page surfaces, controls, tables, and workflow actions

**Files:**
- Modify: `ui/anainf/*.py`
- Modify: `ui/analysis/*.py`
- Modify: `ui/adjustment/*.py`
- Modify: `ui/regression/*.py`
- Modify: `ui/settings/*.py`
- Modify: `ui/report/*.py`
- Modify: `ui/maintenance/*.py`
- Test: `tests/test_theme_migration.py`

**Interfaces:**
- Preserve every public page constructor, slot, signal, worker, repository/service call, and navigation callback.
- Preserve page-specific read-only/editable/selected state semantics.
- Use shared object names and theme helpers from `ui.theme`; do not introduce page-local palettes or new business logic.

- [ ] **Step 1: Write failing migration tests**

  Add representative tests for Analytical Condition, Channel, Attenuator, Working Curve, Matrix, Master Elements, Report, and Maintenance pages. Assert that each page constructs under the theme, uses the new page-surface/header object names, and that representative buttons/tables/inputs do not carry legacy beige, blue title-bar, or bevel styles.

- [ ] **Step 2: Run the focused migration tests and capture the existing failures**

  Run:

  ```bash
  QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q tests/test_theme_migration.py
  ```

- [ ] **Step 3: Add shared page object names and surface roles**

  For each page family, mark the root/page surface, page header, content card, action bar, primary action, secondary action, table, editable cell, read-only cell, info note, warning/error message, and status label with object names or dynamic properties. This is a styling-only migration.

- [ ] **Step 4: Replace legacy page-local visual rules**

  Remove or replace `#d4d0c8`, `#5c9bd5`, `#0078d7`, Arial-only declarations, `QPalette` light/dark-gray overrides, and `outset`/`inset` button borders from the migrated surfaces. Use the centralized palette: white cards, light cool-gray canvas, navy/slate shell, teal primary actions, neutral secondary actions, colorful graph series, muted separators, and semantic warning/error colors.

- [ ] **Step 5: Make dense content use available width**

  Replace visual-only fixed-width/fixed-height constraints that prevent normal laptop expansion with size policies, layout stretches, and scroll-area behavior. Retain fixed dimensions only when they encode a domain grid or a control that must remain compact for data readability.

- [ ] **Step 6: Keep confirmation dialogs and messages readable**

  Migrate QMessageBox and custom dialog styles to the same dark theme while preserving titles, buttons, confirmation requirements, and result messages.

- [ ] **Step 7: Run focused migration tests and verify they pass**

  Run the command from Step 2. Expected: PASS.

### Task 4: Regression coverage and real startup verification

**Files:**
- Modify: `tests/test_maintenance_ui.py` only if existing assertions need stable object-name coverage.
- Modify: `tests/test_*ui*.py` only where new visual invariants belong beside existing behavior tests.
- Create or modify: `tests/test_theme.py`, `tests/test_main_window_theme.py`, `tests/test_theme_migration.py`.

**Interfaces:**
- No production behavior beyond visual properties is introduced.

- [ ] **Step 1: Run all UI and domain tests in the project environment**

  Run:

  ```bash
  QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q
  ```

  Expected: all tests pass. Do not use system `python3` for project verification.

- [ ] **Step 2: Run compile and whitespace checks**

  Run:

  ```bash
  .venv/bin/python -m compileall -q core ui tests
  git diff --check
  ```

  Expected: both commands exit successfully.

- [ ] **Step 3: Run the offscreen startup smoke test**

  Instantiate `QApplication`, call `init_db()`, construct `MainWindow`, show it, process events, resize it to a laptop-sized window, and construct representative pages through their existing entry points. Expected output: a successful startup message and no exceptions.

- [ ] **Step 4: Review the final diff for logic preservation**

  Inspect `git diff --stat`, `git diff --check`, and the full changed-file list. Confirm that changes are limited to theme/layout/object-name code, tests, and the design/plan documents; preserve all unrelated working-tree changes.
