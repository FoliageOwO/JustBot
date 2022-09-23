from .logger import Logger
from .listener import Listener
from ..apis import MessageEvent, NoticeEvent, Matcher
from ..matchers import CommandMatcher
from ..utils import MessageChain, PriorityQueue
from ..utils.nlp import NLP

from typing import Awaitable, Type, Union, Any


class ListenerManager:
    """
    > 说明
        监听器管理类
    """

    def __init__(self) -> None:
        self.listeners = dict()
        self.pq = PriorityQueue()
        self.nlp = NLP()
        self.logger = Logger('Util/ListenerManager')

    def join(self, listener: Listener, priority: int = 5) -> None:
        self.pq.join(dict(listener=listener), priority)
    
    def __set_data(self, function: Awaitable, key: str, value: Any) -> bool:
        flag = False
        for data in self.pq.items:
            if data['listener'].target == function:
                data[key] = value
                flag = True
        return flag
    
    def set_matcher(self, function: Awaitable, matcher: Matcher) -> bool:
        return self.__set_data(function, 'matcher', matcher)
    
    def set_param_convert(self, function: Awaitable, param_convert: Type[Union[str, list, dict, None]]) -> bool:
        return self.__set_data(function, 'convert', param_convert)
    
    def set_role(self, function: Awaitable, role: dict) -> bool:
        role_list = role['role']
        mapping = {
            'Role': lambda: [role_list],
            'list': lambda: [*role_list],
            'tuple': lambda: [*role_list]
        }
        get_role = mapping.get(role_list.__class__.__name__, None)
        return self.__set_data(function, 'role', {'role': get_role(), 'todo': role['todo']}) if get_role else False

    def set_nlp(self, function: Awaitable, nlp: dict) -> bool:
        self.nlp.add_handler(function=function, keywords=nlp['keywords'], params=nlp['params'], c=nlp['c'])
        return self.__set_data(function, 'nlp', nlp)

    async def handle_message(self, event_type: Type[MessageEvent], message: str, message_chain: MessageChain, event: MessageEvent) -> None:
        for data in self.pq:
            listener: Listener = data['listener']
            matcher: Matcher = data.get('matcher', None)
            convert: Any = data.get('convert', None)
            role: dict = data.get('role', {'role': [], 'todo': lambda: None})
            nlp: dict = data.get('nlp', None)
            is_command_matcher = isinstance(matcher, CommandMatcher)

            nlp_params, nlp_flag, nlp_command = await self.nlp.handle(message_chain=message_chain, command=matcher.cmd if is_command_matcher else '') if nlp else ({}, False)
            trigger = lambda: self.trigger(listener, event, message_chain, message, is_command_matcher, convert, matcher, nlp_flag, nlp_params, nlp_command)
            if listener.event == event_type:
                role_list = [i.value for i in role['role']]
                if role_list != [] and event.__class__.__name__ == 'GroupMessageEvent':
                    if event.sender.role in role_list:
                        await trigger()
                    else:
                        todo = role['todo']
                        (await todo(event=event, message=message, message_chain=message_chain)) if todo else None
                else:
                    await trigger()
                    
        self.pq.rejoin()
    
    async def trigger(self, listener, event, message_chain, message, is_command_matcher, convert, matcher, nlp_flag, nlp_params, nlp_command):
        params = nlp_params if nlp_flag else (self.__get_parameters(message, convert) if is_command_matcher else None)
        execute_function = lambda: listener.target(
            event=event, message=message, message_chain=message_chain,
            command=nlp_command if nlp_flag else (message.split()[0] if is_command_matcher else None),
            **params)
        await execute_function() \
            if not matcher else \
            (await execute_function() if matcher.match(message_chain) or nlp_flag else None)
    
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
