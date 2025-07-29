import datetime
import enum
from abc import abstractmethod, ABC


class Severity(enum.Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Logger(ABC):
    def __init__(self, severity_level: Severity = Severity.INFO):
        self._severity_level: Severity = severity_level

    def set_severity_level(self, severity_level: Severity = Severity.INFO) -> None:
        self._severity_level = severity_level

    def log(self, message: str, severity_level: Severity = None) -> None:
        severity_level = severity_level or self._severity_level
        self._log(message, severity_level)

    @abstractmethod
    def initialize(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _log(self, message: str, severity_level: Severity) -> None:
        raise NotImplementedError()


class ConsoleLogger(Logger):
    def initialize(self, *args, **kwargs) -> None:
        pass

    def _log(self, message: str, severity_level: Severity) -> None:
        print(f"[{severity_level.value}] {datetime.datetime.now()} | {message}")


# TODO: to implement
class AdlsTableLogger(Logger):
    def initialize(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def _log(self, message: str, severity_level: Severity) -> None:
        raise NotImplementedError()


# TODO: to implement
class InMemoryLogger(Logger):
    def initialize(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def _log(self, message: str, severity_level: Severity) -> None:
        raise NotImplementedError()


# TODO: to implement
class RestEndpointLogger(Logger):
    def initialize(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def _log(self, message: str, severity_level: Severity) -> None:
        raise NotImplementedError()


class NoLogger(Logger):
    def initialize(self, *args, **kwargs) -> None:
        pass

    def _log(self, message: str, severity_level: Severity) -> None:
        pass
