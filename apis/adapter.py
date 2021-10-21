from JustBot.apis.session_config import SessionConfig

from abc import ABCMeta, abstractmethod


class Adapter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config: SessionConfig) -> None:
        pass

    @abstractmethod
    def __request_api(self, api_path: str) -> str:
        pass

    @property
    def login_info(self) -> dict:
        pass

    @property
    def account(self) -> int:
        pass

    @property
    def nick_name(self) -> str:
        pass

    @abstractmethod
    async def check(self) -> None:
        pass

    @abstractmethod
    async def start_listen(self) -> None:
        pass

    @abstractmethod
    def receiver(self, event: str):
        pass
