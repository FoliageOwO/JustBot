from JustBot.apis import Listener
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.exceptions import InvalidFunctionType
from JustBot.matchers import KeywordsMatcher, CommandMatcher

from typing import Type, Union

import asyncio


class ListenerManager:
    def __init__(self) -> None:
        self.l = {}

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

                    def run():
                        try:
                            asyncio.run(listener.target(event=event))
                        except TypeError:
                            InvalidFunctionType(
                                '请将函数更改为 `异步 (async) 函数` 而非 `同步 (sync) 函数`!')

                    if matcher:
                        if matcher.match(message):
                            run()
                    else:
                        run()
