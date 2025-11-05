import sys
import os
import pathlib

PID_FILE = "brightness_fader.pid"
MAIN_DISPLAY = 0
DEFAULT_INTERVAL = 0.1

executable = getattr(sys, 'frozen', False) == True
base_folder_name = "SreenBrightnessControl"

if executable:
    settings_dir = pathlib.Path(f"C:/ProgramData/{base_folder_name}")
else:
    settings_dir = pathlib.Path(f"C:/ProgramData/dev/{base_folder_name}")

settings_dir.mkdir(parents=True, exist_ok=True)
logfile  = settings_dir.joinpath("app.log")