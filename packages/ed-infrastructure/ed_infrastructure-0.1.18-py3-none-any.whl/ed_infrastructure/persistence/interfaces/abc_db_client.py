from abc import ABCMeta, abstractmethod


class ABCDbClient(metaclass=ABCMeta):
    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...
