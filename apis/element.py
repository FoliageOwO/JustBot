from abc import ABCMeta, abstractmethod


class Element:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def as_display(self) -> str:
        pass

    @abstractmethod
    def as_code(self) -> str:
        pass
