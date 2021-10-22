from JustBot.utils import Logger, MessageChain
from JustBot.apis import Adapter,  Config as config
from JustBot.objects import Friend, Group

from typing import Callable, Type, Union, Coroutine, Any

import asyncio

VERSION = '2.0.1'
HTTP_PROTOCOL = 'http://'
WS_PROTOCOL = 'ws://'

# TODO: 可选参数使用 typing.Optional
class BotApplication:
    def __init__(self, adapter: Adapter) -> None:
        """
        ``BotApplication``

        机器人实例

        >>> from JustBot import BotApplication, CQHttpAdapter, CQHttpConfig
        >>> cqhttp_config = CQHttpConfig(ws_host='127.0.0.1', ws_port=6700,
        ...                              http_host='127.0.0.1', http_port=5700, ws_reverse=False)
        ...
        >>> cqhttp_adapter = CQHttpAdapter(cqhttp_config)
        >>> bot = BotApplication(cqhttp_adapter)
        >>> bot.start_running()
        """

        self.adapter = adapter
        self.logger = Logger(f'Application/{VERSION}')
        self.sender_handler = self.adapter.sender_handler
        self.adapter_utils = self.adapter.utils

        self.logger.info(f'加载 JustBot<v{VERSION}> 中...')
        self.logger.info(f'使用的适配器: `{adapter.name}`.')
        self.nick_name = self.coroutine(self.adapter.nick_name)
        self.logger.info(f'登录成功: `{self.nick_name}`.')
        self.set_config()
        self.coroutine(self.adapter.check())

    def set_config(self) -> None:
        config.adapter = self.adapter
        config.nick_name = self.nick_name

    def start_running(self) -> None:
        self.coroutine(self.adapter.start_listen())

    async def send_msg(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain):
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
        await self.sender_handler.send_message(receiver_type, target_id, message)

    @staticmethod
    def coroutine(coroutine: Union[Coroutine, Any]) -> Any:
        return asyncio.run(coroutine)
