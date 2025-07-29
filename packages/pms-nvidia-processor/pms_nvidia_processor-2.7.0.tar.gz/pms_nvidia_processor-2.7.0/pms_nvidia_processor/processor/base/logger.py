from .dependency import *


class LogLevel(enum.Enum):
    TRACE = enum.auto()
    DEBUG = enum.auto()
    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()
    CRITICAL = enum.auto()


class ILogger(ABC):

    @abstractmethod
    def log(self, level: LogLevel, message: str, **kwargs): ...

    def trace(self, message: str, **kwargs):
        self.log(LogLevel.TRACE, message, **kwargs)

    def debug(self, message: str, **kwargs):
        self.log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        self.log(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self.log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        self.log(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        self.log(LogLevel.CRITICAL, message, **kwargs)


class LoguruLogger(ILogger):
    def __init__(self):
        self._logger = loguru.logger

    def log(self, level: LogLevel, message: str):
        return self._logger.log(level.name, message)
