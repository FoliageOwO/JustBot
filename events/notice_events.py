from ..apis import NoticeEvent

from dataclasses import dataclass
from enum import Enum


class GroupUpload(NoticeEvent):
    """
    > 说明
        群文件上传事件.
    > 参数
        + group_id [int]: 群号
        + user_id [int]: 发送者 QQ 号
        + file [GroupUpload.FileData]: 文件信息
    """
    
    @dataclass
    class FileData:
        """
        > 说明
            存储文件信息.
        > 参数
            + id [str]: 文件 ID
            + name [str]: 文件名
            + size [int]: 文件大小 (字节数)
            + busid [int]: busid
        """
        
        id: str
        name: str
        size: int
        busid: int
    
    __type__ = '群文件上传'
    __code__ = 'group_upload'
    
    def __init__(self, group_id: int, user_id: int, file: FileData, **kwargs) -> None:
        super().__init__(**kwargs)
        self.group_id = group_id
        self.user_id = user_id
        self.file = self.FileData(**dict(file))
    
    def as_display(self) -> str:
        return '群成员 %s 在群 %s 上传了文件 [yellow]%s[/yellow]' % (self.user_id, self.group_id, self.file.name)


@dataclass
class GroupAdmin(NoticeEvent):
    """
    > 说明
        群管理员变动事件.
    > 参数
        + sub_type [GroupAdmin.Type]: 事件类型
        + group_id [int]: 群号
        + user_id [int]: 管理员 QQ 号
    """

    class Type(Enum):
        """
        > 说明
            管理员变动事件类型.

            * SET => 设置管理员 => "set"
            * UNSET => 取消管理员 => "unset"
        """
        SET = 'set'
        UNSET = 'unset'

    __type__ = '群管理员变动'
    __code__ = 'group_admin'
    
    def __init__(self, sub_type: Type, group_id: int, user_id: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sub_type = self.Type(sub_type)
        self.group_id = group_id
        self.user_id = user_id
    
    def as_display(self) -> str:
        value = '[green]被设置管理[/green]' if self.sub_type == self.Type.SET else '[red]被取消管理[/red]'
        return '群成员 %s 在群 %s %s' % (self.user_id, self.group_id, value)


@dataclass
class GroupDecrease(NoticeEvent):
    """
    > 说明
        群成员减少事件.
    > 参数
        + sub_type [GroupDecrease.Type]: 减少事件类型
        + group_id [int]: 群号
        + operator_id [int]: 操作者 QQ 号 (如果是主动退群则与 `user_id` 相同)
        + user_id [int]: 离开者 QQ 号
    """
    
    class Type(Enum):
        """
        > 说明
            群成员减少事件类型.

            * LEAVE => 主动退群 => "leave"
            * KICK => 被踢 => "kick"
            * KICK_ME => 机器人被踢 => "kick_me"
        """
        LEAVE = 'leave'
        KICK = 'kick'
        KICK_ME = 'kick_me'
    
    __type__ = '群成员减少'
    __code__ = 'group_decrease'

    def __init__(self, sub_type: Type, group_id: int, operator_id: int, user_id: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sub_type = self.Type(sub_type)
        self.group_id = group_id
        self.operator_id = operator_id
        self.user_id = user_id
    
    def as_display(self) -> str:
        value_mapping = {
            self.Type.LEAVE: self.user_id,
            self.Type.KICK: self.user_id,
            self.Type.KICK_ME: '[red]你[/red]'
        }
        operator_mapping = {
            self.Type.LEAVE: '你自己',
            self.Type.KICK: self.operator_id,
            self.Type.KICK_ME: self.operator_id
        }
        return '%s 被 %s 移出群 %s' % (value_mapping[self.sub_type], operator_mapping[self.sub_type], self.group_id)


@dataclass
class GroupIncrease(NoticeEvent):
    """
    > 说明
        群成员增加事件.
    > 参数
        + sub_type [GroupIncrease.Type]: 增加事件类型
        + group_id [int]: 群号
        + operator_id [int]: 操作者 QQ 号
        + user_id [int]: 加入者 QQ 号
    """
    
    class Type(Enum):
        """
        > 说明
            群成员增加事件类型.
            
            * APPROVE => 管理员同意入群 => "approve"
            * INVITE => 管理员邀请入群 => "invite"
        """
        APPROVE = 'approve'
        INVITE = 'invite'

    __type__ = '群成员增加'
    __code__ = 'group_increase'
    
    def __init__(self, sub_type: Type, group_id: int, operator_id: int, user_id: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sub_type = self.Type(sub_type)
        self.group_id = group_id
        self.operator_id = operator_id
        self.user_id = user_id

    def as_display(self) -> str:
        return '%s 进入了群 %s' % (self.user_id, self.group_id)


@dataclass
class GroupBan(NoticeEvent):
    """
    > 说明
        群禁言事件.
    > 参数
        + sub_type [GroupBan.Type]: 禁言类型
        + group_id [int]: 群号
        + operator_id [int]: 操作者 QQ 号
        + user_id [int]: 被禁言 QQ 号
        + duration [int]: 禁言时长 (单位秒)
    """
    
    class Type(Enum):
        """
        > 说明
            群禁言事件类型.
            
            * BAN => 禁言 => "ban"
            * LIFT_BAN => 解除禁言 => "lift_ban"
        """
        BAN = 'ban'
        LIFT_BAN = 'lift_ban'

    __type__ = '群禁言'
    __code__ = 'group_ban'

    def __init__(self, sub_type: Type, group_id: int, operator_id: int, user_id: int, duration: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sub_type = self.Type(sub_type)
        self.group_id = group_id
        self.operator_id = operator_id
        self.user_id = user_id
        self.duration = duration
    
    def as_display(self) -> str:
        value_mapping = {
            self.Type.BAN: '[red]被 %s 禁言 %s 秒[/red]' % (self.operator_id, self.duration),
            self.Type.LIFT_BAN: '[green]被 %s 取消禁言[/green]' % self.operator_id
        }
        return '群成员 %s 在群 %s %s' % (self.user_id, self.group_id, value_mapping[self.sub_type])


@dataclass
class FriendAdd(NoticeEvent):
    """
    > 说明
        好友添加事件.
    > 参数
        + user_id [int]: 新添加好友 QQ 号
    """
    
    __type__ = '好友添加'
    __code__ = 'friend_add'
    
    def __init__(self, user_id: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
    
    def as_display(self) -> str:
        return '%s 请求添加你为好友' % (self.user_id)
