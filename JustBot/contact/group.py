from ..apis import Contact

from dataclasses import dataclass


@dataclass
class Group(Contact):
    group_id: int
    group_name: str = None
    max_member: int = None
    member_count: int = None
    group_level: int = None
    group_create_time: int = None
