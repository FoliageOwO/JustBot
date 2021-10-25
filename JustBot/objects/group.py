class Group:
    def __init__(self,
                 group_name: str, group_id: int,
                 max_member: int = 0, member_count: int = 0,
                 group_level: int = 0, group_create_time: int = 0,
                 group_memo: str = "") -> None:
        self.group_name = group_name
        self.group_id = group_id
        self.max_member = max_member
        self.member_count = member_count
        self.group_level = group_level
        self.group_create_time = group_create_time
        self.group_memo = group_memo
