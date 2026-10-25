# SpectraSoft Application Theme Design

## Intent

Give the PyQt6 laptop application one professional, readable, full-width visual
language inspired by the supplied dark project-management screenshot, without
changing the analytical workflow, persistence behavior, hardware behavior, or
navigation destinations.

The intended user is an operator configuring analytical groups, running
instrument workflows, reviewing results, and maintaining backups. The UI
should make the current area, active group, editable fields, read-only data,
and primary actions obvious at a glance.

## Goals

- Replace the current mixed Windows-95/legacy styling with a consistent light
  laboratory dashboard theme with a navy/slate shell and colorful accents.
- Make the main window resizable and use the available laptop screen width,
  while retaining sensible minimum sizes for dense analytical controls.
- Preserve every existing control, label, validation rule, signal, and data
  flow unless a visual adjustment is required for layout.
- Centralize application-level QSS tokens and shared widget rules.
- Make navigation, analytical-group selection, forms, tables, dialogs, status
  messages, and action buttons visually coherent in the new shell.
- Keep the interface readable in offscreen tests and on normal desktop DPI.

## Non-goals and anti-goals

- No dark-mode system or runtime theme switch in this change.
- No new third-party UI dependency.
- No hardware protocol, database, calculation, or business-rule changes.
- No decorative dashboard that hides or removes required instrument fields.
- No fixed-size main window or page layout that wastes the available width.
- No broad rewrite of working page logic solely to change appearance.

## Proposed visual language

- **Shell:** deep navy/slate application chrome with a compact top toolbar and
  a dark left navigation rail.
- **Canvas:** light cool-gray work surface with white cards and panels, so the
  application stays bright and readable on a laptop screen.
- **Accent:** teal/cyan for active navigation and primary progress, with blue,
  violet, magenta, amber, and green used deliberately for semantic emphasis,
  graph series, validation, and status.
- **Data state:** pale blue/teal selected rows, clear read-only contrast,
  muted table separators, and restrained warning/error colors.
- **Typography:** Qt's platform sans-serif font rather than hard-coded Arial,
  with compact but readable labels and stronger section hierarchy.
- **Shape:** 5–7px corner radius, 1px low-contrast borders, consistent
  8/12/16px spacing, and no raised/inset 1990s button borders.

## Approaches considered

1. **Global-only stylesheet**
   - Smallest code change.
   - Rejected because page-level `setStyleSheet()` calls and palette overrides
     would continue to produce visibly different themes.

2. **Shared theme module plus targeted migration — selected**
   - Add one theme module with application QSS and reusable style helpers.
   - Update the main shell, analytical-group panel, core analytical pages,
     settings/regression/report/maintenance surfaces, and inline message
     styling that currently overrides the global palette.
   - Use a three-zone laptop layout where practical: left navigation, central
     working area, and a narrow contextual/status area; pages that need more
     width may use the full central area.
   - Preserve page behavior and use layout managers with stretch policies.
   - Best balance of consistency, safety, and reviewability for this codebase.

3. **Full page-by-page redesign**
   - Maximum visual control.
   - Rejected for this pass because it would unnecessarily risk working
     analytical workflows and expand the scope beyond a uniform theme.

## Implementation outline

1. Add `ui/theme.py` containing light color/spacing tokens, the application
   QSS, and small helpers for page headers, primary/secondary buttons, and
   status labels.
2. Apply the stylesheet once in `main.py` using the existing QApplication.
3. Refactor `MainWindow` to use a resizable/minimizable/maximizable laptop
   window, a compact dark navigation panel, full-width right content, and the
   new toolbar/menu/status-bar styling.
4. Migrate `GroupPanel` and the most visible shared/page surfaces away from
   hard-coded legacy colors and fixed-width-only containers.
5. Keep specialized table cell background colors only where they communicate
   read-only/editable state; replace legacy colors with theme tokens.
6. Add UI regression tests for the theme application, resizable shell, and
   key widget state/style properties without asserting fragile pixel output.

## Acceptance criteria

- Starting the app displays the new light dashboard theme without exceptions.
- The main window can be resized and uses the available laptop width; no
  fixed 1100x680 restriction remains.
- Analytical Group selection, page navigation, forms, tables, dialogs, and
  status messages remain usable.
- Primary and secondary actions are visually distinguishable across pages.
- No visible legacy `#d4d0c8`, outset/inset button treatment, or conflicting
  per-page theme remains in the migrated surfaces.
- Existing project tests pass in `.venv`, and an offscreen startup smoke test
  passes.

## Builder decisions

- The selected palette is a light application canvas with navy/slate shell
  surfaces and colorful semantic accents. This keeps dense analytical pages
  readable and avoids an uninviting all-charcoal interface.
- This is a laptop-only desktop layout: it should use the available screen
  width rather than behave like a narrow responsive phone/tablet layout.
- The first migration focuses on shared shell and high-traffic surfaces; any
  page-specific styling that is semantically meaningful remains but is mapped
  to the same visual tokens.
