from JustBot.apis import Adapter
from JustBot.adapters.mirai.config import MiraiConfig
from JustBot.adapters.mirai.message_handler import MiraiMessageHandler
from JustBot.adapters.mirai.sender_handler import MiraiSenderHandler
from JustBot.utils import Logger, ListenerManager
from JustBot.application import HTTP_PROTOCOL, WS_PROTOCOL

from aiohttp import request
from typing import Any


class MiraiAdapter(Adapter):
    def __init__(self, config: MiraiConfig) -> None:
        self.name = 'Mirai'
        self.ws_host = config.ws_host
        self.ws_port = config.ws_port
        self.http_host = config.http_host
        self.http_port = config.http_port
        self.session_key = config.session_key
        self.ws_reverse = config.ws_reverse

        self.logger = Logger(f'Adapter/{self.name}')
        self.listener_manager = ListenerManager()
        self.utils = MiraiUtils(self)
        self.sender_handler = MiraiSenderHandler(self)
        self.message_handler = MiraiMessageHandler(self)
        global_config.listener_manager = self.listener_manager
        global_config.message_handler = self.message_handler
        global_config.adapter_utils = self.utils

    async def __request_api(self, api_path: str) -> str:
        try:
            async with request('GET', f'{HTTP_PROTOCOL}{self.http_host}:{self.http_port}{api_path}') as response:
                return (await response.json())['data']
        except ClientConnectorError as e:
            raise Exception(
                f'无法连接到 Mirai-Api-Http, 请检查是否配置完整! {e}')

    @property
    async def login_info(self) -> dict:
        pass

    @property
    async def account(self) -> int:
        pass

    @property
    async def nick_name(self) -> str:
        pass

    async def check(self) -> None:
        pass

    async def start_listen(self) -> None:
        pass

    def receiver(self, event: str) -> Any:
        pass
