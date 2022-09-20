from ...events import NoticeEvent


class CQHTTPEventHandler:
    """
    > 说明
        CQHTTP 事件处理器.
    > 参数
        + adapter [Adapter]: 适配器对象
    """
    def __init__(self, adapter: "Adapter") -> None:
        self.adapter = adapter
        self.logger = adapter.logger
    
    async def handle(self, data: dict) -> None:
        post_type = data['post_type']
        if post_type == 'notice':
            notice_type = data['notice_type']
            e_list = [e for e in NoticeEvent.__subclasses__() if e.__code__ == notice_type]
            event = e_list[0] if len(e_list) >= 1 else None
            if event:
                instance = event(**data)
                self.logger.info('[yellow]<事件> %s[/yellow]' % instance.as_display())
