from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.matchers import KeywordsMatcher, CommandMatcher
from JustBot.utils.logger import Logger
from JustBot.utils.listener import Listener

from typing import Type, Union, NoReturn

import asyncio


class ListenerManager:
    """
    监听管理器 ``ListenerManager`` 类
    """

    def __init__(self) -> None:
        self.l = {}
        self.logger = Logger('Util/ListenerManager')

    def join(self, listener: Listener, priority: int = 1,
             matcher: Union[KeywordsMatcher, CommandMatcher] = None,
             parameters_convert: Type[Union[str, list, dict, None]] = str) -> NoReturn:
        lists: list = [] if not str(priority) in self.l.keys() else self.l[str(priority)]
        lists.append({'listener': listener,
                      'matcher': matcher,
                      'parameters_convert': parameters_convert})
        self.l[str(priority)] = lists
        new_l = {}
        for i in sorted(self.l.items(), reverse=True):
            new_l[i[0]] = i[1]
        self.l = new_l

    async def execute(self, event_type: Type[Union[PrivateMessageEvent, GroupMessageEvent]],
                      message: str, event: Union[PrivateMessageEvent, GroupMessageEvent]) -> NoReturn:
        for priority in self.l.keys():
            for listener_obj in self.l[priority]:
                listener = listener_obj['listener']
                if listener.event == event_type:
                    matcher = listener_obj['matcher']

                    async def run_target():
                        await self.__run_target(listener, event, message,
                                                isinstance(matcher, CommandMatcher),
                                                listener_obj['parameters_convert'])

                    if matcher:
                        if matcher.match(message):
                            await run_target()
                    else:
                        await run_target()

    async def __run_target(self, listener: Listener, event: Union[PrivateMessageEvent, GroupMessageEvent], message: str,
                           is_command_matcher: bool, parameters_convert: Type[Union[str, list, dict, None]]) -> NoReturn:
        run_mapping = {
            (lambda: listener.target(event=event)): False,
            (lambda: listener.target(event=event, message=message)): False,
            (lambda: listener.target(event=event,
                                     command=message.split()[0] if is_command_matcher else None,
                                     parameters=self.__get_parameters(message, parameters_convert)
                                     if is_command_matcher else None)): False
        }
        for target in run_mapping.keys():
            try:
                await target()
                break
            except TypeError:
                run_mapping[target] = True
                continue

        if list(set(run_mapping.values())) == [True]:
            self.logger.warning(f'无法回调函数 [light_green]{listener.target}[/light_green], 因为它的定义不规范!')

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
