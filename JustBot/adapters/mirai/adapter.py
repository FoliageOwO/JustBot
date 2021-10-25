from JustBot.apis import Adapter
from JustBot.adapters.mirai.config import MiraiConfig
from JustBot.adapters.mirai.message_handler import MiraiMessageHandler
from JustBot.adapters.mirai.sender_handler import MiraiSenderHandler
from JustBot.adapters.mirai.utils import MiraiUtils
from JustBot.utils import Logger, ListenerManager
from JustBot.application import HTTP_PROTOCOL, WS_PROTOCOL, CONFIG

from aiohttp import request, ClientConnectorError
from typing import Any, NoReturn, Coroutine
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

        self.logger = Logger(f'Adapter/{self.name}')
        self.utils = MiraiUtils(self)
        self.sender_handler = MiraiSenderHandler(self)
        self.message_handler = MiraiMessageHandler(self)

    async def check(self) -> NoReturn:
        await self.verify()

    async def _request_api(self, api_path: str, method: str = 'GET', data: dict = None) -> dict:
        try:
            async with request(method, f'{HTTP_PROTOCOL}{self.http_host}:{self.http_port}{api_path}', data=data) as response:
                return await response.json()
        except ClientConnectorError as e:
            raise Exception(
                f'无法连接到 MiraiApiHttp, 请检查是否配置完整! {e}')

    async def verify(self) -> NoReturn:
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

    async def start_listen(self) -> NoReturn:
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
            with self.logger.status(f'正在尝试连接至 {self.name} WebSocket 服务器...') as status:
                async with ws_connect(f'{WS_PROTOCOL}{self.ws_host}:{self.ws_port}/message?verifyKey={self.verify_key}') as ws:
                    self.logger.success('连接成功, 开始监听消息!')
                    status.stop()
                    while True:
                        data = json.loads(await ws.recv())
                        print(data)
                        await self.auto_handle(data)

        return run()

    async def __reverse_listen(self) -> NoReturn:
        self.logger.error('暂未支持反向 WebSocket!')

    async def auto_handle(self, data: dict) -> None:
        if 'session' in data['data']:
            if data['data']['session'] == 'SINGLE_SESSION':
                self.logger.success('认证成功!')
            else:
                raise Exception(
                    '认证失败, 请确认相关配置正确!')
        else:
            _type = data['data']['type']
            if not _type.endswith('Event'):
                await self.message_handler.handle(data['data'])
            else:
                # TODO: 增加返回事件
                pass
