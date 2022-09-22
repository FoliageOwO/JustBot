from ..apis import Contact

from abc import ABCMeta, abstractmethod


class Event:
    """
    > 说明
        事件 ``Event`` 基类.
    """
    
    pass


class MessageEvent(Event, metaclass=ABCMeta):
    """
    > 说明
        消息事件.
    > 参数
        + message [str]: 消息字符串
        + message_id [int]: 消息 ID
        + raw_message [str]: 源消息, 未经加工
        + message_chain [MessageChain]: 消息链对象
        + sender [Contact]: 发送者, 联系人对象
        + receiver [Contact]: 接受者, 如果为私聊则是用户对象, 反之为群对象
    """
    
    @abstractmethod
    def __init__(self, message: str, message_id: int, raw_message: str,
                 message_chain: 'MessageChain', sender: Contact, receiver: Contact,
                 *args, **kwargs) -> None:
        self.message = message
        self.message_id = message_id
        self.raw_message = raw_message
        self.message_chain = message_chain
        self.sender = sender
        self.receiver = receiver


class NoticeEvent(Event, metaclass=ABCMeta):
    """
    > 说明
        通知事件.
    > 参数
        + time [int]: 事件发生的时间戳
        + self_id [int]: 始终为机器人本身 QQ 号
        + post_type [str]: 始终为 `notice`
        + notice_type [str]: 通知时间的类型, 和 `NoticeEvent#__code__` 相同
    """
    
    __type__: str
    __code__: str

    @abstractmethod
    def __init__(self, time: int, self_id: int, post_type: str, notice_type: str, *args, **kwargs) -> None:
        self.time = time
        self.self_id = self_id
        self.post_type = post_type
        self.notice_type = notice_type
    
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
