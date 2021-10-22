from JustBot.apis import AdapterConfig

from typing import Optional, Any, NoReturn

class MiraiConfig(AdapterConfig):
    def __init__(self,
                 ws_host: str, ws_port: int,
                 http_host: str, http_port: int,
                 enable_verify: Optional[bool] = False,
                 verify_key: Optional[str] = None,
                 ws_reverse: Optional[bool] = False) -> None:
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.http_host = http_host
        self.http_port = http_port
        self.ws_reverse = ws_reverse

        self.enable_verify = enable_verify
        self.verify_key = verify_key

        if self.enable_verify and self.verify_key is None:
            raise ValueError(
                f'当 `enable_verify` 启用的时候 `verify_key` 不能为空!')
