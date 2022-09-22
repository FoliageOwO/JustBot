from ..apis import Contact

from dataclasses import dataclass


@dataclass
class Friend(Contact):
    user_id: int
    nickname: str = None
    remark: int = None
