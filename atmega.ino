/*
 * Spectroscopy Controller
 * =======================
 * Target : ATmega 2560 Pro
 * Baud   : 115200
 *
 * Command protocol (received from Python):
 *   O,<port>,<value>\n   — set output port  (port = A or B)
 *   I\n                  — read 12-bit ADC value from INPUT_PINS
 *   T,<ms>\n             — non-blocking delay of <ms> milliseconds
 *
 * Response protocol (sent back to Python):
 *   K\n                  — ACK: command was accepted / GPIO was set
 *                          Sent immediately after O and T commands.
 *   D,<value>\n          — ADC result: response to I command (also acts as ACK)
 *   # <text>\n           — debug / info message (Python ignores these)
 *
 * IMPORTANT — flow control:
 *   Python waits for K (or D,…) before sending the next command.
 *   The uC must therefore NEVER stop draining the serial RX buffer,
 *   including while a T delay is in progress.  The loop() function
 *   reads serial bytes unconditionally at the top, then decides
 *   whether to execute the buffered command based on the delay state.
 */

// ============================================================================
// PIN DEFINITIONS
// ============================================================================

// Port A — 8 digital output bits (D0..D7 of the logical "PortA")
const uint8_t PORTA_PINS[8] = {22, 23, 24, 25, 26, 27, 28, 29};

// Port B — 7 digital output bits (only 7 LSBs used, MSB ignored)
const uint8_t PORTB_PINS[7] = {30, 31, 32, 33, 34, 35, 36};

// Pulse pin — toggled briefly every time PortA value changes
const uint8_t PULSE_PIN = 37;

// ADC input pins — 12 bits read as individual digital lines
const uint8_t INPUT_PINS[12] = {54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65};

// Built-in LED — heartbeat toggle on every processed command
const uint8_t DEBUG_LED = 13;

// ============================================================================
// STATE VARIABLES
// ============================================================================

String       inputString    = "";      // Accumulates incoming serial chars
bool         commandReady   = false;   // True when a complete line is buffered
unsigned long delayEndTime  = 0;       // millis() target for non-blocking delay
bool         inDelay        = false;   // True while a T command is running
uint8_t      lastPortAValue = 0;       // Used to detect PortA changes for pulse

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(115200);
  inputString.reserve(128);   // Generous buffer — longest command is ~12 chars

  pinMode(DEBUG_LED, OUTPUT);
  digitalWrite(DEBUG_LED, LOW);

  pinMode(PULSE_PIN, OUTPUT);
  digitalWrite(PULSE_PIN, LOW);

  for (int i = 0; i < 8; i++) {
    pinMode(PORTA_PINS[i], OUTPUT);
    digitalWrite(PORTA_PINS[i], LOW);
  }
  for (int i = 0; i < 7; i++) {
    pinMode(PORTB_PINS[i], OUTPUT);
    digitalWrite(PORTB_PINS[i], LOW);
  }
  for (int i = 0; i < 12; i++) {
    pinMode(INPUT_PINS[i], INPUT);
  }

  Serial.println("# Spectroscopy Controller Ready.");
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {

  // --------------------------------------------------------------------------
  // 1. ALWAYS drain the hardware serial RX buffer.
  //    This runs unconditionally — even while a T delay is active —
  //    so incoming bytes never overflow the 64-byte hardware FIFO.
  //    Characters are appended to inputString until '\n' is received.
  // --------------------------------------------------------------------------
  while (Serial.available()) {
    char c = (char)Serial.read();

    if (c == '\n' || c == '\r') {
      if (inputString.length() > 0) {
        commandReady = true;
      }
    } else {
      // Guard against overrun (shouldn't happen with reserve(128),
      // but be defensive).
      if (inputString.length() < 127) {
        inputString += c;
      }
    }
  }

  // --------------------------------------------------------------------------
  // 2. Check whether an active delay has expired.
  // --------------------------------------------------------------------------
  if (inDelay) {
    if (millis() >= delayEndTime) {
      inDelay = false;
      // Delay just finished — fall through and process any buffered command.
    } else {
      // Still waiting.  Do NOT execute commands yet, but continue the loop
      // so serial bytes keep being read (handled above).
      return;
    }
  }

  // --------------------------------------------------------------------------
  // 3. Process one buffered command per loop iteration.
  //    (commandReady is only acted on when NOT in a delay.)
  // --------------------------------------------------------------------------
  if (commandReady) {
    digitalWrite(DEBUG_LED, !digitalRead(DEBUG_LED));   // Heartbeat
    processCommand(inputString);
    inputString    = "";
    commandReady   = false;
  }
}

// ============================================================================
// COMMAND PROCESSOR
// ============================================================================

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  char type = toupper(cmd.charAt(0));

  // --------------------------------------------------------------------------
  // O,<port>,<value>  —  Set output port and ACK
  // --------------------------------------------------------------------------
  if (type == 'O') {
    int firstComma  = cmd.indexOf(',');
    int secondComma = cmd.indexOf(',', firstComma + 1);

    if (firstComma == -1 || secondComma == -1) {
      Serial.println("# ERROR: Malformed O command");
      return;
    }

    char    port = toupper(cmd.charAt(firstComma + 1));
    uint8_t val  = (uint8_t)cmd.substring(secondComma + 1).toInt();

    if (port == 'A') {
      writePortA(val);
    } else if (port == 'B') {
      writePortB(val);
    } else {
      Serial.println("# ERROR: Unknown port");
      return;
    }

    Serial.println("K");   // ACK — GPIO is now set
  }

  // --------------------------------------------------------------------------
  // I  —  Read 12-bit value from INPUT_PINS and return as D,<value>
  // --------------------------------------------------------------------------
  else if (type == 'I') {
    uint16_t result = 0;
    for (int i = 0; i < 12; i++) {
      if (digitalRead(INPUT_PINS[i])) {
        result |= (1 << i);
      }
    }
    Serial.print("D,");
    Serial.println(result);   // D,<value> is the implicit ACK for I commands
  }

  // --------------------------------------------------------------------------
  // T,<ms>  —  Start non-blocking delay and ACK immediately
  //
  // The ACK is sent BEFORE the delay starts so Python can begin its own
  // matching sleep at the same moment, keeping both clocks in sync.
  // --------------------------------------------------------------------------
  else if (type == 'T') {
    int comma = cmd.indexOf(',');

    if (comma == -1) {
      Serial.println("# ERROR: Malformed T command");
      return;
    }

    unsigned long ms = (unsigned long)cmd.substring(comma + 1).toInt();

    delayEndTime = millis() + ms;
    inDelay      = true;
    Serial.println("K");        // ACK first — Python starts its sleep now
    // loop() will return early on the next iterations until millis() >= delayEndTime
  }

  // --------------------------------------------------------------------------
  // Unknown command
  // --------------------------------------------------------------------------
  else {
    Serial.print("# ERROR: Unknown command: ");
    Serial.println(cmd);
  }
}

// ============================================================================
// GPIO HELPERS
// ============================================================================

/*
 * writePortA — write all 8 bits to PORTA_PINS.
 * Generates a short pulse on PULSE_PIN whenever the value changes.
 */
void writePortA(uint8_t val) {
  for (int i = 0; i < 8; i++) {
    digitalWrite(PORTA_PINS[i], (val >> i) & 0x01);
  }

  // Pulse only on value change to avoid spurious triggers
  if (val != lastPortAValue) {
    digitalWrite(PULSE_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(PULSE_PIN, LOW);
    lastPortAValue = val;
  }
}

/*
 * writePortB — write 7 LSBs to PORTB_PINS (MSB is ignored by hardware).
 */
void writePortB(uint8_t val) {
  val = val & 0x7F;   // Mask to 7 bits
  for (int i = 0; i < 7; i++) {
    digitalWrite(PORTB_PINS[i], (val >> i) & 0x01);
  }
}
