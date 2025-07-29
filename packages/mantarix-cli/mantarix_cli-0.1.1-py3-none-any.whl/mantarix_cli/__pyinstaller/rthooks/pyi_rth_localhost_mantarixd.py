import logging
import os

import mantarix

logger = logging.getLogger(mantarix.__name__)


logger.info("Running PyInstaller runtime hook for Mantarix...")

os.environ["MANTARIX_SERVER_IP"] = "127.0.0.1"
