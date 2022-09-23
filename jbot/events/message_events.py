from ..apis import MessageEvent
from ..contact import Group


class PrivateMessageEvent(MessageEvent):
    """
    > 说明
        私聊消息事件.
    > 参数
        + message [str]: 消息字符串
        + message_id [int]: 消息 ID
        + raw_message [str]: 源消息, 未经加工
        + message_chain [MessageChain]: 消息链对象
        + sender [Contact]: 发送者, 联系人对象
        + receiver [Contact]: 接受者, 好友对象
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class GroupMessageEvent(MessageEvent):
    """
    > 说明
        群聊消息事件.
    > 参数
        + message [str]: 消息字符串
        + message_id [int]: 消息 ID
        + raw_message [str]: 源消息, 未经加工
        + message_chain [MessageChain]: 消息链对象
        + sender [Contact]: 发送者, 联系人对象
        + receiver [Contact]: 接受者, 群对象
        + group [Group]: 群对象, 和 `receiver` 相同
    """
    def __init__(self, group: Group, **kwargs) -> None:
        super().__init__(**kwargs)
        self.group = group
