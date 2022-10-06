import logging
import os

from from_root import from_root

from sensor.constant import ARTIFACTS_DIR, LOG_DIR, LOG_FILE

logs_path = os.path.join(from_root(), ARTIFACTS_DIR, LOG_DIR)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
