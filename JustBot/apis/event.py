from abc import ABCMeta, abstractmethod


class Event:
    """
    事件 ``Event`` 基类.
    """
    
    pass


class NoticeEvent(Event, metaclass=ABCMeta):
    """
    通知事件.
    """
    
    __type__: str
    __code__: str
    
    time: int
    self_id: int
    post_type: str
    notice_type: str
    
    @abstractmethod
    def __init__(self, time: int, self_id: int, post_type: str, notice_type: str, *args, **kwargs) -> None:
        ...
    
    @abstractmethod
    def as_display(self) -> str:
        """
        > 说明
            将 ``NoticeEvent 对象`` 转换为 ``易读字符串``.
        > 返回
            * str: 转换后的字符串
        > 示例
            >>> group_ban = GroupBan(sub_type='ban', group_id=114514, operator_id=1919810, user_id=23333, duration=1)
            >>> group_ban.as_display()
            '群成员 23333 在群 114514 被 1919810 禁言 1 秒'
        """

        ...
