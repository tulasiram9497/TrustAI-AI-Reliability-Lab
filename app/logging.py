import logging


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Set up a structured, application-scoped logger."""

    logger = logging.getLogger("trustai")
    logger.setLevel(level.upper())
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    return logger
