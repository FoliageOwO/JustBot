from JustBot.utils import Logger
from JustBot.apis import Adapter, MessageChain, Config as config
from JustBot.objects import Friend, Group

from typing import Callable, Type, Union, Awaitable

import asyncio

VERSION = '2.0.1'


class BotApplication:
    def __init__(self, adapter: Adapter) -> None:
        """
        ``BotApplication``

        机器人实例

        >>> from JustBot import BotApplication, CQHTTPAdapter, CQHTTPConfig
        >>> cqhttp_config = CQHTTPConfig(ws_host='127.0.0.1', ws_port=6700,
        ...                               http_host='127.0.0.1', http_port=5700, ws_reverse=False)
        ...
        >>> cqhttp_adapter = CQHTTPAdapter(cqhttp_config)
        >>> bot = BotApplication(cqhttp_adapter)
        >>> bot.start_running()
        """

        self.adapter = adapter
        self.logger = Logger(f'Application/{VERSION}')
        self.sender_handler = self.adapter.sender_handler
        self.adapter_utils = self.adapter.utils

        self.logger.info(f'加载 JustBot<v{VERSION}> 中...')
        self.logger.info(f'使用的适配器: `{adapter.name}`.')
        self.__run_coroutine(self.adapter.connect())
        self.logger.info(f'获取账号信息: 账号 `{self.adapter.account}`, 昵称 `{self.adapter.nick_name}`.')
        self.set_config()

    def set_config(self) -> None:
        config.adapter = self.adapter
        config.account = self.adapter.account
        config.nick_name = self.adapter.nick_name

    def start_running(self) -> None:
        self.__run_coroutine(self.adapter.start_listen())

    def send_msg(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain):
        """
        向联系人发送消息

        >>> from JustBot import BotApplication, Friend, MessageChain
        >>> from JustBot import Text
        >>> bot = ...
        >>> bot.send_msg(Friend, 10001, MessageChain.create([Text('Hello, World!')]))

        :param receiver_type: 联系人类型 [Friend 或 Group]
        :param target_id: 联系人 ID [qq 号或群号]
        :param message: 要发送的消息的消息链
        """
        self.sender_handler.send_message(receiver_type, target_id, message)

    @staticmethod
    def __run_coroutine(awaitable: Awaitable):
        asyncio.run(awaitable)
