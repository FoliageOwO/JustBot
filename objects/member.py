from JustBot.objects import Group


class Member:
    def __init__(self,
                 group: Group, nickname: str, user_id: int,
                 role: str = None, last_sent_time: int = None,
                 join_time: int = None) -> None:
        self.group = group
        self.nickname = nickname
        self.user_id = user_id
        self.role = role
        self.last_sent_time = last_sent_time
        self.join_time = join_time
