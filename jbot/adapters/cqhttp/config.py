from ...apis import AdapterConfig

from dataclasses import dataclass


@dataclass
class CQHTTPConfig(AdapterConfig):
    """
    > 说明
        CQHTTP 适配器配置类.
    > 参数
        * ws_host [str]: WebSocket 主机地址
        * ws_port [int]: WebSocket 主机端口
        * http_host [str]: HTTP 主机地址
        * http_port [int]: HTTP 主机端口
        * ws_reverse [bool]: 是否为反向 WebSocket [default=False]
    """
    ws_host: str
    ws_port: int
    http_host: str
    http_port: int
    ws_reverse: bool = False
