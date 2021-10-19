class Friend:
    def __init__(self, nickname: str, user_id: int, remark: str = None):
        self.nickname = nickname
        self.user_id = user_id
        self.remark = remark if remark else self.nickname
