# Working-Curve Normalized Storage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add normalized working-curve standards, measurements, versioned coefficients, activation, migration, and regression visualization without breaking the existing workflow.

**Architecture:** Add group-scoped SQLAlchemy tables and a pure service layer for standards, measurements, curve versions, activation, migration, and fit statistics. Existing JSON remains a compatibility source, while UI pages move to normalized reads/writes and Page 5 becomes an explicit curve-version manager.

**Tech Stack:** Python, PyQt6, SQLAlchemy/SQLite, NumPy when available, native QPainter graph, `.venv` pytest.

**Spec:** `docs/superpowers/specs/2026-10-24-working-curve-normalized-storage-design.md`

## Global Constraints

- Run all checks only through `.venv`.
- Keep working-curve standards distinct from H/L/K drift samples.
- Keep all normalized records scoped to an Analytical Group.
- Preserve existing JSON and make migration idempotent.
- Store at most one active curve per Analytical Group + element.
- Do not auto-activate a newly calculated curve.
- Do not add a plotting dependency.

## Review Focus

- Existing JSON data on first startup must migrate without duplication.
- Re-saving the same standard or Job 7 measurement must update rather than duplicate it.
- Activating a curve must deactivate only the same group + element's previous active curve.
- A curve with too few points or singular data must not be filed as a valid active curve.
- Correction must prefer the active normalized curve while retaining compatibility fallback.

---

### Task 1: Normalized Models and Migration

**Files:**
- Modify: `core/persistence/models.py`
- Create: `core/persistence/working_curve_repository.py`
- Modify: `core/persistence/database.py`
- Test: `tests/test_working_curve_repository.py`

**Interfaces:**
- Models: `WorkingStandard`, `WorkingStandardValue`, `WorkingCurveMeasurement`, `WorkingCurve`, `WorkingCurveCoefficient`.
- `migrate_working_curve_json(session) -> dict`.
- `list_standards(session, group_id)`, `upsert_standard(session, group_id, sample, values)`.
- `upsert_measurement(session, group_id, sample, intensities, burn_count)`.
- `create_curve_version(session, group_id, element, curve_type, coefficients, fit_stats, source_point_count)`.
- `activate_curve(session, curve_id)` and `retire_curve(session, curve_id)`.
- `get_active_coefficients(session, group_id, element)`.

- [ ] **Step 1: Write failing repository tests** for model creation, idempotent JSON migration, standard/value upsert, measurement replacement, version creation, and one-active-per-group-element activation.
- [ ] **Step 2: Run focused tests with `.venv`** and confirm missing model/repository failures.
- [ ] **Step 3: Add normalized SQLAlchemy models** with uniqueness constraints for group/sample, group/sample/element measurements, and group/element/curve activation rules enforced in service transactions.
- [ ] **Step 4: Implement repository operations** with uppercase sample normalization, numeric coercion, and no duplicate writes.
- [ ] **Step 5: Implement idempotent migration** from the three existing JSON fields and call it after `create_all` in `init_db()`.
- [ ] **Step 6: Run focused tests and the full `.venv` suite.**

### Task 2: Curve Math and Correction Integration

**Files:**
- Create: `core/analysis/working_curve_service.py`
- Modify: `core/analysis/correction_engine.py`
- Test: `tests/test_working_curve_service.py`
- Modify: `tests/test_correction_engine.py`

**Interfaces:**
- `fit_polynomial(points, degree) -> dict` returning `a,b,c,d,r2,rmse,residuals`.
- `build_calibration_pairs(measurements, standards, element) -> list`.
- `predict_intensity(coefficients, intensity) -> float`.
- `active_curve_coefficients(group_id, element, session) -> dict | None`.

- [ ] **Step 1: Write failing tests** for linear/quadratic/cubic coefficient mapping, residual/R² calculation, insufficient/singular points, and active normalized coefficient precedence.
- [ ] **Step 2: Run focused tests and observe expected failures.**
- [ ] **Step 3: Implement pure fit/pair/statistics services** using NumPy if available and the existing Gaussian fallback otherwise.
- [ ] **Step 4: Update correction loading** so active normalized coefficients are preferred when a session/group id is available; retain current JSON fallback for callers without a repository lookup.
- [ ] **Step 5: Run focused and full `.venv` tests.**

### Task 3: Standards and Job 7 Normalized Writes

**Files:**
- Modify: `ui/regression/chemical_standards_page.py`
- Modify: `ui/analysis/analysis_run_job7.py`
- Test: `tests/test_working_curve_ui_dataflow.py`

**Interfaces:**
- Standards page loads/saves through repository operations.
- Job 7 `_save_standard_measurement()` writes `WorkingCurveMeasurement` and keeps legacy JSON compatibility write only if needed by old callers.

- [ ] **Step 1: Write failing dataflow tests** for standards read/write, duplicate standard replacement, Job 7 measurement replacement, and import/export compatibility.
- [ ] **Step 2: Run focused UI/dataflow tests and observe failures.**
- [ ] **Step 3: Replace direct JSON persistence in Chemical Standards with repository-backed persistence while preserving the existing table behavior.
- [ ] **Step 4: Update Job 7 storage to normalized measurements and fix its average display formatting if still incorrect.
- [ ] **Step 5: Run focused and full `.venv` tests.**

### Task 4: Regression Filing and Version Management UI

**Files:**
- Modify: `ui/regression/regression_calculation_page.py`
- Modify: `ui/anainf/page_05_working_curve.py`
- Create: `ui/regression/working_curve_chart.py`
- Test: `tests/test_working_curve_regression_ui.py`

**Interfaces:**
- Regression reads normalized standards/measurements, calculates candidate fits, and files a new inactive `WorkingCurve` version.
- Page 5 loads normalized versions and exposes explicit Activate/Retire actions.
- `WorkingCurveChart.set_points(points, coefficients)` stores renderable observed/predicted/residual data and paints a diagnostic chart.

- [ ] **Step 1: Write failing UI/service-boundary tests** for normalized pair loading, filing a new inactive curve, version listing, activation, retirement, and chart data.
- [ ] **Step 2: Run focused tests and observe failures.**
- [ ] **Step 3: Update Regression Calculation to use repository data, show fit statistics, and file versions without auto-activation.
- [ ] **Step 4: Add the native chart and residual summary; avoid pixel-based tests by asserting stored chart data.
- [ ] **Step 5: Update Page 5 to list curve versions/coefficient summaries and provide explicit activation/retirement controls while retaining manual coefficient editing for the active record.
- [ ] **Step 6: Run focused and full `.venv` tests.**

### Task 5: Navigation, Compatibility, and Final Verification

**Files:**
- Modify: `ui/main_window.py` or existing regression navigation only if needed
- Modify: `README.md`
- Test: existing suite plus offscreen startup smoke

- [ ] **Step 1: Ensure the existing Chemical Standards, Job 7, Regression, and Page 5 navigation paths expose the normalized workflow without a new duplicate menu.
- [ ] **Step 2: Update README with table ownership, migration behavior, active-curve semantics, and standard-versus-drift distinction.
- [ ] **Step 3: Run `QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q`.
- [ ] **Step 4: Run `.venv/bin/python -m py_compile` on all changed Python files and `git diff --check`.
- [ ] **Step 5: Run an offscreen startup and repository migration smoke test, then report exact results and any hardware-only limitations.**
