from JustBot.events import PrivateMessageEvent, GroupMessageEvent

from typing import Callable, Type, Union


class Listener:
    def __init__(self, event: Type[Union[PrivateMessageEvent, GroupMessageEvent]], target: Callable):
        self.event = event
        self.target = target
