from ..objects import Group

from dataclasses import dataclass


@dataclass
class Member:
    group: Group
    nickname: str
    user_id: int
    role: str = None
    last_sent_time: int = None
    join_time: int = None
