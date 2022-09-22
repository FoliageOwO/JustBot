from ...apis import AdapterConfig

from dataclasses import dataclass


@dataclass
class MiraiConfig(AdapterConfig):
    ws_host: str
    ws_port: int
    http_host: str
    http_port: int
    ws_reverse: bool = False

    enable_verify: bool = False
    verify_key: str = None

    if enable_verify and verify_key is None:
        raise ValueError('当 `enable_verify` 启用的时候 `verify_key` 不能为空!')
