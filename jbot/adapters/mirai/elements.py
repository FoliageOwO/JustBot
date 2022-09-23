from ...apis import Element


class MiraiElement(Element):
    """
    > 说明
        Mirai 消息链元素.
    """
    pass



# TODO: 完善
class Utils:
    @staticmethod
    def format_display(name: str, *args) -> str:
        string = ''
        for i in args:
            if i:
                string = '%s:%s' % (string, i)
        return '[%s%s]' % (name, string)

    @staticmethod
    def format_code(el_name: str, **kwargs) -> dict:
        return dict(type=el_name, **kwargs)

    @staticmethod
    def get_element_by_code(code: dict) -> MiraiElement:
        _code = code.copy()
        _type = _code.pop('type')
        mapping = {
            'Plain': Plain, 'Face': Face
        }
        return mapping[_type](**_code) if _type in mapping.keys() else None

    @staticmethod
    def format_unsupported_display(code: dict, colored: bool = False, color: str = 'bold yellow') -> str:
        _code = code.copy()
        _type = _code.pop('type')
        result = '|%s' % type
        result = '[%s]%s[/%s]' % (color, result, color) if colored else result
        return Utils.format_display(result, *tuple(_code.values())) if _type != 'Source' else ''


class Plain(MiraiElement):
    def __init__(self, text: str or list) -> None:
        self.text = '\n'.join(text) if type(text) is list else text

    def as_display(self) -> str:
        return self.text.replace('\n', '<\\n>')

    def to_code(self) -> dict:
        return Utils.format_code('Plain', text=self.text)

    @staticmethod
    def as_code_display(code: dict) -> str:
        return Plain(code['text']).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class Face(MiraiElement):
    def __init__(self, face_id: int) -> None:
        self.id = face_id

    def as_display(self) -> str:
        return Utils.format_display('表情', self.id)

    def to_code(self) -> dict:
        return Utils.format_code('face', faceId=self.id)

    @staticmethod
    def as_code_display(code: dict) -> str:
        return Face(code['faceId']).as_display()

    def __str__(self) -> str:
        return Utils.as_str(self)


class At(MiraiElement):
    pass


class Share(MiraiElement):
    pass


class Reply(MiraiElement):
    pass
