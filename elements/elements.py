from JustBot.elements import Element

from typing import Union


class Text(Element):
    def __init__(self, text: str):
        self.text = text

    def as_display(self) -> str:
        return self.text

    def as_code(self) -> str:
        return self.text


class Face(Element):
    def __init__(self, face_id: int):
        self.face_id = face_id

    def as_display(self) -> str:
        return f'[表情:{self.face_id}]'

    def as_code(self) -> str:
        return f'[CQ:face,id={self.face_id}]'


class At(Element):
    def __init__(self, qq: Union[str, int], name: str = None):
        self.qq = qq
        self.name = name

    def as_display(self) -> str:
        return f'[At:{self.qq}:{self.name}]'

    def as_code(self) -> str:
        return f'[CQ:at,qq={self.qq},name={self.name}]' if self.name else f'[CQ:at,qq={self.qq}]'


class Share(Element):
    def __init__(self, url: str, title: str, content: str = None, image_url: str = None):
        self.url = url
        self.title = title
        self.content = content
        self.image_url = image_url

    def as_display(self) -> str:
        return f'[链接分享:{self.url}:{self.title}]'

    def as_code(self) -> str:
        arg1 = f',content={content}' if content else ''
        arg2 = f',image={image_url}' if image_url else ''
        return f'[CQ:share,url={self.url},title={self.title}{arg1}{arg2}]'


class Reply(Element):
    def __init__(self, message_id: int):
        self.message_id = message_id

    def as_display(self) -> str:
        return f'[回复:{self.message_id}]'

    def as_code(self) -> str:
        return f'[CQ:reply,id={self.message_id}]'
