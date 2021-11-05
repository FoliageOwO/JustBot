from dataclasses import dataclass


@dataclass
class Group:
    group_name: str
    group_id: int
    max_member: int = None
    member_count: int = None
    group_level: int = None
    group_create_time: int = None
    group_memo: str = None
