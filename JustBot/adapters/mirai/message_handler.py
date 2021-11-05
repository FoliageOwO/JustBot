from .elements import Utils as ElementsUtils
from ...application import CONFIG
from ...objects import Friend, Group, Member
from ...events import PrivateMessageEvent, GroupMessageEvent
from ...utils import ListenerManager

from typing import NoReturn
from dataclasses import dataclass

import re


@dataclass
class Data:
    pass


d = Data()


class MiraiMessageHandler:
    def __init__(self, adapter) -> None:
        self.listener_manager = CONFIG.listener_manager
        self.logger = adapter.logger
        self.utils = adapter.utils

    async def handle(self, data: dict) -> NoReturn:
        for k in data.keys():
            v = data[k]
            if type(v) is not dict:
                d.__setattr__(k, data[k])
            else:
                for kk in v.keys():
                    d.__setattr__(kk, v[kk])

        d.message = ''
        d.colored_message = ''
        for i in d.messageChain:
            element = ElementsUtils.get_element_by_code(i)
            if element:
                d.message += element.as_display()
                d.colored_message += element.as_display()
            else:
                d.message += ElementsUtils.format_unsupported_display(i)
                d.colored_message = ElementsUtils.format_unsupported_display(i, True)

        if d.type == 'FriendMessage':
            self.logger.info(f'{d.nickname}({d.id}) -> {d.colored_message}')
        elif d.type == 'GroupMessage':
            self.logger.info(
                f'{d.group["name"]}({d.group["id"]}) -> {d.memberName}({d.id}) -> {d.colored_message}')
        await self.trigger(d.type, d.message)

    async def trigger(self, message_type: str, message: str) -> NoReturn:
        lm: ListenerManager = CONFIG.listener_manager
        if message_type == 'FriendMessage':
            event = PrivateMessageEvent(message, d.messageChain[0]['id'], message,
                                        Friend(d.nickname, d.id))
        elif message_type == 'GroupMessage':
            member = Member(Group(d.group['name'], d.group['id']), d.memberName, d.id)
            event = GroupMessageEvent(message, d.messageChain[0]['id'], message, member, member.group)
        else:
            event = None
        await lm.execute(PrivateMessageEvent if message_type == 'FriendMessage'
                         else (GroupMessageEvent if message_type == 'GroupMessage' else None), message, event)

