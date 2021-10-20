from JustBot.objects import Friend, Member


class PrivateMessageEvent:
    def __init__(self, message: str, message_id: int, raw_message: str, sender: Friend or Member):
        self.message = message
        self.message_id = message_id
        self.raw_message = raw_message
        self.sender = sender
        self.sender_type = type(self.sender)
        self.receiver = sender.user_id
