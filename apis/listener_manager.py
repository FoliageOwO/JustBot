from JustBot.apis import Listener
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.matchers import KeywordsMatcher, CommandMatcher
from JustBot.utils import Logger

from typing import Type, Union

import asyncio


class ListenerManager:
    def __init__(self) -> None:
        self.l = {}
        self.logger = Logger('Api/ListenerManager')

    def join(self, listener: Listener, priority: int = 1,
             matcher: Union[KeywordsMatcher, CommandMatcher] = None) -> None:
        lists: list = [] if not str(priority) in self.l.keys() else self.l[str(priority)]
        lists.append({'listener': listener,
                      'matcher': matcher})
        self.l[str(priority)] = lists
        new_l = {}
        for i in sorted(self.l.items(), reverse=True):
            new_l[i[0]] = i[1]
        self.l = new_l

    def execute(self, event_type: Type[Union[PrivateMessageEvent, GroupMessageEvent]],
                message: str, event: Union[PrivateMessageEvent, GroupMessageEvent]) -> None:
        for priority in self.l.keys():
            for listener_obj in self.l[priority]:
                listener = listener_obj['listener']
                if listener.event == event_type:
                    matcher = listener_obj['matcher']
                    is_command_matcher = isinstance(matcher, CommandMatcher)

                    def run():
                        mapping = {(lambda: asyncio.run(listener.target(event=event))): False,
                                   (lambda: asyncio.run(listener.target(event=event, message=message))): False,
                                   (lambda: asyncio.run(listener.target(event=event,
                                                                        command=message.split()[
                                                                            0] if is_command_matcher else None,
                                                                        parameters=message.split()[
                                                                                   1:] if is_command_matcher else None))): False}
                        for target_run in mapping.keys():
                            try:
                                target_run()
                                break
                            except TypeError as e:
                                mapping[target_run] = True
                                continue

                        if list(set(mapping.values())) == [True]:
                            self.logger.warning(f'无法回调函数 [light_green]{listener.target}[/light_green], 因为它的定义不规范!')

                    if matcher:
                        if matcher.match(message):
                            run()
                    else:
                        run()
