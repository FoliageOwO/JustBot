from .adapter import Adapter
from ..utils.nlp import NLP

from dataclasses import dataclass
from typing import AnyStr, Any


@dataclass
class Config:
    """
    > 说明
        配置基类
    """
    adapter: Adapter
    nick_name: AnyStr
    listener_manager: 'ListenerManager'
    message_handler: Any
    adapter_utils: Any
    application: 'BotApplication'
