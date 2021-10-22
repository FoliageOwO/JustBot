from abc import ABCMeta, abstractmethod


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
    def to_code(self) -> str:
        """
        将 ``Element 对象`` 转换为 ``CQ 码``

        >>> face = Face(174)
        >>> face.to_code()
        '[CQ:face,id=174]'

        :return: 转换后的 CQ 码
        """

        pass

    @staticmethod
    @abstractmethod
    def as_code_display(code: str) -> str:
        """
        将 ``Element 对象`` 对应的 ``CQ 码`` 转换为 ``可读的字符串``

        >>> Face.as_code_display('[CQ:face,id=174]')
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
