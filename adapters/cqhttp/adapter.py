from JustBot.adapters.cqhttp.config import CQHTTPConfig
from JustBot.adapters.cqhttp.utils import CQHTTPUtils
from JustBot.adapters.cqhttp.message_handler import CQHTTPMessageHandler
from JustBot.adapters.cqhttp.sender_handler import CQHTTPSenderHandler
from JustBot.apis import Adapter, Listener, ListenerManager, Config as global_config
from JustBot.events import PrivateMessageEvent, GroupMessageEvent
from JustBot.matchers import KeywordsMatcher, CommandMatcher
from JustBot.utils import Logger
from JustBot.application import HTTP_PROTOCOL, WS_PROTOCOL

from typing import Type, Union, Callable, Awaitable, List
from websockets import connect as ws_connect, serve as ws_serve, WebSocketServerProtocol
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
        self.listener_manager = ListenerManager()
        self.utils = CQHTTPUtils(self)
        self.sender_handler = CQHTTPSenderHandler(self)
        self.message_handler = CQHTTPMessageHandler(self)
        global_config.listener_manager = self.listener_manager
        global_config.message_handler = self.message_handler
        global_config.adapter_utils = self.utils

    def __request_api(self, api_path: str) -> dict:
        try:
            return sync_get(f'{HTTP_PROTOCOL}{self.http_host}:{self.http_port}{api_path}').json()
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
            self.logger.info('已退出!')

    async def __obverse_listen(self) -> None:
        async def run():
            with self.logger.status(f'正在尝试连接至 {self.name} WebSocket 服务器...') as status:
                async with ws_connect(f'{WS_PROTOCOL}{self.ws_host}:{self.ws_port}') as ws:
                    self.logger.success('连接成功, 开始监听消息!')
                    status.stop()
                    while True:
                        data = json.loads(await ws.recv())
                        self.auto_handle(data)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.run_forever()

    async def __reverse_listen(self) -> None:
        async def run():
            with self.logger.status(f'正在等待 WebSocket 客户端连接...') as status:
                self.is_stopped = False

                async def handle(websocket: WebSocketServerProtocol, path):
                    async for message in websocket:
                        if not self.is_stopped:
                            self.logger.success('连接成功, 开始监听消息!')
                            status.stop()
                            self.is_stopped = True
                        data = json.loads(message)
                        self.auto_handle(data)

                async with ws_serve(handle, self.ws_host, self.ws_port):
                    self.logger.success(f'WebSocket 服务器建立成功: [bold blue]{WS_PROTOCOL}{self.ws_host}:{self.ws_port}[/bold blue]')
                    while True:
                        await asyncio.Future()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.run_forever()

    def auto_handle(self, data: dict) -> None:
        _type = data['post_type']
        if _type == 'message':
            self.message_handler.handle(data)
        else:
            # TODO: 增加返回事件
            pass

    def receiver(self, event: List[Type[Union[PrivateMessageEvent, GroupMessageEvent]]],
                 priority: int = 1, matcher: Union[KeywordsMatcher, CommandMatcher] = None,
                 parameters_convert: Type[Union[str, list, dict, None]] = str):

        parameters_convert = parameters_convert if isinstance(matcher, CommandMatcher) else None

        def wrapper(target: Callable and Awaitable):
            if asyncio.iscoroutinefunction(target):
                if len(event) == 1:
                    self.logger.info(
                        f'注册监听器: [blue]{event} [red]([white]{priority}[/white])[/red][/blue] => [light_green]{target}[/light_green].')
                    self.listener_manager.join(listener=Listener(event[0], target), priority=priority, matcher=matcher,
                                               parameters_convert=parameters_convert)
                else:
                    self.logger.info(
                        f'注册监听器 (多个事件): [blue]{" & ".join([str(e) for e in event])} [red]([white]{priority}[/white])[/red][/blue] => [light_green]{target}[/light_green].')
                    for e in event:
                        self.listener_manager.join(listener=Listener(e, target), priority=priority, matcher=matcher,
                                                   parameters_convert=parameters_convert)
            else:
                self.logger.warning(f'无法注册监听器: 已忽略函数 [light_green]{target}[/light_green], 因为它必须是异步函数!')

        return wrapper
