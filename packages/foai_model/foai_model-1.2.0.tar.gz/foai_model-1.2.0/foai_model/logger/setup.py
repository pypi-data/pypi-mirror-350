import logging
import os
from datetime import datetime
from pathlib import Path

LOGS_PATH = Path("logs")
os.makedirs(LOGS_PATH, exist_ok=True)

now = datetime.now()
filename = now.strftime("%Y%m%d_%H%M%S.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(LOGS_PATH / filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
