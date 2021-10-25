from JustBot.apis.adapter import Adapter
from JustBot.utils import ListenerManager

from dataclasses import dataclass
from typing import AnyStr, Any


@dataclass
class Config:
    """
    配置 ``Config`` 数据类
    """
    adapter: Adapter
    nick_name: AnyStr
    listener_manager: ListenerManager
    message_handler: Any
    adapter_utils: Any

