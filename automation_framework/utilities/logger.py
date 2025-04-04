import logging

logger = logging.getLogger("TestLogger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
