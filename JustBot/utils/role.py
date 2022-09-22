from enum import Enum


class Role(Enum):
    """
    > 说明
        群成员角色枚举类.
    """
    
    OWNER = 'owner'
    ADMIN = 'admin'
    MEMBER = 'member'
