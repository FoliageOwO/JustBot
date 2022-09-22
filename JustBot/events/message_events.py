from ..apis import MessageEvent
from ..contact import Group


class PrivateMessageEvent(MessageEvent):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class GroupMessageEvent(MessageEvent):
    def __init__(self, group: Group, **kwargs) -> None:
        super().__init__(**kwargs)
        self.group = group
