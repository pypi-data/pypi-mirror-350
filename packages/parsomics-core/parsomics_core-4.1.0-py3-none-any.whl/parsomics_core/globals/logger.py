import logging

from parsomics_core.globals.environment import Environment


def setup_logging(env: Environment):
    level = logging.DEBUG if env == Environment.DEVELOPMENT else logging.WARNING
    format = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    logging.warning(f"Logging level configured to {level}")
    logging.basicConfig(level=level, format=format)

    file_handler = logging.FileHandler("parsomics.log")
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(format))
    logging.getLogger().addHandler(file_handler)
