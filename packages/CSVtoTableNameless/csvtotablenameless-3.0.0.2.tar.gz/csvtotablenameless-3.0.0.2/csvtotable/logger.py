import logging
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Apply color based on the log level
        level_color = self.LEVEL_COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        # Apply the color to the entire formatted line
        log_message = super().format(record)
        return f"{level_color}{log_message}{reset}"  # Reset after each message

# Configure the logger
logger = logging.getLogger("csvtotable")
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
