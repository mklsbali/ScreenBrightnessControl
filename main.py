import gui
import sys
import brightness_worker
import logging
import logging.handlers
import config


def setup_logging(logfile=config.logfile):
    """Setup logging for the application.
    Args:
        logfile (str): The path to the log file.
    """
    log_format = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] %(levelname)-8s %(message)s',
                                   datefmt='%y-%m-%d %H:%M:%S')
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    log_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=5e6, backupCount=5)
    log_handler.setFormatter(log_format)
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.DEBUG) 
    # if not config.show_more_logs:
    logging.getLogger("screen_brightness_control").setLevel(logging.ERROR)
    logging.getLogger("wmi").setLevel(logging.ERROR)



if __name__ == "__main__":
    setup_logging()
    if "--background" in sys.argv:
        brightness_worker.main()
    else:
        gui.main()