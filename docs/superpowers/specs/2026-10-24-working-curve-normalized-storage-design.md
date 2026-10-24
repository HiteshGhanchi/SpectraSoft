# Working-Curve Standards and Versioned Curves Design

## Intent

Replace the current single-JSON working-curve storage with normalized,
group-scoped records that support multiple working-curve versions while
preserving the existing standards, Job 7, Regression, and Page 5 workflows.

## Goals

- Store registered working-curve standard samples separately from drift samples.
- Store one known chemical value per standard and applicable element.
- Store Job 7 drift-corrected intensities as measurements tied to a standard.
- Store multiple curve versions per Analytical Group and element.
- Store curve type, coefficients `a`, `b`, `c`, `d`, point count, fit quality,
  and active/retired state.
- Allow only one active curve per Analytical Group + element.
- Preserve and migrate existing JSON data without deleting it.
- Keep the current Page 5, Chemical Standards, Job 7, and Regression entry
  points, but make them use normalized data.
- Show regression fit quality visually with a simple observed-versus-predicted
  chart and residual information.

## Non-goals

- Changing drift-sample storage or H/L/K calculations.
- Automatically choosing a curve degree or activating a curve without operator
  action.
- Treating linear, quadratic, and cubic candidates as simultaneously active.
- Building a global standard-sample library shared across Analytical Groups.
- Adding external plotting dependencies.

## Storage model

```text
AnalyticalGroup
    ├── WorkingStandard (sample identity and inclusion)
    │     └── WorkingStandardValue (known concentration per element)
    ├── WorkingCurveMeasurement (Job 7 corrected intensity per standard/element)
    └── WorkingCurve (version/type/status per element)
          └── WorkingCurveCoefficient (a,b,c,d per curve/element)
```

All records are scoped to an Analytical Group. A standard can be physically
reused by the laboratory, but the registered standard record remains group-
specific, matching the manual's method-centered flow.

## Curve lifecycle

1. Register or edit standards and known values.
2. Job 7 measures one registered standard and replaces that standard's latest
   measurement for each applicable element.
3. Regression reads normalized measurements and known values, fits linear,
   quadratic, or cubic candidates, and displays residuals/R².
4. Operator files a selected candidate as a new curve version.
5. Operator explicitly activates one curve per group + element; activating a
   curve deactivates the previous active curve for that element.
6. Routine correction reads the active normalized curve. Existing JSON remains
   as a fallback during migration/compatibility.

## Migration

At database initialization, an idempotent migration imports:

- `page_05_chemical_standards.standards` into `WorkingStandard` and
  `WorkingStandardValue`.
- `page_05_wc_measurements.measurements` into
  `WorkingCurveMeasurement`.
- `page_05_wc.coefficients` into one imported `WorkingCurve` version per
  element, preserving coefficients and marking it active where it is the
  current Page 5 row.

The migration never overwrites normalized records and never removes JSON.

## UI and graphics

- Chemical Standards page remains the standard registry and writes normalized
  standard/value rows.
- Job 7 writes normalized measurement rows and displays the selected standard's
  current burn average.
- Regression Calculation reads normalized pairs and files a new curve version.
- Add a curve-management panel on Page 5 showing curve versions, type, active
  state, coefficients, and Activate/Retire actions.
- Add a lightweight native `QPainter` observed-versus-predicted chart with a
  residual summary. It is diagnostic only; it does not decide which curve the
  operator must activate.

## Acceptance criteria

1. Existing JSON-only data is migrated once into normalized tables.
2. Standards and known values can be saved/read back from normalized records.
3. Job 7 stores a measurement linked to a registered standard and group.
4. Regression can calculate candidates from normalized data and file a new
   curve version with coefficients and fit statistics.
5. Multiple versions can coexist for one group + element.
6. Activating one version deactivates the previous version for that group +
   element.
7. Correction uses the active normalized coefficient when present.
8. Page 5 displays versions and supports explicit activation/retirement.
9. All existing tests remain green and the application starts offscreen.
