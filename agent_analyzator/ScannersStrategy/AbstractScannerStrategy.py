from abc import ABC, abstractmethod

class AbstractScannerStrategy(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def __parse(self):
        pass