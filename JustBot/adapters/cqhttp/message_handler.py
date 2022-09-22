from .elements import Utils as ElementsUtils
from ...utils import ListenerManager, MessageChain
from ...events import PrivateMessageEvent, GroupMessageEvent
from ...contact import Friend
from ... import CONFIG

from dataclasses import dataclass
from typing import Tuple

import re


@dataclass
class Data:
    pass


d = Data()


class CQHTTPMessageHandler:
    """
    > 说明
        CQHTTP 消息处理器.
    > 参数
        + adapter [Adapter]: 适配器对象
    """
    def __init__(self, adapter: 'Adapter') -> None:
        self.listener_manager = CONFIG.listener_manager
        self.logger = adapter.logger
        self.utils = adapter.utils

    @staticmethod
    def format_message_chain(code_string: str) -> Tuple:
        """
        > 说明
            将消息转换为 MessageChain 对象.
        > 参数
            + code_string [str]: 消息内容
        """
        chain = MessageChain.create()
        replaced_string = code_string
        colored_message = code_string
        while True:
            search_result = re.search('(\\[)CQ:.*?(])', code_string)
            if search_result:
                group = search_result.group()
                element = ElementsUtils.get_element_by_code(group)
                chain.append_elements(element)
                replaced_string = replaced_string.replace(group, '')
                replacement = ElementsUtils.as_colored_display(
                    element) if element else ElementsUtils.format_unsupported_display(group)
                code_string = code_string.replace(group, replacement)
                colored_message = colored_message.replace(group, '[bold yellow]%s[/bold yellow]' % replacement)
            else:
                break
        if replaced_string:
            chain.append_elements(ElementsUtils.get_element_by_code(replaced_string))
        return chain, chain.as_display(), colored_message

    async def handle(self, data: dict) -> None:
        for k in data.keys():
            v = data[k]
            if type(v) is not dict:
                d.__setattr__(k, data[k])
            else:
                for kk in v.keys():
                    d.__setattr__(kk, v[kk])

        d.message_chain, d.message, d.colored_message = CQHTTPMessageHandler.format_message_chain(d.message)
        d.colored_message = d.colored_message if d.colored_message else '[未知消息]'
        if d.message_type == 'private':
            self.logger.info('%s(%s) [green]->[/green] %s' % (d.nickname, d.user_id, d.colored_message))
        elif d.message_type == 'group':
            self.logger.info('%s(%s) [%s(%s)] [green]->[/green] %s' % ((await self.utils.get_group_by_id(d.group_id)).group_name, d.group_id, d.nickname, d.user_id, d.colored_message))
        await self.trigger()

    async def trigger(self) -> None:
        lm: ListenerManager = CONFIG.listener_manager
        if d.message_type == 'private':
            friend = Friend(d.user_id)
            event = PrivateMessageEvent(message=d.message, message_id=d.message_id, raw_message=d.raw_message, message_chain=d.message_chain, sender=friend, receiver=friend)
        else:
            group = await self.utils.get_group_by_id(d.group_id)
            event = GroupMessageEvent(group=group,
                                      message=d.message, message_id=d.message_id, raw_message=d.raw_message, message_chain=d.message_chain,
                                      sender=await self.utils.get_member_by_id(d.group_id, d.user_id), receiver=group)
        await lm.handle_message(PrivateMessageEvent if d.message_type == 'private' else GroupMessageEvent,
                         d.message, d.message_chain, event)
