from dataclasses import dataclass


@dataclass
class Group:
    group_id: int
    group_name: str = None
    max_member: int = None
    member_count: int = None
    group_level: int = None
    group_create_time: int = None
