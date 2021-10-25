from JustBot.utils import ListenerManager
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.objects import Friend, Member, Group
from JustBot.adapters.cqhttp.elements import Utils as ElementsUtils
from JustBot.application import CONFIG

from dataclasses import dataclass
from typing import NoReturn

import re


@dataclass
class Data:
    pass


d = Data()


class CQHttpMessageHandler:
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
        d.colored_message = d.message

        while True:
            search_result = re.search('(\\[)CQ:.*?(])', d.message)
            if search_result:
                group = search_result.group()
                element = ElementsUtils.get_element_by_code(group)
                replacement = ElementsUtils.as_colored_display(
                    element) if element else ElementsUtils.format_unsupported_display(group, colored=True)
                d.message = d.message.replace(group, replacement)
                d.colored_message = d.colored_message.replace(group, f'[bold yellow]{replacement}[/bold yellow]')
            else:
                break

        if d.message_type == 'private':
            self.logger.info(f'{d.nickname}({d.user_id}) -> {d.colored_message}')
        elif d.message_type == 'group':
            group_name = (await self.utils.get_group_by_id(d.group_id)).group_name
            self.logger.info(
                f'{group_name}({d.group_id}) -> {d.nickname}({d.user_id}) -> {d.colored_message}')
        await self.trigger(d.message_type, d.message)

    async def trigger(self, message_type: str, message: str) -> NoReturn:
        lm: ListenerManager = CONFIG.listener_manager
        if message_type == 'private':
            event = PrivateMessageEvent(message, d.message_id, d.raw_message,
                                        Friend((await self.utils.get_friend_by_id(d.user_id)).nickname, d.user_id))
        else:
            event = GroupMessageEvent(message, d.message_id, d.raw_message,
                                      await self.utils.get_member_by_id(d.group_id, d.user_id),
                                      await self.utils.get_group_by_id(d.group_id))
        await lm.execute(PrivateMessageEvent if message_type == 'private' else GroupMessageEvent, message, event)
