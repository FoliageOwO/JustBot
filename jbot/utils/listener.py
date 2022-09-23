from ..apis import Event

from typing import Union, Callable, Any, Type
from dataclasses import dataclass


@dataclass
class Listener:
    """
    > 说明
        监听器类, 通常为入口程序的函数包装而来.
    """

    event: Type[Event]
    target: Union[Callable, Any]
