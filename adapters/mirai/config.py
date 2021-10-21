from JustBot.apis.session_config import SessionConfig


class MiraiConfig(SessionConfig):
    def __init__(self,
                 ws_host: str, ws_port: int,
                 http_host: str, http_port: int, session_key: str,
                 ws_reverse: bool = False) -> None:
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.http_host = http_host
        self.http_port = http_port
        self.session_key = session_key
        self.ws_reverse = ws_reverse
