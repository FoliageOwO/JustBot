from JustBot.objects import Friend, Group, Member
from JustBot.utils import Logger
from JustBot.application import HTTP_PROTOCOL

from requests import get as sync_get


class CQHTTPUtils:
    def __init__(self, adapter):
        self.host = adapter.http_host
        self.port = adapter.http_port
        self.logger = adapter.logger

    def __request_api(self, path: str, data: bool = True) -> dict:
        _ = sync_get(f'{HTTP_PROTOCOL}{self.host}:{self.port}{path}').json()
        return _['data'] if data else _

    def get_friend_by_id(self, user_id: int) -> Friend:
        for i in self.__request_api('/get_friend_list'):
            if i['user_id'] == user_id:
                return Friend(i['nickname'], i['user_id'], i['remark'])
        self.logger.error(
            f'无法找到好友 `{user_id}`, 这可能是个内部错误!')

    def get_group_by_id(self, group_id: int) -> Group:
        for i in self.__request_api('/get_group_list'):
            if i['group_id'] == group_id:
                return Group(i['group_name'], i['group_id'], i['max_member_count'], i['member_count'],
                             i['group_level'], i['group_create_time'], i['group_memo'])
        self.logger.error(
            f'无法找到群 `{user_id}`, 这可能是个内部错误!')

    def get_member_by_id(self, group_id: int, user_id: int) -> Member:
        data = self.__request_api(f'/get_group_member_list?group_id={group_id}', data=False)
        if data['retcode'] == 100:
            NoContact(
                f'{data["wording"]}: `{user_id}`')
        else:
            for i in data['data']:
                if i['user_id'] == user_id:
                    return Member(self.get_group_by_id(group_id), i['nickname'], i['user_id'], i['role'],
                                  i['last_sent_time'], i['join_time'])
            self.logger.error(
                f'无法找到群成员 `{user_id}`, 这可能是个内部错误!')
