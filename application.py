from .utils import Logger
from .apis import Adapter, MessageChain, Config as config
from .objects import Friend, Group
from .exceptions import StatusError
from .handlers import SenderHandler

from typing import Callable, Type, Union

import asyncio

VERSION = '2.0.1'


class BotApplication:
    def __init__(self, adapter: Adapter) -> None:
        self.adapter = adapter
        self.logger = Logger(f'Application/{VERSION}')
        self.sender_handler = SenderHandler(self.adapter)
        self.adapter_utils = self.adapter.adapter_utils

        self.logger.info(f'加载 JustBot<v{VERSION}> 中...')
        self.logger.info(f'使用的适配器: `{adapter.name}`.')
        asyncio.run(self.adapter.connect())
        self.logger.info(f'获取账号信息: 账号 `{self.adapter.account}`, 昵称 `{self.adapter.nick_name}`.')
        self.set_config()

    def set_config(self) -> None:
        config.adapter = self.adapter
        config.account = self.adapter.account
        config.nick_name = self.adapter.nick_name

    def start_running(self) -> None:
        asyncio.run(self.adapter.start_listen())

    def send_msg(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain):
        self.sender_handler.send_message(receiver_type, target_id, message)
