# Matrix Correction Versioning Design

Date: 2026-10-24

## Intent

Complete the matrix-element correction workflow as the next stage after working-curve calibration. Matrix correction uses the active working curve to calculate an initial target concentration (`C0`), compares it with certified target values from working-curve standards, and derives optional interference coefficients for Page 6.

The result must be versioned and explicitly activated, just like working curves, so an operator can review candidates without changing routine analysis unexpectedly.

## Goals

- Use normalized working-curve standards and Job 7 measurements as the matrix-regression inputs.
- Use the active normalized working curve for the target element when calculating `C0`.
- Support both documented correction types:
  - `L`: additive/overlap correction;
  - `D`: multiplicative matrix correction.
- Store matrix coefficient candidates with version, status, fit statistics, and source-point count.
- Allow explicit activation and retirement.
- Enforce one active correction per Analytical Group + target element + interfering element + correction type.
- Keep the existing `page_06_matrix` JSON readable and writable for compatibility.
- Make routine correction prefer active normalized matrix coefficients and fall back to legacy Page 6 JSON.
- Add tests for calculation, pairing, activation, migration, and correction behavior.

## Non-goals

- No new instrument or MCU commands.
- No hardware-specific matrix measurement job.
- No change to the working-curve polynomial itself.
- No automatic activation after matrix regression.
- No removal of legacy JSON fields in this iteration.

## Constraints

- Preserve the existing PyQt6 and SQLAlchemy stack.
- Use the project's `.venv` for verification.
- Keep matrix correction after working-curve conversion and before master-curve correction.
- Do not invent physical hardware mappings absent from `USER_FLOW.md` or verified instrument behavior.
- A matrix correction is optional; no configured rows means neutral correction.

## Approaches

### Option 1: Extend legacy Page 6 JSON

Keep storing calculated coefficients directly in `AnalyticalGroup.page_06_matrix` and improve validation/tests. This is smaller, but does not provide candidate history, explicit activation, or normalized querying.

### Option 2: Normalized versioned matrix corrections — selected

Add normalized matrix correction/version records, migrate legacy Page 6 rows, and make Page 6 display active normalized rows while retaining JSON compatibility. This matches the working-curve architecture and provides safe review/activation behavior.

Option 2 is selected because matrix correction depends directly on the active working curve and must not silently replace a production correction when a new regression candidate is calculated.

## Data model

Add normalized records scoped to `AnalyticalGroup`:

### `MatrixCorrection`

- `id`
- `analytical_group_id`
- `target_element_key`
- `interfering_element_key`
- `correction_type` (`L` or `D`)
- `coefficient`
- `status` (`inactive`, `active`, or `retired`)
- `version_name`
- `point_count`
- `r2`
- `rmse`
- `created_at`
- `retired_at`

Add a partial uniqueness constraint so only one active row exists for:

```text
Analytical Group + target element + interfering element + correction type
```

Each matrix regression operation creates one inactive candidate for the selected target/interfering/type pair. Multiple active rows may exist for one target when they refer to different interfering elements or correction types; the correction engine combines them using the existing L-then-D formula.

## Matrix regression flow

```text
Select target element
Select interfering element
Select L or D
        ↓
Read normalized standards and Job 7 measurements
        ↓
Read active normalized target working curve
        ↓
Calculate C0 for each standard
        ↓
Compare C0 with certified target concentration
        ↓
Calculate coefficient
        ↓
Show paired points, errors, coefficient, R²/RMSE, and point count
        ↓
File inactive matrix candidate
        ↓
Activate explicitly from Page 6
```

The formulas remain:

```text
error = C_true - C0

L = Σ(Cj × error) / Σ(Cj²)

D = Σ((C0 × Cj) × error) / Σ((C0 × Cj)²)
```

where `Cj` is the certified interfering-element concentration.

At least one valid paired point is required, and a zero denominator is rejected. Fit quality is calculated from the predicted corrected concentrations versus certified target values.

## Page 6 behavior

Page 6 remains the operator-facing Matrix Correction Information page.

- List active normalized corrections first.
- Show target, type, interfering element, coefficient, version, point count, and fit quality.
- Allow activation of an inactive candidate.
- Allow retirement of an active candidate.
- Preserve manual editing for compatibility, but save edited active values to normalized storage when possible.
- Keep the legacy JSON representation synchronized for older consumers.
- Empty Page 6 means no matrix correction is applied.

## Correction pipeline

The runtime chain remains:

```text
drift correction
    ↓
active working curve
    ↓
matrix correction
    ↓
master correction
    ↓
purity/result calculation
```

`CorrectionEngine.apply_matrix()` will receive active normalized matrix rows through the same group-data preparation path used for active working-curve coefficients. If no normalized active row exists for a pair, it will use the corresponding legacy Page 6 row.

For each target:

```text
after_l = C0 + Σ(Lj × Cj)
final = after_l × (1 + Σ(Dj × Cj))
```

Interfering values are read from the pre-matrix concentration map so corrections do not cascade through one another.

## Migration

At database initialization:

```text
AnalyticalGroup.page_06_matrix.corrections
        ↓
MatrixCorrection(status="active")
```

Migration is idempotent and must not duplicate rows. Existing JSON remains intact. Normalized active rows take precedence per pair/type, while legacy rows remain a fallback.

## Acceptance criteria

- A matrix candidate can be calculated from normalized standards and Job 7 measurements.
- The calculation uses the active normalized target working curve rather than only legacy Page 5 JSON.
- Both `L` and `D` coefficients calculate correctly.
- A candidate is inactive until explicitly filed and activated.
- Activating a candidate retires/deactivates the prior active row for the same group/target/interfering/type.
- Multiple active interfering-element rows combine correctly for one target.
- Page 6 displays active and candidate versions and supports activation/retirement.
- Legacy Page 6 JSON migrates once and remains compatible.
- `CorrectionEngine` applies normalized matrix rows, then legacy fallback rows where necessary.
- Existing working-curve, drift, ATT, and master-curve tests remain passing.

## Builder calls

- Use the existing normalized working-curve repository patterns rather than introducing a separate service layer unless required by testability.
- Keep the current `MatrixCalculationPage` as the regression entry point and evolve its data source and filing behavior.
- Preserve the existing Page 6 table layout where practical; add version/status information without disrupting manual workflows.
- Treat fit statistics as diagnostics, not as an automatic activation threshold.
