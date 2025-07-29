import logging
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style
import datetime
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


class BasicLog:
    def __init__(
            self, 
            log_file_path: str, 
            stream: bool = True, 
            dsn: str = None, 
            log_level:str = 'error',
            trace_rate: float = 0.5) -> None:
        """
        dsn - sentry dsn key;
        log_level - logging level(debug, info, warning, error):str;
        trace_rate - if 1.0(100%) - all logs will be sent;
        """
        self.log_file_path = log_file_path
        self.stream = stream
        self.dsn = dsn
        self.log_level = log_level
        self.trace_rate = trace_rate

    def log_config(
            self, 
            name:str, 
            loglevel= logging.DEBUG
            ) -> logging.Logger:
        """
        Configuration of the logger.

        Args:
            name (str): The name of the logger.
            stream (bool, optional): Whether to log to a stream or a file. Defaults to True.
            loglevel (int, optional): The level of the messages to log. Defaults to logging.DEBUG.

        Returns:
            logging.Logger: The configured logger.
        """
        level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }
        logger_name = (name)
        logger = logging.getLogger(logger_name)
        if self.dsn:
            """интегрируем Sentry в логгер"""
            sentry_sdk.init(
                dsn=self.dsn,
                traces_sample_rate=self.trace_rate,
                integrations=[
                    LoggingIntegration(
                        level=level[self.log_level],        # Capture info and above as breadcrumbs
                        event_level=level[self.log_level],  # Send records as events
                    ),
                ],
            )
        logger.setLevel(loglevel)
        formater = ColoredFormatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        conf = {
            True: self.stream_conf(formater),
            False: self.file_conf(formater)
        }
        #добавление хендлера
        logger.addHandler(conf[self.stream])
        return logger

    def stream_conf(self, formater):
        #настройки для консоли
        stream = logging.StreamHandler()
        stream.setFormatter(formater)
        return stream
    
    def file_conf(self, formater):
        #настройки для лог-файла
        log_file = RotatingFileHandler(self.log_file_path, maxBytes=100000, backupCount=3)
        log_file.setFormatter(formater)
        return log_file


class ColoredFormatter(logging.Formatter):
    """Добавляем настройки цвета сообщений"""
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,    
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        if record.levelno in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelno]}{record.levelname}{Style.RESET_ALL}"
            record.msg = f"{self.COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}"
            record.filename = f"{self.COLORS[record.levelno]}{record.filename}{Style.RESET_ALL}"
            record.funcName = f"{self.COLORS[record.levelno]}{record.funcName}{Style.RESET_ALL}"
        return super().format(record)