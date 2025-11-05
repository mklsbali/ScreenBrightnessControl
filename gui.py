import tkinter as tk
import brightness_adjuster

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
        self.start_task_button = tk.Button(self._main_frame, text="Start task", command=self._start_task, font=self.buttons_font, width=12)
        self.start_task_button.grid(row=0, column=0, pady=(5, 0), padx=(0, 5), sticky="w")
        # Stop background task button
        self.stop_task_button = tk.Button(self._main_frame, text="Stop task", command=self._stop_task, font=self.buttons_font, width=12, state="disabled")
        self.stop_task_button.grid(row=0, column=1, pady=(5, 0), padx=(0, 5), sticky="w")
        self.sbc = brightness_adjuster.BrightnessAdjuster()

    def _start_task(self):
        self.sbc.start_task()
        self.start_task_button.config(state="disabled")
        self.stop_task_button.config(state="normal")


    def _stop_task(self):  
        self.sbc.stop_task()
        self.start_task_button.config(state="normal")
        self.stop_task_button.config(state="disabled")
