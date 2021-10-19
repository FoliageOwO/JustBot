from JustBot.apis import ListenerManager, Config as config
from JustBot.utils.logger import Logger
from JustBot.exceptions import InternalError
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.objects import Friend, Member, Group

from requests import get as sync_get


class MessageHandler:
    def __init__(self, listener_manager: ListenerManager) -> None:
        self.listener_manager = listener_manager
        self.logger = Logger('Handler/Message')

    def handle(self, data: dict) -> None:
        # __import__('rich').print(data) -> DEBUG
        message_type = data['message_type']
        if message_type == 'private':
            self.logger.info(f'{data["sender"]["nickname"]}({data["sender"]["user_id"]}) -> {data["message"]}')
        elif message_type == 'group':
            group_name = None
            for i in sync_get(f'{config.adapter.http_host}:{config.adapter.http_port}/get_group_list').json()['data']:
                if i['group_id'] == data['group_id']:
                    group_name = i['group_name']
            if not group_name:
                InternalError(
                    '内部错误: 无法获取群聊名称!')
            else:
                self.logger.info(
                    f'{group_name}({data["group_id"]}) > {data["sender"]["nickname"]}({data["sender"]["user_id"]}) -> {data["message"]}')
        self.trigger(data['message_type'], data['raw_message'], data)

    @staticmethod
    def trigger(message_type: str, message: str, data: dict) -> None:
        lm: ListenerManager = config.listener_manager
        lm.execute(PrivateMessageEvent if message_type == 'private' else GroupMessageEvent, message,
                   PrivateMessageEvent(message, data['message_id'], data['raw_message'],
                                       Friend(config.adapter_utils.get_friend_by_id(data['sender']['user_id']).user_id,
                                              data['sender']['user_id'])
                                       if message_type == 'private' else config.adapter_utils.get_member_by_id(
                                           data['group_id'], data['sender']['user_id'])))
