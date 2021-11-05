from dataclasses import dataclass


@dataclass
class Friend:
    nickname: str
    user_id: int
    remark: int = None
