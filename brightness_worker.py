# brightness_worker.py
import screen_brightness_control as sbc
import time
import threading
import signal
import sys
import os
from config import *

stop_event = threading.Event()

def handle_stop_signal(signum, frame):
    stop_event.set()

signal.signal(signal.SIGTERM, handle_stop_signal)
signal.signal(signal.SIGINT, handle_stop_signal)

def fade_loop(start, finish, increment, display, interval):
    print("Brightness fade worker started.")
    init_brightness = sbc.get_brightness(display=display)[0]
    while True:
        try:
            sbc.fade_brightness(start=init_brightness, finish=finish, increment=increment, display=display, interval=interval, blocking=True)
            sbc.fade_brightness(start=finish, finish=start, increment=increment, display=display, interval=interval, blocking=True)                     
            sbc.fade_brightness(start=start, finish=finish, increment=increment, display=display, interval=interval, blocking=True) 
            sbc.fade_brightness(start=finish, finish=init_brightness, increment=increment, display=display, interval=interval, blocking=True) 

            if stop_event.is_set():
                break
        except Exception as e:
            print("Error:", e)
            break
    # sbc.set_brightness(100, display=display)
    print("Brightness fade worker stopped.")


def main():
    # Write PID to file
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    try:
        fade_loop(start=0, finish=100, increment=5, display=MAIN_DISPLAY, interval=DEFAULT_INTERVAL)
    finally:
        # Remove PID file when done
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

if __name__ == "__main__":
    main()
