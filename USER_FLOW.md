# QC-E1 Spectroscopy Application: Functional User Flow

## 1. Purpose of This Document

This document reconstructs the functional user flow of the spectroscopy application described in `Manual.md`.

The purpose is to explain:

- what each application section does;
- what information must exist before another operation can run;
- what the operator enters manually;
- what the instrument measures;
- what each operation calculates;
- what information is stored for later use;
- how setup, calibration, analysis, maintenance, and reporting connect.

This document intentionally focuses on functional behavior. It does not copy the old DOS-style navigation, keyboard controls, or visual layout.

## 2. Interpretation Rules

1. `Manual.md` is the functional source of truth.
2. Features are separated according to the manual's functional sections.
3. Modern ideas such as historical versioning, archiving, reusable shared records, or additional database entities are not treated as manual requirements unless explicitly identified as implementation choices.
4. If the manual does not clearly define a hardware mapping, formula, or automatic behavior, this document labels it as requiring verification.
5. The MCU is treated as a low-level controller. Scientific jobs and calculations belong to the client application.

---

# Part I: Application Structure

## 3. Main Functional Sections

```text
Application
│
├── Analytical Information
│   └── Selected Analytical Group
│       ├── Analytical Group Name
│       ├── Analytical Condition
│       ├── ATT Settings
│       ├── Order of Analytical Channel and Internal Standard
│       ├── Drift Correction Information
│       ├── Working Curve Information
│       ├── Matrix Element Correction Information
│       ├── Master Curve Correction Information
│       └── Result and calculation settings
│
├── Attenuator Adjustment
│   └── Operation used to determine production ATT
│
├── Regression Calculation
│   ├── Standard sample information
│   ├── Working-curve standard assignment
│   ├── Working-curve calculation
│   └── Matrix correction calculation
│
├── Analysis
│   ├── Job 2: One-point recalibration
│   ├── Job 3: Two-point recalibration
│   ├── Job 4: Master-curve/type-standard recalibration
│   ├── Job 5: Raw intensity, INT.1
│   ├── Job 6: Drift-corrected intensity, INT.2
│   ├── Job 7: Working-curve intensity
│   ├── Job 8: Drift target intensity
│   ├── Job X: Content analysis
│   └── Job Y: Special three-time content analysis
│
├── Report
│   ├── Daily reports
│   ├── Long-term repeatability
│   ├── Analytical frequency
│   ├── Stability check
│   ├── Stored result modification
│   └── Histogram
│
└── Maintenance
    ├── Waste Discharge
    ├── Manual Scanning
    ├── Lamp Test
    ├── Date and time
    ├── System backup
    ├── Maintenance Information
    ├── TAN clear
    └── Temperature, voltage, and vacuum display
```

## 4. Important Terminology

### 4.1 Analytical Information

Analytical Information is the complete collection of configuration and calculated values associated with an Analytical Group. It is not one screen.

### 4.2 Analytical Group

An Analytical Group, identified by `AG-No.`, is one complete analytical method, for example `LOW_ALLOY_STEEL`.

The group eventually contains or is associated with:

- analytical operating conditions;
- selected analytical channels;
- channel order and sequence assignment;
- internal-standard references;
- production ATT values;
- drift correction information;
- working curves;
- matrix corrections;
- master corrections;
- result calculation and output settings.

### 4.3 Analytical Condition

The Analytical Condition is a separate information page belonging to the selected Analytical Group. It defines how the instrument operates during measurement.

The manual does not establish that Analytical Conditions must be reusable global records shared by multiple groups. A safe manual-faithful model is that each selected Analytical Group has its own Analytical Condition information.

### 4.4 Job

A Job is a measurement purpose selected inside the Analysis section. Jobs use Analytical Information but do not replace it.

### 4.5 Operation Mode O

Operation Mode O contains run settings such as display behavior, printing, number of analyses, filing, transmission, and sample-index behavior. It is not a separate scientific mode.

---

# Part II: Hardware and MCU Boundary

## 5. MCU Responsibilities

The current MCU protocol provides these primitives:

```text
O,<port>,<value>  Set an output port
I                 Read the 12-bit input
T,<milliseconds>  Start a non-blocking delay
```

Responses are:

```text
K                 Command accepted
D,<value>         12-bit input result
# <text>          Debug information
```

The direct input range is:

```text
0 through 4095
```

The MCU does not know whether the client is running Manual Scanning, ATT Adjustment, Job 8, Job 3, Job 7, or Job X.

## 6. Client Application Responsibilities

The client application must decide:

- which Analytical Group is active;
- which element/channel is selected;
- which source and sequence are used;
- which ATT is applied;
- when purge, preburn, integration, and cleaning occur;
- which physical sample must be placed;
- how many burns are performed;
- how raw values are averaged;
- which formulas are applied;
- where outputs are stored.

The same MCU commands can therefore support multiple jobs. The job meaning is created by client-side workflow and storage behavior.

## 7. Hardware Mapping Requiring Verification

The generic MCU protocol does not itself explain which Port A or Port B values mean:

- select a physical ITG channel;
- set ATT;
- select Source A through F;
- control argon;
- start preburn;
- start integration;
- clean;
- safely stop/reset.

Those mappings must come from verified existing code, wiring information, or real hardware tests. They must not be invented.

The current Python scripts and MCU parser must also use the same number format. The MCU's `toInt()` parses decimal text, while strings such as `9D` or `C3` are hexadecimal-looking values. This protocol detail requires verification before hardware validation.

---

# Part III: First-Time Method Creation Flow

## 8. Step 1: Configure Physical Element Channels

### Purpose

Describe the detector/integrator channels physically present in the instrument.

### Stored information

```text
ITG/channel number
Element symbol
Element/display name
Wavelength
```

### Meaning

This tells the software:

> Physical channel X measures this element at this wavelength.

The physical channel list is global instrument information. It is not yet an Analytical Group.

### Capacity

The actual selectable channels come from the installed instrument configuration. If the current instrument has 40 configured ITG channels, those 40 are the available physical channels.

---

## 9. Step 2: Configure Source Information

### Purpose

Register the available source definitions, such as Source A through Source F.

### Stored information

```text
Source identifier
Source name/meaning
Verified hardware mapping, when available
```

### Meaning

This page defines which source choices exist. It does not decide which Analytical Group uses a source.

---

## 10. Step 3: Register Analytical Group Name

### Purpose

Create the identity of one complete analytical method.

### Fields

```text
AG-No.
Analytical Group Name
```

### Example

```text
AG-No.: 01
Group Name: LOW_ALLOY_STEEL
```

At this point, the group is only identified. It is not ready to analyze samples.

---

## 11. Step 4: Enter Analytical Condition

### Purpose

Define how the selected Analytical Group physically runs a measurement.

### Fields

```text
Purge time

SEQ1:
- Source
- Preburn time
- Integration time

SEQ2:
- Source
- Preburn time
- Integration time

SEQ3:
- Source
- Preburn time
- Integration time

CLEAN:
- Source
- Cleaning time
```

### Meaning of timing

- Purge replaces air around the emission area with the required gas condition.
- Preburn runs the source before useful measurement so the emission can stabilize.
- Integration is the period during which useful analytical intensity is collected.
- Cleaning runs the configured cleaning source for the configured time.

The Analytical Condition does not select elements and does not contain drift or working-curve coefficients.

---

## 12. Step 5: Configure Order of Analytical Channel and Internal Standard

### Purpose

Choose which physical channels are used by the selected Analytical Group and connect them to the group's sequences.

### Fields per analytical position

```text
AR-No.
ITG
ELE
NAME
SEQ
ISE Ref
```

### Meanings

- `AR-No.` is the analytical position/order within the selected group.
- `ITG` selects a physical channel from the instrument channel information.
- `ELE` identifies the element belonging to that ITG.
- `NAME` is the registered element/display name.
- `SEQ` assigns the analytical entry to SEQ1, SEQ2, or SEQ3 from the Analytical Condition.
- `ISE Ref` identifies an Internal Standard Element reference. `0 (none)` means no internal standard.

### Capacity

The analytical page provides up to 32 analytical positions:

```text
AR-No. 1 through AR-No. 32
```

This is different from the number of physically installed ITG channels.

Example:

```text
40 physical channels may exist.
One Analytical Group may select up to 32 analytical positions from them.
```

Unused analytical positions remain empty.

### Data relationship

`ELE` and `NAME` should come from the selected ITG mapping. They should not contradict the physical channel definition.

### Internal-standard calculation

The exact meaning of nonzero `ISE Ref` and the exact internal-standard mathematics must be verified from the relevant manual specification before implementation. The application should not guess whether the reference is an AR-No., ITG number, or another identifier.

---

## 13. Step 6: Determine and Store Production ATT

### 13.1 ATT Settings in Analytical Information

The ATT Settings page stores the production ATT used by the selected Analytical Group's participating channels.

ATT is relevant to the selected analytical channels, not automatically to every unused physical channel.

Example:

```text
LOW_ALLOY_STEEL
- Carbon / selected ITG: ATT value
- Silicon / selected ITG: ATT value
- Manganese / selected ITG: ATT value
```

### 13.2 Attenuator Adjustment Operation

Attenuator Adjustment is a separate main operation used to determine a suitable production ATT.

#### Inputs

```text
Selected Analytical Group
Selected analytical element/channel
Its Analytical Condition and sequence
Suitable high-content physical sample
Initial ATT
```

#### Flow

```text
Load selected group
Load selected element and sequence
Place suitable sample
Start the required source/emission sequence
Read intensity repeatedly
Change ATT
Avoid a signal that is too small or overflowing
Accept the suitable ATT
Store it in Analytical Information → ATT Settings
```

#### Relationship

```text
Attenuator Adjustment finds the value.
ATT Settings stores the accepted value.
```

The exact recommended intensity range should follow the manual's ATT Adjustment instructions and verified intensity representation.

---

# Part IV: Maintenance Preparation

## 14. Manual Scanning

### Location

```text
Maintenance → Manual Scanning
```

### Purpose

Observe one selected element's signal while the operator manually moves the physical scanning dial, so the spectral line can be aligned with the outlet slit.

### Inputs

```text
Profile sample
Selected element/ITG
Manual-scanning source information
Manual-scanning ATT
Display scale
```

### Variable values

```text
Element: selected for the session
ATT: adjustable to make the profile readable
Scale: display-only adjustment
Dial position: moved manually by the operator
Time: generated by the client
ADC intensity: measured continuously
Mark: created by the operator
```

### Flow

```text
Place profile sample
Select one element
Start emission and continuous reading
Adjust ATT if needed
Move physical scanning dial manually
Watch intensity change against time
Wait for stable regions
Mark useful points
Determine the appropriate peak position
Leave the physical dial at the selected position
```

### Output

The primary result is physical alignment. A modern implementation may also store:

```text
Selected element
Time trace
ADC values
ATT values and ATT-change events
Mark events
Optional manually entered dial positions
Session time
```

### Relationship to Task 5/Profile Script

The existing `task5_profile.py` performs the core live signal-monitoring behavior:

- selects one element;
- sets ATT;
- continuously reads ADC;
- permits ATT changes;
- stores time, element, ATT, and ADC.

That behavior is primarily related to Manual Scanning. It is not by itself the full production Attenuator Adjustment workflow.

The script still requires review for:

- operator Mark support;
- user-controlled stop versus fixed duration;
- separation of manual-scanning ATT from production ATT;
- use of verified maintenance source settings;
- verified command-number format;
- consistent timing comments and values;
- installed-channel count instead of a hard-coded total.

---

## 15. Waste Discharge

### Purpose

Prepare or stabilize the electrode/emission condition after maintenance such as electrode replacement or reforming.

### Output

```text
Completion status
Maintenance record
Updated analysis/emission counter behavior according to the manual
```

Waste Discharge is maintenance preparation. It does not create working curves or drift coefficients.

---

## 16. Lamp Test

### Purpose

Check the photometric/readout system, including the photomultiplier, high-voltage, and integration/readout path.

### Inputs

```text
Lamp-test analytical condition
Selected channels/elements
Lamp-test ATT
Repeated measurements
```

### Outputs

```text
Per-measurement result
Average
Range
Standard deviation
Coefficient of variation
Normal/warning evaluation according to the manual
```

---

# Part V: Drift Correction Flow

## 17. Drift Correction Information Page

### Purpose

Store sample identifiers, reference targets, and current drift-correction coefficients for each selected analytical element.

### Fields per element

```text
H sample name, optional
L sample name, optional
K sample name, optional

H target value
L target value
K target value

alpha
beta
k
```

### Initial state

Sample identifiers may be blank. The application must not automatically invent Sample A, B, or C.

A safe initial state is:

```text
H/L/K sample names: blank
H/L/K targets: default 0.00000 or clearly marked Not measured
alpha: 1.0000
beta: 0.00000
k: 1.0000
```

### Meaning of sample identifiers

The operator has physical homogeneous samples in the laboratory and enters identifiers such as `A`, `B`, or `C` on the Drift Correction Information page.

The same physical sample may serve different roles for different elements.

No separate top-level recalibration-sample library is assumed unless another manual section explicitly requires one.

---

## 18. Job 8: Create Drift Target Values

### Purpose

Create the baseline reference intensities for the configured H, L, and K samples.

### Preconditions

```text
Analytical Group exists
Analytical Condition exists
Analytical channels are selected
Production ATT values exist
Required H/L/K sample identifiers are entered
Instrument is in an accepted reference condition
```

### Inputs

```text
Selected Analytical Group
Configured physical H/L/K sample identifier
Physical sample placed by operator
Number of burns/run settings
```

### Flow

```text
Select Analytical Group and Job 8
Application reads H/L/K identifiers from Drift Correction Information
Application instructs operator which sample to place
Operator places that physical sample
Application loads condition, channels, sequence, and ATT
MCU performs low-level output, delay, and input operations
Client receives raw readings
Client averages accepted readings
Client stores the average in the matching target field
```

### Output

```text
H target and/or L target and/or K target
Per-burn measurement information
Accepted average
Measurement timestamp
```

### Important rule

Job 8 creates target values. It does not calculate `alpha`, `beta`, or `k`.

### Intensity representation

The MCU returns 0–4095. The manual may show intensity in another representation. Raw ADC and any processed intensity should be stored separately until the conversion rule is verified. Job 8, Job 3, Job 2, Job 6, and Job 7 must use a consistent intensity representation.

---

## 19. Job 3: Two-Point Recalibration

### Purpose

Compare today's H and L measurements with the stored H and L targets and calculate a straight-line correction.

### Inputs

```text
Stored H target
Stored L target
Current H measurement IH
Current L measurement IL
```

### Formula

```text
alpha = (Htarget - Ltarget) / (IH - IL)

beta = Htarget - alpha × IH
```

### Meaning

- `alpha` corrects the response slope.
- `beta` corrects the response offset.

### Flow

```text
Select Analytical Group and Job 3
Application identifies configured H and L samples
Operator measures H sample
Operator measures L sample
Application averages accepted H and L readings
Application reads stored H and L targets
Application calculates alpha and beta
Application stores alpha and beta in Drift Correction Information
```

### Important rule

Job 3 must not replace H and L target values.

---

## 20. Job 2: One-Point Recalibration

### Purpose

Calculate the one-point scaling factor `k` using the configured K sample.

### Inputs

```text
Stored K target
Current K measurement IK
Current alpha
Current beta
```

### Formula

```text
k = Ktarget / (alpha × IK + beta)
```

### Complete drift correction

```text
Idc = k × (alpha × I + beta)
```

### Flow

```text
Select Analytical Group and Job 2
Application identifies configured K sample
Operator measures the K sample
Application averages accepted readings
Application calculates k
Application stores k in Drift Correction Information
```

### Important rule

Job 2 must not replace the K target.

---

## 21. Other Intensity Jobs

### Job 5: Raw Intensity, INT.1

```text
Input: selected group, sample, run settings
Output: raw intensity and run statistics
No drift correction
No concentration conversion
```

### Job 6: Drift-Corrected Intensity, INT.2

```text
Input: selected group, sample, current alpha/beta/k
Output: raw intensity and Idc
No working-curve concentration conversion
```

---

# Part VI: Working-Curve Creation

## 22. Working-Curve Standard Sample Information

### Purpose

Register physical standard samples whose chemical concentrations are already known.

### Required information

```text
Sample name/identifier
Known chemical value for each applicable element
Analytical Group assignment
Inclusion/exclusion status
Measured corrected intensity, initially empty
```

### Difference from drift samples

```text
Drift sample:
Repeatable intensity is essential.
Certified concentration is not necessarily the primary requirement.

Working-curve standard:
Known chemical concentration is essential.
```

Multiple standards should cover the intended concentration range.

---

## 23. Job 7: Measure Working-Curve Standards

### Purpose

Measure the standards and store drift-corrected calibration intensities.

### Inputs

```text
Selected Analytical Group
Registered standard sample
Known concentrations
Current alpha, beta, and k
The physical standard placed on the instrument
```

### Why both group and sample are required

The Analytical Group answers:

> How should the instrument measure?

The standard sample answers:

> Which known material is being measured and where should its measurements be stored?

### Flow

```text
Select Analytical Group
Select Job 7
Select registered standard sample
Place the matching physical sample
Load group condition, channels, sequences, ISE, and ATT
Measure raw intensity I
Apply current drift correction
Calculate Idc = k × (alpha × I + beta)
Repeat configured burns
Average accepted corrected intensities
Store corrected intensity against group + sample + element
Repeat for the other working-curve standards
```

### Job 7 does not calculate coefficients

Job 7 creates calibration points:

```text
Corrected intensity Idc ↔ known concentration
```

---

## 24. Regression Calculation: Working Curves

### Purpose

Use the Job 7 calibration points to calculate candidate intensity-to-concentration equations.

### General formula

```text
C = a(Idc)³ + b(Idc)² + c(Idc) + d
```

### Candidate types

```text
Linear:
C = c(Idc) + d

Quadratic:
C = b(Idc)² + c(Idc) + d

Cubic:
C = a(Idc)³ + b(Idc)² + c(Idc) + d
```

These are alternative candidates, not three curves used together.

### Flow

```text
Read known concentrations
Read Job 7 corrected intensities
Fit linear candidate
Fit quadratic candidate
Fit cubic candidate
Show predictions, differences/residuals, and fit statistics
Operator selects the appropriate candidate
Store selected curve type and a/b/c/d
```

### Storage scope

The selected working curve belongs to:

```text
Analytical Group + Analytical Element
```

Different Analytical Groups may use the same physical channel but different working curves.

### Working Curve Information stores

```text
Selected curve type
a
b
c
d
Applicable element
Analytical Group
Other manual-defined working-curve settings
```

Historical versioning is a modern implementation option, not a required old-manual behavior. The manual-faithful minimum is one current selected curve per group and element.

---

# Part VII: Matrix Element Correction

## 25. Purpose

Correct an initial concentration when another element interferes with the target element's measurement.

### Concept

```text
Corrected intensity
    ↓
Working curve
    ↓
Initial concentration C0
    ↓
Matrix correction using interfering-element concentration
    ↓
Corrected concentration
```

### Configuration

```text
Target element
Interfering element
Correction type
Correction coefficient
```

### Main correction types

```text
L: additive/overlap-style correction
D: multiplicative/absorption-excitation-style correction
```

A documented general form is:

```text
C = C0 × (1 + Σ(Dj × Cj)) + Σ(Lj × Cj)
```

The exact selected correction form and coefficients come from Regression Calculation and the manual's matrix-correction procedure.

### Preconditions

```text
Active working curve exists
Working-curve standards have known target and interfering-element values
Job 7 measurements exist
```

### Flow

```text
Select target element
Select interfering element(s)
Use known standard compositions and working-curve outputs
Calculate the correction coefficient(s)
Review calculation result
Store selected coefficients in Matrix Correction Information
```

Matrix correction is optional and should only be configured where required.

---

# Part VIII: Master Curve / Type Standard Correction

## 26. Master Curve Correction Information

### Purpose

Store configuration and coefficients for correcting a remaining concentration-level difference against a known type-standard sample.

### Fields

```text
Type-standard/master sample identifier
Known target concentration
D1
D2
AC
MC
```

The operator initially configures the sample and target. Job 4 produces or updates the correction coefficients.

---

## 27. Job 4: Master-Curve or Type-Standard Recalibration

### Purpose

Measure a known type-standard sample and correct remaining concentration-level differences after intensity correction and working-curve conversion.

### Flow

```text
Select Analytical Group and Job 4
Application identifies the configured type-standard sample
Operator places the physical sample
Measure raw intensity
Apply drift correction
Apply working curve
Apply earlier applicable correction stages
Obtain calculated concentration Co
Compare Co with known target Ct
Use D1/D2 decision rules
Calculate or retain AC and MC as required
Store AC and MC in Master Curve Information
```

### Basic coefficient concepts

```text
AC = Ct - Co
MC = Ct / Co
```

The manual's D1/D2 rules determine when correction is accepted, unnecessary, or invalid.

### Difference from drift correction

```text
Drift correction changes intensity.
Master curve correction changes calculated concentration.
```

---

# Part IX: Result and Calculation Settings

## 28. Element Display, Print, and Transmission Information

For each selected analytical element, the method may store:

```text
Display order
Print order
Decimal places/significant digits
Magnification/exponent behavior
Transmission order
```

These change presentation and output behavior, not the physical measurement.

---

## 29. Product Specification Information

### Purpose

Store acceptable result limits for a product or grade.

### Fields

```text
Product/standard identifier
Element
Lower limit
Upper limit
Trace limit
```

A product specification is not necessarily a physical sample.

### Result flags

```text
H: result above upper limit
L: result below lower limit
Tr: trace-level result
```

---

## 30. R-Control Information

### Purpose

Define acceptable differences between repeated burns.

If repeated results differ more than permitted, the application raises an `R` condition.

R-control is also used by the special three-time analysis workflow.

---

## 31. 100% Correction, Purity, and Special Calculations

These are optional method-defined calculation stages.

They must remain disabled unless configured. Their exact formulas and ordering must follow the relevant manual sections and must not be guessed.

Special or virtual element formulas require explicit validation and calculation rules.

---

# Part X: Routine Operational Flow

## 32. First-Time Analytical Method Completion Sequence

```text
1. Configure physical ITG channels, elements, and wavelengths.
2. Configure Source A–F information.
3. Register Analytical Group name.
4. Enter that group's Analytical Condition.
5. Select up to 32 analytical entries from installed ITG channels.
6. Assign AR-No., SEQ, and ISE Ref.
7. Use Attenuator Adjustment to determine production ATT.
8. Store accepted ATT for selected analytical channels.
9. Enter optional H/L/K sample identifiers in Drift Correction Information.
10. Use Job 8 to create required H/L/K target values.
11. Use Job 3 and/or Job 2 to establish current drift coefficients.
12. Register working-curve standards and known compositions.
13. Assign the standards to the Analytical Group.
14. Use Job 7 to measure corrected standard intensities.
15. Use Regression Calculation to calculate candidate working curves.
16. Select and store one active working curve per group and element.
17. Calculate and store matrix corrections where required.
18. Configure master/type-standard information where required.
19. Run Job 4 where master correction is used.
20. Configure display, printing, product limits, R control, and optional calculations.
21. Verify the completed method with appropriate known/check samples.
22. Use the method for routine unknown-sample analysis.
```

Manual Scanning, Waste Discharge, and Lamp Test are maintenance/preparation workflows performed where required by instrument condition and laboratory procedure. Manual Scanning is not automatically required before every operation.

---

## 33. Daily or Routine Preparation

A routine operating sequence is:

```text
Start application and instrument
Check instrument readiness/status
Prepare stand, electrode, and sample surface
Run Waste Discharge when required
Run Manual Scanning when optical alignment requires checking
Run the selected recalibration workflow
Run master/type-standard recalibration when configured
Measure a known/check sample
Proceed only when verification is acceptable
Analyze unknown samples
Store accepted results
```

The exact choice between one-point and two-point recalibration follows the configured laboratory method and manual procedure. An unsupported automatic sequence must not be invented.

---

# Part XI: Unknown Sample Analysis

## 34. Job X: Content Analysis

### Purpose

Determine the elemental composition of an unknown sample.

### Preconditions

The selected Analytical Group must contain all required measurement and calculation information.

### Inputs

```text
Analytical Group
Unknown physical sample
Sample index/name
Optional product specification
Run settings
Number of burns
```

### Calculation pipeline

```text
Raw intensity I
    ↓
Internal-standard processing, if configured
    ↓
Drift correction
Idc = k × (alpha × I + beta)
    ↓
Working-curve conversion
C0 = a(Idc)³ + b(Idc)² + c(Idc) + d
    ↓
Matrix correction, if configured
    ↓
Master-curve correction, if configured
    ↓
100% correction, purity, or special calculations, if configured
    ↓
Final concentration
    ↓
Product-limit and R-control evaluation
```

The exact order of optional stages must match the manual's documented calculation specifications.

### Outputs

Per element:

```text
Individual burn results
Average
Range
Standard deviation
Coefficient of variation
Final concentration
H/L/Tr flags
R flag
Overflow or calculation warnings
```

### Filing

Operation Mode O controls whether results are displayed, printed, transmitted, or filed manually/automatically according to the manual's available settings.

---

## 35. Job Y: Special Three-Time Content Analysis

### Purpose

Handle excessive disagreement between the first two analytical results.

### Flow

```text
Perform burn 1
Perform burn 2
Evaluate R/variance

If acceptable:
    use burns 1 and 2

If unacceptable:
    request burn 3
    compare possible result pairs
    select the pair having minimum variance
    calculate the final result
    raise the documented error/status if still unacceptable
```

All measured burns should remain available for traceability in the new application, although historical-storage policy is an implementation decision.

---

# Part XII: Stored Information and Data Flow

## 36. What Analytical Information Stores

Per Analytical Group, the application must retain the current method information required by later jobs:

```text
Group identity
Analytical Condition
Selected analytical channels
AR order
SEQ assignments
ISE references
ATT settings
H/L/K sample identifiers
H/L/K targets
alpha, beta, k
Working-curve type and a/b/c/d per element
Matrix correction information
Master correction information
Display and output settings
Product limits
R-control values
Optional calculation settings
```

## 37. What Calibration Jobs Store

### Job 8

```text
H/L/K target values
Supporting measurement results as implemented
```

### Job 3

```text
alpha
beta
Current H/L measurement results
```

### Job 2

```text
k
Current K measurement result
```

### Job 7

```text
Corrected standard intensity per:
Analytical Group + standard sample + element
```

### Working-Curve Regression

```text
Candidate fit results
Selected curve type
Selected a/b/c/d per group and element
```

### Matrix Regression

```text
Selected target/interfering-element correction coefficients
```

### Job 4

```text
AC
MC
Supporting type-standard measurement result
```

## 38. What Unknown Analysis Stores

The manual requires filed analytical results and supports later reporting and modification. The exact new storage format is an implementation decision.

A complete modern record should preserve enough information to reproduce and explain the result, including:

```text
Sample identification
Analytical Group identification
Job
Date/time
Per-burn result
Averages and statistics
Final concentrations
Result flags
Method/calculation values used
```

Storing a complete method snapshot with each result is a modern traceability choice, not an explicit old-manual requirement. It is recommended if configuration deletion or replacement will be allowed.

## 39. Storage Format

The manual describes functional records but does not require a modern application to reproduce the old DOS file format.

A practical modern arrangement is:

```text
SQLite database for application data and reporting
JSON for import/export and self-contained snapshots
CSV for tabular export and diagnostic traces
PDF for human-readable final reports
```

This is an implementation decision and not a manual requirement.

---

# Part XIII: Report Flow

## 40. Report Section

The Report section does not operate the instrument. It reads previously filed analytical results.

### Report functions

```text
Daily report by Analytical Group
Daily report by product specification
Daily report by sample index
Long-term X-R repeatability
Analytical frequency
Stability check
Stored-data modification
Histogram
```

### Histogram/statistical outputs

According to the relevant report configuration, outputs can include:

```text
Count
Average
Range
Standard deviation
Cp
Cpk
Distribution/histogram
Over-limit and under-limit status
```

### Stored result modification

The old system supports modification of stored analytical values. A new implementation should preserve the original and record the change, but immutable revision history is a modern safety design rather than an explicitly required old-storage model.

---

# Part XIV: Remaining Maintenance and Administration

## 41. Date and Time

The manual includes date/time setting. A modern desktop application may use the operating-system clock unless a separate instrument clock is required.

## 42. System Backup

The old manual includes system backup. A new implementation must provide a way to back up and restore the application's configuration, calibration, and result data.

The package format is an implementation choice.

## 43. TAN and AN Counters

The manual includes emission-count handling, including TAN clear and waste-discharge-related counter behavior.

Exact rules must follow the maintenance sections and verified existing behavior.

## 44. Temperature, Voltage, and Vacuum

The manual includes display of instrument temperature, voltage, and vacuum information.

The current generic MCU protocol does not explicitly expose these values. Implementation requires a verified hardware mapping or another data provider. The application must not invent commands.

---

# Part XV: Complete Dependency Map

## 45. Values Created and Consumed

```text
Physical Channel Information
    creates ITG → element → wavelength mapping
        ↓
Source Information
    creates available source definitions
        ↓
Analytical Group Name
    creates the method identity
        ↓
Analytical Condition
    creates purge, sequence, and cleaning behavior
        ↓
Analytical Channel / ISE Information
    selects channels and connects them to sequences
        ↓
Attenuator Adjustment
    determines production ATT
        ↓
ATT Settings
    stores production ATT
        ↓
Drift Correction Information
    stores H/L/K identifiers and coefficient fields
        ↓
Job 8
    creates H/L/K targets
        ↓
Job 3 and/or Job 2
    create current alpha/beta/k
        ↓
Working Standard Information
    stores known concentrations
        ↓
Job 7
    creates corrected calibration intensities
        ↓
Working-Curve Regression
    creates candidate curves
        ↓
Working Curve Information
    stores selected a/b/c/d
        ↓
Matrix Regression
    creates optional interference coefficients
        ↓
Matrix Correction Information
    stores selected coefficients
        ↓
Master/Type Standard Configuration
    stores sample, target, D1, and D2
        ↓
Job 4
    creates AC and MC
        ↓
Result and Calculation Settings
    define formatting, product limits, R control, and optional formulas
        ↓
Job X or Job Y
    produces unknown-sample concentrations
        ↓
Report
    retrieves and evaluates filed results
```

---

# Part XVI: Preconditions by Operation

## 46. Manual Scanning

Requires:

```text
Physical ITG/element information
Maintenance Manual Scanning information
Profile sample
Verified hardware-output mapping
```

Does not require a completed working curve.

## 47. Attenuator Adjustment

Requires:

```text
Analytical Group
Analytical Condition
Selected channel and sequence
Suitable physical high-content sample
Verified hardware-output mapping
```

Produces production ATT.

## 48. Job 8

Requires:

```text
Selected Analytical Group
Condition
Channels
Sequences
ATT
Required H/L/K identifier
Physical sample
```

Produces drift targets.

## 49. Job 3

Requires:

```text
H and L sample identifiers
H and L targets
Current physical H and L samples
```

Produces alpha and beta.

## 50. Job 2

Requires:

```text
K sample identifier
K target
Current alpha and beta
Physical K sample
```

Produces k.

## 51. Job 7

Requires:

```text
Analytical Group
Registered working standard
Known concentrations
Current drift correction
Physical standard sample
```

Produces corrected standard intensities.

## 52. Working-Curve Regression

Requires:

```text
Known standard concentrations
Job 7 corrected intensities
Enough suitable calibration points
```

Produces candidate curves and selected a/b/c/d.

## 53. Matrix Correction

Requires:

```text
Active working curve
Standards containing target and interfering-element values
Working-curve calculation results
```

Produces optional matrix coefficients.

## 54. Job 4

Requires:

```text
Active working curve
Current drift correction
Configured type-standard sample
Known target concentration
D1/D2 settings
```

Produces AC and MC.

## 55. Job X

Requires:

```text
Complete usable Analytical Group
Unknown physical sample
Current drift state
Active working curves
Required optional corrections
Run settings
```

Produces final unknown-sample concentrations.

## 56. Job Y

Requires everything needed by Job X plus configured R-control behavior.

---

# Part XVII: Manual Requirements Versus Implementation Choices

## 57. Confirmed Manual-Derived Functional Separation

```text
Analytical Group Name and Analytical Condition are separate information sections.
The Analytical Condition belongs to the selected group's complete Analytical Information.
ATT Settings store ATT values.
Attenuator Adjustment determines ATT values.
Drift Information stores H/L/K targets and coefficients.
Jobs 8, 3, and 2 create/update drift values.
Job 7 collects working-curve intensity data.
Regression calculates working curves and matrix corrections.
Job 4 creates master/type-standard correction.
Jobs X and Y perform content analysis.
Reports consume filed analytical results.
Manual Scanning belongs to Maintenance.
```

## 58. Choices Not to Treat as Manual Requirements

The following are useful modern options but must not be described as required by the old manual:

```text
Globally reusable Analytical Condition records shared by multiple groups
Draft/Active/Archived group status
Mandatory separate recalibration-sample library
Mandatory working-curve version history
Mandatory immutable result records
Specific SQLite/JSON schema
Specific export package format
Automatic method-readiness states
```

These may be implemented later as design choices.

---

# Part XVIII: Unresolved Items Requiring Verification

## 59. Hardware and Scientific Ambiguities

The following must be verified before final implementation:

1. Exact Port A/Port B value mapping for element, ATT, source, argon, preburn, integration, and cleaning.
2. Decimal versus hexadecimal serial command representation.
3. Exact conversion, if any, from 0–4095 ADC counts into the manual's intensity representation.
4. Exact nonzero `ISE Ref` identifier and internal-standard formula.
5. Exact source and timing sequence for each job.
6. Exact D1/D2 master-correction decision rules.
7. Exact 100% correction, purity, and special-calculation formulas and ordering.
8. Exact relationship between counters TAN and AN and successful emissions/maintenance operations.
9. Hardware source for temperature, voltage, and vacuum values.
10. Whether the fixed 70-second behavior in the existing Profile script is a hardware/project requirement or only an implementation assumption.

No unresolved point should be filled with a guessed behavior.

---

# Part XIX: Final End-to-End Story

## 60. Complete Functional Lifecycle

```text
The instrument's physical channels and source choices are first configured.

An Analytical Group is named.

That group's Analytical Condition defines purge, sequence sources,
preburn, integration, and cleaning.

The group selects up to 32 analytical entries from the installed ITG channels,
orders them, assigns sequences, and optionally assigns ISE references.

Attenuator Adjustment is used to find production ATT values,
and those values are stored in the group's ATT Settings.

Maintenance operations are performed when needed:
Manual Scanning aligns the optical signal,
Waste Discharge prepares/stabilizes the electrode condition,
and Lamp Test checks the photometric system.

The operator enters optional H/L/K physical sample identifiers
in Drift Correction Information.

Job 8 measures those samples in the reference state
and stores H/L/K target intensities.

Job 3 and/or Job 2 measure the samples again
and create the current alpha, beta, and k correction values.

Known working-curve standards and their concentrations are registered.

Job 7 measures each standard and stores drift-corrected intensities.

Regression Calculation creates linear, quadratic, and cubic candidates.
The operator selects one curve per Analytical Group and element,
and its a/b/c/d values are stored.

Matrix correction coefficients are calculated where interference requires them.

A type-standard sample and target are configured where master correction is used.
Job 4 measures that sample and creates AC/MC values.

Result display, product limits, R control, and optional calculations are configured.

Job X or Job Y measures an unknown sample.
The application applies the complete configured calculation chain
and produces final elemental concentrations and status flags.

Accepted results are filed.

The Report section later retrieves those results for daily reports,
repeatability, stability, frequency, modification, and histograms.
```

---

# 61. One-Line Responsibility Summary

```text
Analytical Information stores the method.
Maintenance prepares and checks the instrument.
Attenuator Adjustment determines production sensitivity.
Analysis jobs measure samples and create operational/calibration results.
Regression calculates working and matrix coefficients.
Content Analysis uses the completed method on unknown samples.
Report explains stored results over time.
```
