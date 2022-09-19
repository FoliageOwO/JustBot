from ...contact import Friend, Group, Member
from ... import HTTP_PROTOCOL

from aiohttp import request
from typing import Union


class CQHttpUtils:
    def __init__(self, adapter) -> None:
        self.host = adapter.http_host
        self.port = adapter.http_port
        self.logger = adapter.logger

    async def request_api(self, path: str, data: bool = True, params: dict = None) -> dict:
        async with request('GET', '%s%s:%s%s' % (HTTP_PROTOCOL, self.host, self.port, path), params=params) as response:
            _ = await response.json()
            return _['data'] if data else _

    async def get_friend_by_id(self, user_id: int) -> Friend:
        for i in await self.request_api('/get_friend_list'):
            if i['user_id'] == user_id:
                return Friend(i['user_id'], i['nickname'], i['remark'])
        self.logger.error('无法找到好友 `%s`!' % user_id)

    async def get_group_by_id(self, group_id: int) -> Group:
        for i in await self.request_api('/get_group_list'):
            if i['group_id'] == group_id:
                return Group(i['group_id'], i['group_name'], i['max_member_count'], i['member_count'],
                             i['group_level'], i['group_create_time'])
        self.logger.error('无法找到群 `%s`!' % group_id)

    async def get_member_by_id(self, group_id: int, user_id: int) -> Member:
        data = await self.request_api(f'/get_group_member_list', data=False, params={'group_id': group_id})
        if data['retcode'] == 100:
            self.logger.error('%s: `%s`!' % (data['wording'], user_id))
        else:
            for i in data['data']:
                if i['user_id'] == user_id:
                    return Member(await self.get_group_by_id(group_id), i['user_id'], group_id, i['nickname'], i['role'],
                                  i['last_sent_time'], i['join_time'])
            self.logger.error('无法找到群成员 `%s:%s`!' % (group_id, user_id))

    async def get_forward_message(self, id: str) -> Union[dict, None]:
        return await self.request_api(f'/get_forward_msg', data=True, params={'id': id})

    async def get_message_by_id(self, id: int) -> Union[dict, None]:
        return await self.request_api(f'/get_msg', data=True, params={'message_id': id})
