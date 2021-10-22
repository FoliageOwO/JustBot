from JustBot.events import PrivateMessageEvent, GroupMessageEvent

from typing import Union, Callable, Any


class Listener:
    """
    监听 ``Listener`` 类
    """

    def __init__(self, event: Union[PrivateMessageEvent, GroupMessageEvent],
                 target: Union[Callable, Any]) -> None:
        self.event = event
        self.target = target
