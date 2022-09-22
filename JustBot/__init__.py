from .utils import Logger, MessageChain, Listener, ListenerManager
from .apis import Adapter, Config, Event, Element
from .contact import Friend, Group
from .matchers import KeywordMatcher, CommandMatcher

from typing import Type, Union, Coroutine, Any, List, Awaitable, Tuple, Callable
from rich.traceback import install

import asyncio

install()
VERSION = '2.0.2'
HTTP_PROTOCOL = 'http://'
WS_PROTOCOL = 'ws://'
CONFIG = Config(*[None] * 5)


class BotApplication:
    """
    > 说明
        机器人实例类
    > 参数
        + adapter [Adapter]: 适配器实例
    """

    def __init__(self, adapter: Adapter) -> None:
        self.adapter = adapter
        self.nickname = self.coroutine(self.adapter.nick_name)
        self.listener_manager = ListenerManager()
        self.adapter_utils = self.adapter.utils
        self.message_handler = self.adapter.message_handler
        self.set_config()
        self.logger = Logger('Application/%s' % VERSION)

        self.logger.info('加载 JustBot<v%s> 中...' % VERSION)
        self.logger.info('使用的适配器: `%s`.' % adapter.name)
        self.logger.info('登录成功: `%s`.' % self.nickname)
        self.coroutine(self.adapter.check())

    def set_config(self) -> None:
        for k in self.__dict__.keys():
            CONFIG.__setattr__(k, self.__dict__[k])

    def start_running(self) -> None:
        self.coroutine(self.adapter.start_listen())

    async def send_msg(self, target: Union[Friend, Group], message: Union[MessageChain, str]) -> None:
        """
        > 说明
            向联系人发送消息
        > 参数
            + target [Friend | Group]: 联系人实例
            + message [MessageChain | str]: 消息链或纯文本 (纯文本会自动转为 ``Plain``)
        > 示例
            >>> await app.send_msg(Friend(123456789), MessageChain.create(Reply(123456789), Plain('Example Message')))
            >>> await app.send_msg(Friend(123456789), 'Example Message')
        """

        try:
            if type(message) is MessageChain:
                await self.adapter.send_message(target, message)
            elif type(message) is str:
                plain: Element = \
                    [i for i in Element.__subclasses__()
                     if self.adapter.name.lower() in str(i) and i.__name__ == 'Plain'
                     ][0](message)
                await self.adapter.send_message(target, MessageChain.create(plain))
            else:
                self.adapter.logger.warning(
                    '无法发送消息: 参数 [light_green]message[/light_green] 必须是 [light_green]消息链[/light_green] 或 [light_green]纯文本[/light_green] 类型!')
        except Exception as e:
            self.adapter.logger.error('无法发送消息: `%s`' % str(e))
            raise

    @staticmethod
    def coroutine(coroutine: Union[Coroutine, Any]) -> Any:
        return asyncio.run(coroutine)

    def receiver(self, *,
                 event: Union[List[Type[Event]], Tuple[Type[Event]], Type[Event]],
                 priority: int = 5, matcher: Union[KeywordMatcher, CommandMatcher] = None,
                 parameters_convert: Type[Union[str, list, dict, None]] = list) -> "wrapper":
        """
        > 说明
            添加消息监听器
        > 参数
            + event [type[Event] | list[type[Event]] | tuple[type[Event]]]: 事件类型
            + priority [int]: 优先级 (越小越优先, 不能小于 0) [default=5]
            + parameters_convert [type[str] | type[list] | type[dict] | None]: 消息事件中命令参数转换类型 [default=str]
        > 返回
            * wrapper [Callable]: 监听器装饰器
        """

        if priority > 0:
            parameters_convert = parameters_convert if isinstance(matcher, CommandMatcher) else None

            def wrapper(target: Callable and Awaitable):
                if asyncio.iscoroutinefunction(target):
                    ev = event
                    if ev.__class__ == list and len(list(ev)) == 1:
                        ev = ev[0]
                    
                    join = lambda e: self.listener_manager.join(listener=Listener(e, target), priority=priority, matcher=matcher, parameters_convert=parameters_convert)
                    register = lambda multi, name: self.logger.info('注册监听器%s: [blue]%s[red][%s][/red][/blue] => [light_green]Function <%s>[/light_green].' % (
                        ' (多个事件)' if multi else '', name, priority, target.__name__))

                    if ev.__class__ not in [list, tuple]:
                        register(True, ev.__name__)
                        join(ev)
                    else:
                        register(False, ' & '.join([e.__name__ for e in ev]))
                        for e in ev:
                            join(e)
                else:
                    self.logger.warning('无法注册监听器: 已忽略函数 [light_green]%s[/light_green], 因为它必须是异步函数!' % target)

            return wrapper
        else:
            self.logger.error('无法注册监听器: 优先级不能小于 0!')
