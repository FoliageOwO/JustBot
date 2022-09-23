from ..apis import Contact, Element

from abc import ABCMeta, abstractmethod
from typing import Union, List, Tuple


class Event:
    """
    > 说明
        事件基类.
    """
    
    pass


class MessageEvent(Event, metaclass=ABCMeta):
    """
    > 说明
        消息事件基类.
    > 参数
        + message [str]: 消息字符串
        + message_id [int]: 消息 ID
        + raw_message [str]: 源消息, 未经加工
        + message_chain [MessageChain]: 消息链对象
        + sender [Contact]: 发送者, 联系人对象
        + receiver [Contact]: 接受者, 如果为私聊则是好友对象, 反之为群对象
    """
    
    @abstractmethod
    def __init__(self, message: str, message_id: int, raw_message: str,
                 message_chain: 'MessageChain', sender: Contact, receiver: Contact,
                 app: 'BotApplication',
                 *args, **kwargs) -> None:
        self.message = message
        self.message_id = message_id
        self.raw_message = raw_message
        self.message_chain = message_chain
        self.sender = sender
        self.receiver = receiver
        self._app = app
    
    """
    > 说明
        快速对该消息对象进行回复.
    > 参数
        + message [MessageChain | Element | str]: 消息链或元素或纯文本 (纯文本会自动转为 ``Plain``, 元素会自动转化为 ``MessageChain``)
        + with_reply [bool]: 是否带上回复 ``Reply`` 当前消息链 [default=True]
    """
    async def reply(self,
                    message: Union['MessageChain', Union[Element, List[Element], Tuple[Element]], str],
                    with_reply: bool = True) -> None:
        reply = self._app.adapter_utils.get_element('reply')(self.message_id)
        plain = self._app.adapter_utils.get_element('plain')
        mapping = {
            'MessageChain': lambda: message.append_elements(reply) if with_reply else message,
            'Element': lambda: [reply, message] if with_reply else [message],
            'list': lambda: [reply] + message if with_reply else message,
            'tuple': lambda: ((reply,) + message) if with_reply else message,
            'str': lambda: [reply, plain(message)] if with_reply else [plain(message)]
        }
        t = message.__class__.__name__
        await self._app.send_msg(self.receiver, mapping[t]() if t in mapping else None)

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
