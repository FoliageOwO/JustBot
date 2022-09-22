from .config import MiraiConfig
from .message_handler import MiraiMessageHandler
from .utils import MiraiUtils
from ...apis import Adapter
from ...utils import Logger, MessageChain
from ...contact import Friend, Group
from ... import HTTP_PROTOCOL, WS_PROTOCOL

from aiohttp import request, ClientConnectorError
from typing import Coroutine, Type, Union
from websockets import connect as ws_connect

import asyncio
import json


class MiraiAdapter(Adapter):
    def __init__(self, config: MiraiConfig) -> None:
        self.name = 'Mirai'
        self.ws_host = config.ws_host
        self.ws_port = config.ws_port
        self.http_host = config.http_host
        self.http_port = config.http_port
        self.ws_reverse = config.ws_reverse

        # TODO: 添加 single_mode 与 session_key
        self.enable_verify = config.enable_verify
        self.verify_key = config.verify_key

        self.logger = Logger('Adapter/[bold bright_cyan]%s[/bold bright_cyan]' % self.name)
        self.utils = MiraiUtils(self)
        self.message_handler = MiraiMessageHandler(self)

    async def check(self) -> None:
        await self.verify()

    async def _request_api(self, api_path: str, method: str = 'GET', data: dict = None) -> dict:
        try:
            async with request(method, '%s%s:%s%s' % (HTTP_PROTOCOL, self.http_host, self.http_port, api_path), data=data) as response:
                return await response.json()
        except ClientConnectorError as e:
            raise Exception('无法连接到 MiraiApiHttp, 请检查是否配置完整! %s' % e)

    async def verify(self) -> None:
        if self.enable_verify:
            await self._request_api('/verify', 'POST', data={'verifyKey': self.verify_key})
        else:
            self.logger.warning('你未启用 `enable_verify` 一步验证, 为了安全请最好启用并配置 `verify_key`!')

    @property
    async def login_info(self) -> dict:
        return await self._request_api('/botProfile')

    @property
    async def nick_name(self) -> str:
        return (await self.login_info)['nickname']

    async def start_listen(self) -> None:
        try:
            coroutine = await self.__reverse_listen() \
                if self.ws_reverse else await self.__obverse_listen()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(coroutine)
            loop.run_forever()
        except KeyboardInterrupt:
            self.logger.info('已退出!')

    async def __obverse_listen(self) -> Coroutine:
        async def run():
            with self.logger.status('正在尝试连接至 %s WebSocket 服务器...' % self.name) as status:
                async with ws_connect('%s%s:%s/message?verifyKey=%s' % (WS_PROTOCOL, self.ws_host, self.ws_port, self.verify_key)) as ws:
                    self.logger.success('连接成功, 开始监听消息!')
                    status.stop()
                    while True:
                        data = json.loads(await ws.recv())
                        print(data)
                        await self.auto_handle(data)

        return run()

    async def __reverse_listen(self) -> None:
        self.logger.error('暂未支持反向 WebSocket!')

    async def auto_handle(self, data: dict) -> None:
        if 'session' in data['data']:
            if data['data']['session'] == 'SINGLE_SESSION':
                self.logger.success('认证成功!')
            else:
                raise Exception('认证失败, 请确认相关配置正确!')
        else:
            _type = data['data']['type']
            if not _type.endswith('Event'):
                await self.message_handler.handle(data['data'])
            else:
                # TODO: 增加返回事件
                pass

    async def send_message(self, receiver_type: Type[Union[Friend, Group]], target_id: int, message: MessageChain) -> None:
        pass
