import logging


class PyLogger:
    @staticmethod
    def get_configured_logger():
        fmt_str = "[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=fmt_str)
        _logger = logging.getLogger(__name__)
        return _logger


if __name__ == "__main__":
    logger = PyLogger.get_configured_logger()
    logger.info("Hi there")
