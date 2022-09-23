import traceback
from ...apis import Element
from ...utils import MessageChain
from ... import CONFIG, BotApplication

from enum import Enum
from typing import Any, List, TypeVar, NewType
from json import dumps, loads as json


class CQHTTPElement(Element):
    """
    > 说明
        CQHTTP 消息链元素.
    """
    pass


class Utils:
    """
    > 说明
        CQHTTP 元素类中的工具类.
    """

    T = NewType('T', Any)

    @staticmethod
    def remove_brackets(code: str) -> str:
        """
        > 说明
            将完整的 CQ 码 ``code`` 前后的 ``中括号`` 删除.
        > 参数
            + code [str]: 完整的 CQ 码
        > 返回
            * str: 删除后的字符串
        > 示例
            >>> Utils.remove_brackets('[CQ:foo,bar=1]')
            'CQ:foo,bar=1'
        """

        return code.strip('[]')

    @staticmethod
    def to_mapping(code: str) -> dict:
        """
        > 说明
            将去除中括号后的 CQ 码 ``code`` 中的参数转换为 ``dict`` 并返回.
        > 参数
            + code [str]: 去除中括号后的 CQ 码
        > 返回
            * dict: CQ 码中的参数组成的字典
        > 示例
            >>> Utils.to_mapping('CQ:foo,bar=1')
            {'bar': '1'}
        """

        args = dict()
        for i in code.split(',')[1:]:
            k = i.split('=')
            if len(k) != 1:
                args[k[0]] = k[1]
        return args

    @staticmethod
    def get(code: str, key: str, *, default: Any = None, T_: T = T) -> T:
        """
        > 说明
            将参数值从完整的 CQ 码 ``code`` 中分离出来.
        > 参数
            + code [str]: 完整的 CQ 码
            + key [str]: 参数值键值
            + default [Any]: 默认值 [可选]
            + t [Any]: 转换类型 [可选] [default=str]
        > 返回
            * str: 获取到的参数值
            * Any: 无法找到键值时的默认值
        > 示例
            >>> Utils.get('[CQ:foo,bar=1]', 'bar')
            '1'
            >>> Utils.get('[CQ:foo,bar=1]', 'bar', type=int)
            1
            >>> Utils.get('[CQ:foo,bar=1]', 'bar2', default='default')
            'default'
        """

        mapping = Utils.to_mapping(Utils.remove_brackets(code))
        return T_(mapping[key]) if key in mapping.keys() else default

    @staticmethod
    def format_code(element: CQHTTPElement) -> str:
        """
        > 说明
            将 ``CQHTTPElement 对象`` 转换成 CQ 码.
        > 参数
            + element [CQHTTPElement]: 元素对象
        > 返回
            * str: 完整的 CQ 码
        > 示例
            >>> Utils.format_code(Foo(bar=1))
            '[CQ:foo,bar=1]'
        """

        string = ''
        for k in element.__dict__.keys():
            v = element.__dict__[k]
            if v is not None:
                string = '%s,%s=%s' % (string, k, v)
        return '[CQ:%s%s]' % (element.__code__, string)

    @staticmethod
    def format_display(element: CQHTTPElement, ignore: List[str] = ()) -> str:
        """
        > 说明
            将 ``CQHTTPElement 对象`` 转换成易读字符串.
        > 参数
            + element [CQHTTPElement]: 元素对象
            + ignore [list[str]]: 忽略转换时的某些参数 [可选]
        > 返回
            * str: 易读字符串
        > 示例
            >>> Utils.format_display(Foo(bar=1))
            '[Foo|1]'
            >>> Utils.format_display(Foo(bar=1), ignore=['bar'])
            '[Foo]'
        """

        string = ''
        for i in [element.__dict__[k] for k in element.__dict__ if k not in ignore]:
            if i is not None:
                string = '%s|%s' % (string, i)
        is_element = element.__class__.__name__ != TypeVar.__name__
        return '[%s%s]' % (element.__type__ if is_element else '[red]ERROR[/red]', string if is_element else '')

    @staticmethod
    def get_element_by_code(code: str) -> CQHTTPElement:
        """
        > 说明
            将完整的 CQ 码 ``code`` 转换成 ``CQHTTPElement 对象``,
            如果该 ``code`` 暂未支持将会返回 ``Plain(code)``.
        > 参数
            + code [str]: 完整的 CQ 码
        > 返回
            * CQHTTPElement[?]: 转换后的 ``CQHTTPElement`` 对象
            * CQHTTPElement[Plain]: 未支持 CQ 码时的 ``Plain`` 对象
        > 示例
            >>> foo = Utils.get_element_by_code('[CQ:foo,bar=1]')
            >>> foo
            <Foo object at ...>
            >>> foo.bar
            1
            >>> unknown = Utils.get_element_by_code('[CQ:unknown_element,idk=0]')
            >>> unknown
            <Plain object at ...>
            >>> unknown.as_display()
            '[CQ:unknown_element,idk=0]'
        """

        kwargs = Utils.to_mapping(Utils.remove_brackets(code))
        elements = [i for i in CQHTTPElement.__subclasses__() if 'cqhttp' in str(i)]
        try:
            key = Utils.remove_brackets(code).split(',')[0].split(':')[1]
            for element in elements:
                if element.__code__ == key:
                    return element(**kwargs)
        except Exception as err:
            if '[CQ:' not in code:
                return Plain(code)
            else:
                traceback.print_exc()

    @staticmethod
    def format_unsupported_display(code: str) -> str:
        """
        > 说明
            将不支持的完整的 CQ 码转换为字符串.
        > 参数
            + code [str]: 不支持的完整的 CQ 码
        > 返回
            * str: 字符串
        > 示例
            >>> Utils.format_unsupported_display('[CQ:unsupported_element,bar=1]')
            '[unsupported_element]'
        """

        name = Utils.remove_brackets(code).split(',')[0].split(':')[1]
        element = TypeVar(name, bound=CQHTTPElement)
        return Utils.format_display(element)

    @staticmethod
    def as_colored_display(element: CQHTTPElement) -> str:
        """
        > 说明
            将 ``CQHTTPElement 对象`` 转化为带有颜色的易读字符串.
        > 参数
            + element [CQHTTPElement]: CQHTTPElement 对象
        > 返回
            * str: 带有颜色的易读字符串
        > 示例
            >>> Utils.as_colored_display(Foo(bar=1))
            '[bold yellow][Foo[bold red]|[/bold red]1][/bold yellow]'
        """

        split_color = 'bold red'
        color = 'bold yellow'
        return ('[%s]%s[/%s]' % (color, element.as_display(), color)).replace('|', '[%s]|[/%s]' % (split_color, split_color))

    @staticmethod
    def as_str(element: CQHTTPElement) -> str:
        """
        > 说明
            将 ``CQHTTPElement 对象`` 转换为 ``<CQHTTPElement:{name}|{display}>`` 的格式.
        > 参数
            + element [CQHTTPElement]: 元素对象
        > 返回
            * str: 转换后的字符串
        > 示例
            >>> Utils.as_str(Foo(bar=1))
            '<CQHTTPElement:Foo|[Foo:1]>'
        """

        return '<CQHTTPElement:%s|%s>' % (element.__class__.__name__, element.as_display())


class Plain(CQHTTPElement):
    """
    > 说明
        纯文本, 支持多行.
    > 参数
        + *texts [*str]: 文本
    > 示例
        >>> plain1 = Plain('Hello, World!')
        >>> plain2 = Plain('Line1', 'Line2')
    """

    __type__ = '纯文本'
    __code__ = 'plain'

    def __init__(self, *texts) -> None:
        super().__init__()
        self.texts = '\n'.join(texts).replace('\r', '')

    def as_display(self) -> str:
        return self.texts

    def to_code(self) -> str:
        return self.texts

    @staticmethod
    def as_code_display(code: str) -> str:
        return code

    def __str__(self) -> str:
        return Utils.as_str(self)


class Face(CQHTTPElement):
    """
    > 说明
        表情.
    > 参数
        + id [int]: 表情 ID
    > 示例
        >>> face = Face(174)
    """

    __type__ = '表情'
    __code__ = 'face'

    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return Face(Utils.get(code, 'id', T_=int)).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class At(CQHTTPElement):
    """
    > 说明
        @ 某人.
    > 参数
        + qq [int]: 需要 @ 的 QQ 号
    > 示例
        >>> At(123456789)
    """

    __type__ = '@'
    __code__ = 'at'

    def __init__(self, qq: int, name: str = None) -> None:
        super().__init__()
        self.qq = qq
        self.name = name

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return At(Utils.get(code, 'qq', T_=int), Utils.get(code, 'name')).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class Share(CQHTTPElement):
    """
    > 说明
        链接分享.
    > 参数
        + url [str]: 链接
        + title [str]: 标题
        + content [Optional[str]]: 内容 [可选]
        + image [Optional[str]]: 图片 URL [可选]
    > 示例
        >>> Share('https://example.com', 'Title')
        >>> Share('https://example.com', 'Title', 'This is an example share.')
        >>> Share('https://example.com', 'Title', 'This is an example share.', 'https://example.com/image.png')
    """

    __type__ = '分享'
    __code__ = 'share'

    def __init__(self, url: str, title: str, content: str = None, image: str = None) -> None:
        super().__init__()
        self.url = url
        self.title = title
        self.content = content
        self.image = image

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return Share(Utils.get(code, 'url'), Utils.get(code, 'title'), Utils.get(code, 'content'),
                     Utils.get(code, 'image')).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class Reply(CQHTTPElement):
    """
    > 说明
        回复一个消息.
    > 参数
        + id [int]: 消息 ID (可从 Event::message_id 获取)
    > 示例
        >>> Reply(123456789)
        >>> Reply(event.message_id)
    """

    __type__ = '回复'
    __code__ = 'reply'

    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return Reply(Utils.get(code, 'id', T_=int)).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)

    @property
    def message_chain(self) -> MessageChain:
        from .message_handler import CQHTTPMessageHandler

        data = BotApplication.coroutine(CONFIG.adapter.utils.get_message_by_id(self.message_id))
        return CQHTTPMessageHandler.format_message_chain(data['message'])[0]


class Image(CQHTTPElement):
    """
    > 说明
        图片.
    > 参数
        + file [str]: 图片文件
        + url [str]: 图片的 URL [可选]
        + type [Optional[ImageType]]: 图片类型 [可选]
        + subType [Optional[int]]: 图片子类型 [可选] (只出现在群聊)
        + id [EffectType]: 秀图特效 ID [可选] (当 type 为 ImageType.SHOW 时有效)
        + c [int]: 通过网络下载图片时的线程数 [可选]
    > 示例
        >>> Image(None, url='https://example.com/image.png')
        >>> Image('C:\\image.png')
    """

    class ImageType(Enum):
        """
        > 说明
            图片类型枚举类

            * FLASH => 闪照 => "flash"
            * SHOW => 秀图 => "show"
            * NORMAL => 普通 => ""
        """

        FLASH = 'flash'
        SHOW = 'show'
        NORMAL = ''

    class EffectType(Enum):
        """
        > 说明
            图片效果枚举类

            * PUTONG => 普通 => 40000
            * HUANYING => 幻影 => 40001
            * DOUDONG => 抖动 => 40002
            * SHENGRI => 生日 => 40003
            * AINI => 爱你 => 40004
            * ZHENGYOU => 征友 => 40005
        """

        PUTONG = 40000
        HUANYING = 40001
        DOUDONG = 40002
        SHENGRI = 40003
        AINI = 40004
        ZHENGYOU = 40005

    __type__ = '图片'
    __code__ = 'image'

    def __init__(self, file: str, *,
                 url: str = None,
                 type: ImageType = ImageType.NORMAL, subType: int = 0,
                 id: EffectType = None, c: int = None) -> None:
        super().__init__()
        self.file = file if file != None else url
        self.url = url
        self.type = Image.ImageType(type).value
        self.subType = subType
        self.id = Image.EffectType(id).value if id != None else None # Image.EffectType.PUTONG.value
        self.c = c

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return Image(Utils.get(code, 'file'),
                     url=Utils.get(code, 'url'), subType=Utils.get(code, 'subType', T_=int), type=Image.ImageType(Utils.get(code, 'type')),
                     id=Image.EffectType(Utils.get(code, 'id', T_=int)), c=Utils.get(code, 'c', T_=int)).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class _Forward(CQHTTPElement):
    """
    > 说明
        合并转发. [仅接收] [接收非 CQ 码]
    > 参数
        + id [str]: 转发的消息 ID
    > 示例
        >>> message_chain[_Forward]
    """

    __type__ = '合并转发'
    __code__ = 'forward'

    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id
        self.data = BotApplication.coroutine(CONFIG.adapter.utils.get_forward_message(id=id))

    def as_display(self) -> str:
        return Utils.format_display(self, ['data'])

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return _Forward(Utils.get(code, 'id')).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)

    @property
    def message_chain(self) -> MessageChain:
        chain = MessageChain.create()
        for message in self.data['messages']:
            chain.append_elements(Utils.get_element_by_code(message['content']))
        return chain


class Poke(CQHTTPElement):
    """
    > 说明
        戳一戳. [仅群聊]
    > 参数
        + qq [int]: 要戳的群成员 QQ 号
    > 示例
        >>> Poke(123456789)
    """

    __type__ = '戳一戳'
    __code__ = 'poke'

    def __init__(self, qq: int) -> None:
        super().__init__()
        self.qq = qq

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return Poke(Utils.get(code, 'qq', T_=int)).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class JSON(CQHTTPElement):
    """
    > 说明
        JSON 消息.
    > 参数
        + data [dict]: JSON 数据
        + resid [Optional[int]]: 默认不填为 ``0``, 走小程序通道, 填了走富文本通道发送 [default=0]
    > 示例
        >>> JSON({"app":"com.tencent.miniapp", ...})
    """

    __type__ = 'JSON'
    __code__ = 'json'

    def __init__(self, data: dict, resid: int = 0) -> None:
        super().__init__()
        self.raw_data = data
        self.data = JSON.escape(dumps(data))
        self.resid = resid

    @staticmethod
    def escape(data: str) -> str:
        """
        > 说明
            对 JSON 字符串进行转义处理

            * "," => "&#44"
            * "&" => "&amp"
            * "[" => "&#91"
            * "]" => "&#93"
        > 参数
            + data [str]: JSON 字符
        > 返回
            * str: 转义后的 JSON 字符
        """

        return data.replace(',', '&#44;').replace('&', '&amp;').replace('[', '&#91;').replace(']', '&#93;')

    def as_display(self) -> str:
        return Utils.format_display(self, ['raw_data', 'data', 'resid'])

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return JSON(Utils.get(code, 'data', T_=json), Utils.get(code, 'resid', T_=int)).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class Music(CQHTTPElement):
    """
    > 说明
        音乐分享. [仅发送]
    > 参数
        + type [MusicType]: 音乐类型
        + id [int]: 音乐 ID (不是自定义音乐必填) [选填]
        + url [str]: 点击跳转链接 (自定义音乐必填) [选填]
        + audio [str]: 音乐 URL (自定义音乐必填) [选填]
        + title [str]: 标题 (自定义音乐必填) [选填]
        + content [str]: 内容 (自定义音乐有效) [选填]
        + image [str]: 图片 URL (自定义音乐有效) [选填]
    > 示例
        >>> Music(MusicType.QQ, id=123456)
        >>> Music(MusicType.CUSTOM, url='https://example.com/music_detail', audio='https://example.com/music.mp3')
        >>> Music(MusicType.CUSTOM, url='https://example.com/music_detail', audio='https://example.com/music.mp3',
            title='Music', content='Music that beautiful', image='https://example.com/music.png')
    """
    
    __type__ = '音乐分享'
    __code__ = 'music'

    class MusicType(Enum):
        """
        > 说明
            音乐类型枚举类

            * QQ => QQ 音乐 => "qq"
            * NETEASE => 网易云音乐 => "163"
            * XIAMI => 虾米音乐 => "xm"
            * CUSTOM => 自定义 => "custom"
        """

        QQ = 'qq'
        NETEASE = '163'
        XIAMI = 'xm'
        CUSTOM = 'custom'

    def __init__(self, type: MusicType, *,
                 id: int = None, url: str = None, audio: str = None, title: str = None,
                 content: str = None, image: str = None):
        super().__init__()
        self.type = Music.MusicType(type).value
        self.id = id
        self.url = url
        self.audio = audio
        self.title = title
        self.content = content
        self.image = image
        if self.type != Music.MusicType.CUSTOM and id is None:
            raise ValueError('非自定义音乐需要传入 `id` 参数!')
        if self.type == Music.MusicType.CUSTOM and not (self.url and self.audio and self.title):
            raise ValueError('自定义音乐需要传入 `url`, `audio`, `title` 参数!')

    def as_display(self) -> str:
        return Utils.format_display(self)

    def to_code(self) -> str:
        return Utils.format_code(self)

    @staticmethod
    def as_code_display(code: str) -> str:
        return Music(Music.MusicType(Utils.get(code, 'type')),
                     id=Utils.get(code, 'id', T_=int), url=Utils.get(code, 'url'),
                     audio=Utils.get(code, 'audio'), title=Utils.get(code, 'title'),
                     content=Utils.get(code, 'content'), image=Utils.get(code, 'image')).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)
