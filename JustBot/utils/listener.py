from ..apis import Event

from typing import Union, Callable, Any
from dataclasses import dataclass


@dataclass
class Listener:
    """
    监听 ``Listener`` 类
    """

    event: Event
    target: Union[Callable, Any]
