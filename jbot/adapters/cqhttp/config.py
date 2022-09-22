from ...apis import AdapterConfig

from dataclasses import dataclass


@dataclass
class CQHTTPConfig(AdapterConfig):
    """
    > 说明
        CQHTTP 适配器配置类.
    > 参数
        * ws_host [str]: WebSocket 主机地址 [default='127.0.0.1']
        * ws_port [int]: WebSocket 主机端口 [default=6700]
        * http_host [str]: HTTP 主机地址 [default='127.0.0.1']
        * http_port [int]: HTTP 主机端口 [default=5700]
        * ws_reverse [bool]: 是否为反向 WebSocket [default=False]
    """
    ws_host: str = '127.0.0.1'
    ws_port: int = 6700
    http_host: str = '127.0.0.1'
    http_port: int = 5700
    ws_reverse: bool = False
