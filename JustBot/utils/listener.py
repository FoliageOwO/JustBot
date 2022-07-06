from ..apis import Event

from typing import Union, Callable, Any, Type
from dataclasses import dataclass


@dataclass
class Listener:
    """
    监听 ``Listener`` 类
    """

    event: Type[Event]
    target: Union[Callable, Any]
