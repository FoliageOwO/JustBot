from JustBot.apis.session_config import SessionConfig

from abc import ABCMeta, abstractmethod


class Adapter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config: SessionConfig) -> None:
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def start_listen(self) -> None:
        pass

    @abstractmethod
    def receiver(self, event: str):
        pass
