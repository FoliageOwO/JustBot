from .logger import Logger
from .listener import Listener
from ..apis import MessageEvent, NoticeEvent
from ..matchers import KeywordMatcher, CommandMatcher
from ..utils import MessageChain, PriorityQueue

from typing import Type, Union, Any


class ListenerManager:
    """
    > 说明
        监听器管理类
    """

    def __init__(self) -> None:
        self.listeners = dict()
        self.pq = PriorityQueue()
        self.logger = Logger('Util/ListenerManager')

    def join(self, listener: Listener, priority: int = 5,
             matcher: Union[KeywordMatcher, CommandMatcher] = None,
             parameters_convert: Type[Union[str, list, dict, None]] = str) -> None:
        """
        > 说明
            向监听器管理添加新的监听器.
        > 参数
            + listener [Listener]: 监听器
            + priority [int]: 优先级 (越小越优先, 不能小于 0) [default=5]
            + matcher [KeywordMatcher | CommandMatcher]: 匹配器 [可选]
            + parameters_convert [type[str] | type[list] | type[dict] | None]: 参数转换类型 [default=str]
        """

        self.pq.join(dict(listener=listener, matcher=matcher, convert=parameters_convert), priority)

    async def handle_message(self, event_type: Type[MessageEvent], message: str, message_chain: MessageChain, event: MessageEvent) -> None:
        for data in self.pq:
            listener: Listener = data['listener']
            matcher: Union[KeywordMatcher, CommandMatcher] = data['matcher']
            convert: Any = data['convert']
            is_command_matcher = isinstance(matcher, CommandMatcher)

            if listener.event == event_type:
                execute_function = lambda: listener.target(
                    event=event, message=message, message_chain=message_chain,
                    command=message.split()[0] if is_command_matcher else None,
                    parameters=self.__get_parameters(message, convert) if is_command_matcher else None)
                await execute_function() \
                    if not matcher else \
                    (await execute_function() if matcher.match(message_chain) else None)
        self.pq.rejoin()
    
    async def handle_event(self, event_type: Type[NoticeEvent], code:str, event: NoticeEvent) -> None:
        for data in self.pq:
            listener: Listener = data['listener']
            
            if listener.event == event_type:
                execute_funtion = lambda: listener.target(event=event, code=code)
                await execute_funtion()
        self.pq.rejoin()

    # TODO: 优化 parameters 获取
    @staticmethod
    def __get_parameters(message: str, parameters_convert: Type[Union[str, list, dict, None]]) -> dict:
        def __get_multi_parameters() -> list or dict:
            _dict = {}
            _list = []
            for i in message.split()[1:]:
                k = i.split('=')
                if len(k) == 2:
                    _dict[k[0]] = k[1]
                else:
                    _list.append(k[0])
            return [_dict, _list] if _list else _dict

        return {
            str: ' '.join(message.split()[1:]),
            list: message.split()[1:],
            dict: __get_multi_parameters(),
            None: None
        }[parameters_convert]
