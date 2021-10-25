from abc import ABCMeta, abstractmethod
from typing import Any

class Element(metaclass=ABCMeta):
    """
    消息链元素 ``Element`` 抽象类
    """

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def as_display(self) -> str:
        """
        将 ``Element 对象`` 转换为 ``可读的字符串``

        >>> face = Face(174)
        >>> face.as_display()
        '[表情:174]'

        :return: 转换后的字符串
        """

        pass

    @abstractmethod
    def to_code(self) -> Any:
        """
        将 ``Element 对象`` 转换为 ``适配器特有形式``

        >>> from JustBot.adapters.cqhttp import Face as CQHttpFace
        >>> face = CQHttpFace(174)
        >>> face.to_code()
        '[CQ:face,id=174]'
        >>> from JustBot.adapters.mirai import Face as MiraiFace
        >>> face2 = MiraiFace(174)
        >>> face2.to_code()
        {'type': 'Face', 'faceId': 174}

        :return: 转换后的特有形式
        """

        pass

    @staticmethod
    @abstractmethod
    def as_code_display(code: Any) -> str:
        """
        将 ``Element 对象`` 对应的 ``适配器特有形式`` 转换为 ``可读的字符串``

        >>> from JustBot.adapters.cqhttp import Face as CQHttpFace
        >>> CQHttpFace.as_code_display('[CQ:face,id=174]')
        '[表情:174]'
        >>> from JustBot.adapters.mirai import Face as MiraiFace
        >>> MiraiFace.as_code_display({'type': 'Face', 'faceId': 174})
        '[表情:174]'

        :return: 可读的字符串
        """

        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        返回 ``Element 对象`` 的描述

        :return: ``Element 对象`` 的描述
        """

        pass
