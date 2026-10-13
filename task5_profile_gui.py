"""
Task 5 - Profile GUI
====================
Simple GUI for task5_profile that:
  - Allows selection of element (1-45)
  - Allows input of ATT value (0-63)
  - Displays live ADC data as it comes in
  - Allows changing ATT value during execution
  - Runs independently from the task
  
The GUI communicates with the task via shared_state:
  - shared_state["stop_event"]: Set to stop the task
  - shared_state["att_queue"]: Queue to send new ATT values
  - shared_state["data_list"]: List of readings to display
"""

import tkinter as tk
from tkinter import ttk, messagebox
import queue
import threading
from datetime import datetime
import json

TOTAL_ELEMENTS = 45


class ProfileGUI:
    def __init__(self, root, shared_state=None):
        self.root = root
        self.root.title("Task 5 - Profile GUI")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Shared state with task
        if shared_state is None:
            shared_state = {
                "stop_event": threading.Event(),
                "att_queue": queue.Queue(),
                "data_list": []
            }
        self.shared_state = shared_state
        
        # Local state
        self.task_running = False
        self.last_data_count = 0
        self.element_var = tk.StringVar(value="1")
        self.att_var = tk.StringVar(value="0")
        
        # Color scheme
        self.bg_color = "#f5f5f5"
        self.root.configure(bg=self.bg_color)
        
        self._create_ui()
        self._start_monitor_thread()
        
    def _create_ui(self):
        """Build the GUI layout."""
        
        # ===== TOP SECTION: CONTROLS =====
        control_frame = tk.LabelFrame(self.root, text="Configuration", 
                                      bg="white", font=("Arial", 11, "bold"),
                                      padx=15, pady=15)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Element selection
        elem_sub = tk.Frame(control_frame, bg="white")
        elem_sub.pack(fill=tk.X, pady=8)
        
        tk.Label(elem_sub, text="Element (1-45):", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.elem_spinbox = tk.Spinbox(elem_sub, from_=1, to=TOTAL_ELEMENTS, 
                                       textvariable=self.element_var, width=6,
                                       font=("Arial", 10), state="normal")
        self.elem_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(elem_sub, text="ATT Value (0-63):", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=20)
        self.att_spinbox = tk.Spinbox(elem_sub, from_=0, to=63, 
                                      textvariable=self.att_var, width=6,
                                      font=("Arial", 10), state="normal")
        self.att_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_sub = tk.Frame(control_frame, bg="white")
        btn_sub.pack(fill=tk.X, pady=12)
        
        self.btn_start = tk.Button(btn_sub, text="▶ Start Profile", command=self._on_start,
                                   bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                                   cursor="hand2", padx=15, pady=8)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = tk.Button(btn_sub, text="⏹ Stop", command=self._on_stop,
                                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                                  cursor="hand2", padx=15, pady=8, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        self.btn_update_att = tk.Button(btn_sub, text="↻ Update ATT", command=self._on_update_att,
                                        bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                        cursor="hand2", padx=15, pady=8, state=tk.DISABLED)
        self.btn_update_att.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = tk.Label(control_frame, text="Status: Ready", 
                                     bg="white", font=("Arial", 10), fg="#2c3e50")
        self.status_label.pack(fill=tk.X, pady=8)
        
        # ===== DATA DISPLAY SECTION =====
        display_frame = tk.LabelFrame(self.root, text="Live Data (Last 50 readings)", 
                                      bg="white", font=("Arial", 11, "bold"),
                                      padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview with scrollbars
        tree_container = tk.Frame(display_frame, bg="white")
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(tree_container, 
                                 columns=("Time", "Element", "ATT", "ADC Value"),
                                 height=20, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Column setup
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Time", anchor=tk.W, width=180)
        self.tree.column("Element", anchor=tk.CENTER, width=80)
        self.tree.column("ATT", anchor=tk.CENTER, width=60)
        self.tree.column("ADC Value", anchor=tk.CENTER, width=100)
        
        self.tree.heading("#0", text="")
        self.tree.heading("Time", text="Timestamp")
        self.tree.heading("Element", text="Element")
        self.tree.heading("ATT", text="ATT")
        self.tree.heading("ADC Value", text="ADC Value")
        
        # Pack tree and scrollbars
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # ===== STATS SECTION =====
        stats_frame = tk.Frame(self.root, bg="white", relief=tk.SUNKEN, bd=1)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Readings: 0 | Min: — | Max: — | Avg: —",
                                    bg="white", font=("Arial", 10), justify=tk.LEFT)
        self.stats_label.pack(fill=tk.X, padx=10, pady=8)
        
    def _on_start(self):
        """Start the profile task in a separate thread."""
        try:
            element = int(self.element_var.get())
            att = int(self.att_var.get())
            
            if not (1 <= element <= TOTAL_ELEMENTS):
                messagebox.showerror("Invalid Input", f"Element must be 1-{TOTAL_ELEMENTS}")
                return
            if not (0 <= att <= 63):
                messagebox.showerror("Invalid Input", "ATT value must be 0-63")
                return
            
            # Disable controls
            self.elem_spinbox.config(state=tk.DISABLED)
            self.att_spinbox.config(state=tk.DISABLED)
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_update_att.config(state=tk.NORMAL)
            
            # Clear previous data
            self.shared_state["data_list"].clear()
            self.shared_state["stop_event"].clear()
            self.last_data_count = 0
            
            # Update UI
            self.task_running = True
            self.status_label.config(text=f"Status: Running (Element {element}, ATT {att})", fg="#27ae60")
            
            # Import and run task in background thread
            def task_thread():
                try:
                    from task5_profile import run_profile
                    
                    # Use shared connection if available, otherwise create new one
                    conn = self.shared_state.get("conn")
                    if conn is None:
                        from task1_usb_init import init_uart
                        conn = init_uart()
                        should_close = True
                    else:
                        should_close = False
                    
                    try:
                        run_profile(conn, element - 1, att, self.shared_state)
                    finally:
                        if should_close:
                            conn.close()
                        
                    # Task completed
                    self.root.after(100, self._task_completed)
                except Exception as e:
                    messagebox.showerror("Task Error", f"Error running profile task:\n{e}")
                    self.root.after(100, self._task_completed)
            
            thread = threading.Thread(target=task_thread, daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers")
    
    def _on_stop(self):
        """Signal the task to stop."""
        self.shared_state["stop_event"].set()
        self.btn_stop.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopping...", fg="#e67e22")
    
    def _on_update_att(self):
        """Send a new ATT value to the running task."""
        try:
            new_att = int(self.att_var.get())
            if not (0 <= new_att <= 63):
                messagebox.showerror("Invalid Input", "ATT value must be 0-63")
                return
            
            self.shared_state["att_queue"].put(new_att)
            # Visual feedback
            self.btn_update_att.config(bg="#f39c12")
            self.root.after(300, lambda: self.btn_update_att.config(bg="#3498db") if self.btn_update_att.cget("state") == tk.NORMAL else None)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid ATT value (0-63)")
    
    def _task_completed(self):
        """Called when task completes."""
        self.task_running = False
        self.elem_spinbox.config(state=tk.NORMAL)
        self.att_spinbox.config(state=tk.NORMAL)
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_update_att.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Complete", fg="#27ae60")
    
    def _start_monitor_thread(self):
        """Start background thread to monitor shared_state for updates."""
        def monitor():
            while True:
                try:
                    data_list = self.shared_state.get("data_list", [])
                    
                    # Check if new data available
                    if len(data_list) > self.last_data_count:
                        self.root.after(0, self._update_display)
                        self.last_data_count = len(data_list)
                    
                    threading.Event().wait(0.2)  # Check every 200ms
                except Exception:
                    pass
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def _update_display(self):
        """Update the treeview with latest data."""
        data_list = self.shared_state.get("data_list", [])
        
        # Clear all items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get last 50 entries
        display_data = data_list[-50:] if len(data_list) > 50 else data_list
        
        for reading in display_data:
            time_str = reading.get("timestamp", "—")
            element = reading.get("element", "—")
            att = reading.get("att_value", "—")
            adc = reading.get("adc_value", "—")
            
            self.tree.insert("", tk.END, values=(time_str, element, att, adc))
        
        # Scroll to bottom
        if display_data:
            self.tree.see(self.tree.get_children()[-1])
        
        # Update stats
        self._update_stats(data_list)
    
    def _update_stats(self, data_list):
        """Update statistics display."""
        if not data_list:
            self.stats_label.config(text="Readings: 0 | Min: — | Max: — | Avg: —")
            return
        
        values = [d.get("adc_value", 0) for d in data_list if d.get("adc_value") is not None]
        
        if not values:
            self.stats_label.config(text="Readings: 0 | Min: — | Max: — | Avg: —")
            return
        
        min_val = min(values)
        max_val = max(values)
        avg_val = sum(values) / len(values)
        
        stats_text = f"Readings: {len(values)} | Min: {min_val} | Max: {max_val} | Avg: {avg_val:.1f}"
        self.stats_label.config(text=stats_text)


def main():
    """Launch the profile GUI."""
    root = tk.Tk()
    
    # Create shared state
    shared_state = {
        "stop_event": threading.Event(),
        "att_queue": queue.Queue(),
        "data_list": []
    }
    
    app = ProfileGUI(root, shared_state)
    root.mainloop()


if __name__ == "__main__":
    main()
