from JustBot.objects import Friend, Group
from JustBot.apis import MessageChain, Adapter, Config as config
from JustBot.utils import Logger

from typing import Type, Union
from requests import post as sync_post


class CQHTTPSenderHandler:
    def __init__(self, adapter: Adapter):
        self.adapter = adapter
        self.logger = self.adapter.logger

    def send_message(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain) -> None:
        string = message.to_code()
        data = {
            'user_id' if receiver_type == Friend else 'group_id': target_id,
            'message': string
        }
        url = f'http://{self.adapter.http_host}:{self.adapter.http_port}/send_' + (
            'private' if receiver_type == Friend else 'group') + '_msg'
        response = sync_post(url, data=data)
        d = response.json()
        retcode = d['retcode']
        if retcode != 0:
            self.logger.error(
                f'发送消息失败: 状态码错误. 返回结果: `{retcode["wording"]}`.')
        else:
            if receiver_type == Friend:
                self.logger.info(
                    f'{message._elements} -> {config.adapter_utils.get_friend_by_id(target_id).nickname}({target_id})')
