__all__ = [
    "logger"
]

import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='{%(asctime)s: (%(name)s, %(levelname)s, %(message)s)}'))
logger.addHandler(handler)
