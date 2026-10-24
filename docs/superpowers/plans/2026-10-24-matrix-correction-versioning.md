# Matrix Correction Versioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a versioned, normalized matrix-correction workflow that uses the active working curve to calculate matrix coefficients and requires explicit activation before routine analysis uses them.

**Architecture:** Extend the existing SQLAlchemy normalized calibration model with a `MatrixCorrection` version table and repository operations. Update matrix regression and Page 6 to read/write normalized active/candidate records while preserving `page_06_matrix` JSON compatibility. Feed active normalized rows into the existing correction engine with legacy fallback.

**Tech Stack:** Python, PyQt6, SQLAlchemy 2.x, SQLite, unittest/pytest, native Qt widgets.

**Spec:** `docs/superpowers/specs/2026-10-24-matrix-correction-versioning-design.md`

## Global Constraints

- Use the project's `.venv` for verification.
- Preserve the existing PyQt6 and SQLAlchemy stack.
- No new instrument or MCU commands.
- Matrix correction remains after working-curve conversion and before master-curve correction.
- No automatic activation after matrix regression.
- Keep legacy Page 6 JSON readable and writable.
- No configured matrix correction means neutral correction.
- Use Page 3 normalized element symbols/`ELE` values as canonical element keys.

## Review Focus

- A candidate calculated from one working-curve version must retain that source curve ID; test that the source ID is stored and displayed.
- A new active matrix row must not cause a legacy JSON row to be applied twice; test normalized precedence and de-duplication.
- Multiple interfering elements and mixed L/D rows must combine as L-first then D using original pre-matrix values; test the full correction formula.
- Retired/deactivated normalized rows must not silently reappear through legacy fallback; test the merge rule.
- Missing, invalid, or zero-denominator paired data must fail clearly without filing a candidate; test the boundary.

---

### Task 1: Add normalized matrix-correction model and repository

**Files:**
- Modify: `core/persistence/models.py`
- Modify: `core/persistence/working_curve_repository.py` or create `core/persistence/matrix_correction_repository.py` if separation is cleaner
- Modify: `core/persistence/database.py`
- Test: `tests/test_matrix_correction_repository.py`

**Interfaces:**
- Produces `MatrixCorrection` with target/interfering element keys, `L`/`D` type, coefficient, lifecycle status, source working-curve ID, point count, R², RMSE, timestamps, and version name.
- Produces repository functions: `create_matrix_candidate`, `activate_matrix_correction`, `retire_matrix_correction`, `list_matrix_corrections`, `get_active_matrix_corrections`, `update_active_matrix_coefficient`, `migrate_matrix_json`.

- [ ] **Step 1: Write failing repository tests** for candidate creation, multiple versions, activation uniqueness per group/target/interfering/type, retirement, active lookup, source curve ID, and idempotent legacy JSON migration.
- [ ] **Step 2: Run the focused tests** with `QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q tests/test_matrix_correction_repository.py`; expect failures because the model and repository functions do not exist.
- [ ] **Step 3: Add the SQLAlchemy model** with a SQLite partial unique index for active rows on `(analytical_group_id, target_element_key, interfering_element_key, correction_type)`.
- [ ] **Step 4: Implement repository operations** using normalized uppercase element keys, inactive candidates by default, explicit activation, retirement, and active lookup.
- [ ] **Step 5: Implement idempotent migration** from `AnalyticalGroup.page_06_matrix["corrections"]`, preserving legacy JSON and treating migrated rows as active compatibility records.
- [ ] **Step 6: Call matrix JSON migration from `init_db()`** after table creation and working-curve migration.
- [ ] **Step 7: Rerun the focused repository tests** and expect PASS.

### Task 2: Add matrix-pair regression service

**Files:**
- Create: `core/analysis/matrix_correction_service.py`
- Test: `tests/test_matrix_correction_service.py`

**Interfaces:**
- `build_matrix_pairs(session, group_id, target_element, interfering_element, working_curve_id=None) -> list[dict]`
- `calculate_matrix_coefficient(pairs, correction_type) -> dict`
- `predict_matrix_corrected(pair, coefficient, correction_type) -> float`

- [ ] **Step 1: Write failing tests** for normalized standard/measurement joins, active working-curve polynomial use, L and D formulas, point count, R²/RMSE, case-insensitive keys, and missing/zero-denominator data.
- [ ] **Step 2: Run the focused service tests** and expect failures because the service does not exist.
- [ ] **Step 3: Implement normalized joins** by `WorkingStandard.id`, using known target/interfering values and `WorkingCurveMeasurement.corrected_intensity`.
- [ ] **Step 4: Resolve the active working curve** through the existing repository; allow explicit `working_curve_id` for reproducible candidate calculation and legacy Page 5 fallback only when no normalized curve exists.
- [ ] **Step 5: Implement the exact formulas**:
  - `error = certified_target - C0`
  - `L = Σ(Cj * error) / Σ(Cj²)`
  - `D = Σ((C0 * Cj) * error) / Σ((C0 * Cj)²)`
  - report coefficient, point count, R², RMSE, and per-point predictions/residuals.
- [ ] **Step 6: Reject empty pairs and zero denominators** with clear `ValueError` messages.
- [ ] **Step 7: Rerun the focused service tests** and expect PASS.

### Task 3: Integrate matrix regression UI and filing

**Files:**
- Modify: `ui/regression/matrix_calculation_page.py`
- Modify: `ui/regression/regression_calculation_page.py` only if shared active-curve or navigation helpers are needed
- Test: `tests/test_matrix_calculation_ui_dataflow.py`

**Interfaces:**
- Matrix Calculation page consumes `build_matrix_pairs()` and `calculate_matrix_coefficient()`.
- Filing creates an inactive normalized candidate with the selected source working-curve ID and diagnostics.

- [ ] **Step 1: Write failing data-flow tests** for selecting target/interfering/type, using active normalized working-curve coefficients, calculating diagnostics, and filing inactive candidates without changing the active row.
- [ ] **Step 2: Run the focused UI data-flow tests** and expect failures.
- [ ] **Step 3: Replace legacy-only pair construction** with the matrix service while retaining legacy fallback for groups not yet migrated.
- [ ] **Step 4: Extend the result display** with coefficient, point count, R², RMSE, and source working-curve version.
- [ ] **Step 5: Change “File to Page 6”** to create a normalized inactive candidate and synchronize the compatibility JSON representation without activating it.
- [ ] **Step 6: Rerun the focused UI data-flow tests** and expect PASS.

### Task 4: Integrate version management into Page 6

**Files:**
- Modify: `ui/anainf/page_06_matrix.py`
- Test: `tests/test_matrix_page_ui.py`

**Interfaces:**
- Page 6 lists active and inactive/retired normalized candidates.
- Page 6 exposes activation, retirement, and compatible manual editing.

- [ ] **Step 1: Write failing tests** for loading version rows, activating a candidate, retiring an active row, editing an active coefficient, and synchronizing legacy JSON.
- [ ] **Step 2: Run the focused Page 6 tests** and expect failures.
- [ ] **Step 3: Load normalized rows first**, preserving the current table layout and adding status/version/source diagnostics where space allows.
- [ ] **Step 4: Add explicit Activate and Retire actions** with confirmation and repository calls.
- [ ] **Step 5: Keep manual edits compatible** by updating the active normalized row when a matching row exists, then writing the active representation to `page_06_matrix`.
- [ ] **Step 6: Ensure retired normalized rows cannot be resurrected by JSON fallback** when the normalized store is authoritative for the same pair/type.
- [ ] **Step 7: Rerun the focused Page 6 tests** and expect PASS.

### Task 5: Feed normalized matrix corrections into runtime correction

**Files:**
- Modify: `core/analysis/correction_engine.py`
- Modify: the shared group-data preparation path used by analysis workers/jobs, identified by existing `page_05_active_coefficients` loading
- Test: `tests/test_correction_engine.py`

**Interfaces:**
- Runtime group data may contain `page_06_active_corrections` or an equivalent normalized active-row map/list.
- `CorrectionEngine._get_page6_corrections()` merges normalized active rows over legacy rows by target/interfering/type without duplicates.

- [ ] **Step 1: Add failing tests** for normalized precedence, legacy fallback, retired-row suppression, multiple interferers, and L-before-D calculation.
- [ ] **Step 2: Run the focused correction tests** and expect failures.
- [ ] **Step 3: Implement normalized/legacy merge logic** with canonical uppercase keys and normalized rows authoritative for matching pair/type.
- [ ] **Step 4: Preserve the current non-cascading behavior** by reading interfering concentrations from the original pre-matrix map.
- [ ] **Step 5: Rerun correction tests** and expect PASS.

### Task 6: Migration, startup, full regression, and cleanup checks

**Files:**
- Modify: `README.md` if the matrix storage documentation needs updating
- Modify: `docs/superpowers/specs/2026-10-24-matrix-correction-versioning-design.md` only for implementation clarifications discovered during coding
- Modify: `docs/superpowers/plans/2026-10-24-matrix-correction-versioning.md` to check off completed steps

- [x] **Step 1: Run all matrix tests** with `QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q tests/test_matrix_correction_repository.py tests/test_matrix_correction_service.py tests/test_matrix_calculation_ui_dataflow.py tests/test_matrix_page_ui.py tests/test_correction_engine.py` — 17 passed.
- [x] **Step 2: Run the full project test suite** with `QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q` — 86 passed.
- [x] **Step 3: Run compile checks** for changed Python files with `.venv/bin/python -m py_compile ...` — passed.
- [x] **Step 4: Run `git diff --check`** and fix only whitespace introduced by this feature — passed.
- [x] **Step 5: Run an offscreen startup/migration smoke test** that initializes the database, loads Page 6, and verifies normalized matrix rows are available without duplicating legacy rows — passed.
- [x] **Step 6: Run the requested system check** `python3 -m pytest -q` — blocked by system SQLAlchemy 1.4.50 lacking `DeclarativeBase`; project `.venv` uses SQLAlchemy 2.0.36.
