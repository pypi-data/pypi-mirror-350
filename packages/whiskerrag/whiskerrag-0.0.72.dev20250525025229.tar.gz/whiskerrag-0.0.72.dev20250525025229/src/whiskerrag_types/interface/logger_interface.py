from abc import ABC, abstractmethod
from typing import Any


class LoggerManagerInterface(ABC):
    @abstractmethod
    def get_logger(self) -> Any:
        pass

    @abstractmethod
    def info(self, message: str, *args: tuple, **kwargs: dict) -> None:
        pass

    @abstractmethod
    def error(self, message: str, *args: tuple, **kwargs: dict) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, *args: tuple, **kwargs: dict) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, *args: tuple, **kwargs: dict) -> None:
        pass
