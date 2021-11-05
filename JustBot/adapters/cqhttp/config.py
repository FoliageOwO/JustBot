from ...apis import AdapterConfig

from dataclasses import dataclass


@dataclass
class CQHttpConfig(AdapterConfig):
    ws_host: str
    ws_port: int
    http_host: str
    http_port: int
    ws_reverse: bool = False
