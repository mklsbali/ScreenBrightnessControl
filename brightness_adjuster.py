
import screen_brightness_control as sbc
import threading

MAIN_DISPLAY = 0  
SECONDARY_DISPLAY_1 = 1 
DEFAULT_INTERVAL = .1

class BrightnessAdjuster:
   
    def __init__(self, start=0, finish=100, increment=5, display=MAIN_DISPLAY, interval=DEFAULT_INTERVAL):
        self.start = start
        self.finish = finish
        self.increment = increment
        self.display = display
        self.interval = interval
        self._init_brightness = sbc.get_brightness(display=self.display)[0]
        self.stop_event = threading.Event()
        self._thread = None
    

    def start_task(self):
        # Prevent starting multiple background threads
        if self._thread is not None and self._thread.is_alive():
            return
        self.stop_event.clear()
        # store the thread so we can later check or join it
        self._thread = threading.Thread(target=self._start_task, daemon=True)
        self._thread.start()

    def _start_task(self):
        """Test fade brigthness method"""
        init_brightness = sbc.get_brightness(display=self.display)[0]
        while True:
            try:
                sbc.fade_brightness(start=init_brightness, finish=self.finish, increment=self.increment, display=self.display, interval=self.interval, blocking=True)
                sbc.fade_brightness(start=self.finish, finish=self.start, increment=self.increment, display=self.display, interval=self.interval, blocking=True)                     
                sbc.fade_brightness(start=self.start, finish=self.finish, increment=self.increment, display=self.display, interval=self.interval, blocking=True) 
                sbc.fade_brightness(start=self.finish, finish=init_brightness, increment=self.increment, display=self.display, interval=self.interval, blocking=True) 

                if self.stop_event.is_set():
                    break
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error adjusting brightness: {e}")
                break
    
            
    def stop_task(self):
        self.stop_event.set()