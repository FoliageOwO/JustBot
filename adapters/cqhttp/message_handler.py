from JustBot.apis import ListenerManager, Config as config
from JustBot.utils import Logger
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.objects import Friend, Member, Group
from JustBot.adapters.cqhttp.elements import Utils as ElementsUtils
from JustBot.adapters.cqhttp.utils import CQHTTPUtils

import re


class CQHTTPMessageHandler:
    def __init__(self, listener_manager: ListenerManager, logger: Logger, utils: CQHTTPUtils) -> None:
        self.listener_manager = listener_manager
        self.logger = logger
        self.utils = utils

    def handle(self, data: dict) -> None:
        message_type = data['message_type']
        message = data['message']
        colored_message = message

        while True:
            search_result = re.search('(\\[)CQ:.*?(])', message)
            if search_result:
                group = search_result.group()
                element = ElementsUtils.get_element_by_code(group)
                replacement = element.as_display() if element else ElementsUtils.format_unsupported_display(group)
                message = message.replace(group, replacement)
                colored_message = colored_message.replace(group, f'[bold yellow]{replacement}[/bold yellow]')
            else:
                break

        if message_type == 'private':
            self.logger.info(f'{data["sender"]["nickname"]}({data["sender"]["user_id"]}) -> {colored_message}')
        elif message_type == 'group':
            group_name = self.utils.get_group_by_id(data['group_id']).group_name
            self.logger.info(
                f'{group_name}({data["group_id"]}) -> {data["sender"]["nickname"]}({data["sender"]["user_id"]}) -> {colored_message}')
        self.trigger(message_type, message, data)

    # TODO: 使用 data_manager 来管理 json data

    def trigger(self, message_type: str, message: str, data: dict) -> None:
        lm: ListenerManager = config.listener_manager
        if message_type == 'private':
            event = PrivateMessageEvent(message, data['message_id'], data['raw_message'],
                                        Friend(self.config.adapter_utils.get_friend_by_id(
                                            data['sender']['user_id']).nickname,
                                               data['sender']['user_id'])
                                        )
        else:
            event = GroupMessageEvent(message, data['message_id'], data['raw_message'],
                                      self.utils.get_member_by_id(data['group_id'], data['sender']['user_id']),
                                      self.utils.get_group_by_id(data['group_id'])
                                      )
        lm.execute(PrivateMessageEvent if message_type == 'private' else GroupMessageEvent, message, event)
