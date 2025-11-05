import tkinter as tk
import brightness_adjuster
from config import *
import psutil
import os
import subprocess   
import signal
import time 
import sys

def is_worker_running():
    """Check if the brightness worker is running."""
    if not os.path.exists(PID_FILE):
        return False
    try:
        pid = int(open(PID_FILE).read())
    except (OSError, ValueError):
        return False
    return psutil.pid_exists(pid)


       
def start_fade():
    if is_worker_running():
        print("Brightness fader is already running.")
        return
        # Launch detached process
    subprocess.Popen([sys.executable, "--background"], creationflags=subprocess.DETACHED_PROCESS if os.name == "nt" else 0)
    print("Brightness fader started.")

def stop_fade():
    """Stop the brightness fading background process."""
    if not os.path.exists(PID_FILE):
        print("No running brightness fader found.")
        return

    try:
        pid = int(open(PID_FILE).read())
        print(f"Stopping brightness fader (PID {pid})...")
        os.kill(pid, signal.SIGTERM)

        # Wait for it to exit gracefully
        for _ in range(10):
            if not psutil.pid_exists(pid):
                break
            time.sleep(0.5)
    except Exception as e:
        print("Error stopping fader:", e)
    finally:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        print("Brightness fader stopped.")


class ScreenBrightnessControlGUI(tk.Tk):
    buttons_font = ("Arial", 10, "bold")
    def __init__(self):
        super().__init__()
        self.title("Screen Brightness Control")
        # self.geometry("+0+0")
        self.resizable(False, False)
        self._create_widgets()


    def _create_widgets(self):
        """Create and place widgets in the main window."""
        # Main frame 
        self._main_frame = tk.Frame(self, width=200, height=100)
        self._main_frame.pack(padx=10, pady=10)

        # Start background task button
        self.start_task_button = tk.Button(self._main_frame, text="Start task", command=self._start_task, font=self.buttons_font, width=12, state="normal" if not is_worker_running() else "disabled")
        self.start_task_button.grid(row=0, column=0, pady=(5, 0), padx=(0, 5), sticky="w")
        # Stop background task button
        self.stop_task_button = tk.Button(self._main_frame, text="Stop task", command=self._stop_task, font=self.buttons_font, width=12, state="normal" if is_worker_running() else "disabled")
        self.stop_task_button.grid(row=0, column=1, pady=(5, 0), padx=(0, 5), sticky="w")
        # self.sbc = brightness_adjuster.BrightnessAdjuster()

    def _start_task(self):
        start_fade()
        self.start_task_button.config(state="disabled")
        self.stop_task_button.config(state="normal")


    def _stop_task(self):  
        stop_fade()
        self.start_task_button.config(state="normal")
        self.stop_task_button.config(state="disabled")


def main():
    app = ScreenBrightnessControlGUI()
    app.mainloop()