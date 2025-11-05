# brightness_worker.py
import screen_brightness_control as sbc
import time
import threading
import signal
import sys
import os
from config import PID_FILE, DEFAULT_INTERVAL, MAIN_DISPLAY
import logging  
import pythoncom

stop_event = threading.Event()

def handle_stop_signal(signum, frame):
    stop_event.set()

signal.signal(signal.SIGTERM, handle_stop_signal)
signal.signal(signal.SIGINT, handle_stop_signal)

def fade_loop(start, finish, increment, display, interval):

    try:
        logging.info("Brightness fade worker started.")
        init_brightness = sbc.get_brightness(display=display)[0]
        # pythoncom.CoInitialize()  # Initialize COM for this thread

        while True:
            try:
                sbc.fade_brightness(start=init_brightness, finish=finish, increment=increment, display=display, interval=interval, blocking=True)
                sbc.fade_brightness(start=finish, finish=start, increment=increment, display=display, interval=interval, blocking=True)                     
                sbc.fade_brightness(start=start, finish=finish, increment=increment, display=display, interval=interval, blocking=True) 
                sbc.fade_brightness(start=finish, finish=init_brightness, increment=increment, display=display, interval=interval, blocking=True) 
                if stop_event.is_set():
                    break
            except Exception as e:
                logging.error("Error:", e)
                break
    finally:
        # pythoncom.CoUninitialize()
        logging.info("Brightness fade worker stopped.")




def main():
    # Write PID to file
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    try:
        fade_loop(start=1, finish=100, increment=5, display=MAIN_DISPLAY, interval=DEFAULT_INTERVAL)
    finally:
        # Remove PID file when done
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

            
if __name__ == "__main__":
    main()
