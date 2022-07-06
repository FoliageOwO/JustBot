from dataclasses import dataclass


@dataclass
class Friend:
    user_id: int
    nickname: str = None
    remark: int = None
