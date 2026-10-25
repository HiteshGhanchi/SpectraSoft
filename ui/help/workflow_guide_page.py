"""Read-only in-app guide for the SpectraSoft operating workflow."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


WORKFLOW_GUIDE_HTML = """
<h1>Working Flow &amp; Input Parameters</h1>
<p class="lead">Use this guide to understand what must be configured before a
measurement, what each operation does, and how the software maps analytical
information to the spectrometer.</p>

<h2>1. Working flow</h2>
<ol>
  <li>Configure the physical instrument channels and their element names and
      wavelengths.</li>
  <li>Configure the available source codes.</li>
  <li>Create or select an Analytical Group.</li>
  <li>Enter the group's Analytical Condition: purge, source, preburn,
      integration, and cleaning parameters.</li>
  <li>Choose the group's analytical channel order and internal-standard
      references.</li>
  <li>Set or determine production ATT values for the selected channels.</li>
  <li>Run the required analysis job and review or file the result.</li>
</ol>

<h2>2. Input parameters by screen</h2>
<table>
  <tr><th>Area</th><th>Inputs</th><th>Purpose</th></tr>
  <tr><td>Master Elements</td><td>ITG number, element name, wavelength</td>
      <td>Describe the physical detector/integrator channels.</td></tr>
  <tr><td>Source Codes</td><td>Hex source identifier, source name</td>
      <td>Define source choices available to Analytical Conditions.</td></tr>
  <tr><td>Analytical Condition</td><td>Purge; SEQ1/2/3 source, preburn,
      integration; clean source and time</td>
      <td>Define how the selected group runs a burn.</td></tr>
  <tr><td>Channel and ISE Order</td><td>AR-No., ITG, ELE, NAME, SEQ, ISE Ref</td>
      <td>Select channels for the group and assign their sequence/order.</td></tr>
  <tr><td>ATT Settings</td><td>ATT value per selected ITG channel</td>
      <td>Store the production attenuator value used for the group.</td></tr>
  <tr><td>Result Settings</td><td>Product, R control, optional result settings</td>
      <td>Control result evaluation and reporting behavior.</td></tr>
</table>

<h2>3. Identifier mapping used by the current code</h2>
<div class="callout teal"><b>Important:</b> the ITG number is used for
physical channel selection in the hardware instruction.</div>
<table>
  <tr><th>Identifier</th><th>Meaning</th><th>Used in spectrometer instruction?</th></tr>
  <tr><td>AR-No.</td><td>Analytical position/order within the selected group.</td>
      <td><b>No.</b> It is client-side ordering information.</td></tr>
  <tr><td>ITG</td><td>Physical integrator/detector channel number.</td>
      <td><b>Yes.</b> The UART controller converts it to the channel-select
      hexadecimal value.</td></tr>
  <tr><td>Element name</td><td>Software-facing element/result label.</td>
      <td><b>No.</b> It keys the returned intensity in the result mapping.</td></tr>
</table>
<p>The current channel-select instruction is derived from ITG as
<code>O,A,&lt;ITG - 1&gt;</code> in hexadecimal. ATT programming also selects the
channel by ITG first. The exact physical meaning of controller Port A/Port B
values still requires verified wiring or hardware testing.</p>
<p><b>AR-No. is not sent to the spectrometer.</b> It remains the client-side
analytical order used by the selected method.</p>

<h2>4. Measurement sequence</h2>
<ol>
  <li>Reset the controller.</li>
  <li>For each enabled sequence, purge with argon.</li>
  <li>Select the configured source code and run the preburn.</li>
  <li>Select each requested ITG channel and read its ADC intensity.</li>
  <li>Run the configured cleaning operation.</li>
  <li>Return the controller to standby and pass results to the client-side
      calculation/reporting pipeline.</li>
</ol>

<h2>5. Analysis jobs and outputs</h2>
<table>
  <tr><th>Job</th><th>Working purpose</th><th>Typical output</th></tr>
  <tr><td>Job 2</td><td>One-point recalibration</td><td>Updated calibration/drift values</td></tr>
  <tr><td>Job 3</td><td>Two-point recalibration</td><td>Alpha/beta correction values</td></tr>
  <tr><td>Job 4</td><td>Master-curve/type-standard recalibration</td><td>Master correction values</td></tr>
  <tr><td>Job 5</td><td>Raw intensity</td><td>INT.1 values</td></tr>
  <tr><td>Job 6</td><td>Drift-corrected intensity</td><td>INT.2 values</td></tr>
  <tr><td>Job 7</td><td>Working-curve intensity</td><td>Calibration measurements</td></tr>
  <tr><td>Job 8</td><td>Drift target intensity</td><td>Drift target values</td></tr>
  <tr><td>Job X/Y</td><td>Content analysis</td><td>Calculated analytical results</td></tr>
</table>

<h2>6. Before starting a run</h2>
<ul>
  <li>Select the correct Analytical Group.</li>
  <li>Confirm the selected ITG channels have the intended element and
      wavelength mapping.</li>
  <li>Confirm SEQ assignments and nonzero integration times.</li>
  <li>Confirm ATT values are configured for the participating ITG channels.</li>
  <li>Place the appropriate sample and verify the instrument connection.</li>
</ul>

<p class="source">This in-app reference is based on <b>USER_FLOW.md</b> and
the current hardware abstraction code. It intentionally does not invent
unverified instrument wiring or scientific formulas.</p>
"""


class WorkflowGuidePage(QWidget):
    """Read-only operator reference displayed as one full application page."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setObjectName("pageSurface")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QLabel("Workflow Guide")
        header.setObjectName("pageHeader")
        header.setMinimumHeight(36)
        header.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        root.addWidget(header)

        card = QFrame()
        card.setObjectName("contentCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QTextBrowser()
        content.setObjectName("workflowGuideContent")
        content.setReadOnly(True)
        content.setOpenExternalLinks(False)
        content.setHtml(self._styled_html())
        self.content = content
        scroll.setWidget(content)
        card_layout.addWidget(scroll)
        root.addWidget(card, stretch=1)

    @staticmethod
    def _styled_html() -> str:
        return f"""
        <style>
            body {{ color: #1f2937; font-family: 'Sans Serif'; font-size: 10pt; line-height: 1.35; }}
            h1 {{ color: #203047; font-size: 18pt; margin: 4px 0 8px; }}
            h2 {{ color: #2d3d55; font-size: 12pt; margin: 18px 0 8px; border-bottom: 2px solid #0f9f9a; padding-bottom: 4px; }}
            p.lead {{ color: #64748b; font-size: 10.5pt; }}
            p.source {{ color: #64748b; font-size: 9pt; margin-top: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 6px 0 12px; }}
            th {{ background: #2d3d55; color: white; text-align: left; padding: 7px; }}
            td {{ border: 1px solid #d7e0ea; padding: 7px; vertical-align: top; }}
            tr:nth-child(even) {{ background: #f3f6fa; }}
            code {{ color: #087f7b; background: #dff7f4; padding: 2px 4px; }}
            div.callout {{ padding: 9px 11px; margin: 8px 0 12px; border-radius: 5px; }}
            div.teal {{ background: #dff7f4; border-left: 4px solid #0f9f9a; }}
            li {{ margin: 4px 0; }}
        </style>
        {WORKFLOW_GUIDE_HTML}
        """
