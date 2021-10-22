from JustBot.apis.adapter_config import AdapterConfig

from abc import ABCMeta, abstractmethod
from typing import Any


class Adapter(metaclass=ABCMeta):
    """
    适配器 ``Adapter`` 抽象类
    """

    @abstractmethod
    def __init__(self, config: AdapterConfig) -> None:
        pass

    # TODO: 添加文档
    @abstractmethod
    def _request_api(self, api_path: str) -> str:
        pass

    @abstractmethod
    def login_info(self) -> dict:
        pass

    @abstractmethod
    def nick_name(self) -> str:
        pass

    @abstractmethod
    async def start_listen(self) -> None:
        pass

    @abstractmethod
    def receiver(self, event: str) -> Any:
        pass
