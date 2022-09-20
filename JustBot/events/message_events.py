from ..apis import Event
from ..contact import Friend, Group, Member
from ..utils import MessageChain

from dataclasses import dataclass


@dataclass
class PrivateMessageEvent(Event):
    message: str
    message_id: int
    raw_message: str
    message_chain: MessageChain
    sender: Friend or Member
    receiver: Friend or Member


@dataclass
class GroupMessageEvent(Event):
    message: str
    message_id: int
    raw_message: str
    message_chain: MessageChain
    sender: Member
    group: Group
    receiver: Group
