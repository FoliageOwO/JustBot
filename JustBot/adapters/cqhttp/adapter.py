from .config import CQHttpConfig
from .utils import CQHttpUtils
from .message_handler import CQHttpMessageHandler
from ...apis import Adapter
from ...utils import Logger, MessageChain
from ...contact import Friend, Group
from ... import HTTP_PROTOCOL, WS_PROTOCOL, CONFIG

from typing import Coroutine, Union, Any
from websockets import connect as ws_connect, serve as ws_serve, WebSocketServerProtocol
from aiohttp import request, ClientConnectorError
from overrides import overrides
from rich.traceback import install

import asyncio
import json
import nest_asyncio

nest_asyncio.apply()
install()


class CQHttpAdapter(Adapter):
    """
    > 说明
        CQHTTP 适配器.
    > 参数
        * config [CQHttpConfig]: 适配器对应的配置对象
    """
    def __init__(self, config: CQHttpConfig) -> None:
        self.name = 'CQHTTP'
        self.ws_host = config.ws_host
        self.ws_port = config.ws_port
        self.http_host = config.http_host
        self.http_port = config.http_port
        self.ws_reverse = config.ws_reverse
        self.logger = Logger('Adapter/%s' % self.name)
        self.utils = CQHttpUtils(self)
        self.message_handler = CQHttpMessageHandler(self)
        self.websocket = None

    @overrides
    async def check(self) -> None:
        if not (await self._request_api('/get_status'))['online']:
            raise ConnectionError('尝试连接 CQHTTP 时返回了一个错误的状态, 请尝试重启 CQHTTP!')

    @overrides
    async def _request_api(self, api_path: str) -> dict:
        try:
            async with request('GET', '%s%s:%s%s' % (HTTP_PROTOCOL, self.http_host, self.http_port, api_path)) as response:
                return (await response.json())['data']
        except ClientConnectorError:
            raise ConnectionError('无法连接到 CQHTTP 服务, 请检查是否配置完整!')

    @property
    async def login_info(self) -> dict:
        return await self._request_api('/get_login_info')

    @property
    async def nick_name(self) -> str:
        return (await self.login_info)['nickname']

    @overrides
    async def start_listen(self) -> Any:
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
            with self.logger.console.status('正在尝试连接至 %s WebSocket 服务器...' % self.name) as status:
                async with ws_connect('%s%s:%s' % (WS_PROTOCOL, self.ws_host, self.ws_port)) as self.websocket:
                    self.logger.success('连接成功, 开始监听消息!')
                    status.stop()
                    while True:
                        data = json.loads(await self.websocket.recv())
                        await self.auto_handle(data)
        return run()

    async def __reverse_listen(self) -> Coroutine:
        async def run():
            with self.logger.console.status('正在等待 WebSocket 客户端连接...') as status:
                self.is_stopped = False

                async def handle(websocket: WebSocketServerProtocol, path):
                    self.websocket = websocket
                    async for message in self.websocket:
                        if not self.is_stopped:
                            self.logger.success('连接成功, 开始监听消息!')
                            status.stop()
                            self.is_stopped = True
                        data = json.loads(message)
                        await self.auto_handle(data)

                async with ws_serve(handle, self.ws_host, self.ws_port):
                    self.logger.success('WebSocket 服务器建立成功: [bold blue]%s%s:%s[/bold blue]' % (WS_PROTOCOL, self.ws_host, self.ws_port))
                    while True:
                        await asyncio.Future()
        return run()

    async def auto_handle(self, data: dict) -> None:
        _type = data['post_type']
        if _type == 'message':
            await self.message_handler.handle(data)
        else:
            # TODO: 增加返回事件
            pass

    @overrides
    async def send_message(self, target: Union[Friend, Group], message: MessageChain) -> Any:
        await super().send_message(target, message)
        string = message.to_code()
        is_friend = isinstance(target, Friend)
        t = ('user_id' if is_friend else 'group_id',
             target.user_id if is_friend else target.group_id,
             'private_msg' if is_friend else 'group_msg',
             (await CONFIG.adapter_utils.get_friend_by_id(target.user_id)).nickname
             if is_friend else (await CONFIG.adapter_utils.get_group_by_id(target.group_id)).group_name)
        data = {t[0]: t[1], 'message': string}
        url = '%s%s:%s/send_%s' % (HTTP_PROTOCOL, self.http_host, self.http_port, t[2])
        async with request('POST', url, data=data) as response:
            d = await response.json()
            if d['retcode'] != 0:
                self.logger.error('发送消息失败: 状态码错误. 返回结果: `%s`.' % d['wording'])
            else:
                self.logger.info('%s -> %s(%s)' % (message.as_display(), t[3], t[1]))
