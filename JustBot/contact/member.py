from ..apis import Contact
from ..contact import Group

from dataclasses import dataclass


@dataclass
class Member(Contact):
    group: Group
    user_id: int
    group_id: int
    nickname: str = None
    role: str = None
    last_sent_time: int = None
    join_time: int = None
