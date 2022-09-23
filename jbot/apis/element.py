from abc import ABCMeta, abstractmethod
from typing import Any

class Element(metaclass=ABCMeta):
    """
    > 说明
        消息链元素基类.
    """

    __type__: str
    __code__: str

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def as_display(self) -> str:
        """
        > 说明
            将 `Element 对象` 转换为 `易读字符串`.
        > 返回
            * str: 转换后的字符串
        > 示例
            >>> Foo(bar=1).as_display()
            '[Foo:1]'
        """

        ...

    @abstractmethod
    def to_code(self) -> Any:
        """
        > 说明
            将 ``Element 对象`` 转换为 ``适配器的特有形式``.
        > 返回
            * Any: 转换后的形式
        > 示例
            >>> CQ_Foo(bar=1).to_code()
            '[CQ:foo,bar=1]'
            >>> MIRAI_Foo(bar=1).to_code()
            {'type': 'foo', 'bar': 1}
        """

        ...

    @staticmethod
    @abstractmethod
    def as_code_display(code: Any) -> str:
        """
        > 说明
            将 ``Element 对象`` 对应的 ``适配器特有形式`` 转换为 ` 易读字符串``.
        > 参数
            * code [Any]: 适配器特有形式
        > 返回
            * str: 易读字符串
        """

        ...

    @abstractmethod
    def __str__(self) -> str:
        """
        > 说明
            返回 ``Element 对象`` 的描述.
        > 返回
            * str: 描述
        """

        ...

    @property
    def sendable(self) -> bool:
        return not self.__class__.__name__.startswith('_')
