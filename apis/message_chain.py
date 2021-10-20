from JustBot.apis.element import Element

from typing import List


class MessageChain:
    def __new__(cls, strings: List[str]):
        cls._elements: List[Element]
        cls._strings = strings
        cls._result = ''
        for i in strings:
            cls._result += i
        return cls

    @classmethod
    def create(cls, elements: List[Element]):
        cls._elements = elements
        strings: List[str] = []
        for i in elements:
            strings.append(i.to_code())
        return cls(strings)

    @classmethod
    def to_code(cls) -> str:
        return cls._result
