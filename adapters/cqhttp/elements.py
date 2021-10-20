from JustBot.apis import Element

from typing import Union


class Utils:
    @staticmethod
    def remove_brackets(code: str):
        """
        将完整的 CQ 码 ``code`` 中的最前和最后的 ``中括号`` 删除

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> Utils.remove_brackets('[CQ:face,id=174]')
        'CQ:face,id=174'

        :param code: 完整的 CQ 码
        :return: 删除后的字符串
        """

        return code[1:-1]

    @staticmethod
    def to_mapping(code: str):
        """
        将去除中括号后的 CQ 码 ``code`` 中的参数转换为 ``dict``

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> Utils.to_mapping('CQ:face,id=174')
        >>> # 等价于 Utils.to_mapping(Utils.remove_brackets('[CQ:face,id=174]'))
        {'id': '174'}

        :param code: 去除中括号后的 CQ 码
        :return: CQ 码中的参数组成的字典
        """

        mapping = {}
        for i in code.split(',')[1:]:
            k = i.split('=')
            if k != ['']:
                mapping[k[0]] = k[1]
        return mapping

    @staticmethod
    def get(code: str, name: str):
        """
        将参数值从完整的 CQ 码 ``code`` 中剥离出来

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> Utils.get('[CQ:face,id=174]', 'id')
        '174'

        :param code: 完整的 CQ 码
        :param name: 参数名
        :return: 获取的参数值
        """

        mapping = Utils.to_mapping(Utils.remove_brackets(code).split(',')[1])
        return mapping[name] if name in mapping.keys() else None

    @staticmethod
    def format_code(name: str, **kwargs):
        """
        将传入的 CQ 码名称 ``name`` 和 ``kwargs`` 参数拼合成一个完整的 CQ 码

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> Utils.format_code('face', id=174)
        '[CQ:face,id=174]'

        :param name: CQ 码名称
        :param kwargs: CQ 码中的参数
        :return: 完整的 CQ 码
        """

        string = ''
        for k in kwargs.keys():
            v = kwargs[k]
            if v:
                string = f'{string},{k}={v}'
        return f'[CQ:{name}{string}]'

    @staticmethod
    def format_display(name: str, *args):
        """
        将传入的 CQ 码对应的名称 ``name`` 和 ``args`` 参数拼合成一个可读的字符串

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> Utils.format_display('表情', 174)
        '[表情:174]'

        :param name: CQ 码对应的名称
        :param args: 字符串中的参数
        :return: 可读的字符串
        """

        string = ''
        for i in args:
            if i:
                string = f'{string}:{i}'
        return f'[{name}{string}]'

    @staticmethod
    def get_element_by_code(code: str):
        """
        将完整的 CQ 码 ``code`` 转换成 ``Element`` 实例

        如果该 ``code`` 暂未支持将会返回 ``None``

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> face = Utils.get_element_by_code('[CQ:face,id=174]')
        >>> face
        <JustBot.adapters.cqhttp.elements.Face object at 0x0000000002121880>
        >>> face.as_display()
        '[表情:174]'
        >>> image = Utils.get_element_by_code('[CQ:image,file=xxx,url=yyy]')
        >>> image is None
        True

        :param code: 完整的 CQ 码
        :return: Element 实例
        """

        kwargs = Utils.to_mapping(Utils.remove_brackets(code))
        mapping = {
            'text': Text, 'face': Face, 'at': At, 'share': Share, 'reply': Reply
        }
        key = Utils.remove_brackets(code).split(',')[0].split(':')[1]
        return mapping[key](**kwargs) if key in mapping.keys() else None

    @staticmethod
    def format_unsupported_display(code: str, colored: bool = False, color: str = 'bold yellow'):
        """
        将为支持的完整的 CQ 码转换为暂时字符串

        >>> from JustBot.adapters.cqhttp.elements import Utils
        >>> Utils.format_unsupported_display('[CQ:image,file=xxx,url=yyy]')
        '[|image:xxx:yyy]'
        >>> Utils.format_unsupported_display('[CQ:image,file=xxx,url=yyy]', colored=True)
        '[bold yellow][|image:xxx:yyy][/bold yellow]'
        >>> Utils.format_unsupported_display('[CQ:image,file=xxx,url=yyy]', colored=True, color='red')
        '[red][|image:xxx:yyy][/red]'

        :param code: 暂未支持的完整的 CQ 码
        :param colored: 是否转换成带颜色的字符串
        :param color: 字符串颜色 [默认 'bold yellow']
        :return: 字符串
        """

        removed_code = Utils.remove_brackets(code)
        result = '|' + removed_code.split(',')[0].split(':')[1]
        result = f'[{color}]{result}[/{color}]' if colored else result
        return Utils.format_display(result,
                                    *tuple(Utils.to_mapping(removed_code).values()))

    @staticmethod
    def as_colored_display(element: Element, color: str = 'bold yellow'):
        """
        将 ``Element`` 对象转化为带有颜色的可读的字符串

        >>> from JustBot.adapters.cqhttp.elements import Utils, Face
        >>> Utils.as_colored_display(Face(174))
        '[bold yellow][表情:174][/bold yellow]'
        >>> Utils.as_colored_display(Face(174), color='red')
        '[red][表情:174][/red]'

        :param element: Element 对象
        :param color: 字符串颜色 [默认 'bold yellow']
        :return: 带有颜色的可读的字符串
        """

        return f'[{color}]{element.as_display()}[/{color}]'


# TODO: 添加对更多 CQ 码的支持

class Text(Element):
    def __init__(self, *texts):
        self.texts = ' \n'.join(texts)

    def as_display(self):
        return self.texts

    def to_code(self):
        return self.texts

    @staticmethod
    def as_code_display(code: str):
        return code


class Face(Element):
    def __init__(self, id: int):
        self.id = id

    def as_display(self):
        return Utils.format_display('表情', self.id)

    def to_code(self):
        return Utils.format_code('face', id=self.id)

    @staticmethod
    def as_code_display(code: str):
        return Face(int(Utils.get(code, 'id'))).as_display()


class At(Element):
    def __init__(self, qq: Union[str, int], name: str = None):
        self.qq = qq
        self.name = name

    def as_display(self):
        return Utils.format_display('At', self.qq, self.name)

    def to_code(self):
        return Utils.format_code('at', qq=self.qq, name=self.name)

    @staticmethod
    def as_code_display(code: str):
        return At(int(Utils.get(code, 'qq')), Utils.get(code, 'name')).as_display()


class Share(Element):
    def __init__(self, url: str, title: str, content: str = None, image_url: str = None):
        self.url = url
        self.title = title
        self.content = content
        self.image_url = image_url

    def as_display(self):
        return Utils.format_display('分享', self.url, self.title)

    def to_code(self):
        return Utils.format_code('share', url=self.url, title=self.title, content=self.content, image=self.image_url)

    @staticmethod
    def as_code_display(code: str):
        return Share(Utils.get(code, 'url'), Utils.get(code, 'title'), Utils.get(code, 'content'),
                     Utils.get(code, 'image')).as_display()


class Reply(Element):
    def __init__(self, message_id: int):
        self.message_id = message_id

    def as_display(self):
        return Utils.format_display('回复', self.message_id)

    def to_code(self):
        return Utils.format_code('reply', id=self.message_id)

    @staticmethod
    def as_code_display(code: str):
        return Reply(int(Utils.get(code, 'id'))).as_display()
