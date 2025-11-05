import gui
import sys
import brightness_worker

if __name__ == "__main__":
    if "--background" in sys.argv:
        brightness_worker.main()
    else:
        gui.main()