from JustBot.utils import Logger, MessageChain, Listener, ListenerManager
from JustBot.apis import Adapter, Config
from JustBot.objects import Friend, Group
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.matchers import KeywordsMatcher, CommandMatcher

from typing import Callable, Type, Union, Coroutine, Any, List, Awaitable

import asyncio

VERSION = '2.0.1'
HTTP_PROTOCOL = 'http://'
WS_PROTOCOL = 'ws://'
CONFIG = Config(None, None, None, None, None)

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
        self.nickname = self.coroutine(self.adapter.nick_name)
        self.listener_manager = ListenerManager()
        self.sender_handler = self.adapter.sender_handler
        self.adapter_utils = self.adapter.utils
        self.message_handler = self.adapter.message_handler
        self.set_config()
        self.logger = Logger(f'Application/{VERSION}')

        self.logger.info(f'加载 JustBot<v{VERSION}> 中...')
        self.logger.info(f'使用的适配器: `{adapter.name}`.')
        self.logger.info(f'登录成功: `{self.nickname}`.')
        self.coroutine(self.adapter.check())

    def set_config(self) -> None:
        CONFIG.adapter = self.adapter
        CONFIG.nickname = self.nickname
        CONFIG.listener_manager = self.listener_manager
        CONFIG.sender_handler = self.sender_handler
        CONFIG.adapter_utils = self.adapter_utils
        CONFIG.message_handler = self.message_handler

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

    @staticmethod
    def get_config(name: str) -> Any:
        print(CONFIG.__dict__)
        print(CONFIG)
        # return config.__dict__

    def receiver(self, event: List[Type[Union[PrivateMessageEvent, GroupMessageEvent]]],
                 priority: int = 1, matcher: Union[KeywordsMatcher, CommandMatcher] = None,
                 parameters_convert: Type[Union[str, list, dict, None]] = str) -> Any:

        parameters_convert = parameters_convert if isinstance(matcher, CommandMatcher) else None

        def wrapper(target: Callable and Awaitable):
            if asyncio.iscoroutinefunction(target):
                if len(event) == 1:
                    self.logger.info(
                        f'注册监听器: [blue]{event} [red]([white]{priority}[/white])[/red][/blue] => [light_green]{target}[/light_green].')
                    self.listener_manager.join(listener=Listener(event[0], target), priority=priority, matcher=matcher,
                                               parameters_convert=parameters_convert)
                else:
                    self.logger.info(
                        f'注册监听器 (多个事件): [blue]{" & ".join([str(e) for e in event])} [red]([white]{priority}[/white])[/red][/blue] => [light_green]{target}[/light_green].')
                    for e in event:
                        self.listener_manager.join(listener=Listener(e, target), priority=priority, matcher=matcher,
                                                   parameters_convert=parameters_convert)
            else:
                self.logger.warning(f'无法注册监听器: 已忽略函数 [light_green]{target}[/light_green], 因为它必须是异步函数!')

        return wrapper

