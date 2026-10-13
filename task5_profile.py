"""
Task 5 - Profile
=================
Profiles a single selected element with continuous ADC readings over 70 seconds.

Sequence:
  Step 1 — INITIALIZATION
    - Select element (input)
    - Set ATT value (input, 0-63)
    - Send O,A,9D  (reset)
    - Send O,A,C3  (HV on after reset)
    - Wait INIT_DELAY

  Step 2 — ARGON FLUSH + PRESPARK (70 seconds total)
    - Send O,A,CB  (Argon valve open)
    - Wait ARGON_DELAY
    - Send O,A,C9  (prespark enable)
    - Send O,A,85  (Argon flush command)
    
  Step 3 — CONTINUOUS READING (next 70 seconds)
    For each 100 ms interval (up to 70 seconds):
      - Send O,A,7C                  (ADC trigger 1)
      - Wait 10 ms
      - Send O,A,3C                  (ADC trigger 2)
      - Wait 1s
      - Read D,<value>               (12-bit result, timeout 5 s)
      - Store result with timestamp
    - Allow ATT value to be changed during this loop

  Step 4 — SHUTDOWN (after 70 seconds)
    - Send O,A,9D  (reset)
    - Send O,A,C3  (HV on)

Results stored in profile_data.csv with columns: [timestamp, element, att_value, adc_value]
All commands/responses logged to profile.log

The task supports external control:
  - shared_state["stop_event"]:     Set to stop the task early
  - shared_state["att_queue"]:      Queue to receive new ATT values during execution
  - shared_state["data_list"]:      List to append data readings (GUI can read this live)
"""

import time
import csv
import os
import queue
import threading
from datetime import datetime

# ============================================================================
# CONSTANTS
# ============================================================================
LOG_FILE            = "profile.log"
CSV_FILE            = "profile_data.csv"

# Step 1 — Initialization
INIT_DELAY          = 0.5       # seconds after HV on

# Step 2 — Argon flush
ARGON_DELAY         = 0.5       # seconds (CB command hold time)

# Step 3 — Continuous reading
PROFILE_DURATION    = 70.0      # seconds total for ADC reads
READ_INTERVAL       = 0.100     # 100 ms between read cycles

# ADC command timing
ADC_INTER_DELAY     = 0.010     # 10 ms between 7C and 3C
ADC_SETTLE_DELAY    = 1     # 100 ms after 3C
READ_TIMEOUT        = 5.0       # Max seconds to wait for D,<value>

ACK_TIMEOUT         = 1.0       # Max seconds to wait for K ACK
ATT_OFFSET          = 0x40      # att_value 0 -> 0x40, att_value 63 -> 0x7F

TOTAL_ELEMENTS      = 45        # ele1 ... ele45 → indices 0x00 ... 0x2C


# ============================================================================
# LOGGING
# ============================================================================

def _log(log_fh, direction, message):
    """Write a timestamped entry to the log file and print to console."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    arrow = ">>" if direction == "TX" else ("<<" if direction == "RX" else "--")
    line = f"[{ts}] {arrow} {message}"
    print(f"  {line}")
    log_fh.write(line + "\n")
    log_fh.flush()


# ============================================================================
# LOW-LEVEL HELPERS
# ============================================================================

def _send_command(conn, cmd, log_fh):
    """Transmit a command string followed by CR+LF and flush immediately."""
    _log(log_fh, "TX", cmd)
    conn.write((cmd + "\r\n").encode("utf-8"))
    conn.flush()


def _wait_for_ack(conn, log_fh, timeout=ACK_TIMEOUT):
    """
    Wait for 'K' ACK from uC.
    Lines starting with '#' are treated as debug output.

    Returns:
        bool: True if 'K' received within timeout.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if conn.in_waiting > 0:
            line = conn.readline().decode("utf-8", errors="replace").strip()
            if not line:
                continue
            _log(log_fh, "RX", line)
            if line.startswith("#"):
                continue
            if line == "K":
                return True
            return False
        time.sleep(0.001)
    _log(log_fh, "RX", "TIMEOUT -- no ACK received")
    return False


def _wait_for_data(conn, log_fh, timeout=READ_TIMEOUT):
    """
    Wait for a 'D,<value>' response from uC.
    Ignores ACK ('K') and debug lines (starting with '#'), which may precede or interleave the data.

    Returns:
        int or None: 12-bit ADC value if received, None on timeout/error.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if conn.in_waiting > 0:
            line = conn.readline().decode("utf-8", errors="replace").strip()
            if not line:
                continue
            _log(log_fh, "RX", line)
            if line.startswith("#"):
                continue
            if line == "K":
                # ACK may be sent after I command; skip and continue waiting for data
                continue
            if line.startswith("D,"):
                try:
                    value = int(line.split(",")[1].strip())
                    return value
                except (IndexError, ValueError) as e:
                    _log(log_fh, "RX", f"Parse error: {e}")
                    return None
            _log(log_fh, "RX", f"Unexpected response (expected D,<value>): {line}")
            return None
        time.sleep(0.001)
    _log(log_fh, "RX", "TIMEOUT -- no D,<value> received within 5 s")
    return None


# ============================================================================
# CSV INITIALIZATION
# ============================================================================

def _init_csv(csv_file=CSV_FILE):
    """Initialize CSV file with headers if it doesn't exist."""
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "element", "att_value", "adc_value"])


# ============================================================================
# CORE TASK
# ============================================================================

def run_profile(conn, element_idx, att_value, shared_state=None):
    """
    Execute profile task on selected element for 70 seconds with continuous ADC reads.

    Args:
        conn:         Open serial.Serial connection
        element_idx:  Element index 0-44 (ele1=0, ele45=44)
        att_value:    Attenuator value 0-63
        shared_state: Optional dict with:
            - "stop_event": threading.Event to stop early
            - "att_queue": queue.Queue to receive new ATT values
            - "data_list": list to append readings (for GUI)

    Returns:
        int: Number of readings collected
    """
    if shared_state is None:
        shared_state = {
            "stop_event": threading.Event(),
            "att_queue": queue.Queue(),
            "data_list": []
        }

    stop_event = shared_state.get("stop_event", threading.Event())
    att_queue = shared_state.get("att_queue", queue.Queue())
    data_list = shared_state.get("data_list", [])

    # Validate inputs
    if not (0 <= element_idx <= TOTAL_ELEMENTS - 1):
        print(f"  ✗ Invalid element index {element_idx}. Must be 0-{TOTAL_ELEMENTS - 1}.")
        return 0
    if not (0 <= att_value <= 63):
        print(f"  ✗ Invalid att_value {att_value}. Must be 0-63.")
        return 0

    element_name = f"ele{element_idx + 1}"
    element_hex = f"{element_idx:02X}"
    att_cmd_val = att_value + ATT_OFFSET
    att_hex = f"{att_cmd_val:02X}"
    current_att = att_value

    _init_csv()

    print("\n" + "=" * 60)
    print(f"  PROFILE TASK - {element_name} (index {element_idx})")
    print(f"  Initial ATT value: {att_value}")
    print("=" * 60)

    with open(LOG_FILE, "a") as log_fh:
        log_fh.write(f"\n\n{'='*60}\n")
        log_fh.write(f"PROFILE TASK - {element_name} (index {element_idx})\n")
        log_fh.write(f"Initial ATT value: {att_value}\n")
        log_fh.write(f"{'='*60}\n\n")
        log_fh.flush()

        try:
            # ===== STEP 1: INITIALIZATION =====
            print(f"\n  [Step 1] Initialization...")
            log_fh.write("[Step 1] Initialization\n")
            log_fh.flush()

            # Reset
            _send_command(conn, "O,A,9D", log_fh)
            _wait_for_ack(conn, log_fh)
            time.sleep(0.050)

            # HV on
            _send_command(conn, "O,A,C3", log_fh)
            _wait_for_ack(conn, log_fh)
            time.sleep(INIT_DELAY)

            # Select element
            _send_command(conn, f"O,A,{element_hex}", log_fh)
            _wait_for_ack(conn, log_fh)
            time.sleep(0.100)

            # Set ATT
            _send_command(conn, f"O,A,{att_hex}", log_fh)
            _wait_for_ack(conn, log_fh)
            time.sleep(0.100)

            print(f"  ✓ Initialization complete")

            # ===== STEP 2: ARGON FLUSH + PRESPARK =====
            print(f"\n  [Step 2] Argon flush + prespark...")
            log_fh.write("[Step 2] Argon flush + prespark\n")
            log_fh.flush()

            _send_command(conn, "O,A,CB", log_fh)
            _wait_for_ack(conn, log_fh)
            time.sleep(ARGON_DELAY)

            _send_command(conn, "O,A,C9", log_fh)
            _wait_for_ack(conn, log_fh)

            _send_command(conn, "O,A,85", log_fh)
            _wait_for_ack(conn, log_fh)

            print(f"  ✓ Argon flush + prespark complete")

            # ===== STEP 3: CONTINUOUS READING (70 seconds) =====
            print(f"\n  [Step 3] Starting 70-second profiling...")
            log_fh.write("[Step 3] Continuous profiling for 70 seconds\n")
            log_fh.flush()

            start_time = time.time()
            read_count = 0

            while True:
                elapsed = time.time() - start_time
                if elapsed >= PROFILE_DURATION:
                    break
                if stop_event.is_set():
                    _log(log_fh, "--", "Stop event triggered - ending profile early")
                    break

                # Check for ATT value change from queue
                try:
                    new_att = att_queue.get_nowait()
                    if 0 <= new_att <= 63:
                        current_att = new_att
                        att_cmd_val = current_att + ATT_OFFSET
                        att_hex = f"{att_cmd_val:02X}"
                        _send_command(conn, f"O,A,{att_hex}", log_fh)
                        _wait_for_ack(conn, log_fh)
                        print(f"  ! ATT value changed to {current_att}")
                except queue.Empty:
                    pass

                # ADC read sequence
                _send_command(conn, "O,A,7C", log_fh)
                _wait_for_ack(conn, log_fh)
                time.sleep(ADC_INTER_DELAY)

                _send_command(conn, "O,A,3C", log_fh)
                _wait_for_ack(conn, log_fh)
                time.sleep(ADC_SETTLE_DELAY)

                # Request read
                _send_command(conn, "I", log_fh)
                value = _wait_for_data(conn, log_fh, timeout=READ_TIMEOUT)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                if value is not None:
                    # Store to CSV
                    with open(CSV_FILE, "a", newline="") as csv_fh:
                        writer = csv.writer(csv_fh)
                        writer.writerow([timestamp, element_name, current_att, value])

                    # Store to shared data list
                    data_list.append({
                        "timestamp": timestamp,
                        "element": element_name,
                        "att_value": current_att,
                        "adc_value": value
                    })

                    read_count += 1
                    if read_count % 10 == 0:
                        print(f"  ✓ {read_count} readings @ {elapsed:.1f}s (ATT={current_att}): {value}")
                else:
                    print(f"  ✗ Read failed @ {elapsed:.1f}s")

                # Wait until next read interval
                cycle_elapsed = time.time() - start_time - (read_count - 1) * READ_INTERVAL
                if cycle_elapsed < READ_INTERVAL:
                    time.sleep(READ_INTERVAL - cycle_elapsed)

            print(f"\n  ✓ 70-second profiling complete ({read_count} readings)")

            # ===== STEP 4: SHUTDOWN =====
            print(f"\n  [Step 4] Shutdown...")
            log_fh.write("[Step 4] Shutdown\n")
            log_fh.flush()

            _send_command(conn, "O,A,9D", log_fh)
            _wait_for_ack(conn, log_fh)
            time.sleep(0.050)

            _send_command(conn, "O,A,C3", log_fh)
            _wait_for_ack(conn, log_fh)

            print(f"  ✓ Shutdown complete")

            log_fh.write(f"\nProfile task complete. Total readings: {read_count}\n")
            log_fh.flush()

            return read_count

        except KeyboardInterrupt:
            _log(log_fh, "--", "INTERRUPTED by user")
            print(f"\n  ⚠ Profile interrupted")
            return read_count
        except Exception as e:
            _log(log_fh, "--", f"ERROR: {e}")
            print(f"  ✗ Error: {e}")
            raise
