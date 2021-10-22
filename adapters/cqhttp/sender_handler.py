from JustBot.objects import Friend, Group
from JustBot.apis import MessageChain, Config as config
from JustBot.utils import Logger
from JustBot.application import HTTP_PROTOCOL

from typing import Type, Union
from aiohttp import request


class CQHttpSenderHandler:
    def __init__(self, adapter):
        self.host = adapter.http_host
        self.port = adapter.http_port
        self.utils = adapter.utils
        self.logger = adapter.logger

    async def send_message(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain) -> None:
        string = message.to_code()
        data = {
            'user_id' if receiver_type == Friend else 'group_id': target_id,
            'message': string
        }
        url = f'{HTTP_PROTOCOL}{self.host}:{self.port}/send_' + (
            'private' if receiver_type == Friend else 'group') + '_msg'
        async with request('POST', url, data=data) as response:
            d = await response.json()
            if d['retcode'] != 0:
                self.logger.error(
                    f'发送消息失败: 状态码错误. 返回结果: `{d["wording"]}`.')
            else:
                if receiver_type == Friend:
                    nick_name = (await config.adapter_utils.get_friend_by_id(target_id)).nickname
                    self.logger.info(
                        f'{message.as_display()} -> {nick_name}({target_id})')
