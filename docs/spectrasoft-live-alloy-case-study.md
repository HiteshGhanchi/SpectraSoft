# SpectraSoft Live Alloy-Analysis Case Study

## Document purpose

This is a living, screen-by-screen explanation of how SpectraSoft is used by a
researcher to determine the composition of an unknown alloy.

The explanation follows one connected fake case rather than unrelated examples.
Each chapter will describe:

1. what the researcher sees;
2. why the screen exists;
3. realistic values entered on that screen;
4. what SpectraSoft stores;
5. what later screens consume;
6. what the application sends to the MCU;
7. what the MCU returns;
8. formulas and transformations;
9. expected outputs; and
10. implementation gaps or values that still require instrument verification.

The Markdown file is the source document. A PDF should be generated only after
the chapters are complete, so the report can be updated safely one page at a
time.

---

## Case-study setup

### Researcher

Hitesh is investigating an unknown steel sample found in a production batch.
The sample is labelled:

```text
HEAT-2026-001
```

The initial hypothesis is that this is a low-alloy steel. Hitesh wants to
measure the main alloying and residual elements and compare the result with a
future product specification.

### Analytical Group

The method is registered as:

```text
Analytical Group: HITESH_LOW_ALLOY
```

The group is the method identity. It will eventually contain the source
timings, selected physical channels, attenuator values, drift information,
working-curve coefficients, optional matrix corrections, result settings, and
the rules used to store the final analysis.

### Planned analytical elements

The connected story will use these plausible element lines from the bundled
reference table:

| Element | ITG | Wavelength | Intended role |
|---|---:|---:|---|
| FE | 1 | 271.4 | Base element / internal-standard candidate |
| C | 2 | 193.0 | Carbon measurement |
| SI | 3 | 212.4 | Silicon measurement |
| MN1 | 4 | 293.3 | Manganese measurement |
| NI1 | 8 | 231.6 | Nickel measurement |
| CR1 | 10 | 267.7 | Chromium measurement |
| MO | 12 | 202.0 | Molybdenum measurement |

The exact concentration values used later will be fictional but internally
consistent. They are teaching data, not certified chemistry.

### Drift samples

Hitesh has three repeatable physical samples available for checking instrument
drift:

```text
DRIFT-HIGH   high-intensity reference sample
DRIFT-LOW    low-intensity reference sample
DRIFT-CHECK  routine check/reference sample
```

These names will be entered later on the Drift Correction page. The samples
are not the same thing as working-curve standards: drift samples need stable,
repeatable intensity, while working standards need known chemical values.

### Working-curve standards

The later calibration story will use:

```text
STD-01, STD-02, STD-03, STD-04, STD-05, STD-06
```

Each standard will have fictional known values for the elements it contains.
Job 7 will create corrected intensity points, and Regression Calculation will
fit concentration-versus-intensity curves from those points.

### Unknown sample

The final unknown sample remains:

```text
HEAT-2026-001
```

The final report will show how raw detector values become element
concentrations through drift correction, working-curve conversion, optional
matrix correction, optional master correction, and result-limit evaluation.

---

# Chapter 1 — Create the Analytical Group and configure Page 1

## 1.1 What Hitesh does on the first screen

When SpectraSoft starts, the left navigation rail shows the existing
Analytical Groups. Hitesh creates a new group because the unknown alloy needs a
separate method identity.

The relevant implementation is:

```text
ui/anainf/group_panel.py
core/persistence/models.py :: AnalyticalGroup
```

The left panel provides:

```text
New
Delete
Copy
```

### New

Hitesh clicks **New**, enters:

```text
HITESH_LOW_ALLOY
```

The UI uppercases the name, checks for a duplicate, creates an
`AnalyticalGroup` row, and commits it to SQLite.

At this moment the group exists, but it is not ready to measure anything. Its
page JSON fields are still empty or contain defaults.

### Delete

Delete asks for confirmation and removes the selected `AnalyticalGroup` row.
It is destructive from the application's point of view. Hitesh does not use
it in this case.

### Copy — current implementation note

The button label says **Copy**, but the current code intends to copy working
curve information from one group to another rather than clone every page of a
group. The implementation references `page_07_working_curve`, while the
current model defines `page_07_master`. This should be treated as an
implementation issue to fix or explicitly define before relying on Copy in a
production workflow.

## 1.2 Opening Page 1

Hitesh double-clicks `HITESH_LOW_ALLOY` in the left panel.

The application opens:

```text
Analytical Condition - HITESH_LOW_ALLOY
```

The implementation is:

```text
ui/anainf/page_01_source.py :: SourceConditionPage
```

This screen is not the concentration calculator. It is the measurement recipe
for the excitation source.

It tells the application:

```text
How long to purge the spark stand
Which source code to use for each sequence
How long to preburn before reading
How long to integrate/read
Which source and time to use for cleaning
```

The screen has four columns:

```text
SEQ1 | SEQ2 | SEQ3 | CLEAN
```

and rows for:

```text
Purge
Source
Preburn
Integ.
Clean
```

Purge is only editable for SEQ1 because the current sequence engine uses one
purge value before every active sequence. The clean time is only editable in
the CLEAN column.

## 1.3 Hitesh's Page 1 entries

For this low-alloy steel method, Hitesh enters the following teaching data:

| Field | Value entered | Reason in the story |
|---|---:|---|
| Purge | `3` | Replace air around the spark stand before each active sequence |
| SEQ1 source | `1: Normal Spark` | General alloy-line measurement |
| SEQ1 preburn | `200` | Stabilize the discharge before reading |
| SEQ1 integ. | `300` | Collect the analytical signal |
| SEQ2 source | `2: High Power Spark` | Use a different source for the carbon/high-energy part of the method |
| SEQ2 preburn | `150` | Stabilize SEQ2 before reading |
| SEQ2 integ. | `250` | Collect the SEQ2 signal |
| SEQ3 source | `0: Fatigue Lamp` | No SEQ3 element is assigned in this method |
| SEQ3 preburn | `0` | SEQ3 is disabled for this method |
| SEQ3 integ. | `0` | A zero integration disables SEQ3 in the current engine |
| CLEAN source | `5: Cleaning Spark` | Cleaning source definition |
| Clean | `100` | Short cleaning operation after the active sequences |

In the first demonstration run, Hitesh assigns the initial channels as
follows:

```text
SEQ1: FE, SI (AR3), SI (AR5), MN1, NI1, CR1, MO
SEQ2: C, SI (AR4)
SEQ3: no elements; the sequence is disabled
```

Page 1 does not know which elements belong to each sequence. That assignment
is made on the later Channel / Internal Standard page through the `SEQ`
column. Page 1 only defines what each sequence does when it is used.

## 1.4 What is stored when Hitesh clicks OK

Clicking **OK** calls `_save()` and stores the values in the active group's
`page_01_source` JSON column.

The stored shape is:

```json
{
  "purge_seq1": "3",
  "source_seq1": "1: Normal Spark",
  "source_seq2": "2: High Power Spark",
  "source_seq3": "0: Fatigue Lamp",
  "source_clean": "5: Cleaning Spark",
  "preburn_seq1": "200",
  "preburn_seq2": "150",
  "preburn_seq3": "0",
  "integ_seq1": "300",
  "integ_seq2": "250",
  "integ_seq3": "0",
  "clean_value": "100"
}
```

The values are currently stored as strings because they come from `QLineEdit`
widgets. The sequence engine converts the timing fields to numbers when a job
actually runs.

## 1.5 What Page 1 does not do

Saving Page 1 does **not**:

```text
Start the MCU
Create a spark
Measure an element
Read an ADC value
Calculate concentration
Create drift coefficients
Create a working curve
```

It only stores the method's source and timing recipe.

The MCU is contacted later when an analysis or calibration job invokes the
hardware workflow.

## 1.6 What happens later when this Page 1 data is used

When the current sequence engine runs, it performs this high-level flow:

```text
Reset
    ↓
For SEQ1, SEQ2, SEQ3:
    if integration == 0: skip the sequence
    otherwise:
        argon purge
        prespark using the selected source code
        integrate the Page 3 channels assigned to that sequence
    ↓
Cleaning
    ↓
Shutdown
```

For Hitesh's current values, SEQ3 is skipped because:

```text
integ_seq3 = 0
```

The semantic controller calls are therefore:

```text
reset()

argon_purge(3.0)

argon_purge(3.0)

clean(clean_ms=100)
shutdown()
```

The relevant implementation is:

```text
core/hardware/sequence_engine.py
```

## 1.7 Exact MCU command example

The semantic calls above are translated by:

```text
core/hardware/protocols/uart_protocol.py
```

The ATmega sketch is:

```text
atmega2560pro_virtual_ports.ino
```

The application and MCU communicate at:

```text
9600 baud
```

### Reset

```text
Application → MCU: O,A,9E
MCU → Application: K

Application → MCU: T,500
MCU → Application: K

Application → MCU: O,A,C3
MCU → Application: K

Application → MCU: T,500
MCU → Application: K
```

### SEQ1 purge

```text
Application → MCU: O,A,CB
MCU → Application: K

Application → MCU: T,3000
MCU → Application: K
```

The value `3` from the Page 1 purge field is interpreted as `3.0` seconds
and converted to `3000` milliseconds.

### SEQ1 source selection

The source dropdown contains:

```text
1: Normal Spark
```

The sequence engine extracts the hexadecimal token `1` and passes integer
source code `0x1` to the controller.

The controller calculates the Port-B value:

```text
(source_code << 3) | SOURCE_PORT_CONTROL_BITS
```

For source `0x1`:

```text
(1 << 3) | 0b010
= 8 | 2
= 10 decimal
= 0x0A
```

The UART exchange is:

```text
Application → MCU: O,A,C9
MCU → Application: K

Application → MCU: O,B,0A
MCU → Application: K

Application → MCU: T,200
MCU → Application: K
```

### SEQ1 integration

For integration time `300`, the current controller sends:

```text
Application → MCU: O,A,8C
MCU → Application: K

Application → MCU: T,300
MCU → Application: K

Application → MCU: O,B,16
MCU → Application: K
```

The individual ITG reads happen after this setup. Page 1 itself does not
choose the ITG value; Page 3 supplies the element rows.

### SEQ2 source selection

For:

```text
2: High Power Spark
```

the source code is `0x2`:

```text
(2 << 3) | 0b010
= 16 | 2
= 18 decimal
= 0x12
```

The source portion becomes:

```text
Application → MCU: O,A,C9
MCU → Application: K

Application → MCU: O,B,12
MCU → Application: K

Application → MCU: T,150
MCU → Application: K
```

### Cleaning

At the end of the active sequences:

```text
Application → MCU: O,A,9C
MCU → Application: K

Application → MCU: T,100
MCU → Application: K

Application → MCU: O,A,C2
MCU → Application: K

Application → MCU: O,A,00
MCU → Application: K
```

## 1.8 Important timing-unit warning

The screen labels Purge, Preburn, Integ., and Clean as seconds, but the current
implementation does not treat all four fields the same way:

| Field | Current runtime interpretation | Example command |
|---|---|---|
| Purge | seconds, then multiplied by 1000 | `3` → `T,3000` |
| Preburn | passed as milliseconds | `200` → `T,200` |
| Integration | passed as milliseconds | `300` → `T,300` |
| Clean | passed as milliseconds | `100` → `T,100` |

Therefore, the literal current behavior for a displayed value of `200` is a
200 ms MCU delay, even though the UI displays `Sec.` beside the field.

This must be called out in the final report and should be resolved or verified
before production instrument operation. The report will distinguish:

```text
UI label
Stored value
Runtime interpretation
Physical meaning intended by the instrument method
```

## 1.9 Page 1 technical reference

| Question | Current answer |
|---|---|
| What does this page configure? | Purge, source selection, preburn, integration, and cleaning recipe |
| Is it group-specific? | Yes; stored in `AnalyticalGroup.page_01_source` |
| Does it select elements? | No; Page 3 assigns elements to sequences |
| Does Save contact the MCU? | No |
| When is the MCU contacted? | When a later analysis/calibration job runs the sequence |
| What source identifier is sent? | Hexadecimal code extracted from the dropdown text |
| What does the MCU know? | GPIO output values, delay commands, and ADC reads; not scientific meaning |
| What does the sequence engine skip? | Any sequence whose integration value is `0` |
| What is the next page? | Order of Analytical Channel & Internal Standard |

## 1.10 Chapter 1 handoff to the next screen

At the end of Page 1, Hitesh has defined:

```text
SEQ1 = normal spark, 200 preburn, 300 integration
SEQ2 = high-power spark, 150 preburn, 250 integration
SEQ3 = currently disabled because integration is 0
CLEAN = cleaning spark for 100 ms in the current runtime
```

But the method still does not know which physical detector channels should be
read. That is the job of the next screen:

```text
Order of Analytical Channel & Internal Standard
```

There Hitesh will map AR positions to ITG lines, assign each element to SEQ1,
SEQ2, or SEQ3, choose the internal-standard reference, and create the channel
list that the integration stage will actually read.

---

# Chapter 2 — Order of Analytical Channel & Internal Standard

## 2.1 Why Hitesh needs this page

Page 1 defined the burn recipes, but it did not define which detector channels
must be read. Hitesh now opens:

```text
ORDER OF ANALYTICAL CHANNEL & INTERNAL STANDARD
```

The implementation is:

```text
ui/anainf/page_03_channel.py :: ChannelPage
```

This page turns the physical Master Element table into the analytical method
for `HITESH_LOW_ALLOY`.

For every analytical row it answers:

```text
What analytical result position is this?       AR-No.
Which physical integrator line is read?        ITG
Which element does that line represent?       ELE
What short name is used in results/reports?    NAME
Which source sequence measures it?             SEQ
Which internal-standard line normalizes it?    ISE Ref
```

The page provides 32 possible AR rows. Hitesh fills only the rows with an ITG
selection; the remaining rows stay unused.

## 2.2 What Hitesh sees on the screen

| Column | Example | Meaning |
|---|---|---|
| AR-No. | `1`, `2`, `3` | Software result position and order |
| ITG | `1: FE` | Physical integrator line selected from Master Elements |
| ELE | `FE` | Read-only element name resolved from ITG |
| NAME | `FE` or `MN` | Short display/report name, maximum 5 characters |
| SEQ | `1` or `2` | Page 1 source recipe used for this channel |
| ISE Ref | `0 (none)` or `1: FE` | Internal-standard reference line |

The ITG dropdown is built from the nonblank `master_elements` rows. It is not
hardcoded in Page 3. Selecting `ITG 3` causes the page to look up ITG 3 and
fill:

```text
ELE = SI
```

The ITG number is the hardware identity. The element name makes that identity
understandable to Hitesh.

## 2.3 Hitesh's connected Page 3 entries

Because SEQ3 is disabled in this case, Hitesh does not put any element in
SEQ3. The active table is:

| AR-No. | ITG | ELE | NAME | SEQ | ISE Ref | Why |
|---:|---:|---|---|---:|---:|---|
| 1 | 1 | FE | FE | 1 | 0 | Base/reference line |
| 2 | 2 | C | C | 2 | 1 | Carbon measured by SEQ2, normalized to FE |
| 3 | 3 | SI | SI | 1 | 1 | First SI channel-skip row, normal spark |
| 4 | 3 | SI | SI | 2 | 1 | Same ITG measured again by high-power SEQ2 |
| 5 | 3 | SI | SI | 1 | 1 | Same ITG measured again by normal SEQ1 |
| 6 | 4 | MN1 | MN | 1 | 1 | Manganese normalized to FE |
| 7 | 8 | NI1 | NI | 1 | 1 | Nickel normalized to FE |
| 8 | 10 | CR1 | CR | 1 | 1 | Chromium normalized to FE |
| 9 | 12 | MO | MO | 1 | 1 | Molybdenum normalized to FE |

There are no P or S rows in this version of the example. That is intentional:
the method has no active SEQ3 integration, so no element is assigned to a
disabled sequence.

## 2.4 What each column does in the story

### AR-No. — analytical order

AR is the method's result position:

```text
AR 1 = FE
AR 2 = C
AR 3 = SI (SEQ1)
AR 4 = SI (SEQ2)
AR 5 = SI (SEQ1)
AR 6 = MN
AR 7 = NI
AR 8 = CR
AR 9 = MO
```

The application uses AR as the stable software result identity. The internal
result keys are:

```text
AR:1, AR:2, AR:3, AR:4, AR:5, AR:6, AR:7, AR:8, AR:9
```

This prevents collisions between result rows even when display names or
element names are not unique. The helper is:

```text
core/analysis/channel_identity.py :: channel_result_key
```

### ITG — physical channel selection

ITG selects the physical line that the readout must address. For example:

```text
AR 4 → ITG 3 → SI
```

Later, when AR 4 is read, the controller converts ITG 3 to the Port-A selector:

```text
ITG 3 - 1 = 2 decimal = 0x02
```

The MCU receives `O,A,02`. It does not receive `SI` or `AR:4`. AR remains a
software identity; ITG is the physical selector. AR 3 and AR 5 generate the
same selector because they also use ITG 3.

### ELE — resolved element identity

ELE is filled from Master Elements and is read-only in the UI:

```text
Master Elements: ITG 10 → CR1 → 267.7 nm
Page 3:          ELE = CR1
```

The wavelength remains in the Master Element table and is used by later
screens such as ATT Settings.

### NAME — short reporting identity

Hitesh uses short report labels:

```text
MN1 → MN
NI1 → NI
CR1 → CR
```

NAME is a display/report label. It does not change the physical ITG selection.

### SEQ — source/timing recipe selection

SEQ connects each channel to the Page 1 recipe:

```text
SEQ1 → Normal Spark, 200 ms preburn, 300 ms integration
SEQ2 → High Power Spark, 150 ms preburn, 250 ms integration
SEQ3 → disabled because integration is 0
```

The resulting groups are:

```text
SEQ1 rows: FE, SI (AR3), SI (AR5), MN, NI, CR, MO
SEQ2 rows: C, SI (AR4)
SEQ3 rows: none
```

The order within a sequence comes from the Page 3 row order.

### ISE Ref — internal-standard reference

Hitesh selects:

```text
ISE Ref = 0 for FE
ISE Ref = 1 for C, all three SI rows, MN, NI, CR, and MO
```

In the current implementation, the nonzero value is treated as an ITG number.
Therefore all non-reference rows point to:

```text
ITG 1 → FE
```

The manual describes the same identifier rule: ISE values 1 through 45
identify the integrator number of the internal-standard element. It also says
ISE 0 represents constant-time integration, while a nonzero ISE selects an
internal-standard element.

## 2.5 What is saved when Hitesh clicks OK

The page stores active rows in:

```text
AnalyticalGroup.page_03_channel
```

The connected stored JSON is:

```json
[
  {"ar_no": 1, "itg": "1",  "ele": "FE",  "name": "FE", "seq": "1", "ise_ref": 0},
  {"ar_no": 2, "itg": "2",  "ele": "C",   "name": "C",  "seq": "2", "ise_ref": 1},
  {"ar_no": 3, "itg": "3",  "ele": "SI",  "name": "SI", "seq": "1", "ise_ref": 1},
  {"ar_no": 4, "itg": "3",  "ele": "SI",  "name": "SI", "seq": "2", "ise_ref": 1},
  {"ar_no": 5, "itg": "3",  "ele": "SI",  "name": "SI", "seq": "1", "ise_ref": 1},
  {"ar_no": 6, "itg": "4",  "ele": "MN1", "name": "MN", "seq": "1", "ise_ref": 1},
  {"ar_no": 7, "itg": "8",  "ele": "NI1", "name": "NI", "seq": "1", "ise_ref": 1},
  {"ar_no": 8, "itg": "10", "ele": "CR1", "name": "CR", "seq": "1", "ise_ref": 1},
  {"ar_no": 9, "itg": "12", "ele": "MO",  "name": "MO", "seq": "1", "ise_ref": 1}
]
```

The list order is meaningful. It becomes the analytical order used by later
jobs and reports.

## 2.6 Validation Hitesh encounters

Before moving to ATT Settings, the page validates the active rows.

### Empty channel list

If Hitesh selects no ITG rows, Next is blocked with:

```text
Select at least one analytical channel before continuing.
```

### Missing sequence

If Hitesh selects ITG 3 but leaves SEQ blank, Next is blocked because the
application would not know which Page 1 recipe to run.

### Repeated ITG for channel skip

Three Page 3 rows can use the same ITG. In this connected example:

```text
AR 3 → ITG 3 → SEQ1
AR 4 → ITG 3 → SEQ2
AR 5 → ITG 3 → SEQ1
```

All three analytical rows read the same physical ITG line, but AR 3, AR 4, and
AR 5 keep the three analytical results distinct. One repeat uses a different
source sequence and the final repeat uses the same sequence as the first row.
The manual explicitly says to enter the same ITG continuously and distinguish
the rows with AR-No. when one analytical wavelength is used for a channel skip.

The ATT screen is different: ATT is a setting for the physical ITG line, so it
may display one ATT row for a repeated ITG even though Page 3 retains every AR
row.

## 2.7 What happens when the measurement eventually runs

Page 3 itself does not contact the MCU. It prepares the channel list used by
the later sequence run.

For Hitesh's method, the sequence engine combines Page 1 and Page 3 like this:

```text
Page 1 says what SEQ1 and SEQ2 do.
Page 3 says which elements belong to SEQ1 and SEQ2.
The controller reads the ITG line for each row.
```

The resulting flow is:

```text
Reset
    ↓
SEQ1 purge + source 0x1 + preburn 200 ms
    ↓
Read FE, SI (AR3), SI (AR5), MN1, NI1, CR1, MO
    ↓
SEQ2 purge + source 0x2 + preburn 150 ms
    ↓
Read C, then SI (AR4)
    ↓
SEQ3 skipped because integration is 0
    ↓
Clean
    ↓
Shutdown
```

The MCU selector commands are generated from ITG, not from the element label:

| AR | Element | ITG | Port-A selector during read |
|---:|---|---:|---|
| 1 | FE | 1 | `O,A,00` |
| 3 | SI | 3 | `O,A,02` |
| 2 | C | 2 | `O,A,01` |
| 4 | SI | 3 | `O,A,02` |
| 5 | SI | 3 | `O,A,02` |
| 6 | MN1 | 4 | `O,A,03` |
| 7 | NI1 | 8 | `O,A,07` |
| 8 | CR1 | 10 | `O,A,09` |
| 9 | MO | 12 | `O,A,0B` |

The selector formula is:

```text
element_selector = ITG - 1
```

The selector is formatted as two-digit hexadecimal before being placed in the
`O,A,...` command.

## 2.8A The actual MCU limits

The ATmega sketch does not know the word `ITG`. It receives a raw hexadecimal
output value and writes its bits directly to the configured pins:

```text
O,A,<value> → Port A pins 22–29
O,B,<value> → Port B pins 30–36
```

From `atmega2560pro_virtual_ports.ino`:

| Path | Lowest accepted value | Highest accepted value | Effective range |
|---|---:|---:|---|
| Port A parser | `0x00` | `0xFF` | all 8 output bits |
| Port B parser | `0x00` | `0xFF` | masked to `0x00`–`0x7F` because only 7 bits are used |
| Physical ITG selector generated by Python | `0x00` | `0x2C` | ITG 1 through ITG 45 |

The Python mapping is:

```text
ITG 1  → selector 0  → O,A,00
ITG 45 → selector 44 → O,A,2C
```

Therefore the MCU itself does not reject a repeated selector. Sending
`O,A,02` twice simply selects the same physical Port-A bit pattern twice. The
duplicate restriction was a Page 3 validation rule in the Python UI, not an
MCU limitation, and it has now been removed. ITG values outside the physical
Master Element range 1–45 are rejected by Page 3.

## 2.9 Fake MCU return values for this story

For the teaching run, assume the MCU returns:

| AR | Element | Raw response |
|---:|---|---:|
| 1 | FE | `D,2600` |
| 2 | C | `D,1300` |
| 3 | SI | `D,800` |
| 4 | SI | `D,780` |
| 5 | SI | `D,820` |
| 6 | MN1 | `D,500` |
| 7 | NI1 | `D,420` |
| 8 | CR1 | `D,650` |
| 9 | MO | `D,300` |

The software keeps these under AR-based keys:

```python
{
    "AR:1": 2600,
    "AR:2": 1300,
    "AR:3": 800,
    "AR:4": 780,
    "AR:5": 820,
    "AR:6": 500,
    "AR:7": 420,
    "AR:8": 650,
    "AR:9": 300
}
```

## 2.10 Internal-standard calculation for the fake run

The current Job 5 processing is in:

```text
core/analysis/analysis_worker.py :: _apply_ise_ratio
```

For `ISE Ref = 0`, the implementation returns the exact MCU ADC value:

```text
intensity = ADC
```

For a nonzero ISE reference, it uses:

```text
relative intensity = element ADC / reference ADC × 100
```

Hitesh selected ITG 1 / FE as the reference:

```text
FE ADC = 2600
```

The fake results become:

| Element | Formula | Processed intensity |
|---|---|---:|
| FE | `2600 / 4095` | `0.6349206` |
| C | `1300 / 2600 × 100` | `50.0000` |
| SI (AR3, ITG3, SEQ1) | `800 / 2600 × 100` | `30.7692` |
| SI (AR4, ITG3, SEQ2) | `780 / 2600 × 100` | `30.0000` |
| SI (AR5, ITG3, SEQ1) | `820 / 2600 × 100` | `31.5385` |
| MN | `500 / 2600 × 100` | `19.2308` |
| NI | `420 / 2600 × 100` | `16.1538` |
| CR | `650 / 2600 × 100` | `25.0000` |
| MO | `300 / 2600 × 100` | `11.5385` |

These are still intensities, not concentrations. Hitesh needs working-curve
coefficients before the software can report a value such as carbon `0.21%`.

## 2.11 What Page 3 does not do

Page 3 does not:

```text
Calculate carbon, silicon, or manganese concentration
Calculate drift coefficients
Create a working curve
Program ATT values
Start the MCU when the row is saved
```

It creates the channel map required by those later operations.

The next page consumes this map to show ATT rows only for the selected ITGs.

## 2.12 Page 3 technical reference

| Question | Current answer |
|---|---|
| Possible analytical rows | 32 |
| Physical Master Element lines | 45 |
| Physical channel selector | ITG |
| Software result identity | AR-No. |
| ELE source | Master Elements lookup |
| NAME purpose | Short display/report label, maximum 5 characters |
| Page 1 connection | SEQ 1, 2, or 3 |
| ISE Ref 0 | No internal-standard ratio in the current processing path |
| ISE Ref 1 here | Use ITG 1 / FE as the reference line |
| Save contacts MCU? | No |
| MCU receives later | ITG-derived hexadecimal Port-A selectors |
| Does Page 3 produce concentration? | No; it produces the analytical channel map |
| Next screen | ATT Settings |

## 2.13 Chapter 2 handoff to ATT Settings

At the end of Page 3, Hitesh has connected the method to physical channels:

```text
FE, C, SI (three AR rows sharing ITG 3), MN, NI, CR, MO
```

He has defined which sequence measures each element, which row is the
internal-standard reference, which AR position identifies each future result,
and which ITG selector the MCU must receive.

The next screen is ATT Settings. It will show the unique physical ITGs selected
by these nine AR rows: ITG 1, 2, 3, 4, 8, 10, and 12.
Hitesh will enter production attenuator values so the detector signals stay in
a useful range without overflowing.

---

## Sources used for this chapter

```text
ui/anainf/group_panel.py
ui/anainf/page_01_source.py
ui/anainf/page_03_channel.py
core/analysis/channel_identity.py
core/analysis/analysis_worker.py
core/persistence/models.py
core/persistence/database.py
core/hardware/sequence_engine.py
core/hardware/protocols/uart_protocol.py
atmega2560pro_virtual_ports.ino
import_data/source_codes.json
import_data/master_elements.json
USER_FLOW.md
Manual.md
```

## Chapter status

```text
Chapter 1 — complete as a code-traced teaching draft
Chapter 2 — complete as a code-traced teaching draft
Chapter 3 — next: ATT Settings
```
