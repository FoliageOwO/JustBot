from .logger import Logger
from ..apis import Element

from typing import List, Tuple, Any, Union, Type


class MessageChain:
    """
    消息链 ``MessageChain`` 类
    """

    def __init__(self, strings: List[str], elements: List[Element], sendable: bool = True) -> None:
        self.elements = elements
        self.result = ''.join(strings)
        self.sendable = sendable
        self.logger = Logger('Util/MessageChain')

    @staticmethod
    def create(*elements: Element) -> 'MessageChain':
        strings: List[str] = []
        for element in elements:
            strings.append(element.to_code())
        return MessageChain(strings, list(elements), False not in [element.sendable for element in elements])

    def append_elements(self, *elements: Element) -> None:
        self.elements.extend(list(elements))
        self.result = ''.join([element.to_code() for element in self.elements if element != None])
        self.sendable if False not in list(elements) else self.sendable

    def to_code(self) -> str:
        return self.result

    def as_display(self) -> str:
        return ''.join([element.as_display() for element in self.elements if element != None])

    def __str__(self) -> str:
        return '<MessageChain[%s]:%s>' % (len(self.elements), ','.join([element.__class__.__name__ for element in self.elements]))

    def __getitem__(self, key: Union[Type[Element], int]) -> Any:
        if key.__class__ == Element.__class__:
            return [x for x in self.elements if x.__class__ == key]
        else:
            return self.elements[key]
