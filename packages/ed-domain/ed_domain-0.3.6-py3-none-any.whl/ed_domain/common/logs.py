import logging
from logging import Logger, handlers

LEVEL_RELATIONS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "crit": logging.CRITICAL,
}


class CustomLogger(object):
    def __init__(
        self,
        file_name,
        level="info",
        when="D",
        back_count=3,
        log_format="%(asctime)s - %(name)s - %(levelname)s - [%(pathname)s:%(lineno)d - %(funcName)s] - %(message)s",
    ):
        self._logger = logging.getLogger(file_name)
        self._logger.setLevel(LEVEL_RELATIONS.get(level, "info"))

        console_handler = logging.StreamHandler()
        file_handler = handlers.TimedRotatingFileHandler(
            filename=file_name, when=when, backupCount=back_count, encoding="utf-8"
        )

        format_str = logging.Formatter(log_format)
        console_handler.setFormatter(format_str)
        file_handler.setFormatter(format_str)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

    @property
    def logger(self) -> Logger:
        return self._logger


def get_logger() -> Logger:
    log = CustomLogger("example.log", level="debug")
    return log.logger


if __name__ == "__main__":
    LOG = get_logger()
