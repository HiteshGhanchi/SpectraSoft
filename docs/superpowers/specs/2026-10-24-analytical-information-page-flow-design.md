# Analytical Information Page Flow Design

## Intent

Make the Analytical Information setup flow match the requested method-creation
order:

1. Analytical Condition
2. Order of Analytical Channel & Internal Standard
3. ATT Settings for the selected channels only

## Goals

- Preserve the existing three page classes and SQLite JSON storage.
- Rewire Previous/Next navigation to the requested order.
- Prevent navigation from Order/ISE to ATT when no ITG channel is selected.
- Make ATT display and save values only for the selected ITGs in the active
  Analytical Group.
- Keep existing saved ATT values for selected ITGs and default new selections
  to `0`.

## Non-goals

- Changing the MCU protocol or scientific ATT calculation.
- Changing the meaning of Page 3's ISE reference.
- Adding new database tables or replacing the existing page JSON fields.
- Changing later Analytical Information pages.

## Approach

Use the existing page widgets with focused changes:

- Page 1 `Next` opens Page 3; Page 1 `Previous` remains the group home.
- Page 3 `Next` validates that at least one ITG is selected and each selected
  row has SEQ 1, 2, or 3, then opens Page 2.
- Page 3 `Previous` returns to Page 1.
- Page 2 reads the active group's `page_03_channel` JSON, resolves those ITGs
  through `MasterElement`, and renders only those rows.
- Page 2 `Previous` returns to Page 3.
- If Page 2 is constructed with no selected channels, it renders an empty
  table and an explanatory message; normal navigation prevents reaching that
  state.

## Verification

Add hardware-free regression tests for selected-channel ATT collection and
validation, then run the existing test suite and import/compile checks.
