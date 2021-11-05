from ...objects import Friend, Group
from ...utils import MessageChain
from ...application import HTTP_PROTOCOL, CONFIG

from typing import Type, Union, NoReturn
from aiohttp import request


class CQHttpSenderHandler:
    def __init__(self, adapter) -> None:
        self.host = adapter.http_host
        self.port = adapter.http_port
        self.utils = adapter.utils
        self.logger = adapter.logger

    # TODO: 将 SenderHandler 合并到 Adapter 中
    async def send_message(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain) -> NoReturn:
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
                    nick_name = (await CONFIG.adapter_utils.get_friend_by_id(target_id)).nickname
                    self.logger.info(
                        f'{message.as_display()} -> {nick_name}({target_id})')
