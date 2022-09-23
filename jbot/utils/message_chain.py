from .logger import Logger
from ..apis import Element

from typing import List, Any, Union, Type


class MessageChain:
    """
    > 说明
        消息链实例类.
    > 参数
        + strings [list[str]]: CQ 码组成的列表
        + elements [list[Element]]: 元素组成的列表
        + sendable [bool]: 此消息链实例是否可以发送, 如果消息链内包括不可发送的元素则为 `False` [default=True]
    """

    def __init__(self, strings: List[str], elements: List[Element], sendable: bool = True) -> None:
        self.elements = elements
        self.result = ''.join(strings)
        self.sendable = sendable
        self.logger = Logger('Util/MessageChain')

    # TODO 使用 @overload 对方法进行重写
    @staticmethod
    def create(*elements: Element) -> 'MessageChain':
        """
        > 说明
            创建一个消息链实例.
        > 参数
            + [elements] [Element]: 包括的元素对象, 可为列表
        > 返回
            * MessageChain: 消息链实例
        """
        strings: List[str] = []
        if len(elements) == 1 and type(elements[0]) == list:
            elements = elements[0]
        for element in elements:
            strings.append(element.to_code())
        return MessageChain(strings, list(elements), False not in [element.sendable for element in elements])

    def append_elements(self, *elements: Element) -> 'MessageChain':
        self.elements.extend(list(elements))
        self.result = ''.join([element.to_code() for element in self.elements if element != None])
        self.sendable if False not in list(elements) else self.sendable
        return self

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
