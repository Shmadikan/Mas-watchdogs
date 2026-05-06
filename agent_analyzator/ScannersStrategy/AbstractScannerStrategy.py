from abc import ABC, abstractmethod
from typing import Any

class AbstractScannerStrategy(ABC):
    """Стратегия по смыслу, шаблонный метод по душе"""
    def __init__(self, instructions: tuple[str, dict[str, Any]]):
        self.instructions = instructions

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def _parse(self, parse_information):
        pass

    @abstractmethod
    def _script_interpreter(self, script: str):
        pass









