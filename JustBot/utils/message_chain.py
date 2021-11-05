from ..apis import Element

from typing import List, Any


class MessageChain:
    """
    消息链 ``MessageChain`` 类
    """

    def __init__(self, strings: List[str], elements: List[Element] = None) -> None:
        self.elements = elements
        self.result = ''.join(strings)

    @staticmethod
    def create(elements: List[Element]) -> Any:
        strings: List[str] = []
        for i in elements:
            strings.append(i.to_code())
        return MessageChain(strings, elements)

    def to_code(self) -> str:
        return self.result

    def as_display(self) -> str:
        return ''.join([element.as_display() for element in self.elements])
