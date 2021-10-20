from JustBot.adapters.cqhttp.cqhttp_config import CQHTTPConfig
from JustBot.adapters.cqhttp.cqhttp_utils import CQHTTPUtils
from JustBot.apis import Adapter, Listener, ListenerManager, Config as global_config
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.handlers import MessageHandler
from JustBot.matchers import KeywordsMatcher, CommandMatcher
from JustBot.utils import Logger

from typing import Type, Union, Callable, Awaitable
from aiowebsocket.converses import AioWebSocket
from requests import ConnectionError, get as sync_get

import asyncio
import json
import nest_asyncio

nest_asyncio.apply()


class CQHTTPAdapter(Adapter):
    def __init__(self, config: CQHTTPConfig) -> None:
        self.name = 'CQHTTP'
        self.ws_host = config.ws_host
        self.ws_port = config.ws_port
        self.http_host = config.http_host
        self.http_port = config.http_port
        self.ws_reverse = config.ws_reverse

        self.logger = Logger(f'Adapter/{self.name}')
        self.adapter_utils = CQHTTPUtils(self.http_host, self.http_port, self.logger)
        self.listener_manager = ListenerManager()
        self.message_handler = MessageHandler(self.listener_manager)
        global_config.listener_manager = self.listener_manager
        global_config.message_handler = self.message_handler
        global_config.adapter_utils = self.adapter_utils

    def __request_api(self, api_path: str) -> dict:
        try:
            return sync_get(f'http://{self.http_host}:{self.http_port}{api_path}').json()
        except ConnectionError as e:
            raise Exception(
                f'无法连接到 CQHTTP 服务, 请检查是否配置完整! {e}')

    @property
    def login_info(self) -> dict:
        return self.__request_api('/get_login_info')

    @property
    def account(self) -> int:
        return self.login_info['data']['user_id']

    @property
    def nick_name(self) -> str:
        return self.login_info['data']['nickname']

    async def connect(self) -> None:
        if not self.__request_api('/get_status')['data']['online']:
            raise Exception(
                '尝试连接 CQHTTP 时返回了一个错误的状态, 请尝试重启 CQHTTP!')

    async def start_listen(self) -> None:
        try:
            await self.__reverse_listen() if self.ws_reverse else await self.__obverse_listen()
        except KeyboardInterrupt:
            self.logger.success('已退出!')

    async def __obverse_listen(self) -> None:
        async def run():
            self.logger.info(f'正在尝试连接至 {self.name} Websocket 服务器...')
            async with AioWebSocket(f'ws://{self.ws_host}:{self.ws_port}') as aws:
                r = aws.manipulator
                self.logger.success('连接成功, 开始监听消息!')
                while True:
                    data = json.loads((await r.receive()).decode('utf-8'))
                    self.auto_handle(data)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.run_forever()

    async def __reverse_listen(self) -> None:
        # TODO: 支持反向 WebSocket
        self.logger.error('暂未支持反向 WebSocket!')

    def auto_handle(self, data: dict) -> None:
        _type = data['post_type']
        if _type == 'message':
            self.message_handler.handle(data)
        else:
            # TODO: 增加返回事件
            pass

    def receiver(self, event: Type[Union[PrivateMessageEvent, GroupMessageEvent]],
                 priority: int = 1, matcher: Union[KeywordsMatcher, CommandMatcher] = None):
        def wrapper(target: Callable and Awaitable):
            if asyncio.iscoroutinefunction(target):
                self.logger.info(
                    f'注册监听器: [blue]{event} [red]([white]{priority}[/white])[/red][/blue] => [light_green]{target}[/light_green].')
                self.listener_manager.join(listener=Listener(event, target), priority=priority, matcher=matcher)
            else:
                self.logger.warning(f'无法注册监听器: 已忽略函数 [light_green]{target}[/light_green], 因为它必须是异步函数!')

        return wrapper
